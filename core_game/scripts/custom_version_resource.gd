extends Resource

class_name custom_version_resource

@export var version:String 

func init(is_manual_added:bool = false,manual_version:String = "") -> void:
	
	if not is_manual_added :
		print("you do not provided manual version therefore using current project config version")
	else:
		version = manual_version
		
	print("custom version resource init ",version)

func increase_version():
	var _version:PackedStringArray = version.split(".")
	
	var _major_version = int(_version[0])
	var _minor_version = int(_version[1])
	var _patch_version = int(_version[2])
	
	if _patch_version < 9:
		_patch_version+=1
		pass
	elif _patch_version >= 9 and _minor_version < 9:
		_minor_version +=1
		_patch_version = 0 
		pass
	else:
		_major_version += 1
		_minor_version = 0
		_patch_version = 0
		pass	
	
	_version[0] = str(_major_version)
	_version[1] = str(_minor_version)
	_version[2] = str(_patch_version)
	
	version = ".".join(_version)
	
	#update in project setting
	save_version_in_project_export()
	
	pass

func get_current_version():
	return version

func print_current_version():
	print("your project version is ",version)

func save_version_in_project_export() -> void:
	ProjectSettings.set_setting("application/config/version",version)
	print("new version has been saved : ",version)
	pass
