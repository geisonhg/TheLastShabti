# Test Report — The Last Shabti

Date: 2026-07-15

---

## Testing method

Interactive play-testing is not possible from a command-line / WSL environment. All tests below are structural — they inspect the project files, Unity logs and scene data directly. Each test states clearly whether it was automated or requires manual verification.

---

## 1. C# Compilation

| Test | Result | Evidence |
|------|--------|---------|
| All scripts compile without errors | ✓ PASS | Unity batch log: no `CS` error codes; exit code 0 |
| Editor script (LevelBuilder.cs) compiles | ✓ PASS | LevelBuilder.BuildAll executed successfully |
| GoalTrigger.cs compiles | ✓ PASS | Included in build |
| CheckpointManager.cs compiles | ✓ PASS | Included in build |
| CheckpointZone.cs compiles | ✓ PASS | Included in build |
| PlayerRespawn.cs compiles | ✓ PASS | Included in build |
| PlayerController.cs compiles | ✓ PASS | Included in build |
| CameraRig.cs compiles | ✓ PASS | Included in build |
| MovingPlatform.cs compiles | ✓ PASS | Included in build |
| RotatingHazard.cs compiles | ✓ PASS | Included in build |

---

## 2. Scene structure

| Test | Result | Evidence |
|------|--------|---------|
| Scene file exists | ✓ PASS | `Assets/Scenes/LVL_MainPyramid.unity` (310KB) |
| Total GameObjects in scene | 87 | Parsed from .unity YAML |
| Environment hierarchy exists | ✓ PASS | `Environment` found in scene |
| Section 1 (Burial Chamber) exists | ✓ PASS | `S1_BurialChamber` found |
| Section 2 (Collapsed Gallery) exists | ✓ PASS | `S2_CollapsedGallery` found |
| Section 3 (Hall of Weights) exists | ✓ PASS | `S3_HallOfWeights` found |
| Section 4 (Shaft of Ra) exists | ✓ PASS | `S4_ShaftOfRa` found |
| Section 5 (Rooftop Sun Altar) exists | ✓ PASS | `S5_RooftopAltarSection` found |
| Player object exists | ✓ PASS | `Player` found (tag: Player) |
| Camera rig exists | ✓ PASS | `CameraRig` + `Main Camera` found |
| Kill plane exists | ✓ PASS | `KillPlane` at Y = -8 |
| Goal trigger exists | ✓ PASS | `Goal_SunAltarTrigger` found |
| Checkpoint exists | ✓ PASS | `CP_ShaftEntry` + `CP_Marker` found |
| CheckpointManager singleton | ✓ PASS | `CheckpointManager` found in scene |
| UI Canvas found | ✓ PASS | `UI_Canvas` found |
| Title panel found | ✓ PASS | `TitlePanel` found |
| Win panel found | ✓ PASS | `WinPanel` found (set inactive by default) |
| Lighting objects found | ✓ PASS | 6 light objects found |
| Moving platforms (2) | ✓ PASS | `S3_MovingPlatform` + `S4_MovingPlatform` found |
| Rotating hazard | ✓ PASS | `OBS_RotatingHazard` found |
| Falling block | ✓ PASS | `OBS_FallingBlock` found |
| Props placed in sections | ✓ PASS | PROP_BurialJar, PROP_WallTorch, PROP_ScarabWall, PROP_Obelisk, PROP_BrokenColumn, PROP_SunAltar all found |

---

## 3. Assets

| Test | Result | Evidence |
|------|--------|---------|
| Blend file exists and saved | ✓ PASS | `Blender/TheLastShabti.blend` |
| CH_Nebu.fbx | ✓ PASS | 79,036 bytes |
| ENV_SandstonePlatform.fbx | ✓ PASS | 20,204 bytes |
| ENV_Stair.fbx | ✓ PASS | 16,236 bytes |
| ENV_Ramp.fbx | ✓ PASS | 15,596 bytes |
| ENV_Archway.fbx | ✓ PASS | 37,852 bytes |
| PROP_BrokenColumn.fbx | ✓ PASS | 19,852 bytes |
| PROP_Obelisk.fbx | ✓ PASS | 23,388 bytes |
| PROP_BurialJar.fbx | ✓ PASS | 23,468 bytes |
| PROP_WallTorch.fbx | ✓ PASS | 26,748 bytes |
| PROP_ScarabWall.fbx | ✓ PASS | 48,812 bytes |
| PROP_SunAltar.fbx | ✓ PASS | 61,836 bytes |
| All FBX files non-empty | ✓ PASS | 11/11 confirmed |
| Unity materials (10) | ✓ PASS | All .mat files present |
| Preview renders (3) | ✓ PASS | PNG files in Documentation/Screenshots/ |

