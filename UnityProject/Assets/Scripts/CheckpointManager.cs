using UnityEngine;

// Singleton that stores the player's current respawn position.
// Attach to a single empty GameObject named "CheckpointManager" in the scene.
// CheckpointZone.cs calls Save() when the player passes through a checkpoint trigger.
// PlayerRespawn.cs calls Respawn() when the player falls below the kill plane.
public class CheckpointManager : MonoBehaviour
{
    public static CheckpointManager Instance { get; private set; }

    private Vector3 savedPosition;
    private Quaternion savedRotation;
    private bool hasSavedCheckpoint = false;

    private void Awake()
    {
        // Destroy duplicate instances so only one manager exists at a time
        if (Instance != null && Instance != this)
        {
            Destroy(gameObject);
            return;
        }
        Instance = this;
    }

    // Called by CheckpointZone when the player enters a checkpoint trigger
    public void Save(Vector3 position, Quaternion rotation)
    {
        savedPosition = position;
        savedRotation = rotation;
        hasSavedCheckpoint = true;
        Debug.Log("Checkpoint saved at: " + position);
    }

    // Called by PlayerRespawn when the player needs to be reset
    public void Respawn(Transform playerTransform, Vector3 levelStart)
    {
        if (hasSavedCheckpoint)
            playerTransform.SetPositionAndRotation(savedPosition, savedRotation);
        else
            playerTransform.position = levelStart;
    }
}
