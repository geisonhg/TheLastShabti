// LevelBuilder.cs - construye el nivel completo desde el Editor de Unity
// Menú: TheLastShabti > Build Full Level
// También funciona en batch mode: Unity.exe -batchmode -executeMethod LevelBuilder.BuildAll

using System.Collections.Generic;
using System.IO;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;
using UnityEngine.Rendering;
using UnityEngine.SceneManagement;

public class LevelBuilder
{
    // paleta de colores - tiene que coincidir con los materiales de Blender
    static Color C_Sand    = new Color(0.76f, 0.62f, 0.39f);
    static Color C_Stone   = new Color(0.44f, 0.54f, 0.62f);
    static Color C_Turq    = new Color(0.28f, 0.55f, 0.52f);
    static Color C_Gold    = new Color(0.78f, 0.65f, 0.18f);
    static Color C_Dark    = new Color(0.15f, 0.08f, 0.04f);
    static Color C_Fire    = new Color(0.90f, 0.55f, 0.08f);
    static Color C_Clay    = new Color(0.55f, 0.38f, 0.28f);
    static Color C_Blue    = new Color(0.16f, 0.22f, 0.36f);
    static Color C_WarmOrange = new Color(0.78f, 0.42f, 0.08f);

    [MenuItem("TheLastShabti/Build Full Level")]
    public static void BuildAll()
    {
        Debug.Log("=== LevelBuilder.BuildAll starting ===");

        CreateMaterials();
        Scene scene = CreateScene();
        PopulateScene(scene);
        AddBuildSettings();
        AssetDatabase.SaveAssets();
        AssetDatabase.Refresh();
        EditorSceneManager.SaveScene(scene);

        Debug.Log("=== LevelBuilder.BuildAll complete ===");
    }

    static Dictionary<string, Material> mats = new Dictionary<string, Material>();

    static void CreateMaterials()
    {
        string dir = "Assets/Art/Materials";
        Directory.CreateDirectory(Application.dataPath + "/Art/Materials");

        mats["Sand"]  = MakeMat(dir + "/MAT_Sandstone.mat",   C_Sand,       0.85f, 0f);
        mats["Stone"] = MakeMat(dir + "/MAT_StoneBlue.mat",   C_Stone,      0.90f, 0f);
        mats["Turq"]  = MakeMat(dir + "/MAT_Turquoise.mat",   C_Turq,       0.70f, 0f);
        mats["Gold"]  = MakeMat(dir + "/MAT_GoldAccent.mat",  C_Gold,       0.25f, 0.75f);
        mats["Dark"]  = MakeMat(dir + "/MAT_DarkBrown.mat",   C_Dark,       0.92f, 0f);
        mats["Clay"]  = MakeMat(dir + "/MAT_Clay.mat",        C_Clay,       0.92f, 0f);
        mats["Fire"]  = MakeMat(dir + "/MAT_TorchFire.mat",   C_Fire,       0.20f, 0f);
        mats["Blue"]  = MakeMat(dir + "/MAT_TombBlue.mat",    C_Blue,       0.92f, 0f);
        mats["Obs"]   = MakeMat(dir + "/MAT_Obstacle.mat",    new Color(0.7f, 0.2f, 0.15f), 0.7f, 0f);
        mats["Player"]= MakeMat(dir + "/MAT_Player.mat",      C_Turq,       0.80f, 0f);

        Debug.Log("Materials created: " + mats.Count);
    }

    static Material MakeMat(string assetPath, Color col, float roughness, float metallic)
    {
        Material mat = AssetDatabase.LoadAssetAtPath<Material>(assetPath);
        if (mat == null)
        {
            mat = new Material(Shader.Find("Universal Render Pipeline/Lit"));
            if (mat.shader == null || mat.shader.name == "Hidden/InternalErrorShader")
                mat = new Material(Shader.Find("Standard"));
            AssetDatabase.CreateAsset(mat, assetPath);
        }
        mat.color = col;
        if (mat.HasProperty("_Smoothness"))
            mat.SetFloat("_Smoothness", 1f - roughness);
        if (mat.HasProperty("_Metallic"))
            mat.SetFloat("_Metallic", metallic);
        EditorUtility.SetDirty(mat);
        return mat;
    }

