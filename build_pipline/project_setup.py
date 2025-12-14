import os

data ={}

def main():
    export_presets_cfg_path = get_export_preset_cfg_path()
    with open(export_presets_cfg_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith("#") and not line.startswith("["):
                if "=" in line:
                    key, value = line.split("=", 1)
                    data[key.strip()] = value.strip()
    
        file.close()

def get_export_preset_cfg_path():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    return os.path.join(project_dir, "export_presets.cfg")

def get_current_version_code():
    return float(data.get("version/code", "0"))

def get_project_platform_name():
    return data.get("platform", "unknown")

def get_export_path():
    return data.get("export_path", "")

def update_version_code(new_version_code):
    data["version/code"] = str(new_version_code)
    update_presets_cfg_file()

def update_presets_cfg_file():
    export_presets_cfg_path = get_export_preset_cfg_path()
    #TODO: Implement writing back to the file

main()
update_version_code(get_current_version_code() + 0.1)