import pathlib
import argparse
from os import environ
from os import path

parser = argparse.ArgumentParser(description="Godot build pipeline")

parser.add_argument("--exported-project-name", required=True)
parser.add_argument("--exported-project-path", required=False)
parser.add_argument("--exported-platform", choices=["windows", "android"], required=True)

args = parser.parse_args()

exported_project_name = args.exported_project_name
exported_platform = args.exported_platform
exported_project_path = args.exported_project_path

print(f"Exported Project Name: {exported_project_name}")
print(f"Export Platform: {exported_platform}")

try:
    godot_editor_path = environ.get("GODOT_EDITOR_PATH", r"E:\Godot_v4.5.1-stable_win64\Godot_v4.5.1-stable_win64.exe") # if pipeline would be able to find godot editor path from env variable, otherwise set it manually here
    your_project_path = path.dirname(path.dirname(path.abspath(__file__)))# r"D:\Projects\Godot\godot-build-pipeline-python"
    build_output_path = exported_project_path  # if you want to set custom build output path, otherwise leave it as None
    script_path = "res://core_game/scripts/build_pipline_bridge.gd" # bridge script path in your project
    
    if godot_editor_path is None or godot_editor_path == "":
        raise ValueError("Godot editor path is not set.")
    else:
        print(f"Godot editor path is set to: {godot_editor_path}")

    if your_project_path is None or your_project_path == "":
        raise ValueError("Project path is not set.")
    else:
        print(f"Project path is set to: {your_project_path}")    

    if build_output_path is None or build_output_path == "":
        (pathlib.Path(your_project_path) / "builds/test").mkdir(parents=True, exist_ok=True)
        build_output_path = str(pathlib.Path(your_project_path) / "builds/test")
        print(f"Build output path is not set. Using default: {build_output_path}")
    elif not pathlib.Path(build_output_path).exists():
        pathlib.Path(build_output_path).mkdir(parents=True, exist_ok=True)
        print(f"Build output path did not exist. Created directory at: {build_output_path}")
    else:
        print(f"Build output path is set to: {build_output_path}")

    if exported_project_name is None or exported_project_name == "":
        raise ValueError("Exported project name is not set.")
    else:
        print(f"Exported project name is set to: {exported_project_name}")

    if exported_platform is None or exported_platform == "":
        raise ValueError("Export platform is not set.") 
    else:
        print(f"Export platform is set to: {exported_platform}")

    match exported_platform.lower():
        case "windows":
            exported_platform = "Windows"
            exported_project_name += ".exe"
        case "android":
            exported_platform = "Android"
            exported_project_name += ".apk"
        case _:
           raise ValueError(f"Unsupported export platform: {exported_platform}, please use 'windows' or 'android'.")

    if script_path is None or script_path == "":
        raise ValueError("Script path is not set.")
    else:
        print(f"Script path is set to: {script_path}")

    print("Project setup completed successfully.")

except Exception as e:
    print(f"Error: {e}")
    exit(1)

