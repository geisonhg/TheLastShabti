"""
05_render_hq.py  —  The Last Shabti
Renders high-quality PNG images for the Part 1 submission.
Uses Cycles so colours render correctly even without a GPU.

HOW TO USE:
  1. Open TheLastShabti.blend in Blender
  2. Run 04_compose_level.py first (builds the LevelPreview scene)
  3. Go to Scripting tab, open this file, Run Script
  4. Four PNG files are saved to Documentation/Screenshots/

OUTPUT FILES:
  nebu_front_hq.png          — character front view, Egyptian palette visible
  nebu_34_hq.png             — character 3/4 view showing headdress and scarab
  assets_overview_hq.png     — all 10 environment assets on dark bg with labels
  level_scene_hq.png         — composed level scene (replaces the grey overview)
"""

import bpy
import math
import os

# ---------------------------------------------------------------------------
# Output path  (relative to this script → Documentation/Screenshots)
# ---------------------------------------------------------------------------
SCRIPT_DIR      = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR     = os.path.dirname(os.path.dirname(SCRIPT_DIR))
SCREENSHOTS_DIR = os.path.join(PROJECT_DIR, "Documentation", "Screenshots")
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

scene = bpy.context.scene

# ---------------------------------------------------------------------------
# Render settings  (Cycles — works without GPU, shows all material colours)
# ---------------------------------------------------------------------------
scene.render.engine         = 'CYCLES'
scene.cycles.samples        = 64      # fast but clean enough for submission
scene.cycles.use_denoising  = True
scene.render.resolution_x   = 1280
scene.render.resolution_y   = 720
scene.render.image_settings.file_format = 'PNG'
scene.render.film_transparent = False

# World: dark Egyptian sky
world = bpy.data.worlds.get("World") or bpy.data.worlds.new("World")
bpy.context.scene.world = world
world.use_nodes = True
bg = world.node_tree.nodes.get("Background")
if bg:
    bg.inputs["Color"].default_value    = (0.06, 0.05, 0.08, 1.0)
    bg.inputs["Strength"].default_value = 0.25


def deselect():
    bpy.ops.object.select_all(action='DESELECT')


def set_cam(loc, rot_deg, lens=50):
    for obj in list(scene.objects):
        if obj.type == 'CAMERA' and obj.name.startswith("RND_"):
            bpy.data.objects.remove(obj, do_unlink=True)
    deselect()
    bpy.ops.object.camera_add(location=loc)
    cam = bpy.context.active_object
    cam.name = "RND_Cam"
    cam.rotation_euler = tuple(math.radians(d) for d in rot_deg)
    cam.data.lens = lens
    scene.camera = cam
    return cam


def set_lights_character():
    """3-point light rig focused on the character at origin."""
    for obj in list(scene.objects):
        if obj.type == 'LIGHT' and obj.name.startswith("RND_"):
            bpy.data.objects.remove(obj, do_unlink=True)

    # Key — warm Egyptian sun from upper-left
    deselect()
    bpy.ops.object.light_add(type='SUN', location=(2, -3, 5))
    k = bpy.context.active_object
    k.name = "RND_Key"
    k.rotation_euler = (math.radians(42), 0, math.radians(-35))
    k.data.energy = 4.5
    k.data.color  = (1.0, 0.92, 0.78)

    # Fill — cool blue from right
    deselect()
    bpy.ops.object.light_add(type='AREA', location=(-2, -2, 2))
    f = bpy.context.active_object
    f.name = "RND_Fill"
    f.rotation_euler = (math.radians(55), 0, math.radians(25))
    f.data.energy = 40
    f.data.size   = 3
    f.data.color  = (0.60, 0.72, 0.95)

    # Rim — gold back light to separate from background
    deselect()
    bpy.ops.object.light_add(type='SUN', location=(0, 3, 4))
    r = bpy.context.active_object
    r.name = "RND_Rim"
    r.rotation_euler = (math.radians(48), math.radians(180), 0)
    r.data.energy = 2.0
    r.data.color  = (0.95, 0.80, 0.40)


def hide_all_except(prefixes):
    """Hide all mesh/empty objects whose name doesn't start with any of the prefixes."""
    for obj in scene.objects:
        if obj.type in ('MESH', 'EMPTY', 'LIGHT', 'CAMERA'):
            keep = any(obj.name.startswith(p) for p in prefixes)
            obj.hide_render = not keep


