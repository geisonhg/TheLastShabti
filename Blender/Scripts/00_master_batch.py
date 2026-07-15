"""
00_master_batch.py
Master batch script for The Last Shabti.
Run from command line:
  blender.exe --background --python 00_master_batch.py

This script:
  1. Clears the default scene
  2. Creates all shared materials
  3. Creates Nebu character
  4. Creates all 10 environment assets
  5. Saves TheLastShabti.blend
  6. Exports every asset as a separate FBX
  7. Renders preview images
"""

import bpy
import bmesh
import math
import os
import sys

# ---------------------------------------------------------------------------
# Path setup  (all relative to this script's location)
# ---------------------------------------------------------------------------
SCRIPT_DIR  = os.path.dirname(os.path.abspath(__file__))
BLENDER_DIR = os.path.dirname(SCRIPT_DIR)                          # .../Blender/
PROJECT_DIR = os.path.dirname(BLENDER_DIR)                         # .../TheLastShabti/
EXPORTS_DIR = os.path.join(BLENDER_DIR, "Exports")
SCREENSHOTS_DIR = os.path.join(PROJECT_DIR, "Documentation", "Screenshots")
BLEND_PATH  = os.path.join(BLENDER_DIR, "TheLastShabti.blend")

os.makedirs(EXPORTS_DIR, exist_ok=True)
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

print(f"\n=== The Last Shabti — Blender Batch ===")
print(f"Project : {PROJECT_DIR}")
print(f"Exports : {EXPORTS_DIR}")
print(f"Renders : {SCREENSHOTS_DIR}")
print("")

# ---------------------------------------------------------------------------
# Clear default scene
# ---------------------------------------------------------------------------
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()
for col in bpy.data.collections:
    bpy.data.collections.remove(col)

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------
def make_mat(name, rgb, roughness=0.85, metallic=0.0, emission=None):
    if name in bpy.data.materials:
        return bpy.data.materials[name]
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.inputs["Base Color"].default_value = (*rgb, 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metallic
    if emission:
        bsdf.inputs["Emission Color"].default_value = (*emission, 1.0)
        bsdf.inputs["Emission Strength"].default_value = 2.0
    out = nodes.new('ShaderNodeOutputMaterial')
    links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])
    return mat

def add_box(name, loc, scale, mat=None, rot=(0, 0, 0)):
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=loc)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = scale
    obj.rotation_euler = rot
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    if mat:
        obj.data.materials.append(mat)
    obj.data.name = name + "_Mesh"
    return obj

def deselect():
    bpy.ops.object.select_all(action='DESELECT')

def apply_all(obj):
    deselect()
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

def set_collection(obj, col_name):
    col = bpy.data.collections.get(col_name)
    if col is None:
        col = bpy.data.collections.new(col_name)
        bpy.context.scene.collection.children.link(col)
    if obj.name not in col.objects:
        col.objects.link(obj)
    for c in bpy.context.scene.collection.objects:
        pass  # keep in scene root too

# ---------------------------------------------------------------------------
# Materials
# ---------------------------------------------------------------------------
M_STONE  = make_mat("MAT_StoneBlue",   (0.44, 0.54, 0.62), roughness=0.90)
M_SAND   = make_mat("MAT_Sandstone",   (0.76, 0.62, 0.39), roughness=0.85)
M_GOLD   = make_mat("MAT_GoldAccent",  (0.78, 0.65, 0.18), roughness=0.25, metallic=0.75)
M_TURQ   = make_mat("MAT_Turquoise",   (0.28, 0.55, 0.52), roughness=0.70)
M_DARK   = make_mat("MAT_DarkBrown",   (0.15, 0.08, 0.04), roughness=0.92)
M_EYE    = make_mat("MAT_EyeBlack",    (0.05, 0.05, 0.06), roughness=0.95)
M_FIRE   = make_mat("MAT_TorchFire",   (0.90, 0.55, 0.08), roughness=0.20,
                    emission=(0.90, 0.55, 0.08))
M_CLAY   = make_mat("MAT_Clay",        (0.55, 0.38, 0.28), roughness=0.92)