    static Scene CreateScene()
    {
        string scenePath = "Assets/Scenes/LVL_MainPyramid.unity";
        Directory.CreateDirectory(Application.dataPath + "/Scenes");

        Scene scene = EditorSceneManager.NewScene(NewSceneSetup.DefaultGameObjects, NewSceneMode.Single);
        EditorSceneManager.SaveScene(scene, scenePath);
        Debug.Log("Scene created: " + scenePath);
        return scene;
    }

    static void PopulateScene(Scene scene)
    {
        // quitar la luz direccional que viene por defecto con NewScene
        foreach (var go in Object.FindObjectsByType<Light>(FindObjectsSortMode.None))
            if (go.type == LightType.Directional)
                Object.DestroyImmediate(go.gameObject);

        GameObject envRoot   = NewEmpty("Environment");
        GameObject obsRoot   = NewEmpty("Obstacles");
        GameObject cpRoot    = NewEmpty("Checkpoints");
        GameObject lightRoot = NewEmpty("Lighting");
        GameObject goalRoot  = NewEmpty("Goal");
        GameObject uiRoot    = NewEmpty("UI");
        GameObject audioRoot = NewEmpty("Audio");

        BuildPlayer();

        BuildSection1(envRoot);
        BuildSection2(envRoot);
        BuildSection3(envRoot, obsRoot);
        BuildSection4(envRoot, obsRoot, cpRoot);
        BuildSection5(envRoot, goalRoot);

        BuildLighting(lightRoot);
        BuildKillPlane();
        BuildUI(uiRoot);

        Debug.Log("Scene populated.");
    }

    static void BuildPlayer()
    {
        GameObject camRig = new GameObject("CameraRig");
        camRig.transform.position = new Vector3(0f, 4f, -6f);
        CameraRig cr = camRig.AddComponent<CameraRig>();

        GameObject camGO = new GameObject("Main Camera");
        camGO.transform.SetParent(camRig.transform);
        camGO.transform.localPosition = Vector3.zero;
        camGO.transform.localRotation = Quaternion.Euler(15f, 0f, 0f);
        Camera cam = camGO.AddComponent<Camera>();
        cam.fieldOfView = 65f;
        cam.nearClipPlane = 0.1f;
        camGO.AddComponent<AudioListener>();
        camGO.tag = "MainCamera";

        GameObject player = GameObject.CreatePrimitive(PrimitiveType.Capsule);
        player.name = "Player";
        player.tag = "Player";
        player.transform.position = new Vector3(0f, 1.2f, 0f);
        player.transform.localScale = new Vector3(0.7f, 0.85f, 0.7f);
        SetMat(player, "Player");

        CharacterController cc = player.GetComponent<Collider>() as CharacterController;
        if (cc == null)
        {
            Object.DestroyImmediate(player.GetComponent<CapsuleCollider>());
            cc = player.AddComponent<CharacterController>();
        }
        cc.height = 1.7f;
        cc.radius = 0.35f;
        cc.center = new Vector3(0f, 0f, 0f);
        cc.slopeLimit = 45f;
        cc.stepOffset = 0.3f;

        PlayerController pc = player.AddComponent<PlayerController>();
        SerializedObject so = new SerializedObject(pc);
        so.FindProperty("cameraRig").objectReferenceValue = camRig.transform;
        so.ApplyModifiedProperties();

        PlayerRespawn pr = player.AddComponent<PlayerRespawn>();
        SerializedObject sr = new SerializedObject(pr);
        sr.FindProperty("killPlaneY").floatValue = -8f;
        sr.FindProperty("levelStartPos").vector3Value = new Vector3(0f, 1.2f, 0f);
        sr.ApplyModifiedProperties();

        GameObject cpMgr = new GameObject("CheckpointManager");
        cpMgr.AddComponent<CheckpointManager>();

        SerializedObject sc = new SerializedObject(cr);
        sc.FindProperty("target").objectReferenceValue = player.transform;
        sc.FindProperty("followDistance").floatValue = 6f;
        sc.FindProperty("followHeight").floatValue = 3.5f;
        sc.ApplyModifiedProperties();
    }

