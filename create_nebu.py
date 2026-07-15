"""
create_nebu.py  —  Blender 4.x
Genera el personaje CHAR_Nebu: un Shabtí egipcio estilizado.
Guardar archivo .blend + exportar FBX para Unity.

Cómo usarlo en Blender:
  1. Abre Blender
  2. Ve a la pestaña "Scripting"
  3. Haz clic en "Open" y selecciona este archivo
  4. Haz clic en "Run Script"
"""

import bpy
import math

# ── Limpiar escena ────────────────────────────────────────────────────────────
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()
for m in list(bpy.data.meshes):
    bpy.data.meshes.remove(m)

parts = []   # todos los objetos del personaje

# ── Materiales ────────────────────────────────────────────────────────────────
def mat(name, color, metallic=0.0, roughness=0.75):
    m = bpy.data.materials.new(name=name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value   = (*color, 1.0)
    bsdf.inputs["Metallic"].default_value     = metallic
    bsdf.inputs["Roughness"].default_value    = roughness
    return m

M_BODY  = mat("Shabti_Body",   (0.28, 0.55, 0.52))          # turquesa (faience)
M_GOLD  = mat("Shabti_Gold",   (0.78, 0.65, 0.18), 0.8, 0.2) # oro
M_DARK  = mat("Shabti_Dark",   (0.10, 0.06, 0.02))           # marrón oscuro
M_SKIN  = mat("Shabti_Skin",   (0.72, 0.58, 0.44))           # piel
M_LAPIS = mat("Shabti_Lapis",  (0.12, 0.20, 0.55))           # lapislázuli
M_WHITE = mat("Shabti_White",  (0.92, 0.90, 0.85))           # blanco

# ── Primitivas ────────────────────────────────────────────────────────────────
def add(obj, material):
    obj.data.materials.clear()
    obj.data.materials.append(material)
    parts.append(obj)
    return obj

def cyl(name, r, h, loc, rot=(0,0,0), sx=1, sy=1, verts=16):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=h, location=loc)
    o = bpy.context.object
    o.name = name
    o.rotation_euler = rot
    o.scale = (sx, sy, 1)
    return o

def sph(name, r, loc, sx=1, sy=1, sz=1):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=loc, segments=16, ring_count=8)
    o = bpy.context.object
    o.name, o.scale = name, (sx, sy, sz)
    return o

def box(name, s, loc, sx=1, sy=1, sz=1, rot=(0,0,0)):
    bpy.ops.mesh.primitive_cube_add(size=s, location=loc)
    o = bpy.context.object
    o.name, o.scale, o.rotation_euler = name, (sx, sy, sz), rot
    return o

# ─────────────────────────────────────────────────────────────────────────────
#  CUERPO MOMIFORME  (Shabtí envuelto en vendas)
# ─────────────────────────────────────────────────────────────────────────────

# Parte baja — cilindro ligeramente cónico
add(cyl("Lower", 0.22, 1.00, (0,0,0.50), sx=1.0, sy=0.72), M_BODY)

# Pecho — ligeramente más ancho
add(cyl("Chest", 0.23, 0.42, (0,0,1.00), sx=1.0, sy=0.80), M_BODY)

# Líneas de jeroglíficos (bandas horizontales en el cuerpo)
for i, z in enumerate([0.15, 0.32, 0.49, 0.66, 0.83]):
    add(cyl(f"GlyphLine{i}", 0.226, 0.014, (0,0,z), sx=1.0, sy=0.73, verts=20), M_DARK)

# ─────────────────────────────────────────────────────────────────────────────
#  COLLAR USEKH  (collar egipcio ancho)
# ─────────────────────────────────────────────────────────────────────────────
add(cyl("CollarOuter", 0.30, 0.055, (0,0,1.19), sx=1.0, sy=0.76), M_GOLD)
add(cyl("CollarMid",   0.25, 0.050, (0,0,1.19), sx=1.0, sy=0.76), M_LAPIS)
add(cyl("CollarInner", 0.20, 0.045, (0,0,1.19), sx=1.0, sy=0.76), M_GOLD)