print("Materials created.")

# ===========================================================================
# CH_NEBU
# ===========================================================================
print("\n--- Creating CH_Nebu ---")

# Body
body = add_box("CH_Nebu_Body", (0, 0, 0.38), (0.46, 0.36, 0.50), M_STONE)
belt = add_box("CH_Nebu_Belt", (0, 0, 0.34), (0.49, 0.39, 0.07), M_TURQ)
collar = add_box("CH_Nebu_Collar", (0, 0, 0.72), (0.50, 0.40, 0.07), M_TURQ)

# Head (slightly oversized)
deselect()
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 1.02))
head = bpy.context.active_object
head.name = "CH_Nebu_Head"
head.data.name = "CH_Nebu_Head_Mesh"
head.scale = (0.56, 0.50, 0.54)
bpy.ops.object.transform_apply(scale=True)
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.bevel(offset=0.04, segments=1, affect='EDGES')
bpy.ops.object.mode_set(mode='OBJECT')
head.data.materials.append(M_STONE)

# Nemes headdress
nemes_back = add_box("CH_Nebu_NemesBack", (0, -0.09, 1.18), (0.60, 0.08, 0.66), M_SAND)
nemes_l    = add_box("CH_Nebu_NemesLapL", (-0.36, 0.06, 0.84), (0.10, 0.10, 0.30), M_SAND,
                     rot=(0, 0.12, 0))
nemes_r    = add_box("CH_Nebu_NemesLapR", ( 0.36, 0.06, 0.84), (0.10, 0.10, 0.30), M_SAND,
                     rot=(0, -0.12, 0))
crown      = add_box("CH_Nebu_CrownBand", (0, 0.26, 1.24), (0.58, 0.04, 0.07), M_DARK)
uraeus     = add_box("CH_Nebu_Uraeus", (0, 0.28, 1.35), (0.04, 0.04, 0.10), M_GOLD)

# Eyes and kohl
eye_l  = add_box("CH_Nebu_EyeL",  (-0.15, 0.27, 1.02), (0.10, 0.03, 0.055), M_EYE)
eye_r  = add_box("CH_Nebu_EyeR",  ( 0.15, 0.27, 1.02), (0.10, 0.03, 0.055), M_EYE)
kohl_l = add_box("CH_Nebu_KohlL", (-0.24, 0.27, 1.02), (0.07, 0.025, 0.025), M_EYE)
kohl_r = add_box("CH_Nebu_KohlR", ( 0.24, 0.27, 1.02), (0.07, 0.025, 0.025), M_EYE)

# Scarab chest piece
deselect()
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0.37, 0.56))
scarab = bpy.context.active_object
scarab.name = "CH_Nebu_Scarab"
scarab.data.name = "CH_Nebu_Scarab_Mesh"
scarab.scale = (0.10, 0.03, 0.10)
bpy.ops.object.transform_apply(scale=True)
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.bevel(offset=0.02, segments=2, affect='EDGES')
bpy.ops.object.mode_set(mode='OBJECT')
scarab.data.materials.append(M_GOLD)

wing_l = add_box("CH_Nebu_WingL", (-0.17, 0.37, 0.55), (0.09, 0.025, 0.055), M_GOLD,
                 rot=(0, 0,  0.25))
wing_r = add_box("CH_Nebu_WingR", ( 0.17, 0.37, 0.55), (0.09, 0.025, 0.055), M_GOLD,
                 rot=(0, 0, -0.25))

# Arms and legs
arm_l = add_box("CH_Nebu_ArmL", (-0.52, 0, 0.50), (0.13, 0.14, 0.34), M_STONE,
                rot=(0,  0.18, 0))
arm_r = add_box("CH_Nebu_ArmR", ( 0.52, 0, 0.50), (0.13, 0.14, 0.34), M_STONE,
                rot=(0, -0.18, 0))
leg_l = add_box("CH_Nebu_LegL", (-0.16, 0.01, 0.11), (0.15, 0.18, 0.26), M_STONE)
leg_r = add_box("CH_Nebu_LegR", ( 0.16, 0.01, 0.11), (0.15, 0.18, 0.26), M_STONE)

