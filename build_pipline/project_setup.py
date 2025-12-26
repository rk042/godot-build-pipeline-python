import pathlib

try:
    godot_editor_path = r"E:\Godot_v4.5.1-stable_win64\Godot_v4.5.1-stable_win64_console.exe"
    your_project_path = r"D:\Projects\Godot\godot-build-pipeline-python"
    build_output_path = r""
    exported_project_name = "build_pipline_test1"
    export_platform = "android" # available options: "windows", "android"
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
        pathlib.Path.mkdir(pathlib.Path(your_project_path) / "builds/test", exist_ok=True)
        build_output_path = str(pathlib.Path(your_project_path) / "builds/test")
        print(f"Build output path is not set. Using default: {build_output_path}")

    if exported_project_name is None or exported_project_name == "":
        raise ValueError("Exported project name is not set.")
    else:
        print(f"Exported project name is set to: {exported_project_name}")

    if export_platform is None or export_platform == "":
        raise ValueError("Export platform is not set.") 
    else:
        print(f"Export platform is set to: {export_platform}")

    match export_platform.lower():
        case "windows":
            export_platform = "Windows"
            exported_project_name += ".exe"
        case "android":
            export_platform = "Android"
            exported_project_name += ".apk"
        case _:
           raise ValueError(f"Unsupported export platform: {export_platform}, please use 'windows' or 'android'.")

    if script_path is None or script_path == "":
        raise ValueError("Script path is not set.")
    else:
        print(f"Script path is set to: {script_path}")

except Exception as e:
    print(f"Error: {e}")
    exit(1)
