import subprocess
import project_setup

if not project_setup.godot_editor_path or not project_setup.your_project_path:
    print("Godot editor path or project path is not set correctly.")
    exit(1)

script_path = "res://BuildPipline/sayhello.gd"

# command = rf"{project_setup.godot_editor_path} --headless --path {project_setup.your_project_path} -s {script_path} --export-debug Android {project_setup.build_output_path}\my_game.apk"


command = [
    project_setup.godot_editor_path,
    "--headless",
    "--path", project_setup.your_project_path,
    "-s", script_path,
    "--export-debug", "Android",
    rf"{project_setup.build_output_path}\my_game.apk"
]


print("Running build command:")
print("Command:", command)

# Run the Godot editor
result = subprocess.run(command)

if result.returncode != 0:
    print(f"Failed to launch Godot editor. Return code: {result.returncode}")
else:
    print("Build preparation step completed!")



# print(f"Running build command: {command}")
# godot_editor = subprocess.run(command)

# if godot_editor.returncode != 0:
#     print(f"Failed to launch Godot editor. Return code: {godot_editor.returncode} {godot_editor.stderr}")
# else:
#     print("Your First Build is Complete!")