# Root empty - parent for all parts
deselect()
bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
nebu_root = bpy.context.active_object
nebu_root.name = "CH_Nebu"

nebu_parts = [body, belt, collar, head, nemes_back, nemes_l, nemes_r, crown, uraeus,
               eye_l, eye_r, kohl_l, kohl_r, scarab, wing_l, wing_r, arm_l, arm_r,
               leg_l, leg_r]
for p in nebu_parts:
    p.parent = nebu_root

print(f"  CH_Nebu: {len(nebu_parts)} parts created.")

# ===========================================================================
# ENV_SandstonePlatform
# ===========================================================================
print("\n--- Creating ENV_SandstonePlatform ---")
deselect()
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -4, 0))
plat = bpy.context.active_object
plat.name = "ENV_SandstonePlatform"
plat.data.name = "ENV_SandstonePlatform_Mesh"
plat.scale = (2.0, 1.0, 0.4)
bpy.ops.object.transform_apply(scale=True)
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.bevel(offset=0.025, segments=1, affect='EDGES')
bpy.ops.object.mode_set(mode='OBJECT')
plat.data.materials.append(M_SAND)

edge = add_box("ENV_SandstonePlatform_Edge", (0, -3.49, 0), (2.05, 0.02, 0.42), M_DARK)
edge.parent = plat

# ===========================================================================
# PROP_BrokenColumn
# ===========================================================================
print("--- Creating PROP_BrokenColumn ---")
deselect()
bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.28, depth=1.6,
                                     location=(4, -4, 0))
col_obj = bpy.context.active_object
col_obj.name = "PROP_BrokenColumn"
col_obj.data.name = "PROP_BrokenColumn_Mesh"
bpy.ops.object.transform_apply(scale=True)
col_obj.data.materials.append(M_STONE)

bpy.ops.object.mode_set(mode='EDIT')
bm = bmesh.from_edit_mesh(col_obj.data)
bm.verts.ensure_lookup_table()
for i, v in enumerate([v for v in bm.verts if v.co.z > 0.68]):
    if i % 2 == 0:
        v.co.z -= 0.14
        v.co.x *= 0.78
        v.co.y *= 0.78
    else:
        v.co.z -= 0.04
bmesh.update_edit_mesh(col_obj.data)
bpy.ops.object.mode_set(mode='OBJECT')

base_ring = add_box("PROP_BrokenColumn_Base", (4, -4, -0.76), (0.70, 0.70, 0.12), M_SAND)
base_ring.parent = col_obj

# ===========================================================================
# PROP_Obelisk
# ===========================================================================
print("--- Creating PROP_Obelisk ---")
deselect()
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(8, -4, 0))
ob = bpy.context.active_object
ob.name = "PROP_Obelisk"
ob.data.name = "PROP_Obelisk_Mesh"
ob.scale = (0.4, 0.4, 3.0)
bpy.ops.object.transform_apply(scale=True)
bpy.ops.object.mode_set(mode='EDIT')
bm = bmesh.from_edit_mesh(ob.data)
bm.verts.ensure_lookup_table()
for v in bm.verts:
    if v.co.z > 1.5:
        v.co.x *= 0.45
        v.co.y *= 0.45
bmesh.update_edit_mesh(ob.data)
bpy.ops.object.mode_set(mode='OBJECT')
ob.data.materials.append(M_SAND)

deselect()
bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=0.19, radius2=0.0,
                                 depth=0.38, location=(8, -4, 3.19))
ob_cap = bpy.context.active_object
ob_cap.name = "PROP_Obelisk_Cap"
ob_cap.data.name = "PROP_Obelisk_Cap_Mesh"
ob_cap.rotation_euler = (0, 0, math.pi / 4)
bpy.ops.object.transform_apply(rotation=True)
ob_cap.data.materials.append(M_GOLD)
ob_cap.parent = ob

ob_engrave = add_box("PROP_Obelisk_Engrave", (8, -3.79, 1.0), (0.28, 0.01, 1.6), M_DARK)
ob_engrave.parent = ob

