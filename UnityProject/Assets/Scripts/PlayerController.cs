using UnityEngine;

// Third-person player controller for The Last Shabti.
// Uses CharacterController — attach to a Capsule with a CharacterController component.
// Camera is a child of CameraRig which follows the player; rotate camera with the mouse.
//
// NOTE: The Obstacle Course Pack was not available for this project.
// This script is a short custom replacement following the same brief requirements.
[RequireComponent(typeof(CharacterController))]
public class PlayerController : MonoBehaviour
{
    [Header("Movement")]
    [SerializeField] private float moveSpeed = 5f;
    [SerializeField] private float jumpForce = 7f;
    [SerializeField] private float gravity = -18f;

    [Header("Camera")]
    [SerializeField] private Transform cameraRig;     // drag CameraRig here

    private CharacterController cc;
    private Vector3 velocity;
    private bool isGrounded;

    private void Awake()
    {
        cc = GetComponent<CharacterController>();
        // Lock cursor for camera mouse look
        Cursor.lockState = CursorLockMode.Locked;
        Cursor.visible = false;
    }

    private void Update()
    {
        isGrounded = cc.isGrounded;
        if (isGrounded && velocity.y < 0f)
            velocity.y = -2f;   // keep grounded, small negative keeps isGrounded true

        // WASD movement relative to camera forward
        float h = Input.GetAxis("Horizontal");
        float v = Input.GetAxis("Vertical");

        // Camera-relative direction
        Vector3 camFwd = cameraRig != null
            ? Vector3.ProjectOnPlane(cameraRig.forward, Vector3.up).normalized
            : transform.forward;
        Vector3 camRight = cameraRig != null
            ? Vector3.ProjectOnPlane(cameraRig.right, Vector3.up).normalized
            : transform.right;

        Vector3 moveDir = (camFwd * v + camRight * h).normalized;

        if (moveDir.sqrMagnitude > 0.01f)
        {
            // Rotate character to face movement direction
            transform.forward = Vector3.Lerp(transform.forward, moveDir, Time.deltaTime * 12f);
        }

        cc.Move(moveDir * moveSpeed * Time.deltaTime);

        // Jump
        if (Input.GetButtonDown("Jump") && isGrounded)
            velocity.y = jumpForce;

        // Gravity
        velocity.y += gravity * Time.deltaTime;
        cc.Move(velocity * Time.deltaTime);
    }
}