    // S1 - Cámara sepulcral, dos saltos fáciles + escalera
    static void BuildSection1(GameObject envRoot)
    {
        GameObject s1 = NewEmpty("S1_BurialChamber", envRoot.transform);

        MakeFloor(s1, "S1_Floor",    new Vector3(8f,  -0.25f, 0f), new Vector3(18f, 0.5f, 8f),   "Sand");
        MakeWall( s1, "S1_WallBack", new Vector3(-1f, 3f, 0f), new Vector3(0.5f, 7f, 10f), "Blue");
        MakeWall( s1, "S1_WallL",    new Vector3(8f,  3f, -4.5f), new Vector3(18f, 7f, 0.5f), "Blue");
        MakeWall( s1, "S1_WallR",    new Vector3(8f,  3f,  4.5f), new Vector3(18f, 7f, 0.5f), "Blue");
        MakeWall( s1, "S1_Ceiling",  new Vector3(8f,  6.5f, 0f), new Vector3(18f, 0.5f, 10f), "Dark");

        MakePlatform(s1, "S1_StartPlatform", new Vector3(0f, 0.35f, 0f), new Vector3(3f, 0.3f, 3f), "Sand");
        MakePlatform(s1, "S1_Jump1", new Vector3(5f, 0.8f, 0f), new Vector3(2.5f, 0.3f, 2.5f), "Sand");
        MakePlatform(s1, "S1_Jump2", new Vector3(9f, 1.4f, 0f), new Vector3(2.5f, 0.3f, 2.5f), "Sand");

        for (int i = 0; i < 4; i++)
        {
            MakePlatform(s1, $"S1_Step{i}",
                new Vector3(11f + i * 0.55f, 0.25f + i * 0.35f, 0f),
                new Vector3(1.5f, 0.35f, 2.5f), "Sand");
        }

        MakePlatform(s1, "S1_Landing", new Vector3(14f, 1.7f, 0f), new Vector3(3f, 0.3f, 3f), "Sand");

        PlaceProp(s1, "PROP_BurialJar", new Vector3(-0.5f, 0.3f, -2.5f), Vector3.one * 0.9f);
        PlaceProp(s1, "PROP_BurialJar", new Vector3(-0.5f, 0.3f, -3.3f), Vector3.one * 0.7f);
        PlaceProp(s1, "PROP_BurialJar", new Vector3(-0.5f, 0.3f,  2.5f), Vector3.one * 0.85f);
        PlaceProp(s1, "PROP_WallTorch", new Vector3(-0.7f, 1.5f, -1.5f),
                  Vector3.one * 0.6f, Quaternion.Euler(0, 90, 0));
        PlaceProp(s1, "PROP_WallTorch", new Vector3(-0.7f, 1.5f,  1.5f),
                  Vector3.one * 0.6f, Quaternion.Euler(0, 90, 0));
        PlaceProp(s1, "PROP_ScarabWall", new Vector3(-0.8f, 1.8f, 0f),
                  Vector3.one * 0.8f, Quaternion.Euler(0, 90, 0));
        PlaceProp(s1, "ENV_Archway", new Vector3(15.8f, 0f, 0f), Vector3.one,
                  Quaternion.Euler(0, 0, 0));
    }

    // S2 - Galería derrumbada, plataformas rotas, columnas caídas
    static void BuildSection2(GameObject envRoot)
    {
        GameObject s2 = NewEmpty("S2_CollapsedGallery", envRoot.transform);

        MakeWall(s2, "S2_Floor_Main", new Vector3(28f, 0.7f, 0f), new Vector3(22f, 0.5f, 8f), "Blue");
        MakeWall(s2, "S2_Ceiling",    new Vector3(28f, 8f,  0f), new Vector3(22f, 0.5f, 10f), "Dark");
        MakeWall(s2, "S2_WallL",      new Vector3(28f, 4.5f, -5f), new Vector3(22f, 9f, 0.5f), "Blue");
        MakeWall(s2, "S2_WallR",      new Vector3(28f, 4.5f,  5f), new Vector3(22f, 9f, 0.5f), "Blue");

        MakePlatform(s2, "S2_SafeFloor", new Vector3(26f, 0.25f, 0f), new Vector3(14f, 0.5f, 6f), "Stone");
        MakePlatform(s2, "S2_Plat1", new Vector3(18f, 2.2f, 0f), new Vector3(3f, 0.3f, 3f), "Sand");
        MakePlatform(s2, "S2_Plat2", new Vector3(22f, 2.8f, 0f), new Vector3(2.5f, 0.3f, 2.5f), "Sand");
        MakePlatform(s2, "S2_Plat3", new Vector3(26f, 3.4f, 0f), new Vector3(2.5f, 0.3f, 2.5f), "Sand");

        PlaceRamp(s2, "S2_Ramp", new Vector3(29.5f, 2.1f, 0f), new Vector3(2f, 1.5f, 3f));

        MakePlatform(s2, "S2_PostRamp", new Vector3(32f, 3.7f, 0f), new Vector3(3f, 0.3f, 3f), "Sand");
        MakePlatform(s2, "S2_Landing", new Vector3(36f, 4.3f, 0f), new Vector3(3f, 0.3f, 3f), "Sand");

        PlaceProp(s2, "PROP_BrokenColumn", new Vector3(20f, 1.2f, -1.5f),
                  Vector3.one, Quaternion.Euler(90, 25, 0));
        PlaceProp(s2, "PROP_BrokenColumn", new Vector3(25f, 1.0f, 2f),
                  Vector3.one, Quaternion.Euler(90, -15, 0));
        PlaceProp(s2, "ENV_Archway", new Vector3(37.5f, 0f, 0f), Vector3.one);
    }