# ===========================================================================
# PROP_BurialJar
# ===========================================================================
print("--- Creating PROP_BurialJar ---")
deselect()
bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.22, depth=0.9,
                                     end_fill_type='NGON', location=(0, -8, 0))
jar = bpy.context.active_object
jar.name = "PROP_BurialJar"
jar.data.name = "PROP_BurialJar_Mesh"
bpy.ops.object.transform_apply(scale=True)
jar.data.materials.append(M_CLAY)

bpy.ops.object.mode_set(mode='EDIT')
bm = bmesh.from_edit_mesh(jar.data)
bm.verts.ensure_lookup_table()
for v in bm.verts:
    t = (v.co.z + 0.45) / 0.9
    if 0.20 < t < 0.72:
        belly = 1.0 + 0.65 * math.sin(math.pi * ((t - 0.20) / 0.52))
        v.co.x *= belly
        v.co.y *= belly
    elif t > 0.72:
        neck = max(0.40, 1.0 - (t - 0.72) * 2.0)
        v.co.x *= neck
        v.co.y *= neck
bmesh.update_edit_mesh(jar.data)
bpy.ops.object.mode_set(mode='OBJECT')

deselect()
bpy.ops.mesh.primitive_cone_add(vertices=12, radius1=0.12, radius2=0.05,
                                 depth=0.13, location=(0, -8, 0.52))
jar_lid = bpy.context.active_object
jar_lid.name = "PROP_BurialJar_Lid"
jar_lid.data.name = "PROP_BurialJar_Lid_Mesh"
jar_lid.data.materials.append(M_CLAY)
jar_lid.parent = jar

jar_stripe = add_box("PROP_BurialJar_Stripe", (0, -8, 0.05), (0.48, 0.48, 0.06), M_TURQ)
jar_stripe.parent = jar

# ===========================================================================
# PROP_WallTorch
# ===========================================================================
print("--- Creating PROP_WallTorch ---")
deselect()
wall_plate = add_box("PROP_WallTorch", (4, -8, 0), (0.20, 0.06, 0.26), M_STONE)

bracket = add_box("PROP_WallTorch_Bracket", (4, -7.70, 0.07), (0.45, 0.08, 0.07), M_DARK)
bracket.parent = wall_plate

deselect()
bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.09, depth=0.12,
                                     location=(4.22, -7.70, 0.19))
cup = bpy.context.active_object
cup.name = "PROP_WallTorch_Cup"
cup.data.name = "PROP_WallTorch_Cup_Mesh"
cup.data.materials.append(M_DARK)
cup.parent = wall_plate

deselect()
bpy.ops.mesh.primitive_cone_add(vertices=6, radius1=0.07, radius2=0.01,
                                 depth=0.24, location=(4.22, -7.70, 0.38))
flame = bpy.context.active_object
flame.name = "PROP_WallTorch_Flame"
flame.data.name = "PROP_WallTorch_Flame_Mesh"
flame.data.materials.append(M_FIRE)
flame.parent = wall_plate

# ===========================================================================
# PROP_ScarabWall
# ===========================================================================
print("--- Creating PROP_ScarabWall ---")
deselect()
panel = add_box("PROP_ScarabWall", (8, -8, 0), (0.72, 0.07, 0.82), M_SAND)

deselect()
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(8, -8.02, 0.08))
sb = bpy.context.active_object
sb.name = "PROP_ScarabWall_Body"
sb.data.name = "PROP_ScarabWall_Body_Mesh"
sb.scale = (0.18, 0.03, 0.24)
bpy.ops.object.transform_apply(scale=True)
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.bevel(offset=0.03, segments=2, affect='EDGES')
bpy.ops.object.mode_set(mode='OBJECT')
sb.data.materials.append(M_DARK)
sb.parent = panel

sh = add_box("PROP_ScarabWall_Head", (8, -8.02, 0.32), (0.11, 0.03, 0.11), M_DARK)
sh.parent = panel

