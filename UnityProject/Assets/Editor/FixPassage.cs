using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;

public static class FixPassage
{
    [MenuItem("TheLastShabti/Fix Passages")]
    public static void Run()
    {
        var scene = EditorSceneManager.OpenScene(
            "Assets/Scenes/LVL_MainPyramid.unity", OpenSceneMode.Single);

        bool changed = false;

        var s2Plat1 = GameObject.Find("S2_Plat1");
        if (s2Plat1 != null)
        {
            s2Plat1.transform.position = new Vector3(16f, 1.7f, 0f);
            EditorUtility.SetDirty(s2Plat1);
            changed = true;
        }

        var safeFloor = GameObject.Find("S2_SafeFloor");
        if (safeFloor != null)
        {
            safeFloor.transform.position   = new Vector3(24f, 0.25f, 0f);
            safeFloor.transform.localScale = new Vector3(18f, 0.5f, 6f);
            EditorUtility.SetDirty(safeFloor);
            changed = true;
        }

        var floorMain = GameObject.Find("S2_Floor_Main");
        if (floorMain != null)
        {
            floorMain.transform.position   = new Vector3(27f, 0.7f, 0f);
            floorMain.transform.localScale = new Vector3(24f, 0.5f, 8f);
            EditorUtility.SetDirty(floorMain);
            changed = true;
        }

        var wallL = GameObject.Find("S2_WallL");
        if (wallL != null)
        {
            wallL.transform.position   = new Vector3(27f, 4.5f, -5f);
            wallL.transform.localScale = new Vector3(24f, 9f, 0.5f);
            EditorUtility.SetDirty(wallL);
            changed = true;
        }

        var wallR = GameObject.Find("S2_WallR");
        if (wallR != null)
        {
            wallR.transform.position   = new Vector3(27f, 4.5f, 5f);
            wallR.transform.localScale = new Vector3(24f, 9f, 0.5f);
            EditorUtility.SetDirty(wallR);
            changed = true;
        }

        var ceiling = GameObject.Find("S2_Ceiling");
        if (ceiling != null)
        {
            ceiling.transform.position   = new Vector3(27f, 8f, 0f);
            ceiling.transform.localScale = new Vector3(24f, 0.5f, 10f);
            EditorUtility.SetDirty(ceiling);
            changed = true;
        }

        // los arcos son solo decoracion, sus colliders dan problemas
        var allGOs = Object.FindObjectsByType<GameObject>(
            FindObjectsInactive.Include, FindObjectsSortMode.None);
        foreach (var go in allGOs)
        {
            if (go.name != "ENV_Archway") continue;
            var bc = go.GetComponent<BoxCollider>();
            if (bc != null && bc.enabled)
            {
                bc.enabled = false;
                EditorUtility.SetDirty(go);
                changed = true;
            }
        }

        // S4_WallBk bloqueaba la entrada al shaft, lo movi fuera del nivel
        var wallBk = GameObject.Find("S4_WallBk");
        if (wallBk != null)
        {
            wallBk.transform.position = new Vector3(80f, 14f, 0f);
            EditorUtility.SetDirty(wallBk);
            changed = true;
        }

        var s4Entry = GameObject.Find("S4_Entry");
        if (s4Entry != null)
        {
            s4Entry.transform.position = new Vector3(59f, 7.5f, 0f);
            EditorUtility.SetDirty(s4Entry);
            changed = true;
        }

        var s3Ceil = GameObject.Find("S3_Ceiling");
        if (s3Ceil != null)
        {
            s3Ceil.transform.position   = new Vector3(46.5f, 14.0f, 0f);
            s3Ceil.transform.localScale = new Vector3(19f, 0.5f, 10f);
            EditorUtility.SetDirty(s3Ceil);
            changed = true;
        }

        // el bloque estaba configurado para moverse en X, lo cambie a Y para que caiga
        var fallBlock = GameObject.Find("OBS_FallingBlock");
        if (fallBlock != null)
        {
            var obs = fallBlock.GetComponent<MovableObs>();
            if (obs != null) Object.DestroyImmediate(obs);

            fallBlock.transform.position = new Vector3(52f, 10.0f, 0f);
            EditorUtility.SetDirty(fallBlock);

            var mp = fallBlock.AddComponent<MovingPlatform>();
            var smp = new SerializedObject(mp);
            smp.FindProperty("moveAxis").enumValueIndex = 1;
            smp.FindProperty("moveDistance").floatValue = 1.5f;
            smp.FindProperty("speed").floatValue = 0.8f;
            smp.ApplyModifiedProperties();
            changed = true;
        }

        var roofSurface = GameObject.Find("S5_RoofSurface");
        if (roofSurface != null)
        {
            roofSurface.transform.position   = new Vector3(71.5f, 21f, 0f);
            roofSurface.transform.localScale = new Vector3(15f, 0.5f, 14f);
            EditorUtility.SetDirty(roofSurface);
            changed = true;
        }

        if (changed)
        {
            EditorSceneManager.MarkSceneDirty(scene);
            EditorSceneManager.SaveScene(scene);
        }
    }
}
