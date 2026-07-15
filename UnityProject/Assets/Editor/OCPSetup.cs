using UnityEngine;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine.Rendering.Universal;
using System.Linq;

/// <summary>
/// Replaces the custom player + camera with the Obstacle Course Pack equivalents
/// and rewires checkpoints / kill zone to use OCP scripts.
/// Run via  TheLastShabti > Setup OCP Player  or  -executeMethod OCPSetup.Run
/// </summary>
public static class OCPSetup
{
    const string SCENE     = "Assets/Scenes/LVL_MainPyramid.unity";
    const string OCP_ROOT  = "Assets/ObstacleCoursePack";

    [MenuItem("TheLastShabti/Setup OCP Player")]
    public static void Run()
    {
        // ── 1. Locate OCP prefabs ────────────────────────────────────────────
        string playerPrefabPath = OCP_ROOT + "/Controller/Player.prefab";
        string camPrefabPath    = OCP_ROOT + "/Controller/Camera Holder.prefab";

        if (AssetDatabase.LoadAssetAtPath<GameObject>(playerPrefabPath) == null ||
            AssetDatabase.LoadAssetAtPath<GameObject>(camPrefabPath) == null)
        {
            Debug.LogError("[OCPSetup] Cannot find OCP Player or Camera Holder prefab. " +
                           "Ensure ObstacleCoursePack is under Assets/ObstacleCoursePack/.");
            return;
        }

        // ── 2. Open scene ────────────────────────────────────────────────────
        var scene = EditorSceneManager.OpenScene(SCENE, OpenSceneMode.Single);

        // ── 3. Remove old Player & CameraRig ────────────────────────────────
        var oldPlayer = GameObject.Find("Player");
        var oldCamRig = GameObject.Find("CameraRig");

        // Spawn at the start of the level. S1_WallBack (removed below) used to block
        // the camera at this position — without it, the camera has unlimited back space.
        Vector3 spawnPos = new Vector3(0f, 2.0f, 0f);
        if (oldPlayer != null)
            GameObject.DestroyImmediate(oldPlayer);
        if (oldCamRig != null)
            GameObject.DestroyImmediate(oldCamRig);

        // Also remove the old CheckpointManager singleton if present
        var oldCpManager = GameObject.FindObjectOfType<CheckpointManager>();
        if (oldCpManager != null)
            GameObject.DestroyImmediate(oldCpManager.gameObject);

        // Remove any standalone Main Camera — the OCP Camera Holder has its own
        var standaloneCamera = GameObject.Find("Main Camera");
        if (standaloneCamera != null && standaloneCamera.transform.parent == null)
        {
            GameObject.DestroyImmediate(standaloneCamera);
            Debug.Log("[OCPSetup] Removed standalone Main Camera (OCP Camera Holder provides its own).");
        }

        // ── 3b. Remove S1_WallBack — it blocks the camera behind the spawn point ──
        var wallBack = GameObject.Find("S1_WallBack");
        if (wallBack != null)
        {
            GameObject.DestroyImmediate(wallBack);
            Debug.Log("[OCPSetup] Removed S1_WallBack to open space behind spawn.");
        }

        // ── 4. Instantiate OCP Player ────────────────────────────────────────
        var playerPrefab = AssetDatabase.LoadAssetAtPath<GameObject>(playerPrefabPath);
        var player = (GameObject)PrefabUtility.InstantiatePrefab(playerPrefab);
        player.name = "Player";
        player.tag  = "Player";
        player.transform.position = spawnPos;

        // ── 5. Instantiate OCP Camera Holder ─────────────────────────────────
        var camPrefab  = AssetDatabase.LoadAssetAtPath<GameObject>(camPrefabPath);
        var camHolder  = (GameObject)PrefabUtility.InstantiatePrefab(camPrefab);
        camHolder.name = "CameraRig";
        // Camera holder at the same world position as the player.
        // With lookAngle=90 the camera sits 3 units in -X (behind), giving clear space.
        camHolder.transform.position = spawnPos;

        // ── 5b. Add UniversalAdditionalCameraData so URP renders through this camera
        var ocpCamera = camHolder.GetComponentInChildren<Camera>();
        if (ocpCamera != null && ocpCamera.GetComponent<UniversalAdditionalCameraData>() == null)
        {
            ocpCamera.gameObject.AddComponent<UniversalAdditionalCameraData>();
            Debug.Log("[OCPSetup] Added UniversalAdditionalCameraData to OCP camera.");
        }

        // ── 6. Wire CharacterControls ↔ CameraManager ─────────────────────────
        var cc = player.GetComponent<CharacterControls>();
        if (cc != null)
        {
            cc.cam        = camHolder;
            cc.checkPoint = spawnPos;
            Debug.Log("[OCPSetup] CharacterControls.cam wired to CameraRig.");
        }

        var cm = camHolder.GetComponent<CameraManager>();
        if (cm != null)
        {
            cm.target = player.transform;

            // The level runs along +X. CameraManager uses lookAngle (Y rotation)
            // where 0° = facing +Z. 90° makes the camera face +X — correct for this level.
            // Must use SerializedObject so the override is written to the scene file;
            // direct assignment alone is not persisted for prefab-instance fields.
            var cmSO = new SerializedObject(cm);
            cmSO.FindProperty("lookAngle").floatValue = 90f;
            cmSO.ApplyModifiedProperties();
            camHolder.transform.rotation = Quaternion.Euler(0f, 90f, 0f);

            Debug.Log("[OCPSetup] CameraManager wired and oriented to face +X (level direction).");
        }

        // ── 7. Replace kill plane script with OCP KillZone ───────────────────
        var killPlane = GameObject.Find("KillPlane");
        if (killPlane != null)
        {
            // Remove old components that are no longer needed
            var oldRespawn = killPlane.GetComponent<PlayerRespawn>();
            if (oldRespawn != null) GameObject.DestroyImmediate(oldRespawn);

            if (killPlane.GetComponent<KillZone>() == null)
                killPlane.AddComponent<KillZone>();

            Debug.Log("[OCPSetup] KillPlane now uses OCP KillZone.");
        }

        // Also remove PlayerRespawn from player if it exists
        var playerRespawn = player.GetComponent<PlayerRespawn>();
        if (playerRespawn != null) GameObject.DestroyImmediate(playerRespawn);

        // ── 8. Replace checkpoint zone with OCP SavePos ───────────────────────
        var cpZone = GameObject.FindObjectOfType<CheckpointZone>();
        if (cpZone != null)
        {
            var cpGO     = cpZone.gameObject;
            var markerGO = cpGO.transform.Find("CP_Marker")?.gameObject ??
                           cpGO;

            GameObject.DestroyImmediate(cpZone);

            var savePos = cpGO.GetComponent<SavePos>() ?? cpGO.AddComponent<SavePos>();

            // SavePos needs a Transform that holds the respawn position.
            // Use the marker child if it exists, otherwise the trigger itself.
            savePos.checkPoint = markerGO.transform;
            Debug.Log("[OCPSetup] CheckpointZone replaced with OCP SavePos.");
        }

        // ── 9. Replace MovingPlatform.cs with OCP MovableObs on S3 platform ──
        //       S4 platform moves on Y axis (not supported by MovableObs) — keep custom
        var allMoving = GameObject.FindObjectsOfType<MovingPlatform>();
        foreach (var mp in allMoving)
        {
            // MovableObs only supports horizontal (X) or Z movement, not Y
            // Use it for S3 (X axis), keep custom script for S4 (Y axis)
            bool isVertical = mp.name.Contains("S4");
            if (!isVertical)
            {
                var mo = mp.gameObject.GetComponent<MovableObs>() ??
                         mp.gameObject.AddComponent<MovableObs>();
                mo.horizontal = true;   // X-axis movement
                mo.distance   = 2.5f;
                mo.speed      = 1.2f;
                GameObject.DestroyImmediate(mp);
                Debug.Log($"[OCPSetup] Replaced MovingPlatform with MovableObs on {mo.gameObject.name}");
            }
            else
            {
                Debug.Log($"[OCPSetup] Kept custom MovingPlatform on {mp.gameObject.name} (Y-axis, OCP doesn't support Y).");
            }
        }

        // ── 10. Replace RotatingHazard.cs with OCP Rotator ───────────────────
        var allRotating = GameObject.FindObjectsOfType<RotatingHazard>();
        foreach (var rh in allRotating)
        {
            var rotator = rh.gameObject.GetComponent<Rotator>() ??
                          rh.gameObject.AddComponent<Rotator>();
            rotator.speed = 1.5f;
            GameObject.DestroyImmediate(rh);
            Debug.Log($"[OCPSetup] Replaced RotatingHazard with OCP Rotator on {rotator.gameObject.name}");
        }

        // ── 11. Add TitleDismiss to TitlePanel ───────────────────────────────
        var titlePanel = GameObject.Find("TitlePanel");
        if (titlePanel != null)
        {
            if (titlePanel.GetComponent<TitleDismiss>() == null)
                titlePanel.AddComponent<TitleDismiss>();
            Debug.Log("[OCPSetup] TitleDismiss ensured on TitlePanel.");
        }

        // ── 12. Remove duplicate AudioListeners ──────────────────────────────
        var listeners = GameObject.FindObjectsOfType<AudioListener>();
        if (listeners.Length > 1)
        {
            // Keep the one parented inside the OCP camera hierarchy
            AudioListener keep = null;
            foreach (var l in listeners)
                if (l.transform.parent != null) { keep = l; break; }
            if (keep == null) keep = listeners[0];

            foreach (var l in listeners)
            {
                if (l == keep) continue;
                Debug.Log($"[OCPSetup] Removed duplicate AudioListener from '{l.gameObject.name}'");
                GameObject.DestroyImmediate(l);
            }
        }

        // ── 13. Save scene ────────────────────────────────────────────────────
        EditorSceneManager.MarkSceneDirty(scene);
        EditorSceneManager.SaveScene(scene);
        AssetDatabase.SaveAssets();
        Debug.Log("[OCPSetup] Scene saved successfully. OCP integration complete.");
    }
}