    // S3 - Sala de las Pesas: plataforma móvil, peligro rotatorio, bloque que cae
    static void BuildSection3(GameObject envRoot, GameObject obsRoot)
    {
        GameObject s3 = NewEmpty("S3_HallOfWeights", envRoot.transform);

        MakeFloor(s3, "S3_Floor",   new Vector3(48f, 4.0f, 0f), new Vector3(22f, 0.5f, 8f), "Stone");
        MakeWall( s3, "S3_WallL",   new Vector3(48f, 7f, -5f), new Vector3(22f, 7f, 0.5f), "Blue");
        MakeWall( s3, "S3_WallR",   new Vector3(48f, 7f,  5f), new Vector3(22f, 7f, 0.5f), "Blue");
        MakeWall( s3, "S3_Ceiling", new Vector3(48f, 10.5f, 0f), new Vector3(22f, 0.5f, 10f), "Dark");

        MakePlatform(s3, "S3_Entry",   new Vector3(40f, 5.2f, 0f), new Vector3(3f, 0.3f, 3f), "Sand");
        MakePlatform(s3, "S3_StaticA", new Vector3(44f, 5.8f, 0f), new Vector3(2.5f, 0.3f, 2.5f), "Sand");

        GameObject movPlat = MakePlatform(s3, "S3_MovingPlatform",
                                           new Vector3(48f, 6.4f, 0f),
                                           new Vector3(2.5f, 0.3f, 2.5f), "Stone");
        MovingPlatform mp = movPlat.AddComponent<MovingPlatform>();
        SerializedObject smp = new SerializedObject(mp);
        smp.FindProperty("moveAxis").enumValueIndex = 0;   // eje X
        smp.FindProperty("moveDistance").floatValue = 2.5f;
        smp.FindProperty("speed").floatValue = 1.2f;
        smp.ApplyModifiedProperties();
        movPlat.transform.SetParent(obsRoot.transform);
        movPlat.transform.SetParent(s3.transform);

        MakePlatform(s3, "S3_StaticB", new Vector3(52f, 7.0f, 0f), new Vector3(2.5f, 0.3f, 2.5f), "Sand");

        GameObject hazard = MakePlatform(obsRoot, "OBS_RotatingHazard",
                                          new Vector3(46f, 6.0f, 0f),
                                          new Vector3(5f, 0.25f, 0.5f), "Obs");
        hazard.AddComponent<RotatingHazard>();
        SerializedObject srh = new SerializedObject(hazard.GetComponent<RotatingHazard>());
        srh.FindProperty("degreesPerSecond").floatValue = 65f;
        srh.ApplyModifiedProperties();
        hazard.transform.SetParent(s3.transform);

        // bloque que cae: usa MovingPlatform en Y para simular la caída
        GameObject fallBlock = MakePlatform(obsRoot, "OBS_FallingBlock",
                                             new Vector3(52f, 9.0f, 0f),
                                             new Vector3(2f, 0.5f, 2f), "Obs");
        MovingPlatform fb = fallBlock.AddComponent<MovingPlatform>();
        SerializedObject sfb = new SerializedObject(fb);
        sfb.FindProperty("moveAxis").enumValueIndex = 1;   // eje Y
        sfb.FindProperty("moveDistance").floatValue = 1.5f;
        sfb.FindProperty("speed").floatValue = 0.8f;
        sfb.ApplyModifiedProperties();
        fallBlock.transform.SetParent(s3.transform);

        MakePlatform(s3, "S3_Exit", new Vector3(56f, 7.5f, 0f), new Vector3(3f, 0.3f, 3f), "Sand");
        PlaceProp(s3, "ENV_Archway", new Vector3(57.5f, 4f, 0f), Vector3.one,
                  Quaternion.Euler(0, 0, 0));
    }

