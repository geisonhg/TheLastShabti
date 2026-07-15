"""
04_compose_level.py  —  The Last Shabti
Builds a composed level-preview scene in Blender using all the game assets.
Shows the level layout as it exists in Unity: staircase, platforms,
archways, props, lighting atmosphere.

HOW TO USE:
  1. Open TheLastShabti.blend  (run 00_master_batch.py first if not done)
  2. Go to Scripting tab, open this file, Run Script
  3. A new collection "LevelPreview" appears with the full scene
  4. Switch viewport to Rendered view to see colours
  5. Run 05_render_hq.py to save high-quality PNGs
"""

import bpy
import math


def deselect():
    bpy.ops.object.select_all(action='DESELECT')


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
        bsdf.inputs["Emission Strength"].default_value = 3.0
    out = nodes.new('ShaderNodeOutputMaterial')
    links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])
    return mat


def box(name, loc, scale, mat, rot=(0, 0, 0), col=None):
    deselect()
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=loc)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = scale
    obj.rotation_euler = rot
    bpy.ops.object.transform_apply(rotation=True, scale=True)
    obj.data.materials.append(mat)
    if col:
        if col not in bpy.data.collections:
            c = bpy.data.collections.new(col)
            bpy.context.scene.collection.children.link(c)
        bpy.data.collections[col].objects.link(obj)
    return obj


# ---------------------------------------------------------------------------
# Materials
# ---------------------------------------------------------------------------
M_SAND  = make_mat("MAT_Sandstone",  (0.76, 0.62, 0.39), roughness=0.88)
M_DARK  = make_mat("MAT_DarkBrown",  (0.15, 0.08, 0.04), roughness=0.92)
M_TURQ  = make_mat("MAT_Turquoise",  (0.28, 0.55, 0.52), roughness=0.70)
M_GOLD  = make_mat("MAT_GoldAccent", (0.78, 0.65, 0.18), roughness=0.25, metallic=0.75)
M_STONE = make_mat("MAT_StoneBlue",  (0.44, 0.54, 0.62), roughness=0.90)
M_FIRE  = make_mat("MAT_TorchFire",  (0.90, 0.55, 0.08), roughness=0.20,
                   emission=(0.90, 0.55, 0.08))
M_CLAY  = make_mat("MAT_Clay",       (0.55, 0.38, 0.28), roughness=0.92)

COL = "LevelPreview"

# ---------------------------------------------------------------------------
# Ground floor
# ---------------------------------------------------------------------------
box("LP_Floor", (0, 0, -0.15), (14, 5, 0.30), M_SAND, col=COL)

# Back wall
box("LP_BackWall", (0, 2.6, 1.5), (14, 0.2, 3.0), M_STONE, col=COL)

# ---------------------------------------------------------------------------
# Staircase  (S1 — 5 steps going right and up)
# ---------------------------------------------------------------------------
for i in range(5):
    box(f"LP_Step{i}",
        (-5.5 + i * 0.8, 0, 0.11 + i * 0.22),
        (0.8, 4.8, 0.22 + i * 0.22),
        M_SAND, col=COL)

# Landing platform at top of stairs
box("LP_Landing", (-1.5, 0, 1.25), (2.4, 4.8, 0.22), M_SAND, col=COL)

# ---------------------------------------------------------------------------
# Three gap platforms (S2 style)
# ---------------------------------------------------------------------------
box("LP_Plat1", (0.8, 0, 1.58), (1.6, 3.0, 0.20), M_SAND, col=COL)
box("LP_Plat2", (2.4, 0, 1.80), (1.2, 3.0, 0.20), M_SAND, col=COL)
box("LP_Plat3", (3.8, 0, 2.05), (1.4, 3.0, 0.20), M_SAND, col=COL)

# Ramp connecting to higher section
deselect()
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(5.0, 0, 1.55))
ramp = bpy.context.active_object
ramp.name = "LP_Ramp"
ramp.scale = (1.4, 3.0, 0.50)
bpy.ops.object.transform_apply(scale=True)
import bmesh
bpy.ops.object.mode_set(mode='EDIT')
bm = bmesh.from_edit_mesh(ramp.data)
bm.verts.ensure_lookup_table()
for v in bm.verts:
    if v.co.x < -0.45 and v.co.z > 0.15:
        v.co.z = -0.25
bmesh.update_edit_mesh(ramp.data)
bpy.ops.object.mode_set(mode='OBJECT')
ramp.data.materials.append(M_SAND)
if COL not in bpy.data.collections:
    c = bpy.data.collections.new(COL)
    bpy.context.scene.collection.children.link(c)
