# The Last Shabti — Submission Document
**Game Design Module — Semester 1**

---

## 1. Game Title

**The Last Shabti**

---

## 2. Brief Concept

The idea came from thinking about what shabti statues actually were — small figurines placed in tombs to do the work of the dead in the afterlife. I liked the image of one waking up confused inside an unfinished pyramid and just trying to get out. The game is a simple third-person platformer. No combat, no dialogue — just climbing. The environment does most of the storytelling: you start in a dim, cold blue tomb and as you go higher the light gets warmer until you reach open sky at the top.

---

## 3. Player Objective

Get to the Sun Altar at the top of the pyramid. The path goes through five sections, each one higher than the last. There's a checkpoint about halfway through so if you fall in the harder parts you don't have to redo everything.

---

## 4. Controls

| Action | Input |
|--------|-------|
| Move   | WASD |
| Jump   | Space |
| Camera | Mouse (drag) |

The controls appear on screen at the start of the level.

---

## 5. Level Structure

Five sections, always going upward. The player never needs to backtrack.

### Section 1 — Burial Chamber
The starting room. Dark blue lighting, very dim. Two small platform gaps and a short staircase introduce the controls without pressure. Burial jars, wall torches and a scarab panel set the visual theme. A stone archway leads through to the next section.

### Section 2 — Collapsed Gallery
A wider corridor where part of the floor has broken away. Three gap jumps across the broken sections, with a sandstone ramp leading up to a higher path. A couple of broken columns help the player orient themselves.

### Section 3 — Hall of Weights
First room with moving obstacles. There's a platform sliding left and right, a stone block rotating in the middle of the room, and a block that drops from above one of the approach platforms. I kept it to three hazards because the room would get confusing with more. The idea is to read the rhythm, wait, then move.

### Section 4 — Shaft of Ra
A tall vertical section. The player zigzags up through seven platforms at different heights, plus one platform moving vertically. The lighting shifts to warm orange here. There's a checkpoint at the bottom of the shaft so falling in Section 5 doesn't send you all the way back.

### Section 5 — Rooftop Sun Altar
The top of the pyramid. Open sky, warm lighting. Four obelisks and some broken columns frame the final approach. Two or three jumps to the altar, which triggers the win message: *"THE SUN SEAL HAS BEEN RESTORED."*

---

## 6. Character Design

Nebu is a small stone shabti statue — the player character. I kept the shape simple and a bit stylised because I needed it to be readable from a third-person camera and realistic to model in Blender. The head is slightly large for the body, which is a common shortcut in game character design to make the face more visible from a distance.

Details I included:
- A Nemes headdress with two lappets hanging at the sides
- Turquoise collar and waist band, based on colours used in real Egyptian artefacts
- A small gold scarab on the chest
- Carved eyes with extended kohl lines

The character is around 20 separate mesh objects parented under one empty in Blender. The body was built with `bmesh` extrusion and loop scaling. The headdress lappets are thin planes with edge loops to shape them. The scarab legs are individual cylinders rotated in a circle and merged.

---

## 7. Blender Assets Created

All assets were made in Blender 4.5.3 using Python scripting (`bpy` and `bmesh`). Everything was built procedurally — no external textures, downloaded models or add-ons.

| Name | Description |
|------|-------------|
| CH_Nebu.fbx | Player character — shabti statue, ~20 mesh parts |
| ENV_SandstonePlatform.fbx | Main modular platform block with bevelled edges |
| ENV_Stair.fbx | Single stair step, duplicated in Unity to build the full staircase |
| ENV_Ramp.fbx | Wedge ramp used in the Collapsed Gallery |
| ENV_Archway.fbx | Two pillars with a lintel — used at the transitions between sections |
| PROP_BrokenColumn.fbx | 8-sided column with a rough broken top |
| PROP_Obelisk.fbx | Tapered rectangular column with a gold pyramidion cap |
| PROP_BurialJar.fbx | Ceramic jar with a rounded belly, narrow neck and lid |
| PROP_WallTorch.fbx | Wall bracket with a cup and stylised flame |
| PROP_ScarabWall.fbx | Flat panel with raised scarab geometry and turquoise wings |
| PROP_SunAltar.fbx | Three-tier altar with a gold sun disc and rays — the goal object |

