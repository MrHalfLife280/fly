from ursina import *
from random import randint

app = Ursina()

window.borderless = False
window.title = 'Flying Simulator'
mouse.locked = True

# Player body
player = Entity(model='cube', color=color.azure, scale=1)
camera.parent = player
camera.position = (0, 1.5, -5)
camera.rotation = (0, 0, 0)

speed = 10
sensitivity = 100

# First-person view model (simple hand/cockpit)
fp_model = Entity(
    parent=camera,
    model='cube',
    color=color.orange,
    scale=(0.3, 0.3, 0.3),
    position=(0.4, -0.4, 1)
)

# Simple terrain map
ground = Entity(
    model='plane',
    texture='white_cube',
    texture_scale=(100, 100),
    scale=(100, 1, 100),
    color=color.green,
    collider='box'
)

# Add some cubes to simulate structures
for i in range(20):
    Entity(
        model='cube',
        color=color.gray,
        scale_y=5,
        position=(randint(-50, 50), 2.5, randint(-50, 50)),
        collider='box'
    )

def update():
    mouse_movement = Vec2(mouse.velocity.x, mouse.velocity.y) * sensitivity
    player.rotation_y += mouse_movement.x
    camera.rotation_x -= mouse_movement.y
    camera.rotation_x = clamp(camera.rotation_x, -90, 90)

    direction = Vec3(
        camera.forward.x,
        camera.forward.y,
        camera.forward.z
    ).normalized()

    move = Vec3(0, 0, 0)

    if held_keys['w']:
        move += direction
    if held_keys['s']:
        move -= direction
    if held_keys['a']:
        move -= camera.right
    if held_keys['d']:
        move += camera.right

    player.position += move * time.dt * speed

EditorCamera(enabled=False)

Sky(texture='sky_default')

control_panel = Entity(
    parent=camera.ui,
    model='quad',
    texture='img/control.png',
    scale=(2, 0.10),
    position=(0, -0.45)
)

app.run()
