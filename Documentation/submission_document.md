# The Last Shabti — Submission Document
**Game Design Module — Semester 1**

---

## 1. Game Title

**The Last Shabti**

---

## 2. Brief Concept

The player controls a small shabti statue called Nebu that has woken up inside an unfinished pyramid. Shabti statues were small figurines placed in Egyptian tombs to serve the dead. I liked the idea that one of them wakes up and has to find its way out. The game is a simple third-person platformer. There is no story dialogue or combat — the environment communicates the idea: the player starts in a dark tomb and gradually moves toward the light as they climb higher.

---

## 3. Player Objective

Reach the Sun Altar at the top of the pyramid. The route goes through five connected sections, each one higher and slightly warmer in lighting than the last. There is one checkpoint midway through the level.

---

## 4. Controls

| Action | Input |
|--------|-------|
| Move   | WASD |
| Jump   | Space |
| Camera | Mouse (drag) |

Controls are shown on screen at the start of the level.

---

## 5. Level Structure

The level is divided into five connected sections. The route always goes upward — the player never needs to backtrack.

### Section 1 — Burial Chamber
The starting area. Lighting is dark blue and dim. The player learns to move and jump using two easy platform gaps and a short staircase (four steps). Burial jars, wall torches and a scarab decoration establish the visual theme. A stone archway at the far end leads forward.

### Section 2 — Collapsed Gallery
A wider corridor with an uneven floor. Some sections of the floor have broken away, so the player needs to jump across three platform gaps. A sandstone ramp gives access to a higher route. Two fallen broken columns serve as visual landmarks so the player always knows where they are.

### Section 3 — Hall of Weights
This room introduces timed obstacles. There is a moving platform that slides left and right on a sine-wave cycle, a rotating stone hazard in the centre of the room, and a falling block above one of the approach platforms. I kept it to three obstacle types because adding more would make the room confusing. The rhythm is: wait, move when safe, jump.

### Section 4 — Shaft of Ra
A tall narrow vertical section. The player climbs upward using a series of seven zigzag platforms at staggered heights plus one vertical moving platform. Warm orange light comes from an opening at the top. There is a checkpoint (CP_ShaftEntry) here so the player does not have to repeat Sections 1–3 if they fall in the final section. A gold sphere marks the checkpoint position.

### Section 5 — Rooftop Sun Altar
The exterior of the pyramid. The lighting is warm and the sky is open. Four obelisks and two broken columns frame the approach. The player makes two or three final jumps to reach the Sun Altar. Touching the altar trigger fires the win message: *"THE SUN SEAL HAS BEEN RESTORED."*

---

## 6. Character Design

Nebu is a small painted stone shabti. I kept the proportions simple because I wanted the character to be readable from the third-person camera and achievable to model. The head is slightly oversized, which is common in stylised game characters and makes the face easier to read.

I gave Nebu:
- A Nemes headdress with two lappets hanging beside the face
- A turquoise collar and belt detail, based on the colours used in real Egyptian artefacts
- A small gold scarab on the chest
- Carved eyes with extended kohl lines

The character was built from around 20 separate mesh objects combined under one root empty in Blender. The body uses `bmesh` vertex extrusion and scaling. The headdress lappets are thin extruded planes shaped with edge loops. The scarab legs were created with individual cylinders rotated along a circle and merged.

---

## 7. Blender Assets Created

All assets were made in Blender 4.5.3 LTS using Python scripting (`bpy` and `bmesh`). Geometry was built procedurally — no external textures, downloaded models or add-on packs were used.

| Name | Description |
|------|-------------|
| CH_Nebu.fbx | Player character — shabti statue, ~20 mesh parts |
| ENV_SandstonePlatform.fbx | Main modular platform block with bevelled edges |
| ENV_Stair.fbx | Single modular stair step — duplicated in Unity to build flights |
| ENV_Ramp.fbx | Wedge-shaped ramp used in the Collapsed Gallery |
| ENV_Archway.fbx | Two pillars with lintel — used at section transitions |
| PROP_BrokenColumn.fbx | 8-sided cylinder with irregular broken top and base ring |
| PROP_Obelisk.fbx | Tapered rectangular column with gold pyramidion cap |
| PROP_BurialJar.fbx | Ceramic jar with rounded belly, narrow neck and lid |
| PROP_WallTorch.fbx | Wall bracket, cup and stylised flame cone |
| PROP_ScarabWall.fbx | Flat panel with raised scarab geometry and turquoise wings |
| PROP_SunAltar.fbx | Three-tier altar with gold sun disc and rays — the goal object |

Total: 11 FBX files exported and imported into Unity.

---

## 8. Use of Materials and Lighting

I used Principled BSDF materials in Blender with solid base colours — no image textures. In Unity, 10 URP Lit materials were created that mirror the Blender palette.

| Material | Approximate colour | Used for |
|----------|--------------------|----------|
| MAT_Sandstone | #C4A265 warm tan | Platforms, archways, stairs, ramp |
| MAT_StoneBlue | #708AA0 grey-blue | Nebu body, pillars, columns, scarab wall |
| MAT_Turquoise | #489090 teal | Collar, belt, burial jars |
| MAT_GoldAccent | #C8A82E warm gold | Scarab, pyramidion, sun disc, rays |
| MAT_DarkBrown | #261408 near-black | Carved details, kohl lines |
| MAT_Clay | #8C6148 terracotta | Burial jar body |
| MAT_TorchFire | #FF8020 orange, emissive | Torch flame — glows in Play mode |
| MAT_TombBlue | #2A3B4C dark blue | Tomb walls and ceiling |
| MAT_Obstacle | #A05020 dark orange | Moving platforms and rotating hazard |
| MAT_Player | #8894A0 light blue-grey | Player capsule |

