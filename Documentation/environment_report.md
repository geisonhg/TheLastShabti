# Environment Report — The Last Shabti

Generated: 2026-07-15

---

## 1. Blender

| Item | Result |
|------|--------|
| Version | Blender 4.5.3 LTS |
| Build date | 2025-09-09 |
| Executable | `C:\Program Files\Blender Foundation\Blender 4.5\blender.exe` |
| Called from WSL via | `/mnt/c/Program Files/Blender Foundation/Blender 4.5/blender.exe` |
| Batch mode flag | `--background --factory-startup --python <script>` |
| Blender inside Ubuntu | **Not installed** (Windows install used directly from WSL) |

---

## 2. Unity

| Item | Result |
|------|--------|
| Version installed | **6000.2.10f1 (Unity 6)** — NOT 2022.3 LTS as originally specified in README |
| Executable | `C:\Program Files\Unity\Hub\Editor\6000.2.10f1\Editor\Unity.exe` |
| Render pipeline | Universal Render Pipeline (URP) 17.2.0 |
| Batch mode | Supported — `com.unity.editor.headless` entitlement present in local licence |
| Licence type | Unity Personal (active, local XML licence file) |
| Licence file | `C:\Users\geiso\AppData\Local\Unity\licenses\` |
| Licence note | Server returns 404 on token refresh (no active internet session). Local licence is valid and batch mode runs with exit code 0. |

---

## 3. Obstacle Course Pack

| Item | Result |
|------|--------|
| Asset Store ID | 178169 |
| Found in Asset Store cache | **No** |
| Found in any Unity project | **No** |
| Found as .unitypackage | **No** |
| Search locations | AppData, Downloads, Desktop, all Unity project folders |
| Action taken | Placeholder obstacles created using Unity primitives + custom scripts |

The student's course folder contained `PlayerController_Capsule.unitypackage` with basic `MovementRB.cs` and `FollowCam.cs` scripts (no jump). These were noted but NOT used — a proper CharacterController-based controller with jumping was written instead.

---

## 4. Git

| Item | Result |
|------|--------|
| Git version | 2.43.0 |
| Configured user | Geison Herrera <geisonhg@gmail.com> |
| GitHub auth | Not verified (no remote pushed yet) |
| .gitignore | Created — excludes Library/, Build/, .blend1, etc. |

---

## 5. Windows / WSL environment

| Item | Value |
|------|-------|
| OS | Windows (WSL2 - Linux 6.6.87.2-microsoft-standard-WSL2) |
| Windows username | geiso |
| WSL working path | `/home/geisonhg/TheLastShabti/` |
| Windows working path | `C:\Users\geiso\Documents\TheLastShabti\` |
| Primary working copy | Windows path (required for Blender.exe and Unity.exe) |
| WSL copy | Kept in sync, used as Git repository |

---

## 6. Task completion by tool

| Task | Method | Result |
|------|--------|--------|
| Blender asset generation | `blender.exe --background --python 00_master_batch.py` | ✓ Complete |
| FBX export (11 files) | Blender batch script | ✓ Complete |
| Preview renders (3 images) | Blender Eevee Next, batch mode | ✓ Complete |
| .blend file saved | Blender batch script | ✓ Complete |
| Unity ProjectSettings | Copied from GameplayDemoPrototype (same Unity 6 version) | ✓ Complete |
| Unity materials (10) | LevelBuilder.cs Editor script | ✓ Complete |
| Unity scene built | LevelBuilder.cs, -executeMethod in batch mode | ✓ Complete |
| PC build produced | `-buildWindows64Player` batch mode | ✓ Complete |
| Documentation | Written programmatically | ✓ Complete |
| Git setup | Ready to commit | Pending |

---

## 7. Items requiring manual interaction

See `manual_actions_required.md` for the complete list. Summary:

1. **Obstacle Course Pack** — must be downloaded from Unity Asset Store and imported manually
2. **Input System handling** — the new Unity Input System is included; you may need to enable Legacy Input in Project Settings if WASD/Space don't work
3. **UI Font** — Legacy Runtime font used; if it shows blank text, assign Arial or another font in the Inspector
4. **Player CameraRig link** — verify the CameraRig target is correctly linked to Player in the Inspector after opening Unity
5. **GitHub push** — push prepared commit after creating a GitHub repository
6. **Cloud upload** — upload Build/ folder and .blend file to Google Drive

---

## 8. Working copy paths

| File | Windows path |
|------|-------------|
| Project root | `C:\Users\geiso\Documents\TheLastShabti\` |
| Blend file | `C:\Users\geiso\Documents\TheLastShabti\Blender\TheLastShabti.blend` |
| FBX exports | `C:\Users\geiso\Documents\TheLastShabti\Blender\Exports\*.fbx` |
| Unity project | `C:\Users\geiso\Documents\TheLastShabti\UnityProject\` |
| Unity scene | `C:\Users\geiso\Documents\TheLastShabti\UnityProject\Assets\Scenes\LVL_MainPyramid.unity` |
| PC build | `C:\Users\geiso\Documents\TheLastShabti\Build\TheLastShabti\TheLastShabti.exe` |
| WSL project | `/home/geisonhg/TheLastShabti/` |