---

## 4. Build

| Test | Result | Evidence |
|------|--------|---------|
| Build Settings configured | ✓ PASS | `EditorBuildSettings.asset` updated; scene listed |
| Windows x86_64 build produced | ✓ PASS | Exit code 0 |
| TheLastShabti.exe exists | ✓ PASS | 667,648 bytes |
| UnityPlayer.dll exists | ✓ PASS | 34,049,960 bytes |
| TheLastShabti_Data folder exists | ✓ PASS | Present |
| Build log errors | 0 C# errors | Only licensing token refresh warnings (cosmetic) |

---

## 5. Jump and platform distance analysis (numerical, not play-tested)

Platform gaps were designed for a CharacterController with `moveSpeed = 5`, `jumpForce = 7`, `gravity = -18`.

Approximate jump parabola: max height ≈ 1.36 units, total airtime ≈ 0.78 seconds, horizontal distance at flat jump ≈ 3.9 units.

| Platform gap | Target difficulty | Horizontal distance | Elevation change | Assessment |
|---|---|---|---|---|
| S1_Start → S1_Jump1 | Easy | ~3.5 units | +0.45 | Should be reachable — no timing needed |
| S1_Jump1 → S1_Jump2 | Easy | ~3.5 units | +0.6 | Should be reachable |
| S2_Plat1 → S2_Plat2 | Medium | ~3.5 units | +0.6 | Should be reachable |
| S2_Plat2 → S2_Plat3 | Medium | ~3.5 units | +0.6 | Should be reachable |
| S4 zigzag platforms | Medium | ~3.5–4.0 units | +1.8 | May need one movement adjustment manually |
| S5 final jumps | Medium | ~3.5–4.0 units | +0.7 | Should be reachable |

> **Manual verification required**: Jump values must be play-tested. If any jump feels too large, reduce the gap by 0.5 units in the Inspector, or increase `jumpForce` in PlayerController from 7 to 8.

---

## 6. Tests requiring manual interaction (cannot automate)

| Test | Status | Action needed |
|------|--------|--------------|
| Player moves with WASD | Requires play | Open scene, press Play |
| Player jumps with Space | Requires play | Test in Play mode |
| Camera orbits with mouse | Requires play | Test mouse input |
| Platforms have colliders | Requires play | Walk on each surface |
| Ramp is traversable | Requires play | Walk up ENV_Ramp |
| Staircase is traversable | Requires play | Walk up S1_Step0–3 |
| Moving platforms carry player | Requires play | Stand on S3/S4 moving platforms |
| Obstacle collision kills/stops player | Requires play | Contact OBS_RotatingHazard |
| Falling below kill plane triggers respawn | Requires play | Fall off any platform |
| Checkpoint saves correctly | Requires play | Enter CP_ShaftEntry, then fall |
| Goal trigger fires win panel | Requires play | Reach Sun Altar position |
| Win panel displays correctly | Requires play | Complete the game |
| Title panel dismisses on key press | Requires play | Press any key at start |
| FBX models appear with correct materials | Requires Unity | Open project in Unity Editor |
| Input System works (old vs new) | Requires play | Test WASD — see manual_actions_required.md |
| Complete route from start to finish | Requires play | 4–7 minute run-through |
| PC build launches correctly | Requires Windows | Run TheLastShabti.exe |

---

## 7. Known issues identified before play-testing

1. **Input System conflict**: The project includes the New Input System package. If `Input.GetAxis("Horizontal")` doesn't work, enable "Both" input handling in Project Settings > Player > Active Input Handling.

2. **Materials on FBX models**: FBX models may show with grey/default materials on first import. The LevelBuilder assigns URP Lit materials, but sub-meshes on FBX files may need manual material slot assignment in the Inspector.

3. **S2_Ramp**: The ENV_Ramp model was not found by the LevelBuilder (path matching issue possible). A fallback angled cube is used for the ramp. If the FBX ramp appears in the model folder but was not placed in Section 2, add it manually: duplicate `S2_PostRamp` or drag the ENV_Ramp prefab from Assets/Art/Models.

4. **CameraRig → Player link**: Verify in Inspector that `CameraRig` component on the `CameraRig` object has `Target` correctly pointing to the `Player` object.

5. **CH_Nebu model**: The character FBX is imported but not yet placed as the visible Player mesh. The Player object uses a Unity Capsule. To add Nebu visually: drag `Assets/Art/Models/CH_Nebu.fbx` as a child of the Player object, disable the Capsule MeshRenderer, and adjust Nebu's scale to fit the CharacterController capsule height (about Y 0.85 scale).
