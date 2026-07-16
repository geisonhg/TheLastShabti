using UnityEngine;

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

        Time.timeScale = 0f;
    }
}
