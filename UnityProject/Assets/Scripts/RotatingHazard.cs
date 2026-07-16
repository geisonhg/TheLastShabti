using UnityEngine;

public class RotatingHazard : MonoBehaviour
{
    [SerializeField] private float degreesPerSecond = 90f;

    private void Update()
    {
        transform.Rotate(0f, degreesPerSecond * Time.deltaTime, 0f, Space.World);
    }
}
