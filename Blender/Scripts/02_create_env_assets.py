"""
02_create_env_assets.py
Creates all environment and prop assets for The Last Shabti.

HOW TO USE:
  1. Run 01_create_nebu.py first (this script reuses its materials)
  2. Open this file in Blender Scripting tab and click Run Script
  3. All assets will appear in the scene, spread across the X/Y axes
  4. Review each one in the viewport and adjust as needed
  5. Run 03_export_fbx.py when you are satisfied

ASSETS CREATED:
  ENV_SandstonePlatform   - modular platform block (main building piece)
  PROP_BrokenColumn       - fallen/broken Egyptian column with base ring
  PROP_Obelisk            - tapered obelisk with gold pyramidion cap
  PROP_BurialJar          - ceramic jar with lid and stripe decoration
  PROP_WallTorch          - wall bracket, cup and stylised flame
  PROP_ScarabWall         - wall panel with raised scarab geometry
  PROP_SunAltar           - three-tier altar with sun disc and rays
  ENV_Stair               - one modular stair step (duplicate to build flights)
  ENV_Ramp                - wedge ramp for sloped sections
  ENV_Archway             - doorway with two pillars and lintel
"""

import bpy
import bmesh
import math


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def make_mat(name, rgb, roughness=0.85, metallic=0.0):
    if name in bpy.data.materials:
        return bpy.data.materials[name]
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (*rgb, 1.0)
        bsdf.inputs["Roughness"].default_value = roughness
        bsdf.inputs["Metallic"].default_value = metallic
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
    return obj


def set_origin_bottom(obj):
    """Move origin to the bottom centre of the object's bounding box."""
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    # Set origin to geometry centre first
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
    # Then push the object up so its bottom is at the cursor
    obj.location.z += obj.dimensions.z / 2
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')


# ---------------------------------------------------------------------------
# Materials  (all shared across the project)
# ---------------------------------------------------------------------------
M_SAND  = make_mat("MAT_Sandstone",  (0.76, 0.62, 0.39), roughness=0.88)
M_DARK  = make_mat("MAT_DarkBrown",  (0.15, 0.08, 0.04), roughness=0.92)
M_TURQ  = make_mat("MAT_Turquoise",  (0.28, 0.55, 0.52), roughness=0.70)
M_GOLD  = make_mat("MAT_GoldAccent", (0.78, 0.65, 0.18), roughness=0.25, metallic=0.75)
M_STONE = make_mat("MAT_StoneBlue",  (0.44, 0.54, 0.62), roughness=0.90)
M_FIRE  = make_mat("MAT_TorchFire",  (0.90, 0.55, 0.08), roughness=0.20,  metallic=0.0)
M_CLAY  = make_mat("MAT_Clay",       (0.55, 0.38, 0.28), roughness=0.92)


# ===========================================================================
# 1. ENV_SandstonePlatform
#    The main building block of the level. Used for most floor platforms.
#    Scale and rotate copies to vary the environment.
# ===========================================================================
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0))
plat = bpy.context.active_object
plat.name = "ENV_SandstonePlatform"
plat.scale = (2.0, 1.0, 0.4)
bpy.ops.object.transform_apply(scale=True)

# Slight bevel on all edges — gives the block a worn stone look
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.bevel(offset=0.025, segments=1, affect='EDGES')
bpy.ops.object.mode_set(mode='OBJECT')
plat.data.materials.append(M_SAND)

# Add a subtle darker edge strip to suggest block separation
edge_stripe = add_box("ENV_SandstonePlatform_Edge",
                      (0, 0.51, 0), (2.05, 0.02, 0.42), M_DARK)
edge_stripe.parent = plat

print("1. ENV_SandstonePlatform  ✓")


# ===========================================================================
# 2. PROP_BrokenColumn
#    An 8-sided low-poly column with a rough broken top.
#    Used as a visual landmark in the Collapsed Gallery and elsewhere.
# ===========================================================================
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.28, depth=1.6,
                                     location=(4, 0, 0.8))
col = bpy.context.active_object
col.name = "PROP_BrokenColumn"
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
col.data.materials.append(M_STONE)

# Make the top irregular — push some top vertices down and inward
bpy.ops.object.mode_set(mode='EDIT')
bm = bmesh.from_edit_mesh(col.data)
bm.verts.ensure_lookup_table()

