# The Last Shabti — Project Plan

## Phase order (follow this sequence)

---

### Phase 1 — Setup (Do this first)
- [ ] Create GitHub repository and push initial project structure
- [ ] Install Unity 2022.3 LTS via Unity Hub
- [ ] Create a new 3D (URP or Built-in) Unity project in `TheLastShabti/UnityProject/`
- [ ] Import Obstacle Course Pack from Unity Asset Store (link in README)
- [ ] Test that the pack's demo scene opens and the character moves correctly
- [ ] Open Blender 3.6 or 4.x and confirm Scripting workspace works

---

### Phase 2 — Blender assets
- [ ] Run `01_create_nebu.py` in Blender Scripting tab
- [ ] Review Nebu in viewport — adjust proportions if needed
- [ ] Run `02_create_env_assets.py`
- [ ] Review all 10 assets in the viewport
- [ ] Apply All Transforms to all objects (Ctrl+A > All Transforms)
- [ ] Save the .blend file as `Blender/TheLastShabti.blend`
- [ ] Edit `EXPORT_PATH` in `03_export_fbx.py` to match your computer
- [ ] Run `03_export_fbx.py` — check that FBX files appear in `Blender/Exports/`

---

### Phase 3 — Unity import and prefabs
- [ ] Drag FBX files into Unity `Assets/Art/Models/`
- [ ] Set Scale Factor to 1 on all imported models (Inspector > Import Settings)
- [ ] Check materials appear on each model (may need to re-apply in Unity)
  - Create materials in `Assets/Art/Materials/` using the colour values from submission_document.md
  - Assign them to the model slots
- [ ] Create a Prefab for each asset in `Assets/Prefabs/`
  - Add Box Collider to each prefab (Mesh Collider only for ramp)
  - Mark as Static where appropriate
  - Name them with the correct convention: ENV_, PROP_, CH_, etc.
- [ ] Test Nebu prefab with the Obstacle Course Pack character controller

---

### Phase 4 — Level blockout (grey box first)
- [ ] Create a new scene: `Assets/Scenes/LVL_MainPyramid`
- [ ] Set up the scene hierarchy (Environment, Player, Obstacles, etc.)
- [ ] Block out Section 1 using Unity cubes (no art yet)
  - Starting platform
  - Two jumps
  - Short staircase
  - Doorway
  - Confirm the player can cross and jump feels right
- [ ] Block out Section 2
- [ ] Block out Section 3
- [ ] Block out Section 4
- [ ] Block out Section 5
- [ ] Play through the entire route — fix any gaps, too-long jumps or unclear paths
- [ ] Test kill plane — player should die when falling and return to checkpoint

---

### Phase 5 — Replace blockout with art assets
- [ ] Replace cube platforms with ENV_SandstonePlatform prefabs
- [ ] Replace cube stairs with ENV_Stair prefabs (offset and stack in Inspector)
- [ ] Replace cube ramps with ENV_Ramp
- [ ] Place PROP_BrokenColumn in Section 2 as landmarks
- [ ] Place PROP_BurialJar groups in Section 1 (3–5 jars near walls)
- [ ] Place PROP_WallTorch on walls in Sections 1 and 2
- [ ] Place PROP_ScarabWall on a wall in Section 1
- [ ] Place ENV_Archway at each section transition doorway
- [ ] Place PROP_Obelisk pairs on the rooftop
- [ ] Place PROP_SunAltar at the end of Section 5

---

### Phase 6 — Obstacles (Section 3 only)
- [ ] Import the Obstacle Course Pack moving platform prefab into Section 3
  - Adjust its path length to fit the room
  - Apply sandstone material to visually match the level
- [ ] Import the rotating obstacle prefab
  - Place centrally in Section 3
  - Adjust rotation speed in Inspector if needed
- [ ] Import the falling block prefab
  - Place above one platform in Section 3
  - Test that the timing is reasonable
- [ ] Add one moving platform to Section 4 (Shaft of Ra)
- [ ] Test all obstacles — rhythm should be: observe, wait, move, jump

