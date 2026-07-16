# 02_create_env_assets.py - props y assets del entorno para The Last Shabti
# Correr después de 01_create_nebu.py (reutiliza los materiales)

import bpy
import bmesh
import math


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
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
    obj.location.z += obj.dimensions.z / 2
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')


M_SAND  = make_mat("MAT_Sandstone",  (0.76, 0.62, 0.39), roughness=0.88)
M_DARK  = make_mat("MAT_DarkBrown",  (0.15, 0.08, 0.04), roughness=0.92)
M_TURQ  = make_mat("MAT_Turquoise",  (0.28, 0.55, 0.52), roughness=0.70)
M_GOLD  = make_mat("MAT_GoldAccent", (0.78, 0.65, 0.18), roughness=0.25, metallic=0.75)
M_STONE = make_mat("MAT_StoneBlue",  (0.44, 0.54, 0.62), roughness=0.90)
M_FIRE  = make_mat("MAT_TorchFire",  (0.90, 0.55, 0.08), roughness=0.20,  metallic=0.0)
M_CLAY  = make_mat("MAT_Clay",       (0.55, 0.38, 0.28), roughness=0.92)


# --- ENV_SandstonePlatform ---
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0))
plat = bpy.context.active_object
plat.name = "ENV_SandstonePlatform"
plat.scale = (2.0, 1.0, 0.4)
bpy.ops.object.transform_apply(scale=True)

# bevel para que parezca piedra gastada
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.bevel(offset=0.025, segments=1, affect='EDGES')
bpy.ops.object.mode_set(mode='OBJECT')
plat.data.materials.append(M_SAND)

edge_stripe = add_box("ENV_SandstonePlatform_Edge",
                      (0, 0.51, 0), (2.05, 0.02, 0.42), M_DARK)
edge_stripe.parent = plat

print("1. ENV_SandstonePlatform  ✓")


# --- PROP_BrokenColumn ---
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.28, depth=1.6,
                                     location=(4, 0, 0.8))
col = bpy.context.active_object
col.name = "PROP_BrokenColumn"
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
col.data.materials.append(M_STONE)

# romper el tope del cilindro para que parezca columna caída
bpy.ops.object.mode_set(mode='EDIT')
bm = bmesh.from_edit_mesh(col.data)
bm.verts.ensure_lookup_table()

top_verts = [v for v in bm.verts if v.co.z > 0.7]
for i, v in enumerate(top_verts):
    if i % 2 == 0:
        v.co.z -= 0.14
        v.co.x *= 0.78
        v.co.y *= 0.78
    else:
        v.co.z -= 0.04

bmesh.update_edit_mesh(col.data)
bpy.ops.object.mode_set(mode='OBJECT')

base_ring = add_box("PROP_BrokenColumn_Base",
                    (4, 0, -0.74), (0.70, 0.70, 0.12), M_SAND)
base_ring.parent = col

print("2. PROP_BrokenColumn  ✓")


# --- PROP_Obelisk ---
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(8, 0, 0))
ob = bpy.context.active_object
ob.name = "PROP_Obelisk"
ob.scale = (0.4, 0.4, 3.0)
bpy.ops.object.transform_apply(scale=True)

# los vértices de arriba se achican para el efecto piramidal
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

bpy.ops.object.select_all(action='DESELECT')
bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=0.19, radius2=0.0,
                                 depth=0.38, location=(8, 0, 3.19))
cap = bpy.context.active_object
cap.name = "PROP_Obelisk_Cap"
cap.rotation_euler = (0, 0, math.pi / 4)
bpy.ops.object.transform_apply(rotation=True)
cap.data.materials.append(M_GOLD)
cap.parent = ob

engrave = add_box("PROP_Obelisk_Engrave",
                  (8, 0.21, 1.0), (0.28, 0.01, 1.6), M_DARK)
engrave.parent = ob

print("3. PROP_Obelisk  ✓")


# --- PROP_BurialJar ---
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.mesh.primitive_cylinder_add(vertices=10, radius=0.22, depth=0.9,
                                     end_fill_type='NGON', location=(0, 4, 0.45))