top_verts = [v for v in bm.verts if v.co.z > 0.7]
for i, v in enumerate(top_verts):
    # Alternate pattern: every other vertex drops and pulls inward
    if i % 2 == 0:
        v.co.z -= 0.14
        v.co.x *= 0.78
        v.co.y *= 0.78
    else:
        v.co.z -= 0.04

bmesh.update_edit_mesh(col.data)
bpy.ops.object.mode_set(mode='OBJECT')

# Base ring decoration
base_ring = add_box("PROP_BrokenColumn_Base",
                    (4, 0, -0.74), (0.70, 0.70, 0.12), M_SAND)
base_ring.parent = col

print("2. PROP_BrokenColumn  ✓")


# ===========================================================================
# 3. PROP_Obelisk
#    Tapered rectangular pillar with a small gold pyramidion cap.
#    Used in pairs to frame the rooftop and as level landmarks.
# ===========================================================================
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(8, 0, 0))
ob = bpy.context.active_object
ob.name = "PROP_Obelisk"
ob.scale = (0.4, 0.4, 3.0)
bpy.ops.object.transform_apply(scale=True)

# Taper: pull the top vertices inward to create the narrowing profile
bpy.ops.object.mode_set(mode='EDIT')
bm = bmesh.from_edit_mesh(ob.data)
bm.verts.ensure_lookup_table()
for v in bm.verts:
    if v.co.z > 1.5:
        factor = 0.45
        v.co.x *= factor
        v.co.y *= factor
bmesh.update_edit_mesh(ob.data)
bpy.ops.object.mode_set(mode='OBJECT')
ob.data.materials.append(M_SAND)

# Gold pyramidion cap (4-sided cone)
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=0.19, radius2=0.0,
                                 depth=0.38, location=(8, 0, 3.19))
cap = bpy.context.active_object
cap.name = "PROP_Obelisk_Cap"
cap.rotation_euler = (0, 0, math.pi / 4)
bpy.ops.object.transform_apply(rotation=True)
cap.data.materials.append(M_GOLD)
cap.parent = ob

# Carved engraving area on one face (dark inset)
engrave = add_box("PROP_Obelisk_Engrave",
                  (8, 0.21, 1.0), (0.28, 0.01, 1.6), M_DARK)
engrave.parent = ob

print("3. PROP_Obelisk  ✓")


# ===========================================================================
# 4. PROP_BurialJar
#    A ceramic jar with a rounded belly and narrow neck.
#    Place in groups of 2-3 near walls in the Burial Chamber.
# ===========================================================================
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.mesh.primitive_cylinder_add(vertices=10, radius=0.22, depth=0.9,
                                     end_fill_type='NGON', location=(0, 4, 0.45))
jar = bpy.context.active_object
jar.name = "PROP_BurialJar"
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
jar.data.materials.append(M_CLAY)

# Shape the jar belly and neck by scaling vertex rings
bpy.ops.object.mode_set(mode='EDIT')
bm = bmesh.from_edit_mesh(jar.data)
bm.verts.ensure_lookup_table()

for v in bm.verts:
    # normalised height 0=bottom, 1=top
    t = (v.co.z + 0.45) / 0.9
    if 0.2 < t < 0.72:
        # Belly — scale outward using a smooth sine curve
        belly = 1.0 + 0.65 * math.sin(math.pi * ((t - 0.2) / 0.52))
        v.co.x *= belly
        v.co.y *= belly
    elif t > 0.72:
        # Neck — narrow inward
        neck = max(0.45, 1.0 - (t - 0.72) * 1.8)
        v.co.x *= neck
        v.co.y *= neck

bmesh.update_edit_mesh(jar.data)
bpy.ops.object.mode_set(mode='OBJECT')

# Lid
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.mesh.primitive_cone_add(vertices=10, radius1=0.12, radius2=0.05,
                                 depth=0.13, location=(0, 4, 0.97))
lid = bpy.context.active_object
lid.name = "PROP_BurialJar_Lid"
lid.data.materials.append(M_CLAY)
lid.parent = jar

# Turquoise stripe around belly
stripe = add_box("PROP_BurialJar_Stripe",
                 (0, 4, 0.50), (0.48, 0.48, 0.06), M_TURQ)
stripe.parent = jar

print("4. PROP_BurialJar  ✓")


# ===========================================================================
# 5. PROP_WallTorch
#    A small wall bracket with a cup and stylised flame.
#    Origin is at the wall attachment point.
#    Rotate 90 degrees to mount on a wall in Unity.
# ===========================================================================
bpy.ops.object.select_all(action='DESELECT')

