#include <iostream>
#include <algorithm>  // For std::max_element

using namespace std;

int max(const int arr[], int size) {
    if (size == 0) {
        throw invalid_argument("Array size must be greater than 0");
    }
    return *max_element(arr, arr + size);
}

int main() {
    int numbers[] = {8, 3, 4, 1, 7, 6};
    int size = sizeof(numbers) / sizeof(numbers[0]);
    
    try {
        cout << "Max value: " << max(numbers, size) << endl;
    } catch (const exception& e) {
        cerr << "Error: " << e.what() << endl;
    }

    return 0;
}
