// Source: https://bit.ly/2BITbQm
// De-complex-ified with ChatGPT
#include <math.h>
#include <stdio.h>
#include <string.h> // Use <string.h> instead of <cstring> for C compatibility

#define SCREEN_WIDTH 80
#define SCREEN_HEIGHT 22
#define BUFFER_SIZE (SCREEN_WIDTH * SCREEN_HEIGHT)

// ASCII luminance gradient for shading
const char SHADING_CHARS[] = ".,-~:;=!*#$@";

// Function prototypes
void clearScreen();
void renderFrame(float A, float B);

int main()
{
  float A = 0, B = 0; // Rotation angles

  printf("\x1b[2J"); // Clear terminal screen

  while (1)
  {
    renderFrame(A, B);
    A += 0.00004; // Increment rotation angle A
    B += 0.00002; // Increment rotation angle B
  }

  return 0;
}

/**
 * Clears the terminal screen by moving the cursor to the top-left corner.
 */
void clearScreen()
{
  printf("\x1b[H"); // ANSI escape code to reset cursor position
}

/**
 * Renders a frame of the spinning donut.
 *
 * @param A Rotation angle around the x-axis.
 * @param B Rotation angle around the z-axis.
 */
void renderFrame(float A, float B)
{
  char buffer[BUFFER_SIZE];   // Character buffer for rendering
  float zBuffer[BUFFER_SIZE]; // Depth buffer to store depth values

  // Initialize buffers
  memset(buffer, ' ', BUFFER_SIZE);
  memset(zBuffer, 0, sizeof(zBuffer));

  // Iterate over torus angles (theta for the circle, phi for the rotation)
  for (float theta = 0; theta < 2 * M_PI; theta += 0.014)
  {
    for (float phi = 0; phi < 2 * M_PI; phi += 0.004)
    {
      // Compute torus coordinates
      float sinTheta = sin(theta);
      float cosTheta = cos(theta);
      float sinPhi = sin(phi);
      float cosPhi = cos(phi);

      float sinA = sin(A);
      float cosA = cos(A);
      float sinB = sin(B);
      float cosB = cos(B);

      float circleX = cosTheta + 2; // Circle radius + torus radius
      float circleY = sinTheta;

      // Compute 3D point position after rotation
      float invZ = 1 / (sinPhi * circleX * sinA + circleY * cosA + 5);
      float projX = sinPhi * circleX * cosA - circleY * sinA;
      float projY = cosPhi * circleX;

      // Project 3D point onto 2D screen
      int x = SCREEN_WIDTH / 2 + SCREEN_WIDTH / 4 * invZ * (projX * cosB - projY * sinB);
      int y = SCREEN_HEIGHT / 2 + SCREEN_HEIGHT / 4 * invZ * (projX * sinB + projY * cosB);
      int bufferIndex = x + SCREEN_WIDTH * y;

      // Compute luminance
      int luminanceIndex = 8 * ((circleY * sinA - sinPhi * cosTheta * cosA) * cosB -
                                sinPhi * cosTheta * sinA - circleY * cosA - cosPhi * cosTheta * sinB);

      // Bounds checking before modifying the buffer
      if (y >= 0 && y < SCREEN_HEIGHT && x >= 0 && x < SCREEN_WIDTH && invZ > zBuffer[bufferIndex])
      {
        zBuffer[bufferIndex] = invZ;
        buffer[bufferIndex] = SHADING_CHARS[luminanceIndex > 0 ? luminanceIndex : 0];
      }
    }
  }

  // Clear the screen and render the frame
  clearScreen();
  for (int i = 0; i < BUFFER_SIZE; i++)
  {
    putchar(i % SCREEN_WIDTH ? buffer[i] : '\n');
  }
}