---

### Phase 7 — Lighting
- [ ] Delete the default Unity directional light
- [ ] Section 1–2: Add a low-intensity directional light with colour #3A4A7A (cold blue)
  - Add 2–4 point lights near wall torch positions, colour #E87020, range 4–6, intensity 1.5
- [ ] Section 3: Slightly warmer neutral light — move directional light intensity up slightly
- [ ] Section 4: Add a warm area light or directional from above — colour #F0A040
- [ ] Section 5 (Rooftop): Warm golden directional light — colour #F08030, intensity 1.2
  - Add sky or gradient backdrop if using URP
- [ ] Bake lighting if using Built-in render pipeline (Window > Rendering > Lighting)

---

### Phase 8 — Checkpoint and goal
- [ ] Add GoalTrigger.cs to a trigger box at the Sun Altar
  - Create a Canvas with a Panel containing the text "The Sun Seal has been restored"
  - Assign it to the Win Panel slot
- [ ] Add a single CheckpointManager empty in the scene and attach CheckpointManager.cs
- [ ] Add a trigger box at the Section 4 entry and attach CheckpointZone.cs
- [ ] Add PlayerRespawn.cs to the Player (or confirm the pack handles this)
- [ ] Test: fall, check that checkpoint restores correctly
- [ ] Test: reach the altar, confirm win message appears and game pauses

---

### Phase 9 — UI
- [ ] Create a title Canvas with the text "The Last Shabti"
  - Show it for 3–4 seconds at level start
  - Include simple controls text: WASD / Space / Mouse
- [ ] Confirm win panel looks clean and readable
- [ ] Optional: add a small checkpoint notification ("Checkpoint reached")

---

### Phase 10 — Final testing checklist
- [ ] Complete run from start to finish (aim for 4–7 minutes)
- [ ] Check every jump is reachable without needing pixel-perfect timing
- [ ] Check ramp and stair colliders — no invisible walls or sliding
- [ ] Check all obstacles work on correct loop timing
- [ ] Check checkpoint saves and restores correctly after a fall
- [ ] Check goal trigger fires and win panel displays correctly
- [ ] Check no console errors (Window > General > Console)
- [ ] Check all materials appear correctly (no pink/magenta missing material errors)
- [ ] Check Nebu character model imports and displays correctly
- [ ] Check build: File > Build Settings > PC > Build

---

### Phase 11 — Build and submission
- [ ] Build the project: File > Build Settings > PC Standalone > Build
- [ ] Test the .exe build on a clean run (close Unity first)
- [ ] Upload build to Google Drive or itch.io — do NOT commit to Git
- [ ] Add final screenshots to `Documentation/Screenshots/`
- [ ] Export a PNG copy of the SVG level map
- [ ] Upload the .blend file to Google Drive
- [ ] Fill in all [ADD LINK] placeholders in `submission_document.md`
- [ ] Review the submission document — add screenshot captions
- [ ] Push final commit to GitHub
- [ ] Compress the Unity project (zip UnityProject folder excluding Library/)
- [ ] Submit to Moodle: see final checklist below

---

## Approximate time budget

| Phase | Estimated time |
|-------|---------------|
| Setup | 1–2 hours |
| Blender assets | 4–8 hours |
| Unity import + prefabs | 2–3 hours |
| Level blockout + art | 4–6 hours |
| Obstacles + lighting | 2–3 hours |
| Checkpoint + goal + UI | 1–2 hours |
| Testing + fixes | 2–3 hours |
| Build + documentation | 1–2 hours |
| **Total** | **~17–29 hours** |

---

## Final submission checklist (Moodle)

- [ ] Unity project folder (zipped, excluding Library/)
- [ ] .blend file (or Drive link)
- [ ] PC build (executable — Drive or itch.io link)
- [ ] 2D level map (SVG and PNG in Documentation/Map/)
- [ ] Submission document (PDF or Word export of submission_document.md)
- [ ] GitHub repository link (all scripts and structure committed)
- [ ] At least 6 screenshots in the submission document
