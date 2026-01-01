from pathlib import Path

project_directory = Path(__file__).resolve().parents[1]
export_presets_path = project_directory / "export_presets.cfg"
available_platforms = []

try:
    if Path(export_presets_path).exists():
        print("Export presets file found.")
    else:
        raise FileNotFoundError("Export presets file NOT found. Please check export_presets.cfg location.")

    with open(export_presets_path, 'r') as file:
        for line in file:
            if line.rstrip().startswith("name="):
                line_content = line.rstrip().split("=")
                available_platforms.append(line_content[1].lower().rstrip().replace('"', ''))
    
    if len(available_platforms) == 0:
        raise ValueError("No export platforms found in export_presets.cfg. Please add at least one export preset.\nfor more info: https://docs.godotengine.org/en/stable/tutorials/export/")

    print(f"Available export platforms: {', '.join(available_platforms)}")
    
except Exception as e:
    print(f"Error while validating export presets/platforms: {e}")
    exit(1)

