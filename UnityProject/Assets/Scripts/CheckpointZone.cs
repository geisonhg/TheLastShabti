using UnityEngine;

public class CheckpointZone : MonoBehaviour
{
    [SerializeField] private Vector3 spawnOffset = new Vector3(0f, 1.5f, 0f);

    private bool alreadyActivated = false;

    private void OnTriggerEnter(Collider other)
    {
        if (alreadyActivated) return;
        if (!other.CompareTag("Player")) return;

        alreadyActivated = true;
        CheckpointManager.Instance.Save(
            transform.position + spawnOffset,
            other.transform.rotation
        );
    }
}