jar = bpy.context.active_object
jar.name = "PROP_BurialJar"
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
jar.data.materials.append(M_CLAY)

# deformar el cilindro para que tenga panza y cuello
bpy.ops.object.mode_set(mode='EDIT')
bm = bmesh.from_edit_mesh(jar.data)
bm.verts.ensure_lookup_table()

for v in bm.verts:
    t = (v.co.z + 0.45) / 0.9
    if 0.2 < t < 0.72:
        belly = 1.0 + 0.65 * math.sin(math.pi * ((t - 0.2) / 0.52))
        v.co.x *= belly
        v.co.y *= belly
    elif t > 0.72:
        neck = max(0.45, 1.0 - (t - 0.72) * 1.8)
        v.co.x *= neck
        v.co.y *= neck

bmesh.update_edit_mesh(jar.data)
bpy.ops.object.mode_set(mode='OBJECT')

bpy.ops.object.select_all(action='DESELECT')
bpy.ops.mesh.primitive_cone_add(vertices=10, radius1=0.12, radius2=0.05,
                                 depth=0.13, location=(0, 4, 0.97))
lid = bpy.context.active_object
lid.name = "PROP_BurialJar_Lid"
lid.data.materials.append(M_CLAY)
lid.parent = jar

stripe = add_box("PROP_BurialJar_Stripe",
                 (0, 4, 0.50), (0.48, 0.48, 0.06), M_TURQ)
stripe.parent = jar

print("4. PROP_BurialJar  ✓")


# --- PROP_WallTorch ---
bpy.ops.object.select_all(action='DESELECT')

wall_plate = add_box("PROP_WallTorch_Plate",
                     (4, 4.04, 0), (0.20, 0.06, 0.26), M_STONE)

bracket = add_box("PROP_WallTorch_Bracket",
                  (4, 4.25, 0.07), (0.45, 0.08, 0.07), M_DARK)
bracket.parent = wall_plate

bpy.ops.object.select_all(action='DESELECT')
bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.09, depth=0.12,
                                     location=(4.22, 4.25, 0.18))
cup = bpy.context.active_object
cup.name = "PROP_WallTorch_Cup"
cup.data.materials.append(M_DARK)
cup.parent = wall_plate

bpy.ops.object.select_all(action='DESELECT')
bpy.ops.mesh.primitive_cone_add(vertices=6, radius1=0.07, radius2=0.01,
                                 depth=0.22, location=(4.22, 4.25, 0.36))
flame = bpy.context.active_object
flame.name = "PROP_WallTorch_Flame"
flame.data.materials.append(M_FIRE)
flame.parent = wall_plate

print("5. PROP_WallTorch  ✓")


# --- PROP_ScarabWall ---
bpy.ops.object.select_all(action='DESELECT')

panel = add_box("PROP_ScarabWall", (0, 8, 0), (0.72, 0.07, 0.82), M_SAND)

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

sh = add_box("PROP_ScarabWall_Head", (0, 7.93, 0.32), (0.11, 0.03, 0.11), M_DARK)
sh.parent = panel

wl = add_box("PROP_ScarabWall_WingL",
             (-0.27, 7.93, 0.08), (0.24, 0.03, 0.18), M_TURQ,
             rot=(0, 0, 0.30))
wl.parent = panel

wr = add_box("PROP_ScarabWall_WingR",
             (0.27, 7.93, 0.08), (0.24, 0.03, 0.18), M_TURQ,
             rot=(0, 0, -0.30))
wr.parent = panel

# 6 patas, 3 por lado
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


# --- PROP_SunAltar (el objetivo final del juego) ---
bpy.ops.object.select_all(action='DESELECT')

tier1 = add_box("PROP_SunAltar", (4, 8, 0.15), (2.2, 2.2, 0.30), M_SAND)
tier2 = add_box("PROP_SunAltar_Tier2", (4, 8, 0.48), (1.55, 1.55, 0.24), M_SAND)
tier2.parent = tier1
tier3 = add_box("PROP_SunAltar_Tier3", (4, 8, 0.74), (0.95, 0.95, 0.20), M_STONE)
tier3.parent = tier1

