using System.Collections.Generic;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;
using UnityEngine.Rendering;

public static class FixMaterials
{
    [MenuItem("TheLastShabti/Fix Materials & Lighting")]
    public static void Run()
    {
        Shader urpLit = Shader.Find("Universal Render Pipeline/Lit");
        if (urpLit == null)
        {
            Debug.LogError("[FixMaterials] URP Lit shader not found. Is URP installed?");
            return;
        }

        // ── 1. Upgrade OCP materials from Standard → URP Lit ─────────────────
        UpgradeOCPMaterials(urpLit);

        // ── 2. Ensure custom level materials have correct _BaseColor ──────────
        EnsureLevelMaterialColors(urpLit);

        // ── 3. Open scene and fix lighting + WinPanel + KillPlane ─────────────
        FixScene();

        AssetDatabase.SaveAssets();
        AssetDatabase.Refresh();
        Debug.Log("[FixMaterials] Done. Press Ctrl+S then Play to test.");
    }

    // ─────────────────────────────────────────────────────────────────────────
    static void UpgradeOCPMaterials(Shader urpLit)
    {
        string[] guids = AssetDatabase.FindAssets("t:Material",
            new[] { "Assets/ObstacleCoursePack/Materials" });

        foreach (string guid in guids)
        {
            string path = AssetDatabase.GUIDToAssetPath(guid);
            Material mat = AssetDatabase.LoadAssetAtPath<Material>(path);
            if (mat == null) continue;

            bool isStandard = mat.shader.name == "Standard"
                           || mat.shader.name.StartsWith("Legacy Shaders/");
            if (!isStandard) continue;

            // Preserve the original albedo before changing shader
            Color originalColor = mat.HasProperty("_Color")
                ? mat.GetColor("_Color")
                : Color.white;

            mat.shader = urpLit;
            mat.SetColor("_BaseColor", originalColor);
            mat.SetFloat("_Smoothness", 0.3f);
            mat.SetFloat("_Metallic", 0f);
            EditorUtility.SetDirty(mat);
            Debug.Log($"[FixMaterials] Upgraded OCP material '{mat.name}' to URP Lit  color={originalColor}");
        }
    }

    // ─────────────────────────────────────────────────────────────────────────
    static readonly Dictionary<string, Color> LevelMatColors = new()
    {
        { "MAT_Sandstone",  new Color(0.76f, 0.62f, 0.39f) },
        { "MAT_StoneBlue",  new Color(0.44f, 0.54f, 0.62f) },
        { "MAT_TombBlue",   new Color(0.16f, 0.22f, 0.36f) },
        { "MAT_DarkBrown",  new Color(0.15f, 0.08f, 0.04f) },
        { "MAT_Turquoise",  new Color(0.28f, 0.55f, 0.52f) },
        { "MAT_GoldAccent", new Color(0.78f, 0.65f, 0.18f) },
        { "MAT_Clay",       new Color(0.55f, 0.38f, 0.28f) },
        { "MAT_TorchFire",  new Color(0.90f, 0.55f, 0.08f) },
        { "MAT_Obstacle",   new Color(0.70f, 0.20f, 0.15f) },
        { "MAT_Player",     new Color(0.28f, 0.55f, 0.52f) },
    };

    static void EnsureLevelMaterialColors(Shader urpLit)
    {
        string[] guids = AssetDatabase.FindAssets("t:Material",
            new[] { "Assets/Art/Materials" });

        foreach (string guid in guids)
        {
            string path = AssetDatabase.GUIDToAssetPath(guid);
            Material mat = AssetDatabase.LoadAssetAtPath<Material>(path);
            if (mat == null) continue;

            if (mat.shader != urpLit)
            {
                mat.shader = urpLit;
                Debug.Log($"[FixMaterials] Re-assigned URP Lit to '{mat.name}'");
            }

            if (LevelMatColors.TryGetValue(mat.name, out Color c))
            {
                mat.SetColor("_BaseColor", c);
                mat.SetColor("_Color", c);
                EditorUtility.SetDirty(mat);
            }
        }
    }

