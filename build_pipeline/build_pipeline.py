import json
import subprocess
import project_setup

args=[{
    "version_code":"", # add manully version if you want, othewise leave it empty
    "spawn_rate":10
    }]

payload = json.dumps(args)

try:
    if payload is None or payload == "":
        raise ValueError("Payload is not set.")
    
    _unloaded_payload = json.loads(payload)
    
    if not isinstance(_unloaded_payload, list):
        raise ValueError("Payload must be a JSON array.")
    
    if len(_unloaded_payload) == 0:
        raise ValueError("Payload array is empty.")
    
    if _unloaded_payload[0].get("spawn_rate") < 0:
        raise ValueError("payload spawn_rate must be non-negative.")

except Exception as e:
    print(f"Error: {e}")
    exit(1)


command = [
    project_setup.godot_editor_path,
    "--headless",
    "--path", project_setup.your_project_path,
    "-s", project_setup.script_path,
    "--export-debug", project_setup.exported_platform,
    rf"{project_setup.build_output_path}\{project_setup.exported_project_name}",
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
