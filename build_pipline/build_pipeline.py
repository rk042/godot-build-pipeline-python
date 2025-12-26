import json
import subprocess
import project_setup

if not project_setup.godot_editor_path or not project_setup.your_project_path:
    print("Godot editor path or project path is not set correctly.")
    exit(1)

script_path = "res://core_game/scripts/build_pipline_bridge.gd" #bridge script path in your project
args=[{
    "version_code":"", # add manully version if you want, othewise leave it empty
    "spawn_rate":10
    }]

payload = json.dumps(args)

command = [
    project_setup.godot_editor_path,
    "--headless",
    "--path", project_setup.your_project_path,
    "-s", script_path,
    "--export-debug", "Android",
    rf"{project_setup.build_output_path}\my_game.apk",
    "--",payload
]


print("Running build command:")
print("Command:", command)

# Run the Godot editor
result = subprocess.run(command)

if result.returncode != 0:
    print(f"Failed to launch Godot editor. Return code: {result.returncode}")
else:
    print("Build preparation step completed!")
