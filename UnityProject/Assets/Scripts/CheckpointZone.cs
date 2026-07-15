using UnityEngine;

// Place this script on each checkpoint trigger in the level.
// The GameObject needs a Collider with "Is Trigger" enabled.
//
// SETUP IN UNITY:
//   1. Create an empty GameObject, e.g. "CP_ShaftOfRa"
//   2. Add a Box Collider — tick "Is Trigger", resize to cover the doorway
//   3. Attach this script
//   4. Repeat for each checkpoint location
//   There is one checkpoint in Section 4 (Shaft of Ra) as specified in the brief.
public class CheckpointZone : MonoBehaviour
{
    // The player respawns slightly above the trigger centre so they don't spawn inside geometry
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
