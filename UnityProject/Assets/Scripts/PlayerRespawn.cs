using UnityEngine;

public class PlayerRespawn : MonoBehaviour
{
    [SerializeField] private float killPlaneY = -10f;
    [SerializeField] private Vector3 levelStartPos = new Vector3(0f, 1f, 0f);

    private void Update()
    {
        if (transform.position.y < killPlaneY)
            CheckpointManager.Instance.Respawn(transform, levelStartPos);
    }
}
