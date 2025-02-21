//By: Abdulrahman Alharbi. 02/18/2025
#include <iostream>

/**
 * @brief Swaps two integer values using pointers.
 *
 * This function takes two integer pointers, dereferences them,
 * and swaps their values.
 *
 * @param a Pointer to the first integer.
 * @param b Pointer to the second integer.
 */
void swapValues(int* a, int* b) {
    int temp = *a;
    *a = *b;
    *b = temp;
}

/**
 * @brief Dynamically allocates an array and initializes it.
 *
 * This function creates an array of the given size in heap memory
 * and initializes all elements with the provided value.
 *
 * @param size The number of elements in the array.
 * @param initValue The value to initialize all elements with.
 * @return A pointer to the dynamically allocated array.
 * @note The caller is responsible for freeing the allocated memory using delete[].
 */
int* createArray(int size, int initValue) {
    int* arr = new int[size];  // Allocate memory on the heap
    for (int i = 0; i < size; i++) {
        arr[i] = initValue; // Initialize array elements
    }
    return arr;
}

/**
 * @brief Prints the elements of an array.
 *
 * This function iterates through the given array and prints its elements
 * separated by spaces.
 *
 * @param arr Pointer to the first element of the array.
 * @param size The number of elements in the array.
 */
void printArray(int* arr, int size) {
    for (int i = 0; i < size; i++) {
        std::cout << arr[i] << " ";
    }
    std::cout << std::endl;
}

int main() {
    // Demonstrating swap function
    int x = 10, y = 20;
    std::cout << "Before swap: x = " << x << ", y = " << y << std::endl;
    swapValues(&x, &y);
    std::cout << "After swap: x = " << x << ", y = " << y << std::endl;

    // Demonstrating dynamic array allocation
    int size = 5, initValue = 7;
    int* myArray = createArray(size, initValue);
    std::cout << "Dynamically allocated array: ";
    printArray(myArray, size);
    
    // Free allocated memory
    delete[] myArray;
    
    return 0;
}
