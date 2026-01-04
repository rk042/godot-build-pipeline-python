# godot-build-pipeline-python

A small, opinionated build automation helper for the Godot Engine written in Python.

<img width="1151" height="676" alt="image" src="https://github.com/user-attachments/assets/eff5c9b4-aa56-45ff-a21d-355e0eb82154" />


## Overview 

This project provides a lightweight pipeline for creating **debug** builds for Godot projects on **Windows** and **Android**. It demonstrates how to drive the Godot editor from Python, pass a JSON payload into a Godot script, and update project resources (for example, versioning and simple configuration values) programmatically.

The base goal is to create a robust build automation system for Godot using Python; a roadmap exists to add more platforms, CI integration, build artefact storage and more.

---

## Key features 

- Run Godot headlessly to produce debug builds for Windows and Android.
- Pass a JSON payload from Python into Godot to modify project resources at build time (e.g. version and spawn rate).
- Automatic version incrementing when a manual version is not supplied (patch/minor/major rollovers).
- Simple, easy-to-extend structure intended as a starting point for fuller build automation.

---

## Quick usage example 

From the repository root you can run the pipeline script to generate a debug build:

```powershell
python .\build_pipeline\build_pipeline.py --exported-project-name "test pipeline 1" --exported-platform "windows"
```

This will run Godot in headless mode, execute the bridge script inside your project, and export a **debug** build with the name provided (e.g. `test pipeline 1.exe` for Windows or `test pipeline 1.apk` for Android).

---

## Payload explanation (version and spawn_rate)

The script `build_pipeline.py` constructs a JSON payload and passes it to Godot via the `--` separator. By default the payload looks like:

```json
[{"version_code":"","spawn_rate":10}]
```

- **version_code**: optional. If provided, the pipeline initialises the project version with this value. If omitted or empty, the pipeline will read the existing project version and automatically increase it.
- **spawn_rate**: used as an example of a custom value you can pass at build-time — it writes into a `custom_resource` resource and is consumed by the running project to, for instance, spawn icons in the UI.

---

## How the versioning works 

Version data is managed by `core_game/scripts/custom_version_resource.gd`:

- Versions are stored as strings in the form `MAJOR.MINOR.PATCH` (e.g. `1.2.3`).
- When the pipeline does not receive a manual `version_code`, the current version is read and `increase_version()` is called.
- The increment rules are:
  - Increase the patch number until it reaches 9.
  - When patch > 9, reset patch to 0 and increment minor.
  - When minor > 9, reset minor to 0 and increment major.
- The new version is saved into the project settings via `ProjectSettings.set_setting("application/config/version", version)`.

> See `core_game/scripts/custom_version_resource.gd` for the detailed implementation.

---

## Files and responsibilities 

- `build_pipeline/build_pipeline.py` — Python entry point. Builds the command to run the Godot editor in headless mode, supplies the export target and passes the JSON payload.
- `build_pipeline/project_setup.py` — Command-line argument parsing and project configuration (paths, output location, exported filename and platform). Update `godot_editor_path` and `your_project_path` here.
- `core_game/scripts/build_pipeline_bridge.gd` — Godot-side bridge script (runs as a SceneTree). It reads the JSON payload from the command line, updates `custom_version_resource` and `custom_resource`, saves them and triggers version saving.
- `core_game/scripts/custom_resource.gd` — Small `Resource` that stores `time_to_generate_icon` (used as the spawn example).
- `core_game/scripts/custom_version_resource.gd` — Version management resource with init/increase/save logic.
- `core_game/gui/gui_main_screen.gd` — Example UI that reads `custom_resource` and spawns icons according to `time_to_generate_icon`.
- `build_pipeline/validate_export_templates.py` - Validates the presence of required  [**export_presets**](https://docs.godotengine.org/en/latest/tutorials/export/exporting_projects.html). If the pipeline cannot locate the selected export template, it will stop execution and raise a clear exception, including links to the relevant Godot documentation to help resolve the issue. 
---

## Configuration & setup 
1. Update `project_setup.py` with your local paths:
   - `godot_editor_path` → provide fallback default path.
   - `your_project_path` → this will auto detecte if you face any issue please provide default path.
2. Ensure your Godot project has an export preset for the chosen platform (Windows/Android).
3. Run the `build_pipeline.py` command with the required CLI args.

### Environment Variables

It is recommended to configure the Godot editor path using an environment variable. This helps reduce manual configuration mistakes and makes the pipeline easier to use across different machines.

1. Locate the installed Godot editor executable on your system.
2. Set the full path to this executable as an environment variable named GODOT_EDITOR_PATH.

Once set, the pipeline will automatically use this value without requiring hard-coded paths in the configuration files.

---

## Roadmap & suggestions 

See milestones for the long-term roadmap:
[Milestones](https://github.com/rk042/godot-build-pipeline-python/milestones)

---

## Troubleshooting & tips 

- If Godot fails to run, check `godot_editor_path` is correct and reachable.
- Ensure the export preset name matches your selected platform and that the export templates are installed (Android requires SDK/NDK setup).
- Use the command-line `--` separator carefully — the script relies on Godot's `OS.get_cmdline_user_args()` to retrieve the JSON payload.
- Please check document named ``Common Errors & Mistakes.md``

---

## Contributing & Licence 

Contributions are welcome — raise issues or pull requests. This repository uses the included `LICENSE` file; please follow it when contributing.

---