    // S4 - Pozo de Ra: zigzag vertical con plataforma móvil y checkpoint
    static void BuildSection4(GameObject envRoot, GameObject obsRoot, GameObject cpRoot)
    {
        GameObject s4 = NewEmpty("S4_ShaftOfRa", envRoot.transform);

        MakeWall(s4, "S4_WallL",  new Vector3(62f, 14f, -3.5f), new Vector3(8f, 30f, 0.5f), "Stone");
        MakeWall(s4, "S4_WallR",  new Vector3(62f, 14f,  3.5f), new Vector3(8f, 30f, 0.5f), "Stone");
        MakeWall(s4, "S4_WallBk", new Vector3(58f, 14f,  0f),   new Vector3(0.5f, 30f, 7f), "Stone");

        MakePlatform(s4, "S4_Entry", new Vector3(59f, 8.0f, 0f), new Vector3(3f, 0.3f, 3f), "Sand");

        Vector3[] platPositions =
        {
            new Vector3(63f, 9.8f,  1.5f),
            new Vector3(60f, 11.6f, -1.5f),
            new Vector3(63f, 13.4f,  1.5f),
            new Vector3(60f, 15.2f, -1.5f),
            new Vector3(63f, 17.0f,  1.5f),
            new Vector3(60f, 18.8f, -1.0f),
            new Vector3(62f, 20.6f,  0f),
        };
        for (int i = 0; i < platPositions.Length; i++)
        {
            MakePlatform(s4, $"S4_Plat{i}", platPositions[i],
                         new Vector3(2.5f, 0.3f, 2.5f), "Sand");
        }

        // plataforma que sube y baja a mitad del pozo
        GameObject vMovePlat = MakePlatform(s4, "S4_MovingPlatform",
                                             new Vector3(62f, 14.0f, 0f),
                                             new Vector3(2.5f, 0.3f, 2.5f), "Stone");
        MovingPlatform vmp = vMovePlat.AddComponent<MovingPlatform>();
        SerializedObject svmp = new SerializedObject(vmp);
        svmp.FindProperty("moveAxis").enumValueIndex = 1;   // eje Y
        svmp.FindProperty("moveDistance").floatValue = 1.5f;
        svmp.FindProperty("speed").floatValue = 1.0f;
        svmp.ApplyModifiedProperties();

        // checkpoint en la entrada del pozo
        GameObject cp = new GameObject("CP_ShaftEntry");
        cp.transform.SetParent(cpRoot.transform);
        cp.transform.position = new Vector3(59f, 9.5f, 0f);
        BoxCollider cpCol = cp.AddComponent<BoxCollider>();
        cpCol.isTrigger = true;
        cpCol.size = new Vector3(3f, 2f, 3f);
        cp.AddComponent<CheckpointZone>();

        // marcador visual del checkpoint
        GameObject cpMarker = GameObject.CreatePrimitive(PrimitiveType.Sphere);
        cpMarker.name = "CP_Marker";
        cpMarker.transform.SetParent(cp.transform);
        cpMarker.transform.localPosition = new Vector3(0f, 0.5f, 0f);
        cpMarker.transform.localScale = Vector3.one * 0.4f;
        SetMat(cpMarker, "Gold");
        Object.DestroyImmediate(cpMarker.GetComponent<Collider>());

        // luz cálida desde arriba del pozo
        GameObject shaftLight = new GameObject("Light_ShaftWarm");
        shaftLight.transform.SetParent(s4.transform);
        shaftLight.transform.position = new Vector3(62f, 22f, 0f);
        Light sl = shaftLight.AddComponent<Light>();
        sl.type = LightType.Spot;
        sl.spotAngle = 60f;
        sl.range = 20f;
        sl.intensity = 6f;
        sl.color = new Color(1.0f, 0.75f, 0.4f);
        sl.transform.rotation = Quaternion.Euler(90f, 0f, 0f);
    }

