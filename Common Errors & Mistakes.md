# Common Errors & Mistakes (Godot Python Build Pipeline)

This document lists the most common problems you may hit when using this build pipeline, why they happen, and how to fix them.

It is based on these scripts:

- `build_pipeline.py` — build_pipeline
- `project_setup.py` — project_setup
- `validate_export_templates.py` — validate_export_templates

---

## 1) “Export presets file NOT found” / `export_presets.cfg` missing

**Symptoms**

You see: "Export presets file NOT found. Please check export_presets.cfg location." (from `validate_export_templates`) or the pipeline exits immediately during startup.

**Why it happens**

`validate_export_templates.py` calculates the project directory as:

```py
project_directory = Path(__file__).resolve().parents[1]
export_presets_path = project_directory / "export_presets.cfg"
```

So the pipeline expects `export_presets.cfg` to exist **two levels above** that script file, at the repository/project root.

**Fix**
- Ensure `export_presets.cfg` exists at the expected location.
- Run the scripts from the correct repo structure (don’t move these scripts without updating the `parents[1]` assumption).

---

## 2) “No export platforms found in export_presets.cfg”

**Symptoms**
- You see: `No export platforms found in export_presets.cfg. Please add at least one export preset.`

**Why it happens**

The script only recognises export presets by scanning for lines that start with `name=`:

```py
if line.rstrip().startswith("name="):
    ...
    available_platforms.append(...)
```

If your `export_presets.cfg` is missing preset names, or uses a different format than expected, the list stays empty.

**Fix**
- Open `export_presets.cfg` and confirm it contains presets with `name="..."`.

---

## 3) “Export platform ‘windows’ is not available…” even though you added it

**Symptoms**
- You see:
  `Export platform 'windows' is not available in export_presets.cfg. Available platforms: ...`

**Why it happens (important)**

There are two “name matching” traps:

1) `project_setup.py` converts CLI values into Godot-style names:

```py
match exported_platform.lower():
    case "windows":
        exported_platform = "Windows"
    case "android":
        exported_platform = "Android"
```

2) `validate_export_templates.py` collects preset names from `export_presets.cfg` and lowercases them.

If your preset name in Godot is something like:
- `name="Windows Desktop"`
- `name="Android (APK)"`

…then the pipeline will never match `windows` / `android`.

**Fix options**
- Rename your export preset in Godot to exactly `Windows` or `Android`:
  - Godot → Project → Export → select preset → rename to `Windows` / `Android`
- Or update the matching logic to accept “contains” matches (recommended long-term).

Example improvement (more tolerant check):

```py
wanted = exported_platform.lower()
if not any(wanted in p for p in available_platforms):
    raise ValueError(...)
```

---

## 4) Script path validation fails (`res://...` paths)

**Symptoms**
You see:
`Script path does not exist: res://core_game/scripts/build_pipeline_bridge.gd` (from `project_setup`)

**Why it happens**

`project_setup.py` is checking a Godot `res://` path using Python `Path`, which checks the OS filesystem:

```py
script_path = "res://core_game/scripts/build_pipeline_bridge.gd"
...
elif not Path(script_path).exists():
    raise ValueError(f"Script path does not exist: {script_path}")
```

`res://...` is not a real Windows file path, so this check will almost always fail.

**Fix**
- Use a filesystem path for validation, or skip OS validation for `res://` and let Godot validate it.

A safe approach:

```py
if script_path.startswith("res://"):
    # optionally validate by mapping res:// to your project directory
    local_script = Path(your_project_path) / script_path.replace("res://", "")
    if not local_script.exists():
        raise ValueError(f"Script path not found in project: {local_script}")
else:
    if not Path(script_path).exists():
        raise ValueError(f"Script path does not exist: {script_path}")
```

---

## 5) Godot editor path errors (missing, wrong file, not .exe)

**Symptoms**
- Godot editor path is not set.
- `Godot editor path does not exist: ...`
- `Godot editor path must point to a .exe file on Windows.`

**Why it happens**

`project_setup.py` reads `GODOT_EDITOR_PATH` from environment variables, otherwise it uses a hard-coded fallback:

```py
godot_editor_path = environ.get("GODOT_EDITOR_PATH", r"E:\Godot_v4.5.1-stable_win64\...")
```

It then validates it strictly on Windows.

**Fix**
Set the environment variable so everyone uses their own machine’s path.

**PowerShell**

```powershell
setx GODOT_EDITOR_PATH "C:\Godot\Godot_v4.5.1-stable_win64.exe"
```

**Command Prompt**

```cmd
setx GODOT_EDITOR_PATH "C:\Godot\Godot_v4.5.1-stable_win64.exe"
```

Then open a new terminal (environment variables won’t appear in already-open shells).

---

## 6) Build output path is None or empty (build goes to unexpected folder)

**Symptoms**
- Builds go to `builds/test` instead of where you expected.
- Or output path is created but not where you wanted.

**Why it happens**

`build_output_path` is taken from `--exported-project-path` and if missing/empty, a default is created:

```py
if build_output_path is None or build_output_path == "":
    (Path(your_project_path) / "builds/test").mkdir(...)
    build_output_path = str(Path(your_project_path) / "builds/test")
```

**Fix**
- Always pass `--exported-project-path` when running `project_setup.py`.

Example:

```bash
python project_setup.py --exported-project-name MyGame --exported-platform windows --exported-project-path "D:\Builds\MyGame"
```

---

## 7) Windows path separator issues (backslashes, trailing slashes, non-Windows hosts)

