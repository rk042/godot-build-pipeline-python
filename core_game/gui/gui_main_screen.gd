extends Control

@onready var grid_container: GridContainer = $GridContainer
@export var godot_icon: PackedScene
const CUSTOM_RESOURCE = preload("uid://difd37i8nr7wb")


func _ready():
	
	for i in range(CUSTOM_RESOURCE.time_to_generate_icon):
		var local_godot_icon = godot_icon.instantiate()
		grid_container.add_child(local_godot_icon)
		pass
	
	pass  # Replace with function body.
