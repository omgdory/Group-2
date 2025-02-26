using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CameraSmoothFollow : MonoBehaviour
{
    // Offsets for camera rotation for forward and rear views.
    // These offsets adjust the camera's rotation to provide a smooth, positioned view.
    private Vector3 TargetFwd_Offset = new Vector3(15, 0, 0);  // Forward view offset
    private Vector3 TargetBack_Offset = new Vector3(15, 180, 0);  // Rear view offset
    
    // Speed at which the camera smoothly moves to the target position.
    private float smoothSpeed = 10f;

    // Index for the currently selected camera view (0: forward, 1: rear).
    private int cameraSelection = 0;

    // Maximum number of camera targets (default 2: forward and rear).
    private int maxTargets = 2;

    // Called every fixed frame-rate frame.
    // Smoothly moves and rotates the camera.
    void FixedUpdate() 
    {
        HandleCamera();
    }

    // Called once per frame.
    // Detects keypress for camera switch (Tab key).
    void Update() 
    {
        // Switch between camera views when Tab is pressed.
        if (Input.GetKeyDown(KeyCode.Tab)) 
        {
            // Toggle between camera views (forward and rear).
            if (cameraSelection >= maxTargets - 1) 
            {
                cameraSelection = 0;  // Reset to first camera.
                return;
            }
            cameraSelection++;  // Switch to next camera.
        }
    }

    // Handles the camera movement and rotation based on the selected camera.
    void HandleCamera() 
    {
        // If the camera is set to follow the forward target (cameraSelection == 0).
        if (cameraSelection == 0) 
        {
            // Smoothly move towards the target position using Lerp.
            Vector3 smoothedPosition = Vector3.Lerp(transform.position, CarManager.CamTarget_fwd.position, smoothSpeed * Time.deltaTime);
            transform.position = smoothedPosition;

            // Adjust the camera's rotation with the forward offset.
            transform.rotation = CarManager.CamTarget_fwd.rotation * Quaternion.Euler(TargetFwd_Offset);
        }
        // If the camera is set to follow the rear target (cameraSelection == 1).
        else if (cameraSelection == 1) 
        {
            // Smoothly move towards the target position using Lerp.
            Vector3 smoothedPosition = Vector3.Lerp(transform.position, CarManager.CamTarget_back.position, smoothSpeed * Time.deltaTime);
            transform.position = smoothedPosition;

            // Adjust the camera's rotation with the rear offset.
            transform.rotation = CarManager.CamTarget_back.rotation * Quaternion.Euler(TargetBack_Offset);
        }
    }
}
