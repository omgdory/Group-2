using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CameraSmoothFollow : MonoBehaviour
{
    // A struct to hold both the offset and the target position for each camera mode
    [System.Serializable]
    public struct CameraTarget
    {
        public Transform targetPosition;
        public Vector3 rotationOffset;
    }

    [SerializeField]
    private List<CameraTarget> cameraTargets = new List<CameraTarget>();

    // Speed at which the camera will return to position
    [SerializeField]
    private float smoothSpeed = 10f;

    private int cameraSelection = 0;

    void FixedUpdate() 
    {
        HandleCamera();
    }

    void Update() 
    {
        if (Input.GetKeyDown(KeyCode.Tab)) 
        {
            SwitchCamera();
        }
    }

    private void SwitchCamera()
    {
        cameraSelection = (cameraSelection + 1) % cameraTargets.Count;
    }

    private void HandleCamera()
    {
        if (cameraTargets.Count == 0) return;

        // Get the target for the current camera selection
        CameraTarget currentTarget = cameraTargets[cameraSelection];

        // Smoothly move to the target position
        Vector3 smoothedPosition = Vector3.Lerp(transform.position, currentTarget.targetPosition.position, smoothSpeed * Time.deltaTime);
        transform.position = smoothedPosition;

        // Smoothly rotate to the target rotation with offset
        transform.rotation = currentTarget.targetPosition.rotation * Quaternion.Euler(currentTarget.rotationOffset);
    }
}