# Wall plate (the piece that attaches to the stone)
wall_plate = add_box("PROP_WallTorch_Plate",
                     (4, 4.04, 0), (0.20, 0.06, 0.26), M_STONE)

# Bracket arm extending from wall
bracket = add_box("PROP_WallTorch_Bracket",
                  (4, 4.25, 0.07), (0.45, 0.08, 0.07), M_DARK)
bracket.parent = wall_plate

# Cup that holds the fire
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.09, depth=0.12,
                                     location=(4.22, 4.25, 0.18))
cup = bpy.context.active_object
cup.name = "PROP_WallTorch_Cup"
cup.data.materials.append(M_DARK)
cup.parent = wall_plate

# Stylised flame (a cone)
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.mesh.primitive_cone_add(vertices=6, radius1=0.07, radius2=0.01,
                                 depth=0.22, location=(4.22, 4.25, 0.36))
flame = bpy.context.active_object
flame.name = "PROP_WallTorch_Flame"
flame.data.materials.append(M_FIRE)
flame.parent = wall_plate

print("5. PROP_WallTorch  ✓")


# ===========================================================================
# 6. PROP_ScarabWall
#    A flat wall panel with a raised scarab symbol made from geometry.
#    Mount flush against a wall surface.
# ===========================================================================
bpy.ops.object.select_all(action='DESELECT')

# Panel base
panel = add_box("PROP_ScarabWall", (0, 8, 0), (0.72, 0.07, 0.82), M_SAND)

# Scarab body (bevelled cube)
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 7.93, 0.08))
sb = bpy.context.active_object
sb.name = "PROP_ScarabWall_Body"
sb.scale = (0.18, 0.03, 0.24)
bpy.ops.object.transform_apply(scale=True)
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.bevel(offset=0.03, segments=2, affect='EDGES')
bpy.ops.object.mode_set(mode='OBJECT')
sb.data.materials.append(M_DARK)
sb.parent = panel

# Head (small cube on top of body)
sh = add_box("PROP_ScarabWall_Head", (0, 7.93, 0.32), (0.11, 0.03, 0.11), M_DARK)
sh.parent = panel

# Left wing
wl = add_box("PROP_ScarabWall_WingL",
             (-0.27, 7.93, 0.08), (0.24, 0.03, 0.18), M_TURQ,
             rot=(0, 0, 0.30))
wl.parent = panel

# Right wing
wr = add_box("PROP_ScarabWall_WingR",
             (0.27, 7.93, 0.08), (0.24, 0.03, 0.18), M_TURQ,
             rot=(0, 0, -0.30))
wr.parent = panel

# Six legs (three per side)
leg_positions = [
    (-1, -0.10), (-1, 0.0), (-1, 0.10),
    ( 1, -0.10), ( 1, 0.0), ( 1, 0.10),
]
for i, (side, offset_z) in enumerate(leg_positions):
    leg = add_box(f"PROP_ScarabWall_Leg{i}",
                  (side * 0.21, 7.93, offset_z),
                  (0.14, 0.025, 0.025), M_DARK,
                  rot=(0, 0, math.pi / 2 + side * 0.3))
    leg.parent = panel

print("6. PROP_ScarabWall  ✓")


# ===========================================================================
# 7. PROP_SunAltar
#    The final goal object. Three-tiered platform with a gold sun disc.
#    Place in the centre of the Rooftop section.
# ===========================================================================
bpy.ops.object.select_all(action='DESELECT')

# Base tier (largest)
tier1 = add_box("PROP_SunAltar", (4, 8, 0.15), (2.2, 2.2, 0.30), M_SAND)

tier2 = add_box("PROP_SunAltar_Tier2", (4, 8, 0.48), (1.55, 1.55, 0.24), M_SAND)
tier2.parent = tier1

tier3 = add_box("PROP_SunAltar_Tier3", (4, 8, 0.74), (0.95, 0.95, 0.20), M_STONE)
tier3.parent = tier1

# Gold sun disc
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.52, depth=0.07,
                                     location=(4, 8, 0.89))
disc = bpy.context.active_object
disc.name = "PROP_SunAltar_Disc"
disc.data.materials.append(M_GOLD)
disc.parent = tier1

