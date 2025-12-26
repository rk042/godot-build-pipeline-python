import pathlib

try:
    godot_editor_path = r"E:\Godot_v4.5.1-stable_win64\Godot_v4.5.1-stable_win64_console.exe"
    your_project_path = r"D:\Projects\Godot\godot-build-pipeline-python"
    build_output_path = r""

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

except Exception as e:
    print(f"Error: {e}")
