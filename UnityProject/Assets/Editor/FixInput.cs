using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;

public static class FixInput
{
    [MenuItem("TheLastShabti/Fix Input + Title")]
    public static void Run()
    {
        var scene = EditorSceneManager.OpenScene(
            "Assets/Scenes/LVL_MainPyramid.unity", OpenSceneMode.Single);

        var titlePanel = GameObject.Find("TitlePanel");
        if (titlePanel == null)
        {
            Debug.LogError("[FixInput] TitlePanel not found in scene.");
            return;
        }

        if (titlePanel.GetComponent<TitleDismiss>() == null)
        {
            titlePanel.AddComponent<TitleDismiss>();
            Debug.Log("[FixInput] TitleDismiss added to TitlePanel.");
        }
        else
        {
            Debug.Log("[FixInput] TitleDismiss already present.");
        }

        EditorSceneManager.MarkSceneDirty(scene);
        EditorSceneManager.SaveScene(scene);
        AssetDatabase.SaveAssets();
        Debug.Log("[FixInput] Done.");
    }
}
