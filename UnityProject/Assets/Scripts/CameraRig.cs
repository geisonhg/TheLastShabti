using UnityEngine;

// Attaches to the CameraRig empty that follows the player.
// The actual Camera is a child of CameraRig at a fixed offset.
// Move the mouse to orbit around the player.
public class CameraRig : MonoBehaviour
{
    [SerializeField] private Transform target;          // drag Player here
    [SerializeField] private float followDistance = 6f;
    [SerializeField] private float followHeight = 3.5f;
    [SerializeField] private float rotateSpeed = 120f;
    [SerializeField] private float verticalMin = -20f;
    [SerializeField] private float verticalMax = 50f;

    private float yaw;
    private float pitch = 15f;

    private void LateUpdate()
    {
        if (target == null) return;

        yaw   += Input.GetAxis("Mouse X") * rotateSpeed * Time.deltaTime;
        pitch -= Input.GetAxis("Mouse Y") * rotateSpeed * Time.deltaTime;
        pitch  = Mathf.Clamp(pitch, verticalMin, verticalMax);

        Quaternion rot = Quaternion.Euler(pitch, yaw, 0f);
        transform.rotation = rot;
        transform.position = target.position
                           - rot * Vector3.forward * followDistance
                           + Vector3.up * followHeight;
    }
}