wl = add_box("PROP_ScarabWall_WingL", (7.73, -8.02, 0.08), (0.24, 0.03, 0.18), M_TURQ,
             rot=(0, 0, 0.30))
wl.parent = panel
wr = add_box("PROP_ScarabWall_WingR", (8.27, -8.02, 0.08), (0.24, 0.03, 0.18), M_TURQ,
             rot=(0, 0, -0.30))
wr.parent = panel

for i, (sx, sz) in enumerate([(-0.24,-0.10),(-0.22,0.0),(-0.20,0.10),
                                (0.20,-0.10),(0.22,0.0),(0.24,0.10)]):
    side_sign = -1 if sx < 0 else 1
    leg = add_box(f"PROP_ScarabWall_Leg{i}", (8+sx, -8.02, sz),
                  (0.14, 0.025, 0.025), M_DARK,
                  rot=(0, 0, math.pi/2 + side_sign*0.3))
    leg.parent = panel

# ===========================================================================
# PROP_SunAltar
# ===========================================================================
print("--- Creating PROP_SunAltar ---")
deselect()
tier1 = add_box("PROP_SunAltar", (0, -12, 0.15), (2.2, 2.2, 0.30), M_SAND)

tier2 = add_box("PROP_SunAltar_Tier2", (0, -12, 0.48), (1.55, 1.55, 0.24), M_SAND)
tier2.parent = tier1
tier3 = add_box("PROP_SunAltar_Tier3", (0, -12, 0.74), (0.95, 0.95, 0.20), M_STONE)
tier3.parent = tier1

deselect()
bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.52, depth=0.07,
                                     location=(0, -12, 0.89))
disc = bpy.context.active_object
disc.name = "PROP_SunAltar_Disc"
disc.data.name = "PROP_SunAltar_Disc_Mesh"
disc.data.materials.append(M_GOLD)
disc.parent = tier1

for i in range(8):
    angle = (i / 8) * 2 * math.pi
    ray = add_box(f"PROP_SunAltar_Ray{i}",
                  (0 + 0.72 * math.cos(angle), -12 + 0.72 * math.sin(angle), 0.89),
                  (0.08, 0.22, 0.04), M_GOLD, rot=(0, 0, angle + math.pi/2))
    ray.parent = tier1

for dx, dy in [(-0.90,-0.90),(0.90,-0.90),(-0.90,0.90),(0.90,0.90)]:
    post = add_box("PROP_SunAltar_Post", (0+dx, -12+dy, 0.55), (0.12, 0.12, 0.60), M_SAND)
    post.parent = tier1

# ===========================================================================
# ENV_Stair
# ===========================================================================
print("--- Creating ENV_Stair ---")
deselect()
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(4, -12, 0))
step = bpy.context.active_object
step.name = "ENV_Stair"
step.data.name = "ENV_Stair_Mesh"
step.scale = (1.5, 0.50, 0.22)
bpy.ops.object.transform_apply(scale=True)
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.bevel(offset=0.02, segments=1, affect='EDGES')
bpy.ops.object.mode_set(mode='OBJECT')
step.data.materials.append(M_SAND)

# ===========================================================================
# ENV_Ramp
# ===========================================================================
print("--- Creating ENV_Ramp ---")
deselect()
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(8, -12, 0))
ramp = bpy.context.active_object
ramp.name = "ENV_Ramp"
ramp.data.name = "ENV_Ramp_Mesh"
ramp.scale = (2.0, 1.8, 0.55)
bpy.ops.object.transform_apply(scale=True)
bpy.ops.object.mode_set(mode='EDIT')
bm = bmesh.from_edit_mesh(ramp.data)
bm.verts.ensure_lookup_table()
for v in bm.verts:
    if v.co.y < -0.60 and v.co.z > 0.20:
        v.co.z = -0.275
bmesh.update_edit_mesh(ramp.data)
bpy.ops.object.mode_set(mode='OBJECT')
ramp.data.materials.append(M_SAND)

# ===========================================================================
# ENV_Archway
# ===========================================================================
print("--- Creating ENV_Archway ---")
deselect()
AX, AY = 0, -16