    // ─────────────────────────────────────────────────────────────────────────
    static void FixScene()
    {
        var scene = EditorSceneManager.OpenScene(
            "Assets/Scenes/LVL_MainPyramid.unity", OpenSceneMode.Single);

        // ── Ambient lighting: raise from nearly-black dark-blue to warm dim ──
        RenderSettings.ambientMode = AmbientMode.Flat;
        RenderSettings.ambientLight = new Color(0.35f, 0.30f, 0.22f);  // warm dim
        Debug.Log("[FixMaterials] Ambient light raised to warm dim (0.35, 0.30, 0.22).");

        // ── Directional light: neutralise the heavy blue tint ────────────────
        var lights = Object.FindObjectsByType<Light>(FindObjectsSortMode.None);
        foreach (var l in lights)
        {
            if (l.type == LightType.Directional && l.gameObject.name == "Light_TombDir")
            {
                l.color = new Color(0.75f, 0.80f, 0.85f);  // cool white, not blue
                l.intensity = 1.2f;
                Debug.Log("[FixMaterials] Light_TombDir neutralised.");
            }
        }

        // ── WinPanel: ensure it's deactivated at start ───────────────────────
        var allObjects = Object.FindObjectsByType<GameObject>(
            FindObjectsInactive.Include, FindObjectsSortMode.None);
        foreach (var go in allObjects)
        {
            if (go.name == "WinPanel" && go.activeSelf)
            {
                go.SetActive(false);
                Debug.Log("[FixMaterials] Deactivated WinPanel.");
            }
        }

        // ── KillPlane: ensure MeshRenderer is disabled ───────────────────────
        var killPlane = GameObject.Find("KillPlane");
        if (killPlane != null)
        {
            var mr = killPlane.GetComponent<MeshRenderer>();
            if (mr != null && mr.enabled)
            {
                mr.enabled = false;
                Debug.Log("[FixMaterials] Disabled KillPlane MeshRenderer.");
            }
        }

        // ── OCP Player: assign custom turquoise material ──────────────────────
        AssignMATPlayerToOCPPlayer();

        // ── Place CHAR_Nebu as a shabtī statue at the Sun Altar ──────────────
        PlaceNebuStatue();

        EditorSceneManager.MarkSceneDirty(scene);
        EditorSceneManager.SaveScene(scene);
    }

    static void AssignMATPlayerToOCPPlayer()
    {
        Material matPlayer = AssetDatabase.LoadAssetAtPath<Material>(
            "Assets/Art/Materials/MAT_Player.mat");
        if (matPlayer == null) return;

        GameObject player = GameObject.Find("Player");
        if (player == null) return;

        foreach (var r in player.GetComponentsInChildren<MeshRenderer>())
        {
            var mats = new Material[r.sharedMaterials.Length];
            for (int i = 0; i < mats.Length; i++) mats[i] = matPlayer;
            r.sharedMaterials = mats;
        }
        Debug.Log("[FixMaterials] MAT_Player assigned to OCP player capsule.");
    }

    static void PlaceNebuStatue()
    {
        GameObject nebuFBX = AssetDatabase.LoadAssetAtPath<GameObject>(
            "Assets/Art/Models/CHAR_Nebu.fbx");
        if (nebuFBX == null)
        {
            Debug.LogWarning("[FixMaterials] CHAR_Nebu.fbx not found — run Assets > Refresh first.");
            return;
        }

        // Remove duplicates if script is re-run
        var existing = GameObject.Find("CHAR_Nebu_Statue");
        if (existing != null) Object.DestroyImmediate(existing);

        // S5_AltarBase is at (72, 23.5, 0) — place statue beside the altar
        GameObject statue = (GameObject)PrefabUtility.InstantiatePrefab(nebuFBX);
        statue.name = "CHAR_Nebu_Statue";
        statue.transform.position = new Vector3(70f, 24.0f, 2.5f);
        statue.transform.rotation = Quaternion.Euler(0f, -30f, 0f);

        // escala ajustada para que quede aprox 1.65m de alto
        statue.transform.localScale = Vector3.one * 0.018f;

        // Add a collider so the player can walk around it
        var bc = statue.AddComponent<BoxCollider>();
        bc.center = new Vector3(0f, 50f, 0f);   // approximate centre in FBX local units
        bc.size   = new Vector3(30f, 100f, 30f);

        statue.isStatic = true;
        Debug.Log("[FixMaterials] CHAR_Nebu placed as statue at Sun Altar (72, 24, 2.5).");
    }
}