    // S5 - Tejado con el Altar Solar (la meta del juego)
    static void BuildSection5(GameObject envRoot, GameObject goalRoot)
    {
        GameObject s5 = NewEmpty("S5_RooftopAltarSection", envRoot.transform);

        MakeFloor(s5, "S5_RoofSurface", new Vector3(66f, 21.0f, 0f), new Vector3(26f, 0.5f, 14f), "Sand");

        MakePlatform(s5, "S5_Jump1", new Vector3(60f, 21.8f, 0f), new Vector3(2.5f, 0.3f, 2.5f), "Sand");
        MakePlatform(s5, "S5_Jump2", new Vector3(64f, 22.5f, 0f), new Vector3(2.5f, 0.3f, 2.5f), "Sand");
        MakePlatform(s5, "S5_Jump3", new Vector3(68f, 23.0f, 0f), new Vector3(2.5f, 0.3f, 2.5f), "Sand");

        MakePlatform(s5, "S5_AltarBase", new Vector3(72f, 23.5f, 0f), new Vector3(4f, 0.5f, 4f), "Sand");

        PlaceProp(s5, "PROP_SunAltar", new Vector3(72f, 24.0f, 0f), Vector3.one);

        PlaceProp(s5, "PROP_Obelisk", new Vector3(58f, 21.5f, -3f), Vector3.one * 0.8f);
        PlaceProp(s5, "PROP_Obelisk", new Vector3(58f, 21.5f,  3f), Vector3.one * 0.8f);
        PlaceProp(s5, "PROP_Obelisk", new Vector3(73f, 24.0f, -3f), Vector3.one * 1.1f);
        PlaceProp(s5, "PROP_Obelisk", new Vector3(73f, 24.0f,  3f), Vector3.one * 1.1f);

        PlaceProp(s5, "PROP_BrokenColumn", new Vector3(62f, 21.5f, -3f), Vector3.one * 0.9f);
        PlaceProp(s5, "PROP_BrokenColumn", new Vector3(66f, 21.5f,  3f), Vector3.one * 0.8f);

        BuildGoal(goalRoot, new Vector3(72f, 25.5f, 0f));
    }

    static void BuildGoal(GameObject goalRoot, Vector3 pos)
    {
        GameObject trigger = new GameObject("Goal_SunAltarTrigger");
        trigger.transform.SetParent(goalRoot.transform);
        trigger.transform.position = pos;
        BoxCollider bc = trigger.AddComponent<BoxCollider>();
        bc.isTrigger = true;
        bc.size = new Vector3(4f, 3f, 4f);
        GoalTrigger gt = trigger.AddComponent<GoalTrigger>();
        Debug.Log("Goal trigger at " + pos);
    }

    static void BuildLighting(GameObject lightRoot)
    {
        RenderSettings.ambientMode = AmbientMode.Flat;
        RenderSettings.ambientLight = new Color(0.08f, 0.10f, 0.18f);

        // luz fría para las secciones interiores (S1-S2)
        AddDirLight(lightRoot, "Light_TombDir", new Vector3(0.4f, -0.5f, 0.3f),
                    new Color(0.4f, 0.5f, 0.8f), 0.8f);

        AddPointLight(lightRoot, "Light_Torch1", new Vector3(-0.5f, 2.2f, -1.5f), C_Fire, 5f, 3f);
        AddPointLight(lightRoot, "Light_Torch2", new Vector3(-0.5f, 2.2f,  1.5f), C_Fire, 5f, 3f);

        AddPointLight(lightRoot, "Light_HallFill", new Vector3(48f, 8f, 0f),
                      new Color(0.6f, 0.55f, 0.5f), 4f, 20f);

        // luz cálida para S5 (exterior)
        AddDirLight(lightRoot, "Light_SunExterior", new Vector3(0.6f, -0.5f, 0.2f),
                    new Color(1.0f, 0.75f, 0.4f), 2.0f);
        AddPointLight(lightRoot, "Light_AltarGlow", new Vector3(72f, 25f, 0f),
                      new Color(1.0f, 0.85f, 0.4f), 8f, 15f);
    }

    static void AddDirLight(GameObject root, string name, Vector3 dir, Color color, float intensity)
    {
        GameObject go = new GameObject(name);
        go.transform.SetParent(root.transform);
        go.transform.rotation = Quaternion.LookRotation(dir);
        Light l = go.AddComponent<Light>();
        l.type = LightType.Directional;
        l.color = color;
        l.intensity = intensity;
    }

    static void AddPointLight(GameObject root, string name, Vector3 pos, Color color,
                               float intensity, float range)
    {
        GameObject go = new GameObject(name);
        go.transform.SetParent(root.transform);
        go.transform.position = pos;
        Light l = go.AddComponent<Light>();
        l.type = LightType.Point;
        l.color = color;
        l.intensity = intensity;
        l.range = range;
    }