bpy.data.collections[COL].objects.link(ramp)

# ---------------------------------------------------------------------------
# Archway  (S1→S2 transition, centre of scene)
# ---------------------------------------------------------------------------
box("LP_ArchPillarL", (-0.4, 2.4, 1.55), (0.28, 0.28, 1.90), M_STONE, col=COL)
box("LP_ArchPillarR", ( 0.4, 2.4, 1.55), (0.28, 0.28, 1.90), M_STONE, col=COL)
box("LP_ArchLintel",  ( 0.0, 2.4, 2.56), (1.10, 0.32, 0.24), M_SAND,  col=COL)
box("LP_ArchGroove",  ( 0.0, 2.32, 2.56),(0.80, 0.02, 0.10), M_DARK,  col=COL)

# ---------------------------------------------------------------------------
# Obelisks  (pair flanking the back)
# ---------------------------------------------------------------------------
for sx in (-5.5, 5.5):
    deselect()
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(sx, 2.0, 1.70))
    ob = bpy.context.active_object
    ob.name = f"LP_Obelisk_{sx}"
    ob.scale = (0.28, 0.28, 2.10)
    bpy.ops.object.transform_apply(scale=True)
    bpy.ops.object.mode_set(mode='EDIT')
    bm2 = bmesh.from_edit_mesh(ob.data)
    bm2.verts.ensure_lookup_table()
    for v in bm2.verts:
        if v.co.z > 1.0:
            v.co.x *= 0.40
            v.co.y *= 0.40
    bmesh.update_edit_mesh(ob.data)
    bpy.ops.object.mode_set(mode='OBJECT')
    ob.data.materials.append(M_SAND)
    bpy.data.collections[COL].objects.link(ob)

    deselect()
    bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=0.13, radius2=0.0,
                                     depth=0.26, location=(sx, 2.0, 2.93))
    cap = bpy.context.active_object
    cap.name = f"LP_ObeliskCap_{sx}"
    cap.rotation_euler = (0, 0, math.pi / 4)
    bpy.ops.object.transform_apply(rotation=True)
    cap.data.materials.append(M_GOLD)
    bpy.data.collections[COL].objects.link(cap)

# ---------------------------------------------------------------------------
# Burial jars (cluster near start)
# ---------------------------------------------------------------------------
for i, (jx, jy) in enumerate([(-5.8, 1.8), (-5.2, 2.0), (-4.9, 1.5)]):
    deselect()
    bpy.ops.mesh.primitive_cylinder_add(vertices=10, radius=0.15, depth=0.60,
                                         location=(jx, jy, 0.15))
    jar = bpy.context.active_object
    jar.name = f"LP_Jar{i}"
    jar.data.materials.append(M_CLAY)
    bpy.ops.object.mode_set(mode='EDIT')
    bm3 = bmesh.from_edit_mesh(jar.data)
    bm3.verts.ensure_lookup_table()
    for v in bm3.verts:
        t = (v.co.z + 0.30) / 0.60
        if 0.20 < t < 0.72:
            belly = 1.0 + 0.55 * math.sin(math.pi * ((t - 0.20) / 0.52))
            v.co.x *= belly
            v.co.y *= belly
        elif t > 0.72:
            v.co.x *= max(0.40, 1.0 - (t - 0.72) * 2.0)
            v.co.y *= max(0.40, 1.0 - (t - 0.72) * 2.0)
    bmesh.update_edit_mesh(jar.data)
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.data.collections[COL].objects.link(jar)

    deselect()
    bpy.ops.mesh.primitive_cone_add(vertices=10, radius1=0.08, radius2=0.04,
                                     depth=0.09, location=(jx, jy, 0.49))
    lid = bpy.context.active_object
    lid.name = f"LP_JarLid{i}"
    lid.data.materials.append(M_CLAY)
    bpy.data.collections[COL].objects.link(lid)

# ---------------------------------------------------------------------------
# Wall torches (on back wall, two positions)
# ---------------------------------------------------------------------------
for tx in (-3.0, 3.0):
    box(f"LP_TorchPlate_{tx}", (tx, 2.52, 1.60), (0.14, 0.06, 0.18), M_STONE, col=COL)
    box(f"LP_TorchBracket_{tx}", (tx+0.18, 2.45, 1.64), (0.30, 0.06, 0.05), M_DARK, col=COL)
    deselect()
    bpy.ops.mesh.primitive_cone_add(vertices=6, radius1=0.06, radius2=0.01,
                                     depth=0.18, location=(tx+0.33, 2.45, 1.82))
    fl = bpy.context.active_object
    fl.name = f"LP_Flame_{tx}"
    fl.data.materials.append(M_FIRE)
    bpy.data.collections[COL].objects.link(fl)

