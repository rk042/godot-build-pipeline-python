extends Control

@onready var grid_container: GridContainer = $GridContainer
@export var godot_icon: PackedScene

func _ready():
	var _custom_resource:custom_resource = load("res://resources/custom_resource.tres") as custom_resource
	for i in range(_custom_resource.time_to_generate_icon):
		var local_godot_icon = godot_icon.instantiate()
		grid_container.add_child(local_godot_icon)
		pass
	pass  # Replace with function body.