def show_all():
    for obj in scene.objects:
        obj.hide_render = False


def render_to(filename):
    filepath = os.path.join(SCREENSHOTS_DIR, filename)
    scene.render.filepath = filepath
    bpy.ops.render.render(write_still=True)
    size = os.path.getsize(filepath + ".png") if os.path.exists(filepath + ".png") else \
           os.path.getsize(filepath) if os.path.exists(filepath) else 0
    print(f"  Saved: {filename}  ({size // 1024} KB)")


# ===========================================================================
# RENDER 1 — Nebu front view
# ===========================================================================
print("\n--- Render 1: Nebu front ---")
set_lights_character()
hide_all_except(["CH_Nebu", "RND_"])
set_cam((0, -2.6, 0.72), (90, 0, 0), lens=60)
render_to("nebu_front_hq")

# ===========================================================================
# RENDER 2 — Nebu 3/4 view
# ===========================================================================
print("--- Render 2: Nebu 3/4 ---")
set_cam((1.6, -2.0, 1.0), (76, 0, 34), lens=55)
render_to("nebu_34_hq")

# ===========================================================================
# RENDER 3 — Assets overview
# ===========================================================================
print("--- Render 3: assets overview ---")

# Remove existing RND_ lights and add an overhead studio light
for obj in list(scene.objects):
    if obj.type == 'LIGHT' and obj.name.startswith("RND_"):
        bpy.data.objects.remove(obj, do_unlink=True)

deselect()
bpy.ops.object.light_add(type='SUN', location=(0, -5, 10))
sl = bpy.context.active_object
sl.name = "RND_StudioKey"
sl.rotation_euler = (math.radians(35), 0, math.radians(-20))
sl.data.energy = 4.0
sl.data.color  = (1.0, 0.95, 0.85)

deselect()
bpy.ops.object.light_add(type='AREA', location=(0, 5, 5))
sa = bpy.context.active_object
sa.name = "RND_StudioFill"
sa.rotation_euler = (math.radians(60), math.radians(180), 0)
sa.data.energy = 60
sa.data.size   = 8
sa.data.color  = (0.70, 0.80, 1.0)

# Show only the individual asset roots (not LP_ level scene)
asset_prefixes = [
    "CH_Nebu", "ENV_SandstonePlatform", "ENV_Stair", "ENV_Ramp", "ENV_Archway",
    "PROP_BrokenColumn", "PROP_Obelisk", "PROP_BurialJar", "PROP_WallTorch",
    "PROP_ScarabWall", "PROP_SunAltar", "RND_"
]
hide_all_except(asset_prefixes)

# Wide angled shot covering all assets (spread at x=0..8, y=0..-16)
set_cam((4, -22, 12), (55, 0, 0), lens=35)
render_to("assets_overview_hq")

# ===========================================================================
# RENDER 4 — Level scene
# ===========================================================================
print("--- Render 4: level scene ---")
show_all()

# Only show LP_ objects + RND_ lights — hide scattered asset grid
hide_all_except(["LP_", "RND_"])

# Restore LP_ lights (they were hidden by hide_all_except above)
for obj in scene.objects:
    if obj.name.startswith("LP_") and obj.type == 'LIGHT':
        obj.hide_render = False

# Use the LP_Camera if it exists, otherwise place our own
lp_cam = scene.objects.get("LP_Camera")
if lp_cam:
    scene.camera = lp_cam
else:
    set_cam((0, -9.5, 4.8), (68, 0, 0), lens=35)

render_to("level_scene_hq")

# ===========================================================================
# Done
# ===========================================================================
show_all()
print("\n=== All renders complete ===")
print(f"Folder: {SCREENSHOTS_DIR}")
print("Files saved:")
for f in ["nebu_front_hq.png", "nebu_34_hq.png",
          "assets_overview_hq.png", "level_scene_hq.png"]:
    fp = os.path.join(SCREENSHOTS_DIR, f)
    if os.path.exists(fp):
        print(f"  {f}  ({os.path.getsize(fp)//1024} KB)")
    else:
        print(f"  {f}  — NOT FOUND")
