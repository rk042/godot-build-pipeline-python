extends SceneTree

var version_resource_object:custom_version_resource
var custom_resource_object:custom_resource

func _init():
	print("Build config updated")
	
	version_resource_object = load("res://resources/custom_version_resource.tres") as custom_version_resource
	custom_resource_object = load("res://resources/custom_resource.tres") as custom_resource
	
	version_resource_object.print_current_version()
	
	var player_args = OS.get_cmdline_user_args()

	print("Raw args:", player_args)

	if player_args.is_empty():
		push_error("No args passed")
		quit(1)

	var json_text: String = player_args[0]

	var parsed = JSON.parse_string(json_text)
	if parsed == null:
		push_error("Invalid JSON")
		quit(1)

	if typeof(parsed) != TYPE_ARRAY:
		push_error("Expected JSON array")
		quit(1)

	var config: Dictionary = parsed[0]

	print("Version:", config["version_code"])
	print("Spawn rate:", config["spawn_rate"])
	
	var _version_incoming = config.get("version_code",null)
	 
	if not _version_incoming == null and not _version_incoming == "0" and not _version_incoming == "":
		version_resource_object.init(true,config["version_code"])
		pass
	else:
		version_resource_object.init()
		print("manual version was not passed so using saved version and increase it")
			
	if config["spawn_rate"] < 0:
		print("spawn_rate must be non-negative.")
		quit(1)
	
	version_resource_object.increase_version()
	var _resource1 = ResourceSaver.save(version_resource_object)
	
	custom_resource_object.init(config["spawn_rate"])
	var _resource2 = ResourceSaver.save(custom_resource_object)
		
	
	
	