# Sun rays (8 small flat spikes around the disc)
for i in range(8):
    angle = (i / 8) * 2 * math.pi
    rx = 4 + 0.72 * math.cos(angle)
    ry = 8 + 0.72 * math.sin(angle)
    ray = add_box(f"PROP_SunAltar_Ray{i}",
                  (rx, ry, 0.89),
                  (0.08, 0.22, 0.04), M_GOLD,
                  rot=(0, 0, angle + math.pi / 2))
    ray.parent = tier1

# Small corner posts
for dx, dy in [(-0.90, -0.90), (0.90, -0.90), (-0.90, 0.90), (0.90, 0.90)]:
    post = add_box("PROP_SunAltar_Post",
                   (4 + dx, 8 + dy, 0.55), (0.12, 0.12, 0.60), M_SAND)
    post.parent = tier1

print("7. PROP_SunAltar  ✓")


# ===========================================================================
# 8. ENV_Stair
#    One modular stair step. In Unity, duplicate and offset to build flights.
#    For a 5-step staircase: each step offset +0.5 in X, +0.22 in Z.
# ===========================================================================
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 12, 0))
step = bpy.context.active_object
step.name = "ENV_Stair"
step.scale = (1.5, 0.50, 0.22)
bpy.ops.object.transform_apply(scale=True)
# Front edge bevel for a stepped look
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.bevel(offset=0.02, segments=1, affect='EDGES')
bpy.ops.object.mode_set(mode='OBJECT')
step.data.materials.append(M_SAND)

print("8. ENV_Stair  ✓")


# ===========================================================================
# 9. ENV_Ramp
#    A wedge-shaped ramp for the Collapsed Gallery section.
#    The front face slopes from ground level up to full height at the back.
# ===========================================================================
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(4, 12, 0))
ramp = bpy.context.active_object
ramp.name = "ENV_Ramp"
ramp.scale = (2.0, 1.8, 0.55)
bpy.ops.object.transform_apply(scale=True)

# Make wedge: pull the front-top vertices down to create the sloped face
bpy.ops.object.mode_set(mode='EDIT')
bm = bmesh.from_edit_mesh(ramp.data)
bm.verts.ensure_lookup_table()
for v in bm.verts:
    # Front = negative Y, top = positive Z
    if v.co.y < -0.60 and v.co.z > 0.20:
        v.co.z = -0.275   # Pull down to base level
bmesh.update_edit_mesh(ramp.data)
bpy.ops.object.mode_set(mode='OBJECT')
ramp.data.materials.append(M_SAND)

print("9. ENV_Ramp  ✓")


# ===========================================================================
# 10. ENV_Archway
#     A doorway with two stone pillars and a sandstone lintel.
#     Used at section transitions to signal a new area.
# ===========================================================================
bpy.ops.object.select_all(action='DESELECT')

AX, AY = 0, 16   # archway centre position

# Left pillar
p_l = add_box("ENV_Archway", (AX - 0.58, AY, 1.1), (0.36, 0.36, 2.4), M_STONE)

p_r = add_box("ENV_Archway_PillarR", (AX + 0.58, AY, 1.1), (0.36, 0.36, 2.4), M_STONE)
p_r.parent = p_l

# Lintel (horizontal slab above)
lintel = add_box("ENV_Archway_Lintel", (AX, AY, 2.45), (1.56, 0.42, 0.30), M_SAND)
lintel.parent = p_l

# Dark carved groove on the lintel
groove = add_box("ENV_Archway_Groove", (AX, AY - 0.17, 2.45), (1.12, 0.02, 0.12), M_DARK)
groove.parent = p_l

# Base caps
for side, name in [(-1, "ENV_Archway_CapL"), (1, "ENV_Archway_CapR")]:
    cap = add_box(name, (AX + side * 0.58, AY, 0.07), (0.46, 0.46, 0.14), M_SAND)
    cap.parent = p_l

# Top caps
for side, name in [(-1, "ENV_Archway_TopL"), (1, "ENV_Archway_TopR")]:
    top = add_box(name, (AX + side * 0.58, AY, 2.33), (0.46, 0.46, 0.10), M_SAND)
    top.parent = p_l

print("10. ENV_Archway  ✓")


print("")
print("=== All 10 environment assets created ===")
print("")
print("BEFORE EXPORTING:")
print("  - Review each asset in the viewport")
print("  - Apply All Transforms (Ctrl+A > All Transforms) to each object")
print("  - Set origin to bottom-centre for floor objects (right-click > Set Origin)")
print("  - Save the .blend file")
print("  - Then run 03_export_fbx.py")