pillar_l = add_box("ENV_Archway", (AX - 0.58, AY, 1.1), (0.36, 0.36, 2.4), M_STONE)

pillar_r = add_box("ENV_Archway_PillarR", (AX + 0.58, AY, 1.1), (0.36, 0.36, 2.4), M_STONE)
pillar_r.parent = pillar_l

lintel = add_box("ENV_Archway_Lintel", (AX, AY, 2.45), (1.56, 0.42, 0.30), M_SAND)
lintel.parent = pillar_l

groove = add_box("ENV_Archway_Groove", (AX, AY - 0.17, 2.45), (1.12, 0.02, 0.12), M_DARK)
groove.parent = pillar_l

for side, cname in [(-1,"ENV_Archway_CapL"),(1,"ENV_Archway_CapR")]:
    cap = add_box(cname, (AX+side*0.58, AY, 0.07), (0.46, 0.46, 0.14), M_SAND)
    cap.parent = pillar_l

for side, cname in [(-1,"ENV_Archway_TopL"),(1,"ENV_Archway_TopR")]:
    top = add_box(cname, (AX+side*0.58, AY, 2.33), (0.46, 0.46, 0.10), M_SAND)
    top.parent = pillar_l

print("\nAll assets created.")

# ===========================================================================
# RENDER SETUP  — render preview images
# ===========================================================================
print("\n--- Setting up render ---")

scene = bpy.context.scene
scene.render.engine = 'BLENDER_EEVEE_NEXT'
scene.render.resolution_x = 960
scene.render.resolution_y = 720
scene.render.film_transparent = True
scene.eevee.taa_render_samples = 32
# use_soft_shadows removed in Eevee Next (Blender 4.2+)

# World background
world = bpy.data.worlds.new("World")
bpy.context.scene.world = world
world.use_nodes = True
bg_node = world.node_tree.nodes.get("Background")
if bg_node:
    bg_node.inputs["Color"].default_value = (0.08, 0.07, 0.06, 1.0)
    bg_node.inputs["Strength"].default_value = 0.5

def add_sun(name, loc, energy=3.0, color=(1,0.95,0.85)):
    deselect()
    bpy.ops.object.light_add(type='SUN', location=loc)
    light = bpy.context.active_object
    light.name = name
    light.data.energy = energy
    light.data.color = color
    light.rotation_euler = (math.radians(45), 0, math.radians(-45))
    return light

def add_area(name, loc, energy=2.0, size=2.0, color=(1,0.95,0.85)):
    deselect()
    bpy.ops.object.light_add(type='AREA', location=loc)
    light = bpy.context.active_object
    light.name = name
    light.data.energy = energy
    light.data.size = size
    light.data.color = color
    return light

def add_cam(name, loc, rot_deg):
    deselect()
    bpy.ops.object.camera_add(location=loc)
    cam = bpy.context.active_object
    cam.name = name
    cam.rotation_euler = tuple(math.radians(d) for d in rot_deg)
    return cam

# Key + Fill + Rim lights for character render
sun_key  = add_sun("Light_Key",  (2, -3, 4),  energy=4.0, color=(1.0, 0.95, 0.85))
sun_fill = add_sun("Light_Fill", (-2, -2, 3), energy=1.5, color=(0.6, 0.7, 0.9))
sun_rim  = add_sun("Light_Rim",  (0, 3, 5),   energy=2.0, color=(1.0, 0.8, 0.4))

# --- RENDER 1: Nebu front ---
cam1 = add_cam("Camera_NebuFront", (0, -2.5, 0.7), (88, 0, 0))
scene.camera = cam1
scene.render.filepath = os.path.join(SCREENSHOTS_DIR, "nebu_character_front")
scene.render.image_settings.file_format = 'PNG'

# Hide all non-Nebu objects temporarily
all_objects = list(bpy.context.scene.objects)
for obj in all_objects:
    if obj.type in ('MESH', 'EMPTY') and not obj.name.startswith("CH_Nebu") and not obj.name.startswith("Light") and obj.type != 'CAMERA':
        obj.hide_render = True

