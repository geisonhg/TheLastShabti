using UnityEngine;

// Attach this script to an invisible trigger box placed over the Sun Altar.
// When the player enters it, the win panel is shown and the game pauses.
//
// SETUP IN UNITY:
//   1. Create an empty GameObject named "Goal_SunAltarTrigger"
//   2. Add a Box Collider — tick "Is Trigger"
//   3. Attach this script
//   4. Drag your win panel UI object into the Win Panel slot in the Inspector
//   5. Make sure the Player GameObject has the tag "Player"
public class GoalTrigger : MonoBehaviour
{
    [SerializeField] private GameObject winPanel;

    private bool triggered = false;

    private void OnTriggerEnter(Collider other)
    {
        if (triggered) return;
        if (!other.CompareTag("Player")) return;

        triggered = true;

        if (winPanel != null)
            winPanel.SetActive(true);

        // Pause the game so the player can read the message
        Time.timeScale = 0f;
    }
}
