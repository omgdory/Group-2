/*
By: Abdulrahman Alharbi. 02/18/2025
Goal: This is a basic Bubble Sort algorithm with a time complexity of O(n^2).
        So, I will ask ChatGPT to to optimize it to a more efficient sorting algorithm (O(n log n)).
        Prompt: 
            "This is a Bubble Sort algorithm with O(n²) complexity. 
            Please optimize it to O(n log n) using a 
            more efficient sorting algorithm like QuickSort or MergeSort, 
            while keeping the structure and readability clear."
        My guess is that GPT will most prop suggest QuickSort or MergeSort, 
            both of which have O(n log n) time complexity. Guess will see! 
*/

#include <iostream>
#include <vector>

// Bubble Sort (O(n^2))
void bubbleSort(std::vector<int>& arr) {
    int n = arr.size();
    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - i - 1; j++) {
            if (arr[j] > arr[j + 1]) {
                std::swap(arr[j], arr[j + 1]);
            }
        }
    }
}

// QuickSort function
int partition(std::vector<int>& arr, int low, int high) {
    int pivot = arr[high]; // Choosing the last element as the pivot
    int i = low - 1; // Index of smaller element

    for (int j = low; j < high; j++) {
        if (arr[j] < pivot) { // If current element is smaller than pivot
            i++;
            std::swap(arr[i], arr[j]);
        }
    }
    std::swap(arr[i + 1], arr[high]); // Place pivot in correct position
    return i + 1;
}

void quickSort(std::vector<int>& arr, int low, int high) {
    if (low < high) {
        int pi = partition(arr, low, high);

        quickSort(arr, low, pi - 1); // Sort elements before pivot
        quickSort(arr, pi + 1, high); // Sort elements after pivot
    }
}

// Function to print the array
void printArray(const std::vector<int>& arr) {
    for (int num : arr) {
        std::cout << num << " ";
    }
    std::cout << std::endl;
}

int main() {
    std::vector<int> arr = {64, 34, 25, 12, 22, 11, 90};

    std::cout << "Original array: ";
    printArray(arr);

    quickSort(arr, 0, arr.size() - 1);

    std::cout << "Sorted array: ";
    printArray(arr);

    return 0;
}