bpy.ops.render.render(write_still=True)
print(f"  Rendered: nebu_character_front.png")

# --- RENDER 2: Nebu 3/4 view ---
cam2 = add_cam("Camera_Nebu34", (1.5, -2.2, 1.1), (78, 0, 32))
scene.camera = cam2
scene.render.filepath = os.path.join(SCREENSHOTS_DIR, "nebu_character_34view")
bpy.ops.render.render(write_still=True)
print(f"  Rendered: nebu_character_34view.png")

# Unhide all objects
for obj in all_objects:
    obj.hide_render = False

# --- RENDER 3: Asset collection overview ---
cam3 = add_cam("Camera_Assets", (4, -18, 8), (58, 0, 0))
scene.camera = cam3
scene.render.filepath = os.path.join(SCREENSHOTS_DIR, "blender_assets_overview")
bpy.ops.render.render(write_still=True)
print(f"  Rendered: blender_assets_overview.png")

# ===========================================================================
# FBX EXPORT
# ===========================================================================
print("\n--- Exporting FBX files ---")

FBX_SETTINGS = dict(
    use_selection=True,
    global_scale=1.0,
    apply_unit_scale=True,
    apply_scale_options='FBX_SCALE_NONE',
    bake_space_transform=False,
    object_types={'MESH', 'EMPTY', 'ARMATURE'},
    use_mesh_modifiers=True,
    mesh_smooth_type='FACE',
    use_tspace=False,
    use_custom_props=False,
    add_leaf_bones=False,
    primary_bone_axis='Y',
    secondary_bone_axis='X',
    bake_anim=False,
    path_mode='AUTO',
    axis_forward='-Z',
    axis_up='Y',
)

def export_root(root_name, filename=None):
    fname = filename or root_name
    if root_name not in bpy.data.objects:
        print(f"  SKIP (not found): {root_name}")
        return False
    root_obj = bpy.data.objects[root_name]
    deselect()
    root_obj.select_set(True)
    for child in root_obj.children_recursive:
        child.select_set(True)
    bpy.context.view_layer.objects.active = root_obj
    fp = os.path.join(EXPORTS_DIR, fname + ".fbx")
    bpy.ops.export_scene.fbx(filepath=fp, **FBX_SETTINGS)
    size = os.path.getsize(fp) if os.path.exists(fp) else 0
    print(f"  {fname}.fbx  ({size} bytes)")
    return size > 0

results = {}
results["CH_Nebu"]               = export_root("CH_Nebu")
results["ENV_SandstonePlatform"] = export_root("ENV_SandstonePlatform")
results["ENV_Stair"]             = export_root("ENV_Stair")
results["ENV_Ramp"]              = export_root("ENV_Ramp")
results["ENV_Archway"]           = export_root("ENV_Archway")
results["PROP_BrokenColumn"]     = export_root("PROP_BrokenColumn")
results["PROP_Obelisk"]          = export_root("PROP_Obelisk")
results["PROP_BurialJar"]        = export_root("PROP_BurialJar")
results["PROP_WallTorch"]        = export_root("PROP_WallTorch")
results["PROP_ScarabWall"]       = export_root("PROP_ScarabWall")
results["PROP_SunAltar"]         = export_root("PROP_SunAltar")

# ===========================================================================
# SAVE BLEND FILE
# ===========================================================================
print(f"\n--- Saving blend file ---")
bpy.ops.wm.save_as_mainfile(filepath=BLEND_PATH)
print(f"  Saved: {BLEND_PATH}")

# ===========================================================================
# SUMMARY
# ===========================================================================
print("\n=== BATCH COMPLETE ===")
ok  = [k for k, v in results.items() if v]
bad = [k for k, v in results.items() if not v]
print(f"FBX exported OK : {len(ok)}")
if bad:
    print(f"FBX FAILED      : {bad}")
print(f"Blend file      : {BLEND_PATH}")
print(f"Exports folder  : {EXPORTS_DIR}")
print(f"Screenshots     : {SCREENSHOTS_DIR}")
if bad:
    sys.exit(1)
