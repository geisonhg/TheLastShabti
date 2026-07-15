"""
05_render_hq.py  —  The Last Shabti
Configura la escena para renders de alta calidad.
NO llama render automáticamente para evitar crashes.

MODO DE USO:
  1. Cambia SHOT abajo al número de render que quieres (1, 2, 3 o 4)
  2. Run Script
  3. Presiona F12 para renderizar
  4. Ctrl+S en la ventana de render para guardar (o se guarda solo si OUTPUT_PATH es válido)
  5. Repite cambiando SHOT

SHOTS:
  1 = Nebu frontal
  2 = Nebu 3/4 view
  3 = Assets overview (grid de todos los assets)
  4 = Level scene compuesta (requiere haber corrido 04_compose_level.py primero)
"""

import bpy
import math
import os

# ── CAMBIA ESTE NÚMERO (1, 2, 3 o 4) ────────────────────────────────────────
SHOT = 1
# ─────────────────────────────────────────────────────────────────────────────

SCRIPT_DIR      = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR     = os.path.dirname(os.path.dirname(SCRIPT_DIR))
SCREENSHOTS_DIR = os.path.join(PROJECT_DIR, "Documentation", "Screenshots")
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

SHOT_NAMES = {
    1: "nebu_front_hq",
    2: "nebu_34_hq",
    3: "assets_overview_hq",
    4: "level_scene_hq",
}

scene = bpy.context.scene

# ── Render engine: Eevee (funciona en modo interactivo con GPU) ───────────────
scene.render.engine       = 'BLENDER_EEVEE_NEXT'
scene.eevee.taa_render_samples = 64
scene.render.resolution_x = 1280
scene.render.resolution_y = 720
scene.render.image_settings.file_format = 'PNG'
scene.render.film_transparent = False
scene.render.filepath = os.path.join(SCREENSHOTS_DIR, SHOT_NAMES[SHOT])


def deselect():
    bpy.ops.object.select_all(action='DESELECT')


def clear_rnd_objects():
    for obj in list(scene.objects):
        if obj.name.startswith("RND_"):
            bpy.data.objects.remove(obj, do_unlink=True)


def add_light(ltype, name, loc, energy, color, rot_deg=(0,0,0), size=None):
    deselect()
    bpy.ops.object.light_add(type=ltype, location=loc)
    light = bpy.context.active_object
    light.name = name
    light.data.energy = energy
    light.data.color  = color
    light.rotation_euler = tuple(math.radians(d) for d in rot_deg)
    if size:
        light.data.size = size
    return light


def set_camera(loc, rot_deg, lens=50):
    deselect()
    bpy.ops.object.camera_add(location=loc)
    cam = bpy.context.active_object
    cam.name = "RND_Camera"
    cam.rotation_euler = tuple(math.radians(d) for d in rot_deg)
    cam.data.lens = lens
    scene.camera = cam
    return cam


def show_all():
    for obj in scene.objects:
        obj.hide_render = False


def hide_all_except(prefixes):
    keep = tuple(prefixes)
    for obj in scene.objects:
        obj.hide_render = not any(obj.name.startswith(p) for p in keep)


# World background
world = bpy.data.worlds.get("World") or bpy.data.worlds.new("World")
scene.world = world
world.use_nodes = True
bg = world.node_tree.nodes.get("Background")
if bg:
    bg.inputs["Color"].default_value    = (0.06, 0.05, 0.08, 1.0)
    bg.inputs["Strength"].default_value = 0.3

# ── Remove previous RND_ objects ──────────────────────────────────────────────
clear_rnd_objects()
show_all()

# =============================================================================
if SHOT == 1:
    # Nebu frontal — muestra cuerpo y collar turquesa
    print("Shot 1: Nebu frontal")
    hide_all_except(["CH_Nebu"])
    add_light('SUN',  "RND_Key",  (2,-3,5),   energy=4.5, color=(1.0,0.92,0.78),
              rot_deg=(42,0,-35))
    add_light('AREA', "RND_Fill", (-2,-2,2),  energy=50,  color=(0.60,0.72,0.95),
              size=3, rot_deg=(55,0,25))
    add_light('SUN',  "RND_Rim",  (0,3,4),    energy=2.0, color=(0.95,0.80,0.40),
              rot_deg=(48,180,0))
    set_camera(loc=(0,-2.6,0.72), rot_deg=(90,0,0), lens=60)

elif SHOT == 2:
    # Nebu 3/4 — muestra tocado Nemes y escarabajo dorado
    print("Shot 2: Nebu 3/4")
    hide_all_except(["CH_Nebu"])
    add_light('SUN',  "RND_Key",  (2,-3,5),   energy=4.5, color=(1.0,0.92,0.78),
              rot_deg=(42,0,-35))
    add_light('AREA', "RND_Fill", (-2,-2,2),  energy=50,  color=(0.60,0.72,0.95),
              size=3, rot_deg=(55,0,25))
    add_light('SUN',  "RND_Rim",  (0,3,4),    energy=2.0, color=(0.95,0.80,0.40),
              rot_deg=(48,180,0))
    set_camera(loc=(1.6,-2.0,1.0), rot_deg=(76,0,34), lens=55)

elif SHOT == 3:
    # Assets overview — todos los assets en grid
    print("Shot 3: Assets overview")
    asset_prefixes = [
        "CH_Nebu", "ENV_SandstonePlatform", "ENV_Stair", "ENV_Ramp", "ENV_Archway",
        "PROP_BrokenColumn", "PROP_Obelisk", "PROP_BurialJar", "PROP_WallTorch",
        "PROP_ScarabWall", "PROP_SunAltar",
    ]
    hide_all_except(asset_prefixes)
    add_light('SUN',  "RND_Key",    (0,-5,10),  energy=4.0, color=(1.0,0.95,0.85),
              rot_deg=(35,0,-20))
    add_light('AREA', "RND_Fill",   (0, 5, 5),  energy=80,  color=(0.70,0.80,1.0),
              size=8, rot_deg=(60,180,0))
    # Wide shot covering the asset grid (assets spread at x=0..8, y=0..-16)
    set_camera(loc=(4,-22,12), rot_deg=(55,0,0), lens=35)

elif SHOT == 4:
    # Level scene (requiere haber corrido 04_compose_level.py)
    print("Shot 4: Level scene")
    lp_objects = [o for o in scene.objects if o.name.startswith("LP_")]
    if not lp_objects:
        print("ERROR: No LP_ objects found. Run 04_compose_level.py first!")
    else:
        hide_all_except(["LP_"])
        # Restore LP_ lights
        for obj in scene.objects:
            if obj.name.startswith("LP_") and obj.type == 'LIGHT':
                obj.hide_render = False
        lp_cam = scene.objects.get("LP_Camera")
        if lp_cam:
            scene.camera = lp_cam
        else:
            set_camera(loc=(0,-9.5,4.8), rot_deg=(68,0,0), lens=35)

print(f"\nListo para renderizar: SHOT {SHOT} — {SHOT_NAMES[SHOT]}")
print(f"Guardado en: {scene.render.filepath}.png")
print("Presiona F12 para renderizar.")
