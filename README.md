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
python .\build_pipline\build_pipeline.py --exported-project-name "test pipeline 1" --exported-platform "windows"
```

This will run Godot in headless mode, execute the bridge script inside your project, and export a **debug** build with the name provided (e.g. `test pipeline 1.exe` for Windows or `test pipeline 1.apk` for Android).

> Note: The project currently uses a hard-coded `godot_editor_path` in `project_setup.py`. Please update that path to point to your local Godot executable.

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

- `build_pipline/build_pipeline.py` — Python entry point. Builds the command to run the Godot editor in headless mode, supplies the export target and passes the JSON payload.
- `build_pipline/project_setup.py` — Command-line argument parsing and project configuration (paths, output location, exported filename and platform). Update `godot_editor_path` and `your_project_path` here.
- `core_game/scripts/build_pipline_bridge.gd` — Godot-side bridge script (runs as a SceneTree). It reads the JSON payload from the command line, updates `custom_version_resource` and `custom_resource`, saves them and triggers version saving.
- `core_game/scripts/custom_resource.gd` — Small `Resource` that stores `time_to_generate_icon` (used as the spawn example).
- `core_game/scripts/custom_version_resource.gd` — Version management resource with init/increase/save logic.
- `core_game/gui/gui_main_screen.gd` — Example UI that reads `custom_resource` and spawns icons according to `time_to_generate_icon`.

---

## Configuration & setup 

1. Update `project_setup.py` with your local paths:
   - `godot_editor_path` → path to your Godot executable
   - `your_project_path` → your project root
2. Ensure your Godot project has an export preset for the chosen platform (Windows/Android).
3. Run the `build_pipeline.py` command with the required CLI args.

---

## Roadmap & suggestions 

Planned / suggested improvements:
- Add CI (GitHub Actions, GitLab CI) to run builds automatically on push/tags.
- Support release & stripped builds as well as debug builds.
- Add a configuration file or environment variables to avoid editing `project_setup.py` directly.
- Accept payload content as CLI arguments rather than hard-coding the payload in the Python file.
- Store build artefacts in a dedicated location or upload to an artefact repository.

---

## Troubleshooting & tips 

- If Godot fails to run, check `godot_editor_path` is correct and reachable.
- Ensure the export preset name matches your selected platform and that the export templates are installed (Android requires SDK/NDK setup).
- Use the command-line `--` separator carefully — the script relies on Godot's `OS.get_cmdline_user_args()` to retrieve the JSON payload.

---

## Contributing & Licence 

Contributions are welcome — raise issues or pull requests. This repository uses the included `LICENSE` file; please follow it when contributing.

---
