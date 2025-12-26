extends Node2D

@export var version_resource:custom_version_resource
@onready var version_label: Label = $GUI_CanvasLayer/version_label

func _ready() -> void:
	refresh_version()
	
func _on_btn_increase_version_pressed() -> void:
	version_resource.increase_version()
	refresh_version()
	
	var _is_resource_save = ResourceSaver.save(version_resource)
	
	print("resource save ? Answer is  ",_is_resource_save)
	
	pass # Replace with function body.

func refresh_version() -> void:
	var _version = version_resource.get_current_version()
	version_label.text = "Version : "+_version
	pass
