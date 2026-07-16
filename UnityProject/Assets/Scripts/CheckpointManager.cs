using UnityEngine;

public class CheckpointManager : MonoBehaviour
{
    public static CheckpointManager Instance { get; private set; }

    private Vector3 savedPosition;
    private Quaternion savedRotation;
    private bool hasSavedCheckpoint = false;

    private void Awake()
    {
        if (Instance != null && Instance != this)
        {
            Destroy(gameObject);
            return;
        }
        Instance = this;
    }

    public void Save(Vector3 position, Quaternion rotation)
    {
        savedPosition = position;
        savedRotation = rotation;
        hasSavedCheckpoint = true;
    }

    public void Respawn(Transform playerTransform, Vector3 levelStart)
    {
        if (hasSavedCheckpoint)
            playerTransform.SetPositionAndRotation(savedPosition, savedRotation);
        else
            playerTransform.position = levelStart;
    }
}
