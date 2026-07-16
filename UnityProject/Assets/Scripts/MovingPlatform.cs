using UnityEngine;

public class MovingPlatform : MonoBehaviour
{
    public enum Axis { X, Y, Z }

    [SerializeField] private Axis moveAxis = Axis.X;
    [SerializeField] private float moveDistance = 3f;
    [SerializeField] private float speed = 1.5f;

    private Vector3 startPos;

    private void Start()
    {
        startPos = transform.position;
    }

    private void Update()
    {
        float offset = Mathf.Sin(Time.time * speed) * moveDistance;
        Vector3 dir = moveAxis == Axis.X ? Vector3.right
                    : moveAxis == Axis.Y ? Vector3.up
                                        : Vector3.forward;
        transform.position = startPos + dir * offset;
    }
}