    static void BuildKillPlane()
    {
        GameObject kp = GameObject.CreatePrimitive(PrimitiveType.Cube);
        kp.name = "KillPlane";
        kp.transform.position = new Vector3(40f, -8f, 0f);
        kp.transform.localScale = new Vector3(200f, 0.5f, 200f);
        kp.GetComponent<Collider>().isTrigger = true;
        var mr = kp.GetComponent<MeshRenderer>();
        if (mr) mr.enabled = false;
        kp.isStatic = true;
    }

    static void BuildUI(GameObject uiRoot)
    {
        GameObject canvasGO = new GameObject("UI_Canvas");
        canvasGO.transform.SetParent(uiRoot.transform);
        Canvas canvas = canvasGO.AddComponent<Canvas>();
        canvas.renderMode = RenderMode.ScreenSpaceOverlay;
        canvasGO.AddComponent<UnityEngine.UI.CanvasScaler>();
        canvasGO.AddComponent<UnityEngine.UI.GraphicRaycaster>();

        GameObject titlePanel = new GameObject("TitlePanel");
        titlePanel.transform.SetParent(canvasGO.transform, false);
        UnityEngine.UI.Image titleBg = titlePanel.AddComponent<UnityEngine.UI.Image>();
        titleBg.color = new Color(0f, 0f, 0f, 0.7f);
        RectTransform trt = titlePanel.GetComponent<RectTransform>();
        trt.anchorMin = Vector2.zero;
        trt.anchorMax = Vector2.one;
        trt.offsetMin = Vector2.zero;
        trt.offsetMax = Vector2.zero;

        AddTextToPanel(titlePanel, "TitleText", "THE LAST SHABTI", 52,
                       new Vector2(0f, 60f), new Vector2(800f, 80f), new Color(0.9f, 0.75f, 0.3f));
        AddTextToPanel(titlePanel, "SubText", "WASD to Move   Space to Jump   Mouse to Look",
                       20, new Vector2(0f, -20f), new Vector2(700f, 40f), Color.white);
        AddTextToPanel(titlePanel, "StartText", "Press any key to start", 18,
                       new Vector2(0f, -70f), new Vector2(400f, 30f), new Color(0.7f, 0.9f, 0.7f));

        // panel de victoria, empieza desactivado
        GameObject winPanel = new GameObject("WinPanel");
        winPanel.transform.SetParent(canvasGO.transform, false);
        winPanel.SetActive(false);
        UnityEngine.UI.Image winBg = winPanel.AddComponent<UnityEngine.UI.Image>();
        winBg.color = new Color(0.05f, 0.02f, 0f, 0.85f);
        RectTransform wrt = winPanel.GetComponent<RectTransform>();
        wrt.anchorMin = new Vector2(0.2f, 0.3f);
        wrt.anchorMax = new Vector2(0.8f, 0.7f);
        wrt.offsetMin = Vector2.zero;
        wrt.offsetMax = Vector2.zero;

        AddTextToPanel(winPanel, "WinTitle", "THE SUN SEAL HAS BEEN RESTORED", 32,
                       new Vector2(0f, 40f), new Vector2(500f, 60f), new Color(0.9f, 0.75f, 0.3f));
        AddTextToPanel(winPanel, "WinSub", "Nebu's duty is complete.", 22,
                       new Vector2(0f, -20f), new Vector2(400f, 40f), Color.white);

        GoalTrigger gt = Object.FindFirstObjectByType<GoalTrigger>();
        if (gt != null)
        {
            SerializedObject sgt = new SerializedObject(gt);
            sgt.FindProperty("winPanel").objectReferenceValue = winPanel;
            sgt.ApplyModifiedProperties();
        }
    }

    static void AddTextToPanel(GameObject parent, string name, string text,
                                int fontSize, Vector2 anchoredPos, Vector2 sizeDelta,
                                Color color)
    {
        GameObject go = new GameObject(name);
        go.transform.SetParent(parent.transform, false);
        UnityEngine.UI.Text t = go.AddComponent<UnityEngine.UI.Text>();
        t.text = text;
        t.fontSize = fontSize;
        t.color = color;
        t.alignment = TextAnchor.MiddleCenter;
        t.font = Resources.GetBuiltinResource<Font>("LegacyRuntime.ttf");
        RectTransform rt = go.GetComponent<RectTransform>();
        rt.anchorMin = rt.anchorMax = new Vector2(0.5f, 0.5f);
        rt.anchoredPosition = anchoredPos;
        rt.sizeDelta = sizeDelta;
    }

