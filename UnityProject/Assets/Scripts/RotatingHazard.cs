using UnityEngine;

// Rotates an obstacle around the Y axis continuously.
// Placeholder for the OCP rotating hazard — replace if OCP is imported.
public class RotatingHazard : MonoBehaviour
{
    [SerializeField] private float degreesPerSecond = 90f;

    private void Update()
    {
        transform.Rotate(0f, degreesPerSecond * Time.deltaTime, 0f, Space.World);
    }
}
