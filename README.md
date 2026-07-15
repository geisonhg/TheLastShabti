# The Last Shabti

**Game Design Module — Semester 1 Recovery Assignment**

A 3D third-person platformer set inside an unfinished Egyptian pyramid. The player controls Nebu, a small shabti statue that has awakened in the burial chamber and must reach the Sun Altar on the rooftop.

---

## Software

| Tool | Version |
|------|---------|
| Unity | 2022.3 LTS (or 2021.3 LTS) |
| Blender | 3.6 or 4.x |
| Obstacle Course Pack | Unity Asset Store (free) |

---

## Controls

| Action | Key |
|--------|-----|
| Move | WASD / Left stick |
| Jump | Space / A button |
| Camera | Mouse / Right stick |

---

## How to open the Unity project

1. Open **Unity Hub**
2. Click **Add > Add project from disk**
3. Navigate to `TheLastShabti/UnityProject/`
4. Select the folder and confirm
5. Open the project with Unity 2022.3 LTS
6. Once open, go to `Assets/Scenes/` and double-click `LVL_MainPyramid`

> **Note:** The Obstacle Course Pack must be imported from the Unity Asset Store before the scene will work correctly. See the setup section in the submission document.

---

## How to play the build

1. Go to the `Build/` folder
2. Run `TheLastShabti.exe` (Windows) or the equivalent for your platform
3. Use WASD to move, Space to jump, Mouse to control camera
4. The goal is to reach the Sun Altar at the top of the pyramid

---

## Asset restrictions

- All 3D models were created in Blender by the author
- No external texture images were used — only Principled BSDF materials with solid colours
- No Mixamo rigs or animations were used
- No downloaded Egyptian asset packs were used
- The only permitted external pack is the **Obstacle Course Pack** (Unity Asset Store ID 178169)
- Simple audio files may be used if included; all other assets are original

---

## Main folders

```
TheLastShabti/
├── Blender/
│   ├── Scripts/         Blender Python scripts to generate all assets
│   └── Exports/         FBX files exported from Blender
├── UnityProject/
│   └── Assets/
│       ├── Art/Models/      Imported FBX models
│       ├── Art/Materials/   Unity materials (MAT_Sandstone etc.)
│       ├── Prefabs/         Prefabs for each asset type
│       ├── Scenes/          Main scene: LVL_MainPyramid
│       ├── Scripts/         Custom C# scripts
│       └── Audio/           Sound effects (if used)
├── Documentation/
│   ├── Map/             2D level map (SVG and PNG)
│   └── Screenshots/     Gameplay screenshots for submission
└── Build/               Final PC build (not committed to Git)
```

---

## Generating Blender assets

1. Open Blender
2. Go to the **Scripting** workspace
3. Open `Blender/Scripts/01_create_nebu.py` and click **Run Script**
4. Open `Blender/Scripts/02_create_env_assets.py` and click **Run Script**
5. Edit the `EXPORT_PATH` variable in `03_export_fbx.py` to match your project path
6. Run `03_export_fbx.py` — FBX files will appear in `Blender/Exports/`
7. Drag the FBX files into Unity's `Assets/Art/Models/` folder

---

## Known limitations

- Nebu does not have skeletal animation — the character uses the Obstacle Course Pack controller without custom animations
- The level currently has no enemy AI or combat — this is intentional (brief scope)
- Audio is minimal or absent in the first playable version
- Some collider edges on ramp pieces may need manual adjustment in Unity Inspector

---

## Links

- GitHub: [ADD LINK]
- Unity Build: [ADD LINK — upload build separately, not to Git]
- Blender file: [ADD LINK — Google Drive or similar]
