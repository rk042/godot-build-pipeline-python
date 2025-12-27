# Contributing to godot-build-pipeline-python

Thanks for taking the time to contribute!
This project aims to automate **Godot exports using Python** (headless CLI), starting with **Windows + Android debug builds**.

> ⚠️ Project status: Work in progress  
> Some parts are still hard-coded and will be improved over time.

---

## Quick ways to help

You can contribute by:
- Reporting bugs (especially export failures on different machines)
- Improving documentation (README, examples, setup steps)
- Adding new platform support (Linux, macOS, Web)
- Making paths/configuration more flexible (config files, env vars)
- Adding GitHub Actions workflows (CI builds)

---

## Requirements

Before contributing, make sure you have:
- **Python 3.10+**
- **Godot 4.x (console build recommended)**
- A **working Godot project** with **export templates installed**
- Basic knowledge of:
  - Godot
  - GDScript
  - Python CLI tools

---

## Repo overview

Key files:
- `build_pipeline.py` — runs the build using Godot in headless mode
- `project_setup.py` — parses arguments and prepares platform/export output
- `core_game/scripts/build_pipline_bridge.gd` — bridge script called inside Godot

---

## How to run locally (example)

```bash
python build_pipeline.py --exported-project-name "test pipeline 1" --exported-platform "windows"
