"""
03_export_fbx.py
Exports all named assets to individual FBX files for Unity import.

HOW TO USE:
  1. Run scripts 01 and 02 first and review the results
  2. Edit EXPORT_PATH below to match your project's Blender/Exports folder
  3. Click Run Script — FBX files will be saved to that folder
  4. Drag the FBX files into Unity: Assets/Art/Models/

IMPORTANT:
  - If you are using Blender on Windows (not WSL), use a Windows path:
    EXPORT_PATH = r"C:\\Users\\YourName\\TheLastShabti\\Blender\\Exports"
  - If Blender is running on Linux/WSL:
    EXPORT_PATH = "/home/geisonhg/TheLastShabti/Blender/Exports"
"""

import bpy
import os


# -----------------------------------------------------------------------
# EDIT THIS PATH to match your machine
# -----------------------------------------------------------------------
EXPORT_PATH = r"C:\Users\YourName\TheLastShabti\Blender\Exports"
# EXPORT_PATH = "/home/geisonhg/TheLastShabti/Blender/Exports"
# -----------------------------------------------------------------------


# Shared FBX export settings for Unity
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
    # Unity expects Y-up, forward on -Z
    axis_forward='-Z',
    axis_up='Y',
)


def select_object_and_children(obj_name):
    """Deselect everything then select the named object and all its children."""
    bpy.ops.object.select_all(action='DESELECT')
    if obj_name not in bpy.data.objects:
        return False
    obj = bpy.data.objects[obj_name]
    obj.select_set(True)
    for child in obj.children_recursive:
        child.select_set(True)
    bpy.context.view_layer.objects.active = obj
    return True


def export_single(obj_name, filename=None):
    """Export one object (and its children) as a single FBX file."""
    if not select_object_and_children(obj_name):
        print(f"  SKIP — '{obj_name}' not found in scene")
        return
    fname = filename or obj_name
    filepath = os.path.join(EXPORT_PATH, f"{fname}.fbx")
    bpy.ops.export_scene.fbx(filepath=filepath, **FBX_SETTINGS)
    print(f"  Exported: {fname}.fbx")


def export_group(filename, obj_names):
    """Export a list of objects as a single FBX file."""
    bpy.ops.object.select_all(action='DESELECT')
    found = False
    for name in obj_names:
        if name in bpy.data.objects:
            bpy.data.objects[name].select_set(True)
            if not found:
                bpy.context.view_layer.objects.active = bpy.data.objects[name]
                found = True
    if not found:
        print(f"  SKIP — no objects found for group '{filename}'")
        return
    filepath = os.path.join(EXPORT_PATH, f"{filename}.fbx")
    bpy.ops.export_scene.fbx(filepath=filepath, **FBX_SETTINGS)
    print(f"  Exported: {filename}.fbx")


# -----------------------------------------------------------------------
# Create output folder if it does not exist
# -----------------------------------------------------------------------
os.makedirs(EXPORT_PATH, exist_ok=True)
print(f"Output folder: {EXPORT_PATH}")
print("")

# -----------------------------------------------------------------------
# Character (CH_Nebu has all parts as children of the root empty)
# -----------------------------------------------------------------------
print("--- Character ---")
export_single("CH_Nebu")

# -----------------------------------------------------------------------
# Environment pieces (each exported as a self-contained FBX)
# -----------------------------------------------------------------------
print("\n--- Environment ---")
export_single("ENV_SandstonePlatform")
export_single("ENV_Stair")
export_single("ENV_Ramp")

# Archway: root is ENV_Archway; children are parented to it
export_single("ENV_Archway", filename="ENV_Archway")

# -----------------------------------------------------------------------
# Props
# -----------------------------------------------------------------------
print("\n--- Props ---")
export_single("PROP_BrokenColumn")
export_single("PROP_Obelisk")
export_single("PROP_BurialJar")
export_single("PROP_WallTorch_Plate", filename="PROP_WallTorch")
export_single("PROP_ScarabWall")
export_single("PROP_SunAltar")

# -----------------------------------------------------------------------
# Done
# -----------------------------------------------------------------------
print("\n=== Export complete ===")
print(f"Check: {EXPORT_PATH}")
print("")
print("NEXT STEPS IN UNITY:")
print("  1. Open your Unity project")
print("  2. Drag all FBX files into Assets/Art/Models/")
print("  3. For each imported model:")
print("     - Set Scale Factor to 1 in the Import Settings")
print("     - Enable 'Generate Colliders' only for simple meshes")
print("     - Check that materials appear correctly")
print("  4. Create prefabs for each asset in Assets/Prefabs/")
