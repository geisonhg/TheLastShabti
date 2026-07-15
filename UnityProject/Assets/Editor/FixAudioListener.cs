using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;

public static class FixAudioListener
{
    [MenuItem("TheLastShabti/Fix Audio Listener")]
    public static void Run()
    {
        var scene = EditorSceneManager.OpenScene(
            "Assets/Scenes/LVL_MainPyramid.unity", OpenSceneMode.Single);

        var listeners = GameObject.FindObjectsOfType<AudioListener>();
        Debug.Log($"[FixAudioListener] Found {listeners.Length} AudioListeners.");

        if (listeners.Length <= 1) { Debug.Log("Nothing to fix."); return; }

        // Keep the one that is a child of CameraRig / Camera Holder (OCP camera).
        // Remove all others.
        AudioListener keep = null;
        foreach (var l in listeners)
        {
            if (l.transform.parent != null)   // child of something = OCP camera
            { keep = l; break; }
        }
        if (keep == null) keep = listeners[0]; // fallback: keep first

        foreach (var l in listeners)
        {
            if (l == keep) continue;
            Debug.Log($"[FixAudioListener] Removing AudioListener from '{l.gameObject.name}'");
            GameObject.DestroyImmediate(l);
        }

        EditorSceneManager.MarkSceneDirty(scene);
        EditorSceneManager.SaveScene(scene);
        Debug.Log("[FixAudioListener] Done — exactly one AudioListener remains.");
    }
}