Lighting in Unity transitions from cold blue (Sections 1–2) through neutral (Section 3) to warm orange (Sections 4–5). Six light objects: one main directional, one directional for the tomb interior, plus four point lights (cold fill in the tomb, warm fill in the Hall of Weights, orange shaft light, gold altar glow).

---

## 9. Obstacles

The Obstacle Course Pack was not available in my Unity installation. I wrote two short scripts that cover the same design role:

| Script | Behaviour | Where placed |
|--------|-----------|-------------|
| `MovingPlatform.cs` | Moves back and forth using a sine-wave on a chosen axis (X, Y, or Z). Distance and speed are configurable in the Inspector. | S3 Hall of Weights (X axis), S4 Shaft of Ra (Y axis) |
| `RotatingHazard.cs` | Rotates continuously around the Y axis at a configurable speed in degrees per second. | S3 Hall of Weights centre |

---

## 10. Unity Implementation

The project uses **Unity 6 (6000.2.10f1)** with Universal Render Pipeline (URP 17.2.0). The entire scene was built programmatically using a custom Unity Editor script (`Assets/Editor/LevelBuilder.cs`) run in batch mode. The scene contains 87 GameObjects.

Scene hierarchy:
```
LVL_MainPyramid (scene)
├── Environment
│   ├── S1_BurialChamber
│   ├── S2_CollapsedGallery
│   ├── S3_HallOfWeights
│   ├── S4_ShaftOfRa
│   └── S5_RooftopAltarSection
├── Player (CharacterController + PlayerController + CameraRig)
├── CameraRig / Main Camera
├── CheckpointManager
├── Lighting (6 lights)
├── KillPlane (Y = -8, isTrigger)
├── Goal_SunAltarTrigger
└── UI_Canvas
    ├── TitlePanel
    └── WinPanel
```

Custom scripts written for the project:

| Script | Purpose |
|--------|---------|
| `PlayerController.cs` | WASD camera-relative movement, Space to jump. |
| `CameraRig.cs` | Third-person orbit camera. Mouse X/Y rotates yaw and pitch, follows the player. |
| `GoalTrigger.cs` | Activates WinPanel and pauses the game when the player reaches the altar. |
| `CheckpointManager.cs` | Singleton that stores the last activated checkpoint position. |
| `CheckpointZone.cs` | OnTriggerEnter — saves the player position via CheckpointManager. |
| `PlayerRespawn.cs` | Teleports the player back to the checkpoint when they fall below the kill plane. |
| `MovingPlatform.cs` | Sine-wave platform movement on a configurable axis. |
| `RotatingHazard.cs` | Continuous Y-axis rotation at configurable degrees per second. |

---

## 11. Challenges Encountered

**Blender Eevee API change**: When I ran the render script, Blender threw an error about `use_soft_shadows` not existing. It turns out Blender 4.2 replaced Eevee with Eevee Next and removed that property. Removing the line fixed it.

**FBX axis orientation**: The first exports came into Unity rotated 90 degrees. Adding `axis_forward='-Z', axis_up='Y'` to the export call fixed the orientation.

**Unity in terminal mode**: Running Unity from WSL terminal produced a lot of licence server errors in the log. The build still completed and the exit code was 0 — the messages were just noise from Unity not being able to reach the licence server through the terminal session.

**Obstacle Course Pack missing**: The pack was not installed so I wrote the two movement scripts myself. They are simple but they do the job — the obstacles move and rotate correctly in Play mode.

**Input System conflict**: Unity 6 ships with the New Input System package enabled. The player script uses the old `Input.GetAxis` API. If WASD does not respond, the fix is: **Edit > Project Settings > Player > Active Input Handling → Both**.

**Burial jar rim**: The vertex loop scaling for the jar's top rim produced small irregularities. A `bmesh.ops.smooth_vert` pass on that loop evened it out before export.

---

## 12. Improvements I Would Make With More Time

- Add a walk and jump animation cycle for Nebu using a simple armature. Even two keyframes would make the character feel more alive.
- Add ambient sound: stone echoes in the tomb sections, wind on the rooftop.
- Create a second platform variation with different proportions so not every surface looks identical.
- Make the lighting transition gradual instead of jumping per section — a `RenderSettings.ambientLight` lerp tied to the player's Y position.
- Add a pause menu and a restart-from-checkpoint button on the win panel.
- Replace the player capsule with CH_Nebu.fbx as the visible character mesh.

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

`Documentation/Screenshots/nebu_front_hq.png`
*Nebu character from front. Shows Nemes headdress, scarab on chest, turquoise collar, kohl eye lines.*

**Blender render — Nebu three-quarter view**

`Documentation/Screenshots/nebu_34_hq.png`
*Nebu from a three-quarter angle showing the back headdress cloth and side profile.*

**Blender render — Environment assets overview**

`Documentation/Screenshots/assets_overview_hq.png`
*All 10 environment and prop assets arranged in a single Blender scene for review.*

**Blender render — Level scene**

`Documentation/Screenshots/level_scene_hq.png`
*Composed level preview showing the staircase, gap platforms, archway and Nebu placed at the start.*

**2D Level Map**

`Documentation/Map/level_map.svg`
*Side-elevation map of all five sections with platform symbols, route arrows, checkpoint marker and section labels.*

---

## 17. Technical Specifications

| Item | Value |
|------|-------|
| Engine | Unity 6 (6000.2.10f1) |
| Render pipeline | Universal Render Pipeline (URP) 17.2.0 |
| Blender version | 4.5.3 LTS |
| Target platform | Windows x86_64 |
| FBX models | 11 |
| Unity materials | 10 |
| Custom scripts | 8 |

---

*Submitted for Game Design Module — Semester 1*