bpy.ops.object.select_all(action='DESELECT')
bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.52, depth=0.07,
                                     location=(4, 8, 0.89))
disc = bpy.context.active_object
disc.name = "PROP_SunAltar_Disc"
disc.data.materials.append(M_GOLD)
disc.parent = tier1

for i in range(8):
    angle = (i / 8) * 2 * math.pi
    rx = 4 + 0.72 * math.cos(angle)
    ry = 8 + 0.72 * math.sin(angle)
    ray = add_box(f"PROP_SunAltar_Ray{i}",
                  (rx, ry, 0.89),
                  (0.08, 0.22, 0.04), M_GOLD,
                  rot=(0, 0, angle + math.pi / 2))
    ray.parent = tier1

for dx, dy in [(-0.90, -0.90), (0.90, -0.90), (-0.90, 0.90), (0.90, 0.90)]:
    post = add_box("PROP_SunAltar_Post",
                   (4 + dx, 8 + dy, 0.55), (0.12, 0.12, 0.60), M_SAND)
    post.parent = tier1

print("7. PROP_SunAltar  ✓")


# --- ENV_Stair (un escalón modular, duplicar para hacer una escalera) ---
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 12, 0))
step = bpy.context.active_object
step.name = "ENV_Stair"
step.scale = (1.5, 0.50, 0.22)
bpy.ops.object.transform_apply(scale=True)
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.bevel(offset=0.02, segments=1, affect='EDGES')
bpy.ops.object.mode_set(mode='OBJECT')
step.data.materials.append(M_SAND)

print("8. ENV_Stair  ✓")


# --- ENV_Ramp ---
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(4, 12, 0))
ramp = bpy.context.active_object
ramp.name = "ENV_Ramp"
ramp.scale = (2.0, 1.8, 0.55)
bpy.ops.object.transform_apply(scale=True)

# bajar los vértices del frente-arriba para crear la pendiente
bpy.ops.object.mode_set(mode='EDIT')
bm = bmesh.from_edit_mesh(ramp.data)
bm.verts.ensure_lookup_table()
for v in bm.verts:
    if v.co.y < -0.60 and v.co.z > 0.20:
        v.co.z = -0.275
bmesh.update_edit_mesh(ramp.data)
bpy.ops.object.mode_set(mode='OBJECT')
ramp.data.materials.append(M_SAND)

print("9. ENV_Ramp  ✓")


# --- ENV_Archway ---
bpy.ops.object.select_all(action='DESELECT')

AX, AY = 0, 16

p_l = add_box("ENV_Archway", (AX - 0.58, AY, 1.1), (0.36, 0.36, 2.4), M_STONE)

p_r = add_box("ENV_Archway_PillarR", (AX + 0.58, AY, 1.1), (0.36, 0.36, 2.4), M_STONE)
p_r.parent = p_l

lintel = add_box("ENV_Archway_Lintel", (AX, AY, 2.45), (1.56, 0.42, 0.30), M_SAND)
lintel.parent = p_l

groove = add_box("ENV_Archway_Groove", (AX, AY - 0.17, 2.45), (1.12, 0.02, 0.12), M_DARK)
groove.parent = p_l

for side, name in [(-1, "ENV_Archway_CapL"), (1, "ENV_Archway_CapR")]:
    cap = add_box(name, (AX + side * 0.58, AY, 0.07), (0.46, 0.46, 0.14), M_SAND)
    cap.parent = p_l

for side, name in [(-1, "ENV_Archway_TopL"), (1, "ENV_Archway_TopR")]:
    top = add_box(name, (AX + side * 0.58, AY, 2.33), (0.46, 0.46, 0.10), M_SAND)
    top.parent = p_l

print("10. ENV_Archway  ✓")

print("\nTodos los assets creados. Revisar en viewport antes de exportar.")
