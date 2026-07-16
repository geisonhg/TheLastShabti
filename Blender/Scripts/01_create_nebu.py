# 01_create_nebu.py - crea el personaje Nebu en Blender
# Abrir en la pestaña Scripting y darle Run Script

import bpy
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


def add_box(name, loc, scale, mat, rot=(0, 0, 0)):
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


# colores de la paleta del juego
M_STONE  = make_mat("MAT_StoneBlue",  (0.44, 0.54, 0.62), roughness=0.90)
M_SAND   = make_mat("MAT_Sandstone",  (0.76, 0.62, 0.39), roughness=0.85)
M_GOLD   = make_mat("MAT_GoldAccent", (0.78, 0.65, 0.18), roughness=0.25, metallic=0.75)
M_TURQ   = make_mat("MAT_Turquoise",  (0.28, 0.55, 0.52), roughness=0.70)
M_DARK   = make_mat("MAT_DarkBrown",  (0.15, 0.08, 0.04), roughness=0.92)
M_EYE    = make_mat("MAT_EyeBlack",   (0.05, 0.05, 0.06), roughness=0.95)

body   = add_box("CH_Nebu_Body",   (0, 0, 0.38), (0.46, 0.36, 0.50), M_STONE)
belt   = add_box("CH_Nebu_Belt",   (0, 0, 0.34), (0.49, 0.39, 0.07), M_TURQ)
collar = add_box("CH_Nebu_Collar", (0, 0, 0.72), (0.50, 0.40, 0.07), M_TURQ)

# cabeza un poco grande a propósito, estilo low-poly
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 1.02))
head = bpy.context.active_object
head.name = "CH_Nebu_Head"
head.scale = (0.56, 0.50, 0.54)
bpy.ops.object.transform_apply(scale=True)
# bevel suave para que no quede tan cubo
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.bevel(offset=0.04, segments=1, affect='EDGES')
bpy.ops.object.mode_set(mode='OBJECT')
head.data.materials.append(M_STONE)

# tocado Nemes: panel trasero + dos lappets laterales
nemes_back = add_box("CH_Nebu_NemesBack",
                     (0, -0.09, 1.18), (0.60, 0.08, 0.66), M_SAND)
nemes_l = add_box("CH_Nebu_NemesLapL",
                  (-0.36, 0.06, 0.84), (0.10, 0.10, 0.30), M_SAND,
                  rot=(0, 0.12, 0))
nemes_r = add_box("CH_Nebu_NemesLapR",
                  ( 0.36, 0.06, 0.84), (0.10, 0.10, 0.30), M_SAND,
                  rot=(0, -0.12, 0))

crown_band = add_box("CH_Nebu_CrownBand",
                     (0, 0.26, 1.24), (0.58, 0.04, 0.07), M_DARK)
# uraeus = la cobra del frente (simplificada)
uraeus = add_box("CH_Nebu_Uraeus",
                 (0, 0.28, 1.35), (0.04, 0.04, 0.10), M_GOLD)

# ojos con líneas de kohl egipcias
eye_l  = add_box("CH_Nebu_EyeL",  (-0.15, 0.27, 1.02), (0.10, 0.03, 0.055), M_EYE)
eye_r  = add_box("CH_Nebu_EyeR",  ( 0.15, 0.27, 1.02), (0.10, 0.03, 0.055), M_EYE)
kohl_l = add_box("CH_Nebu_KohlL", (-0.24, 0.27, 1.02), (0.07, 0.025, 0.025), M_EYE)
kohl_r = add_box("CH_Nebu_KohlR", ( 0.24, 0.27, 1.02), (0.07, 0.025, 0.025), M_EYE)

# escarabajo en el pecho con alas
scarab = add_box("CH_Nebu_Scarab", (0, 0.37, 0.56), (0.10, 0.03, 0.10), M_GOLD)

bpy.ops.object.select_all(action='DESELECT')
scarab.select_set(True)
bpy.context.view_layer.objects.active = scarab
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.bevel(offset=0.025, segments=2, affect='EDGES')
bpy.ops.object.mode_set(mode='OBJECT')

wing_l = add_box("CH_Nebu_WingL",
                 (-0.17, 0.37, 0.55), (0.09, 0.025, 0.055), M_GOLD,
                 rot=(0, 0, 0.25))
wing_r = add_box("CH_Nebu_WingR",
                 ( 0.17, 0.37, 0.55), (0.09, 0.025, 0.055), M_GOLD,
                 rot=(0, 0, -0.25))

arm_l = add_box("CH_Nebu_ArmL",
                (-0.52, 0, 0.50), (0.13, 0.14, 0.34), M_STONE,
                rot=(0, 0.18, 0))
arm_r = add_box("CH_Nebu_ArmR",
                ( 0.52, 0, 0.50), (0.13, 0.14, 0.34), M_STONE,
                rot=(0, -0.18, 0))

leg_l = add_box("CH_Nebu_LegL", (-0.16, 0.01, 0.11), (0.15, 0.18, 0.26), M_STONE)
leg_r = add_box("CH_Nebu_LegR", ( 0.16, 0.01, 0.11), (0.15, 0.18, 0.26), M_STONE)

# empty raíz para exportar todo junto como CH_Nebu.fbx
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
root = bpy.context.active_object
root.name = "CH_Nebu"

all_parts = [
    body, belt, collar,
    head, nemes_back, nemes_l, nemes_r, crown_band, uraeus,
    eye_l, eye_r, kohl_l, kohl_r,
    scarab, wing_l, wing_r,
    arm_l, arm_r, leg_l, leg_r,
]

for part in all_parts:
    part.parent = root

print("CH_Nebu listo —", len(all_parts), "partes")