**Symptoms**
- Godot fails to export.
- Output path is malformed (double slashes or missing separator).
- Works on one machine, fails on another.

**Why it happens**

`build_pipeline.py` builds the output path using a Windows-only string:

```py
rf"{project_setup.build_output_path}\{project_setup.exported_project_name}"
```

**Fix**
- Use `Path` joining to be safe:

```py
from pathlib import Path
output = str(Path(project_setup.build_output_path) / project_setup.exported_project_name)
```

Then pass `output` into the command list.

---

## 8) Payload errors (JSON must be an array, empty array, negative spawn_rate)

**Symptoms**
- Payload is not set.
- Payload must be a JSON array.
- Payload array is empty.
- payload `spawn_rate` must be non-negative.

**Why it happens**

`build_pipeline.py` validates the payload very strictly:

```py
_unloaded_payload = json.loads(payload)

if not isinstance(_unloaded_payload, list):
    raise ValueError("Payload must be a JSON array.")

if len(_unloaded_payload) == 0:
    raise ValueError("Payload array is empty.")

if _unloaded_payload[0].get("spawn_rate") < 0:
    raise ValueError("payload spawn_rate must be non-negative.")
```

**Fix**
- Always pass payload as a JSON list, e.g.:

```json
[
  { "version_code": "", "spawn_rate": 10 }
]
```

If you don’t want to set `version_code`, leaving it as an empty string is fine (as your code suggests).

---

## 9) Godot runs but nothing exports (or the bridge script doesn’t receive payload)

**Symptoms**
- Godot opens headless and exits.
- No exported file appears.
- Your GDScript doesn’t receive expected `--` arguments.

**Why it happens**

The pipeline passes payload after `--`:

```py
"--", payload
```

This is correct for passing arguments through to scripts, but your `build_pipeline_bridge.gd` must explicitly read CLI args properly (e.g., `OS.get_cmdline_args()` and parse what comes after `--`).

**Fix**
In your GDScript bridge, ensure you:
- read the full command line args
- locate the payload argument after `--`
- parse JSON safely and validate again inside Godot (defensive)

A minimal GDScript pattern:

```gdscript
var args := OS.get_cmdline_args()
var sep := args.find("--")
if sep != -1 and sep + 1 < args.size():
    var payload_json := args[sep + 1]
    var data = JSON.parse_string(payload_json)
    if data == null:
        push_error("Invalid JSON payload")
```

---

## 10) Subprocess return code is non-zero (Godot failed to launch/export)

**Symptoms**
- `Failed to launch Godot editor. Return code: X`

**Why it happens**

The pipeline currently uses:

```py
result = subprocess.run(command)
```

This doesn’t capture stdout/stderr, so you may not see Godot’s actual error message in your terminal output.

**Fix (recommended improvement)**
Capture logs:

```py
result = subprocess.run(command, capture_output=True, text=True)

if result.returncode != 0:
    print("Godot stdout:\n", result.stdout)
    print("Godot stderr:\n", result.stderr)
    raise SystemExit(result.returncode)
```

This makes debugging 10x easier.

---

## 11) Import-time failures (pipeline crashes before you run anything)

**Symptoms**
- `project_setup.py` fails immediately even before printing expected setup messages.

**Why it happens**

`project_setup.py` imports `available_platforms` directly:

```py
from validate_export_templates import available_platforms
```

`validate_export_templates.py` runs validation **at import time** and calls `exit(1)` on error. So any problem (missing `export_presets.cfg`, no platforms, etc.) kills the whole run early.

**Fix**
For end-user friendliness, move validation into a function instead of executing on import. Example:

```py
# validate_export_templates.py
def load_available_platforms(project_directory: Path) -> list[str]:
    ...
    return available_platforms

# then call it from project_setup.py inside a try: block
```

This lets `project_setup.py` print a clearer message and recover gracefully.

---

## 12) Platform support is currently limited

**Symptoms**
- You try to export a platform other than Windows/Android and it fails.

**Why it happens**

CLI choices are restricted:

```py
parser.add_argument("--exported-platform", choices=["windows", "android"], required=True)
```

And the `match` statement throws for anything else.

**Fix**
- Only use `windows` or `android` for now, or extend both:
  - CLI `choices=[...]`
  - `match` mapping
  - export preset naming/matching rules

---

## Quick “Known Good” Example ✅

**Windows export**

```bash
python project_setup.py --exported-project-name MyGame --exported-platform windows --exported-project-path "D:\Builds\MyGame"
python build_pipeline.py
```

Make sure:

- `GODOT_EDITOR_PATH` points to your Godot `.exe` (`project_setup`)
- `export_presets.cfg` exists and includes a preset named `Windows` (`validate_export_templates`)
- your bridge script exists inside the project (and script_path validation is fixed as described above) (`project_setup`)

### Troubleshooting Checklist 🔧

- `export_presets.cfg` exists where the scripts expect it (`validate_export_templates`)
- Export preset names match `Windows` / `Android` (or you improved matching) (`project_setup` / `validate_export_templates`)
- `GODOT_EDITOR_PATH` is set correctly (and points to a real `.exe`) (`project_setup`)
- `--exported-project-path` is provided (or you’re happy with the `builds/test` default) (`project_setup`)
- Payload is JSON array, non-empty, and `spawn_rate >= 0` (`build_pipeline`)
- Output path joining uses `Path(...) / ...` rather than `\` strings (recommended) (`build_pipeline`)

---

If you want any edits to the wording, additional examples, or more checks added (e.g. sample `export_presets.cfg` snippet), tell me where to expand and I’ll update the file. ✅