    static void AddBuildSettings()
    {
        var scenes = new EditorBuildSettingsScene[]
        {
            new EditorBuildSettingsScene("Assets/Scenes/LVL_MainPyramid.unity", true)
        };
        EditorBuildSettings.scenes = scenes;
        Debug.Log("Build settings configured.");
    }

    static GameObject NewEmpty(string name, Transform parent = null)
    {
        GameObject go = new GameObject(name);
        if (parent != null) go.transform.SetParent(parent);
        return go;
    }

    static GameObject MakeFloor(GameObject parent, string name, Vector3 pos,
                                 Vector3 scale, string matKey)
    {
        return MakePrimitive(parent, name, pos, scale, matKey, true);
    }

    static void MakeWall(GameObject parent, string name, Vector3 pos,
                          Vector3 scale, string matKey)
    {
        MakePrimitive(parent, name, pos, scale, matKey, true);
    }

    static GameObject MakePlatform(GameObject parent, string name, Vector3 pos,
                                    Vector3 scale, string matKey, bool isStatic = true)
    {
        return MakePrimitive(parent, name, pos, scale, matKey, isStatic);
    }

    static GameObject MakePrimitive(GameObject parent, string name, Vector3 pos,
                                     Vector3 scale, string matKey, bool setStatic)
    {
        GameObject go = GameObject.CreatePrimitive(PrimitiveType.Cube);
        go.name = name;
        go.transform.SetParent(parent.transform);
        go.transform.position = pos;
        go.transform.localScale = scale;
        go.isStatic = setStatic;
        SetMat(go, matKey);
        return go;
    }

    static void PlaceRamp(GameObject parent, string name, Vector3 pos, Vector3 scale)
    {
        string rampPath = "Assets/Art/Models/ENV_Ramp.fbx";
        GameObject prefab = AssetDatabase.LoadAssetAtPath<GameObject>(rampPath);
        GameObject go;
        if (prefab != null)
        {
            go = PrefabUtility.InstantiatePrefab(prefab) as GameObject;
            go.name = name;
            go.transform.SetParent(parent.transform);
            go.transform.position = pos;
            go.transform.localScale = scale;
            AddBoxCollider(go);
        }
        else
        {
            // cubo rotado como fallback si no está el modelo
            go = GameObject.CreatePrimitive(PrimitiveType.Cube);
            go.name = name + "_Fallback";
            go.transform.SetParent(parent.transform);
            go.transform.position = pos;
            go.transform.localScale = scale;
            go.transform.rotation = Quaternion.Euler(22f, 0f, 0f);
            SetMat(go, "Sand");
        }
        go.isStatic = true;
    }

    static void PlaceProp(GameObject parent, string modelName, Vector3 pos,
                           Vector3 scale, Quaternion? rot = null)
    {
        string path = $"Assets/Art/Models/{modelName}.fbx";
        GameObject prefab = AssetDatabase.LoadAssetAtPath<GameObject>(path);
        if (prefab == null)
        {
            Debug.LogWarning($"Model not found: {path}");
            return;
        }
        GameObject go = PrefabUtility.InstantiatePrefab(prefab) as GameObject;
        go.name = modelName;
        go.transform.SetParent(parent.transform);
        go.transform.position = pos;
        go.transform.localScale = scale;
        if (rot.HasValue) go.transform.rotation = rot.Value;
        go.isStatic = true;
        AddBoxCollider(go);
    }

    static void SetMat(GameObject go, string matKey)
    {
        if (!mats.ContainsKey(matKey)) return;
        var renderers = go.GetComponentsInChildren<MeshRenderer>();
        foreach (var r in renderers)
        {
            Material[] newMats = new Material[r.sharedMaterials.Length];
            for (int i = 0; i < newMats.Length; i++)
                newMats[i] = mats[matKey];
            r.sharedMaterials = newMats;
        }
    }

    static void AddBoxCollider(GameObject go)
    {
        if (go.GetComponentInChildren<Collider>() == null)
        {
            BoxCollider bc = go.AddComponent<BoxCollider>();
            Renderer r = go.GetComponentInChildren<Renderer>();
            if (r != null)
            {
                bc.center = go.transform.InverseTransformPoint(r.bounds.center);
                bc.size   = r.bounds.size;
            }
        }
    }
}
