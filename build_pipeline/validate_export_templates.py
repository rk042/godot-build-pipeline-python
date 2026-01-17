from pathlib import Path


def find_export_presets_path(project_directory: Path | None = None) -> Path:
    if project_directory is None:
        project_directory = Path(__file__).resolve().parents[1]
    return project_directory / "export_presets.cfg"


def load_available_platforms(export_presets_path: Path) -> list[str]:
    if not export_presets_path.exists():
        raise FileNotFoundError(
            "Export presets file NOT found. Please check export_presets.cfg location."
        )

    available_platforms: list[str] = []
    with export_presets_path.open("r", encoding="utf-8") as file:
        for line in file:
            stripped = line.strip()
            if stripped.startswith("name="):
                platform = stripped.split("=", 1)[1].strip().strip('"').lower()
                if platform:
                    available_platforms.append(platform)

    if not available_platforms:
        raise ValueError(
            "No export platforms found in export_presets.cfg. Please add at least one export preset.\n"
            "for more info: https://docs.godotengine.org/en/stable/tutorials/export/"
        )

    return available_platforms


def main() -> int:
    try:
        export_presets_path = find_export_presets_path()
        available_platforms = load_available_platforms(export_presets_path)
        print("Export presets file found.")
        print(f"Available export platforms: {', '.join(available_platforms)}")
        return 0
    except Exception as exc:
        print(f"Error while validating export presets/platforms: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
