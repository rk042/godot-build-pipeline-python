from __future__ import annotations

from argparse import ArgumentParser, Namespace
from dataclasses import dataclass
from os import environ
from pathlib import Path
from sys import platform

import validate_export_templates

SUPPORTED_PLATFORMS = {
    "windows": ("Windows", ".exe"),
    "android": ("Android", ".apk"),
}


@dataclass(frozen=True)
class ProjectSetup:
    godot_editor_path: str
    your_project_path: Path
    build_output_path: Path
    script_path: str
    exported_project_name: str
    exported_platform: str


def build_parser() -> ArgumentParser:
    parser = ArgumentParser(description="Godot build pipeline")
    parser.add_argument("--exported-project-name", required=True)
    parser.add_argument("--exported-project-path", required=False)
    parser.add_argument(
        "--exported-platform",
        choices=sorted(SUPPORTED_PLATFORMS.keys()),
        required=True,
    )
    parser.add_argument("--godot-editor-path", required=False)
    parser.add_argument("--project-path", required=False)
    parser.add_argument(
        "--script-path",
        required=False,
        default="res://core_game/scripts/build_pipeline_bridge.gd",
    )
    return parser


def _is_path_like(value: str) -> bool:
    if "/" in value or "\\" in value:
        return True
    return Path(value).is_absolute()


def _resolve_godot_editor_path(args: Namespace) -> str:
    godot_editor_path = args.godot_editor_path or environ.get("GODOT_EDITOR_PATH")
    if not godot_editor_path:
        raise ValueError(
            "Godot editor path is not set. Use --godot-editor-path or GODOT_EDITOR_PATH."
        )

    if _is_path_like(godot_editor_path):
        godot_path = Path(godot_editor_path)
        if not godot_path.exists():
            raise ValueError(f"Godot editor path does not exist: {godot_path}")
        if not godot_path.is_file():
            raise ValueError("Godot editor path must point to a file.")
        if platform.startswith("win") and godot_path.suffix.lower() != ".exe":
            raise ValueError("Godot editor path must point to a .exe file on Windows.")

    return godot_editor_path


def _resolve_project_path(project_path: str | None) -> Path:
    resolved = Path(project_path) if project_path else Path(__file__).resolve().parents[1]
    if not resolved.exists():
        raise ValueError(f"Project path does not exist: {resolved}")
    return resolved


def _resolve_build_output_path(
    exported_project_path: str | None, project_path: Path
) -> Path:
    if exported_project_path:
        build_output_path = Path(exported_project_path)
    else:
        build_output_path = project_path / "builds/test"

    build_output_path.mkdir(parents=True, exist_ok=True)
    return build_output_path


def _normalize_export_config(exported_project_name: str, exported_platform: str) -> tuple[str, str]:
    if not exported_project_name:
        raise ValueError("Exported project name is not set.")

    platform_key = exported_platform.strip().lower()
    if platform_key not in SUPPORTED_PLATFORMS:
        raise ValueError(
            f"Unsupported export platform: {exported_platform}, "
            "please use 'windows' or 'android'."
        )

    platform_name, extension = SUPPORTED_PLATFORMS[platform_key]
    return platform_name, f"{exported_project_name}{extension}"


def _validate_script_path(script_path: str) -> None:
    if not script_path:
        raise ValueError("Script path is not set.")
    if script_path.startswith("res://"):
        return
    if not Path(script_path).exists():
        raise ValueError(f"Script path does not exist: {script_path}")


def prepare_setup(args: Namespace) -> ProjectSetup:
    godot_editor_path = _resolve_godot_editor_path(args)
    your_project_path = _resolve_project_path(args.project_path)
    build_output_path = _resolve_build_output_path(args.exported_project_path, your_project_path)
    exported_platform, exported_project_name = _normalize_export_config(
        args.exported_project_name, args.exported_platform
    )
    _validate_script_path(args.script_path)

    export_presets_path = validate_export_templates.find_export_presets_path(your_project_path)
    available_platforms = validate_export_templates.load_available_platforms(export_presets_path)

    if exported_platform.lower() not in available_platforms:
        raise ValueError(
            f"Export platform '{exported_platform.lower()}' is not available in export_presets.cfg. "
            f"Available platforms: {available_platforms}\n"
            "For more info visit : https://docs.godotengine.org/en/stable/tutorials/export/"
        )

    return ProjectSetup(
        godot_editor_path=godot_editor_path,
        your_project_path=your_project_path,
        build_output_path=build_output_path,
        script_path=args.script_path,
        exported_project_name=exported_project_name,
        exported_platform=exported_platform,
    )


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        setup = prepare_setup(args)
        print(f"Exported Project Name: {setup.exported_project_name}")
        print(f"Export Platform: {setup.exported_platform}")
        print(f"Godot editor path is set to: {setup.godot_editor_path}")
        print(f"Project path is set to: {setup.your_project_path}")
        print(f"Build output path is set to: {setup.build_output_path}")
        print(f"Script path is set to: {setup.script_path}")
        print("Project setup completed successfully.")
        print("Validation of export templates completed successfully.")
        return 0
    except Exception as exc:
        print(f"Error: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