# ─────────────────────────────────────────────────────────────────────────────
#  BRAZOS CRUZADOS  (postura clásica del Shabtí)
# ─────────────────────────────────────────────────────────────────────────────
# Brazo izquierdo
add(cyl("ArmL", 0.057, 0.38, (-0.08, 0.17, 1.03),
        rot=(0.42, 0.0, 0.55), verts=8), M_BODY)
# Brazo derecho
add(cyl("ArmR", 0.057, 0.38, ( 0.08, 0.17, 1.03),
        rot=(0.42, 0.0,-0.55), verts=8), M_BODY)

# Cayado Heka (mano izquierda)
add(cyl("CrookV", 0.028, 0.32, (-0.16, 0.13, 0.94), rot=(0, 0,-0.18), verts=6), M_GOLD)
add(cyl("CrookH", 0.022, 0.11, (-0.15, 0.13, 1.10), rot=(1.15, 0,-0.18), verts=6), M_GOLD)

# Flagelo Nejaja (mano derecha)
add(cyl("FlailH", 0.028, 0.28, ( 0.16, 0.13, 0.94), rot=(0, 0, 0.18), verts=6), M_GOLD)
for dx, dz in [(-0.02, 0.04), (0.0, 0.0), (0.02, 0.04)]:
    add(sph("FlailBead", 0.024, (0.18+dx, 0.15, 1.07+dz)), M_GOLD)

# ─────────────────────────────────────────────────────────────────────────────
#  CUELLO + CABEZA
# ─────────────────────────────────────────────────────────────────────────────
add(cyl("Neck", 0.11, 0.13, (0,0,1.27), sx=0.90, sy=0.85), M_SKIN)
add(sph("Head", 0.205, (0,-0.012,1.52), sx=0.95, sy=0.88, sz=1.05), M_SKIN)

# ─────────────────────────────────────────────────────────────────────────────
#  CARA
# ─────────────────────────────────────────────────────────────────────────────
# Ojos almendrados
add(sph("EyeWhiteL", 0.050, (-0.076,-0.188,1.525), sx=1.5, sy=0.40, sz=0.75), M_WHITE)
add(sph("EyeWhiteR", 0.050, ( 0.076,-0.188,1.525), sx=1.5, sy=0.40, sz=0.75), M_WHITE)
add(sph("EyePupilL", 0.042, (-0.076,-0.192,1.525), sx=1.2, sy=0.35, sz=0.60), M_DARK)
add(sph("EyePupilR", 0.042, ( 0.076,-0.192,1.525), sx=1.2, sy=0.35, sz=0.60), M_DARK)
# Kohl (delineado negro egipcio)
add(box("KohlL", 0.012, (-0.076,-0.186,1.525), sx=1.9, sy=0.25, sz=0.45), M_DARK)
add(box("KohlR", 0.012, ( 0.076,-0.186,1.525), sx=1.9, sy=0.25, sz=0.45), M_DARK)

# Nariz
add(sph("Nose", 0.030, (0,-0.202,1.485), sx=0.75, sy=0.60, sz=0.80), M_SKIN)

# Labios
add(box("LipUp",  0.035, (0,-0.200,1.445), sx=2.0, sy=0.45, sz=0.55), M_DARK)
add(box("LipLow", 0.028, (0,-0.198,1.425), sx=2.2, sy=0.40, sz=0.45), M_SKIN)

# ─────────────────────────────────────────────────────────────────────────────
#  TOCADO NEMES  (tocado a rayas del faraón)
# ─────────────────────────────────────────────────────────────────────────────
# Cúpula superior (cubre la cabeza)
add(sph("NemesCrown", 0.225, (0, 0.005, 1.645), sx=1.0, sy=0.82, sz=0.78), M_GOLD)

# Solapas laterales izquierda y derecha
add(box("LappetL", 0.18, (-0.215, 0.010, 1.455), sx=0.55, sy=0.60, sz=2.25,
        rot=(0.05, 0.0, 0.08)), M_GOLD)
add(box("LappetR", 0.18, ( 0.215, 0.010, 1.455), sx=0.55, sy=0.60, sz=2.25,
        rot=(0.05, 0.0,-0.08)), M_GOLD)

# Rayas del Nemes (oscuras) — izquierda
for i in range(4):
    add(box(f"StrL{i}", 0.018, (-0.215, 0.030, 1.50 - i*0.10),
            sx=1.0, sy=0.28, sz=0.30), M_DARK)