11 FBX files total, all exported and imported into Unity.

---

## 8. Use of Materials and Lighting

Principled BSDF materials in Blender with flat base colours — no image textures. In Unity I created 10 URP Lit materials that match the Blender palette.

| Material | Approximate colour | Used for |
|----------|--------------------|----------|
| MAT_Sandstone | #C4A265 warm tan | Platforms, archways, stairs, ramp |
| MAT_StoneBlue | #708AA0 grey-blue | Nebu body, pillars, columns, scarab wall |
| MAT_Turquoise | #489090 teal | Collar, belt, burial jars |
| MAT_GoldAccent | #C8A82E warm gold | Scarab, pyramidion cap, sun disc, rays |
| MAT_DarkBrown | #261408 near-black | Carved details, kohl lines |
| MAT_Clay | #8C6148 terracotta | Burial jar body |
| MAT_TorchFire | #FF8020 orange, emissive | Torch flame — glows in Play mode |
| MAT_TombBlue | #2A3B4C dark blue | Tomb walls and ceiling |
| MAT_Obstacle | #A05020 dark orange | Moving platforms and rotating hazard |
| MAT_Player | #8894A0 light blue-grey | Player character |

Lighting transitions from cold blue in Sections 1–2, through neutral in Section 3, to warm orange in Sections 4–5. Six lights in total: one main directional, one interior directional for the tomb, and four point lights placed at key moments (cold fill in the tomb, warm fill in the Hall of Weights, orange shaft glow, gold altar light at the top).

---

## 9. Obstacles

The project uses the **Obstacle Course Pack** from the Unity Asset Store. The pack's `CharacterControls` script handles the player movement and the `CameraManager` handles the third-person camera.

For obstacle movement I used a mix of OCP scripts and two short scripts I wrote myself:

| Script | Source | Behaviour | Where placed |
|--------|--------|-----------|-------------|
| `MovableObs.cs` | OCP | Moves an object back and forth on the X or Z axis. | S3 horizontal sliding platform |
| `Rotator.cs` | OCP | Rotates continuously around the Z axis. | S3 rotating stone hazard |
| `MovingPlatform.cs` | Custom | Same as MovableObs but supports Y axis movement, using a sine-wave. | S4 vertical moving platform and OBS_FallingBlock |
| `RotatingHazard.cs` | Custom | Rotates on the Y axis in world space at configurable degrees per second. | S3 Hall of Weights centre |

I wrote the two custom scripts because OCP's `MovableObs` only moves horizontally (X or Z) and `Rotator` uses the Z axis in local space — neither of those worked for the falling block in Section 3 or the Y-axis rotation I needed for the central hazard.

---

## 10. Unity Implementation

The project uses **Unity 6 (6000.2.10f1)** with Universal Render Pipeline (URP 17.2.0). The scene was built using a custom Editor script (`Assets/Editor/LevelBuilder.cs`). The scene has 87 GameObjects.

Scene hierarchy:
```
LVL_MainPyramid (scene)
├── Environment
│   ├── S1_BurialChamber
│   ├── S2_CollapsedGallery
│   ├── S3_HallOfWeights
│   ├── S4_ShaftOfRa
│   └── S5_RooftopAltarSection
├── Player (OCP CharacterControls + CameraManager)
├── CheckpointManager
├── Lighting (6 lights)
├── KillPlane (Y = -8, isTrigger)
├── Goal_SunAltarTrigger
└── UI_Canvas
    ├── TitlePanel
    └── WinPanel
```

Custom scripts written for this project:

| Script | Purpose |
|--------|---------|
| `GoalTrigger.cs` | Activates the WinPanel and pauses the game when the player reaches the altar. |
| `CheckpointManager.cs` | Stores the last activated checkpoint position. |
| `CheckpointZone.cs` | Saves the player position when they walk through a checkpoint trigger. |
| `PlayerRespawn.cs` | Teleports the player back to the checkpoint when they fall below the kill plane. |
| `MovingPlatform.cs` | Sine-wave movement on a configurable axis (X, Y, or Z). |
| `RotatingHazard.cs` | Continuous Y-axis rotation at configurable degrees per second. |

---

## 11. Challenges Encountered

**Blender Eevee API change**: Running the render script gave an error about `use_soft_shadows` not existing. Blender 4.2 replaced Eevee with Eevee Next and removed that property. Removing the line fixed it.

**FBX axis orientation**: First exports came into Unity rotated 90 degrees. Adding `axis_forward='-Z', axis_up='Y'` to the export call fixed the orientation without needing any extra rotation in Unity.

**Unity in terminal mode**: Running Unity from a WSL terminal produced a lot of licence server errors in the log. The build still finished and the exit code was 0 — the messages were just noise from Unity not reaching the server through the terminal session.

**MovableObs only moves on X/Z**: The OCP script doesn't support vertical movement. OBS_FallingBlock needed to drop down on the Y axis so I wrote MovingPlatform with configurable axis support.

**Input System conflict**: Unity 6 ships with the New Input System enabled by default. The OCP movement scripts use the legacy `Input.GetAxis` API. Fix: **Edit > Project Settings > Player > Active Input Handling → Both**.

**Burial jar rim geometry**: The bmesh vertex loop scaling for the jar's top rim produced small irregularities. A `bmesh.ops.smooth_vert` pass on that loop fixed it before export.

---

## 12. Improvements I Would Make With More Time

- Add a walk and jump animation cycle for Nebu. Even two keyframes would make it feel more alive.
- Add sound — stone echoes in the tomb sections and open-sky wind on the rooftop.
- A second platform shape with different proportions so not every surface looks the same.
- Gradual lighting transition instead of a hard cut per section — a coroutine lerping `RenderSettings.ambientLight` based on the player's Y position.
- Pause menu and a restart button on the win screen.
- Swap the player capsule for the Nebu mesh as the visible character.

---

## 13. GitHub Project Link

https://github.com/geisonhg/TheLastShabti

---

## 14. Unity Build Link

https://drive.google.com/file/d/1DCfLFOGF4SlF31X2ievCwI1M7d8b1io2/view?usp=sharing

Build file: `TheLastShabti.exe` — Windows x86_64

---

## 15. Blender File Link

https://drive.google.com/file/d/1DCfLFOGF4SlF31X2ievCwI1M7d8b1io2/view?usp=sharing

Blend file saved with all objects, materials, cameras and render settings intact.

---

## 16. Screenshots

**Blender render — Nebu front view**

`Documentation/Screenshots/Screenshot 2026-07-15 213604.png`
*Nebu character from front. Shows Nemes headdress, scarab on chest, turquoise collar, kohl eye lines.*

**Blender render — Nebu three-quarter view**

`Documentation/Screenshots/Screenshot 2026-07-15 213706.png`
*Nebu from a three-quarter angle showing the back of the headdress and side profile.*

**Blender render — Environment assets overview**

`Documentation/Screenshots/Screenshot 2026-07-16 125808.png`
*All 10 environment and prop assets arranged together for review.*

**Blender render — Level scene**

`Documentation/Screenshots/Screenshot 2026-07-16 125919.png`
*Composed level preview: staircase, gap platforms, archway and Nebu at the start position.*

**2D Level Map**

`Documentation/Map/level_map.svg`
*Side-elevation map of all five sections with platform positions, route arrows, checkpoint marker and section labels.*

---

## 17. Technical Specifications

| Item | Value |
|------|-------|
| Engine | Unity 6 (6000.2.10f1) |
| Render pipeline | Universal Render Pipeline (URP 17.2.0) |
| Blender version | 4.5.3 LTS |
| Target platform | Windows x86_64 |
| FBX models | 11 |
| Unity materials | 10 |
| Custom scripts | 6 |

---

*Submitted for Game Design Module — Semester 1*
