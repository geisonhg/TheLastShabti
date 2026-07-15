using UnityEngine;
using UnityEngine.InputSystem;

public class TitleDismiss : MonoBehaviour
{
    void Start()
    {
        Debug.Log("[TitleDismiss] Running on: " + gameObject.name);
    }

    void Update()
    {
        bool pressed = (Keyboard.current != null && Keyboard.current.anyKey.wasPressedThisFrame)
                    || (Mouse.current   != null && Mouse.current.leftButton.wasPressedThisFrame);

        if (pressed)
        {
            Debug.Log("[TitleDismiss] Input detected — hiding panel.");
            gameObject.SetActive(false);
        }
    }
}