# Rayas del Nemes (oscuras) — derecha
for i in range(4):
    add(box(f"StrR{i}", 0.018, ( 0.215, 0.030, 1.50 - i*0.10),
            sx=1.0, sy=0.28, sz=0.30), M_DARK)

# Cola trasera del Nemes
add(box("NemesBack", 0.13, (0, 0.135, 1.44), sx=0.65, sy=0.75, sz=2.55,
        rot=(-0.06, 0, 0)), M_GOLD)

# ─────────────────────────────────────────────────────────────────────────────
#  URAEUS  (cobra sagrada en la frente)
# ─────────────────────────────────────────────────────────────────────────────
add(cyl("UraeusBody", 0.022, 0.09, (0,-0.218,1.615),
        rot=(math.pi/2, 0, 0), verts=8), M_GOLD)
add(sph("UraeusHead", 0.034, (0,-0.218,1.640), sx=1.0, sy=0.80, sz=0.80), M_GOLD)

# ─────────────────────────────────────────────────────────────────────────────
#  AGRUPAR TODO BAJO UN EMPTY PADRE
# ─────────────────────────────────────────────────────────────────────────────
bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
root = bpy.context.object
root.name = "CHAR_Nebu"

bpy.ops.object.select_all(action='DESELECT')
for o in parts:
    o.select_set(True)
bpy.context.view_layer.objects.active = root
bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)

# ─────────────────────────────────────────────────────────────────────────────
#  ILUMINACIÓN Y CÁMARA  (para renders de presentación)
# ─────────────────────────────────────────────────────────────────────────────
# Luz principal (sol egipcio cálido)
bpy.ops.object.light_add(type='SUN', location=(4, -3, 8))
sun = bpy.context.object
sun.name = "Sun_Key"
sun.rotation_euler = (math.radians(40), 0, math.radians(40))
sun.data.energy = 5.0
sun.data.color = (1.0, 0.85, 0.60)

# Luz de relleno (azul suave)
bpy.ops.object.light_add(type='AREA', location=(-3, 2, 5))
fill = bpy.context.object
fill.name = "Fill_Area"
fill.data.energy = 60
fill.data.size = 4
fill.data.color = (0.55, 0.65, 0.95)

# Cámara frontal
bpy.ops.object.camera_add(location=(0, -3.8, 1.5))
cam = bpy.context.object
cam.name = "Cam_Nebu"
cam.rotation_euler = (math.radians(82), 0, 0)
bpy.context.scene.camera = cam

# Fondo (azul oscuro egipcio)
bpy.context.scene.world.use_nodes = True
bg = bpy.context.scene.world.node_tree.nodes["Background"]
bg.inputs["Color"].default_value = (0.06, 0.08, 0.16, 1.0)
bg.inputs["Strength"].default_value = 0.4

# ─────────────────────────────────────────────────────────────────────────────
#  GUARDAR .blend
# ─────────────────────────────────────────────────────────────────────────────
blend_path = r"C:\Users\geiso\Documents\TheLastShabti\CHAR_Nebu.blend"
bpy.ops.wm.save_as_mainfile(filepath=blend_path)
print(f"[Nebu] .blend guardado: {blend_path}")

# ─────────────────────────────────────────────────────────────────────────────
#  EXPORTAR FBX para Unity
# ─────────────────────────────────────────────────────────────────────────────
fbx_path = r"C:\Users\geiso\Documents\TheLastShabti\UnityProject\Assets\Art\Models\CHAR_Nebu.fbx"
bpy.ops.object.select_all(action='DESELECT')
for o in parts:
    o.select_set(True)
root.select_set(True)

bpy.ops.export_scene.fbx(
    filepath=fbx_path,
    use_selection=True,
    global_scale=1.0,
    apply_unit_scale=True,
    apply_scale_options='FBX_SCALE_NONE',
    object_types={'MESH', 'EMPTY'},
    use_mesh_modifiers=True,
    mesh_smooth_type='FACE',
    add_leaf_bones=False,
    path_mode='AUTO',
    axis_forward='-Z',
    axis_up='Y',
)
print(f"[Nebu] FBX exportado: {fbx_path}")
print("[Nebu] ✓ Personaje completo — 'El Último Shabtí' listo.")
