using UnityEngine;

// Attach to the Player GameObject.
// When the player falls below killPlaneY, they are sent back to the last checkpoint.
//
// SETUP IN UNITY:
//   1. Attach this to the Player (same object the Obstacle Course Pack controller is on)
//   2. Set Kill Plane Y to a value below all platforms (e.g. -10)
//   3. Set Level Start Pos to the player's starting position in the scene
//   4. If the Obstacle Course Pack already handles respawning, you may not need this script
public class PlayerRespawn : MonoBehaviour
{
    [SerializeField] private float killPlaneY = -10f;
    [SerializeField] private Vector3 levelStartPos = new Vector3(0f, 1f, 0f);

    private void Update()
    {
        if (transform.position.y < killPlaneY)
        {
            CheckpointManager.Instance.Respawn(transform, levelStartPos);
        }
    }
}
