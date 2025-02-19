#include <iostream>

// this should swaps two integers using pointers
void swapValues(int* a, int* b) {
    int temp = *a;
    *a = *b;
    *b = temp;
}
// thiss should dynamically allocates an array and initializes it
int* createArray(int size, int initValue) {
    int* arr = new int[size];  
    for (int i = 0; i < size; i++) {
        arr[i] = initValue;
    }
    return arr;
}
// this prints an array
void printArray(int* arr, int size) {
    for (int i = 0; i < size; i++) {
        std::cout << arr[i] << " ";
    }
    std::cout << std::endl;
}
int main() {
    int x = 10, y = 20;
    std::cout << "Before swap: x = " << x << ", y = " << y << std::endl;
    swapValues(&x, &y);
    std::cout << "After swap: x = " << x << ", y = " << y << std::endl;
    int size = 5, initValue = 7;
    int* myArray = createArray(size, initValue);
    std::cout << "Dynamically allocated array: ";
    printArray(myArray, size);
    delete[] myArray; 
    return 0;
}