# ---------------------------------------------------------------------------
# Sun altar (right end of scene — the goal)
# ---------------------------------------------------------------------------
box("LP_AltarBase",  (6.0, 0, 2.30), (1.6, 1.6, 0.22), M_SAND, col=COL)
box("LP_AltarTier2", (6.0, 0, 2.52), (1.1, 1.1, 0.18), M_SAND, col=COL)
box("LP_AltarTier3", (6.0, 0, 2.70), (0.68, 0.68, 0.14), M_STONE, col=COL)
deselect()
bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.36, depth=0.05,
                                     location=(6.0, 0, 2.80))
disc = bpy.context.active_object
disc.name = "LP_SunDisc"
disc.data.materials.append(M_GOLD)
bpy.data.collections[COL].objects.link(disc)

for i in range(8):
    angle = (i / 8) * 2 * math.pi
    box(f"LP_Ray{i}",
        (6.0 + 0.50 * math.cos(angle), 0.50 * math.sin(angle), 2.80),
        (0.06, 0.16, 0.03), M_GOLD,
        rot=(0, 0, angle + math.pi/2), col=COL)

# ---------------------------------------------------------------------------
# Player character (Nebu) — small figure at start of staircase
# ---------------------------------------------------------------------------
box("LP_Nebu_Body",   (-5.5, 0, 0.62), (0.24, 0.19, 0.26), M_STONE, col=COL)
box("LP_Nebu_Belt",   (-5.5, 0, 0.60), (0.26, 0.20, 0.04), M_TURQ,  col=COL)
box("LP_Nebu_Head",   (-5.5, 0, 0.98), (0.28, 0.25, 0.27), M_STONE, col=COL)
box("LP_Nebu_Nemes",  (-5.5,-0.04,1.09),(0.30, 0.04, 0.33), M_SAND, col=COL)

# ---------------------------------------------------------------------------
# Lighting  (Egyptian atmosphere)
# ---------------------------------------------------------------------------
# Remove existing lights
for obj in list(bpy.context.scene.objects):
    if obj.type == 'LIGHT':
        bpy.data.objects.remove(obj, do_unlink=True)

deselect()
bpy.ops.object.light_add(type='SUN', location=(5, -8, 10))
key = bpy.context.active_object
key.name = "LP_KeyLight"
key.rotation_euler = (math.radians(38), 0, math.radians(-25))
key.data.energy = 5.0
key.data.color = (1.0, 0.90, 0.75)

deselect()
bpy.ops.object.light_add(type='AREA', location=(-4, -6, 4))
fill = bpy.context.active_object
fill.name = "LP_FillLight"
fill.rotation_euler = (math.radians(50), 0, math.radians(30))
fill.data.energy = 60
fill.data.size = 5
fill.data.color = (0.55, 0.65, 0.90)

# Point lights for torch glow
for tx in (-3.0, 3.0):
    deselect()
    bpy.ops.object.light_add(type='POINT', location=(tx + 0.4, 2.3, 1.85))
    torch_light = bpy.context.active_object
    torch_light.name = f"LP_TorchGlow_{tx}"
    torch_light.data.energy = 12
    torch_light.data.color = (1.0, 0.55, 0.15)

# ---------------------------------------------------------------------------
# Camera
# ---------------------------------------------------------------------------
for obj in list(bpy.context.scene.objects):
    if obj.type == 'CAMERA' and obj.name.startswith("LP_"):
        bpy.data.objects.remove(obj, do_unlink=True)

deselect()
bpy.ops.object.camera_add(location=(0, -9, 4.5))
cam = bpy.context.active_object
cam.name = "LP_Camera"
cam.rotation_euler = (math.radians(68), 0, 0)
cam.data.lens = 35
bpy.context.scene.camera = cam

# ---------------------------------------------------------------------------
# World
# ---------------------------------------------------------------------------
world = bpy.data.worlds.get("World") or bpy.data.worlds.new("World")
bpy.context.scene.world = world
world.use_nodes = True
bg = world.node_tree.nodes.get("Background")
if bg:
    bg.inputs["Color"].default_value    = (0.06, 0.05, 0.08, 1.0)
    bg.inputs["Strength"].default_value = 0.3

print("")
print("=== LevelPreview scene built ===")
print("Switch to Rendered view (Z → Rendered) to see the colours.")
print("Run 05_render_hq.py to save PNG files.")
