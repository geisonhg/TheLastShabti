# Manual Actions Required — The Last Shabti

This file lists every step that cannot be automated from a WSL command line. Complete these in order before final submission.

---

## Priority 1 — Required to verify the game works

### 1.1 Fix Input System (if WASD/Space do not respond)

**When**: First time you press Play in Unity Editor and the player does not move.

**Steps**:
1. Open the project in Unity Editor (`C:\Users\geiso\Documents\TheLastShabti\UnityProject\`)
2. Go to **Edit > Project Settings > Player**
3. Scroll to **Other Settings > Configuration**
4. Find **Active Input Handling** — change it from `Input System Package (New)` to **Both**
5. Unity will ask to restart — click **Apply**
6. Press Play again — WASD and Space should now work

**Why this may be needed**: The project's `manifest.json` includes the New Input System package. When this package is active, Unity 6 defaults to the new input API. `PlayerController.cs` uses the legacy `Input.GetAxis` / `Input.GetButton` API. Enabling "Both" makes legacy calls work alongside the new system.

---

### 1.2 Verify CameraRig → Player link

**When**: First time you press Play and the camera does not follow the player.

**Steps**:
1. In the Hierarchy, click **CameraRig**
2. In the Inspector, find the **Camera Rig (Script)** component
3. Check the **Target** field — it should say `Player (Transform)`
4. If it is empty: drag the **Player** object from the Hierarchy into the **Target** slot
5. Press Play — the camera should now orbit the player

**Why this may be needed**: The LevelBuilder script sets `cameraRig.target = player.transform` at build time, but Unity's serialized object references can break if objects are rebuilt or the scene is reimported.

---

### 1.3 Play-test the full route

**Steps**:
1. Open `Assets/Scenes/LVL_MainPyramid.unity`
2. Press Play
3. Press any key to dismiss the title panel
4. Walk and jump through all five sections:
   - S1 Burial Chamber → S2 Collapsed Gallery → S3 Hall of Weights → S4 Shaft of Ra → S5 Rooftop Sun Altar
5. Reach the **Goal_SunAltarTrigger** — the win panel should appear: *"THE SUN SEAL HAS BEEN RESTORED"*

**Expected total time**: 4–7 minutes for a complete run without dying.

**Checkpoints**: Fall off a platform after passing through **S4 Shaft of Ra** entry — you should respawn at **CP_ShaftEntry**, not at the beginning.

---

### 1.4 Verify moving platforms carry the player

**When**: In S3 (Hall of Weights) and S4 (Shaft of Ra).

**Steps**:
1. Navigate to the moving platform in Section 3 (`S3_MovingPlatform`)
2. Stand on it — your character should travel with the platform, not slide off
3. Do the same for `S4_MovingPlatform`

**If the player slides off instead of riding**: Add a `PlatformEffector2D` — wait, this is 3D. For a CharacterController the fix is: on the `MovingPlatform` object, add a script that sets `transform.parent` of the player while they stand on it, or use a kinematic Rigidbody on the platform. The current `MovingPlatform.cs` moves by setting `transform.position` directly, which does not push CharacterController-based players. **Workaround**: Set `moveSpeed` in `PlayerController` to a value slightly higher than the platform speed so the player can walk faster than the platform — or parent the player to the platform via a trigger script.

---

### 1.5 Jump distance adjustment (if any jump is unreachable)

**Numerical values**: `moveSpeed = 5`, `jumpForce = 7`, `gravity = -18` → estimated horizontal range ≈ 3.9 units.

**If a gap feels too wide**:
- Select the **Player** object → Inspector → **Player Controller (Script)**
- Increase `Jump Force` from 7 to 8 (adds ~0.5 units of extra range)
- Or select the destination platform and move it 0.5 units closer on the X axis

**Specific gaps to check**: S4 zigzag platforms (elevation change +1.8 units) and S1 Start → Jump1 (elevation +0.45 units).

---

## Priority 2 — Visual polish (recommended before submission)

### 2.1 Place CH_Nebu character model on the Player

**Steps**:
1. In the Hierarchy, expand the **Player** object
2. In the Project window, navigate to `Assets/Art/Models/`
3. Drag **CH_Nebu.fbx** onto the **Player** object in the Hierarchy (makes it a child)
4. Select the new **CH_Nebu** child object
5. Set its Transform: Position `(0, -1, 0)`, Rotation `(0, 0, 0)`, Scale `(0.85, 0.85, 0.85)`
6. Select the **Player** object itself → in the Inspector, find the **Mesh Renderer** component → uncheck it to hide the capsule placeholder
7. Press Play — you should now see Nebu instead of a white capsule

**Note**: The character FBX uses Blender-generated materials. After placing, you may need to assign materials manually in the Inspector → **Skinned Mesh Renderer > Materials** if the model appears grey.

---

### 2.2 Assign materials to FBX models (if they appear grey)

When FBX files are first imported into Unity, Unity creates material slots named after the Blender material names. These may not auto-connect to the `.mat` files in `Assets/Art/Materials/`.

**Steps for each FBX model that looks grey**:
1. In the Project window, select the FBX file (e.g., `PROP_WallTorch.fbx`)
2. In the Inspector → **Materials** tab
3. Click **Extract Materials** (or individually remap each material slot)
4. In the Hierarchy, find the placed object and inspect its **Mesh Renderer > Materials**
5. Drag the correct `.mat` file from `Assets/Art/Materials/` into each slot

**Material reference table**:

| Model | Material to assign |
|-------|--------------------|
| ENV_SandstonePlatform | MAT_Sandstone |
| ENV_Stair | MAT_Sandstone |
| ENV_Ramp | MAT_Sandstone |
| ENV_Archway | MAT_StoneBlue |
| PROP_BurialJar | MAT_Turquoise |
| PROP_WallTorch | MAT_DarkBrown + MAT_TorchFire (emission) |
| PROP_ScarabWall | MAT_StoneBlue |
| PROP_BrokenColumn | MAT_Sandstone |
| PROP_Obelisk | MAT_GoldAccent |
| PROP_SunAltar | MAT_GoldAccent |
| CH_Nebu | MAT_Clay (body) + MAT_StoneBlue (wrap) + MAT_GoldAccent (trim) + MAT_TurquoiseBlue (lapis) + MAT_EyeBlack (eyes) |

---

### 2.3 Fix UI font if text appears blank

**Steps**:
1. In the Hierarchy, expand **UI_Canvas > TitlePanel** and click the text objects
2. In the Inspector → **Text (Legacy) > Font** — if it shows `None`, click the picker and select **Arial**
3. Repeat for all text objects inside **TitlePanel** and **WinPanel**

---

### 2.4 Add S2_Ramp if missing (ENV_Ramp fallback issue)

The LevelBuilder may have placed an angled cube for the Section 2 ramp instead of the ENV_Ramp FBX. To replace it:
1. In the Hierarchy, find **S2_CollapsedGallery > S2_Ramp** and delete it
2. In the Project window, drag `Assets/Art/Models/ENV_Ramp.fbx` into the **S2_CollapsedGallery** object
3. Set its Transform: Position `(21, 1.2, 0)`, Rotation `(0, 0, -20)`, Scale `(1, 1, 1)`
4. Assign **MAT_Sandstone** material

---

## Priority 3 — Submission packaging

### 3.1 Take in-editor screenshots for submission document

Open Unity Editor with the scene loaded. Take at least 3 screenshots:

| Screenshot | What to show | How |
|------------|-------------|-----|
| `screenshot_S1_burial.png` | Section 1 from Scene View (Orthographic, top-right angle) | Scene view → screenshot key or Snipping Tool |
| `screenshot_S5_altar.png` | Section 5 Rooftop Sun Altar from Game View | Press Play, walk to S5, use Snipping Tool |
| `screenshot_player_ui.png` | Title panel on first load | Press Play before pressing a key |

Save screenshots to `Documentation/Screenshots/`.

---

### 3.2 Import Obstacle Course Pack (if available)

If you obtain the Obstacle Course Pack from the Unity Asset Store (ID 178169) before submission:
1. Open the project in Unity Editor
2. **Window > Package Manager > My Assets**
3. Find "Obstacle Course Pack" and import
4. Replace `S3_MovingPlatform` and `S4_MovingPlatform` with the OCP moving platform prefab
5. Replace `OBS_RotatingHazard` with the OCP rotating hazard prefab
6. Remove `MovingPlatform.cs` and `RotatingHazard.cs` (or keep them — Unity will compile both)

**If you skip this**: The project is complete and functional without it. The placeholder scripts are clearly labelled in the code comments.

---

### 3.3 Create GitHub repository and push

```bash
# In WSL, inside the TheLastShabti folder:
cd /home/geisonhg/TheLastShabti

# Create the repo on GitHub first (web UI or gh CLI):
gh repo create TheLastShabti --public --description "The Last Shabti — 3D platformer Unity 6 assignment"

# Push:
git remote add origin https://github.com/geisonhg/TheLastShabti.git
git push -u origin main
```

---

### 3.4 Upload build to Google Drive or itch.io

**Build location**: `C:\Users\geiso\Documents\TheLastShabti\Build\TheLastShabti\`

**Google Drive**:
1. Zip the entire `Build\TheLastShabti\` folder → `TheLastShabti_Build.zip`
2. Upload to Google Drive
3. Set sharing to "Anyone with the link can view"
4. Copy the link and paste it into `submission_document.md` under "Download Link"

**itch.io** (alternative):
1. Create a project at itch.io
2. Upload `TheLastShabti_Build.zip` as a Windows download
3. Set visibility to public

---

### 3.5 Verify the Windows build runs

1. Navigate to `C:\Users\geiso\Documents\TheLastShabti\Build\TheLastShabti\`
2. Double-click `TheLastShabti.exe`
3. Verify the game opens, the title panel appears, and basic movement works
4. Note the resolution/window mode — the build defaults to 1920×1080 fullscreen

---

## Checklist summary

| # | Action | Status |
|---|--------|--------|
| 1.1 | Fix Input System (if needed) | ☐ |
| 1.2 | Verify CameraRig → Player link | ☐ |
| 1.3 | Play-test full route start to finish | ☐ |
| 1.4 | Verify moving platforms carry player | ☐ |
| 1.5 | Adjust jump distances if any gap is unreachable | ☐ |
| 2.1 | Place CH_Nebu model on Player | ☐ |
| 2.2 | Assign materials to FBX models | ☐ |
| 2.3 | Fix UI fonts if blank | ☐ |
| 2.4 | Add ENV_Ramp if S2 ramp is an angled cube | ☐ |
| 3.1 | Take in-editor screenshots | ☐ |
| 3.2 | Import OCP (if available) | ☐ |
| 3.3 | Create GitHub repository and push | ☐ |
| 3.4 | Upload build to Google Drive or itch.io | ☐ |
| 3.5 | Verify Windows build runs end-to-end | ☐ |
