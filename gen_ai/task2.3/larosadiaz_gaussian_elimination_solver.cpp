//CS 472 
//NSHE ID: 5004634201     Franklin La Rosa Diaz

#include <iostream>
#include <vector>
#include <iomanip>
#include <cmath>

// Function to perform Gaussian Elimination with Partial Pivoting
void gaussianElimination(std::vector<std::vector<double>>& matrix, std::vector<double>& b, std::vector<double>& solution) {
    int n = matrix.size();

    // Forward Elimination
    for (int i = 0; i < n; ++i) {
        // Partial Pivoting: Find the row with the largest absolute value in column i
        int maxRow = i;
        for (int k = i + 1; k < n; ++k) {
            if (std::fabs(matrix[k][i]) > std::fabs(matrix[maxRow][i])) {
                maxRow = k;
            }
        }
        
        // Swap the maxRow with the current row
        std::swap(matrix[i], matrix[maxRow]);
        std::swap(b[i], b[maxRow]);

        // Check for singularity (zero pivot element)
        if (std::fabs(matrix[i][i]) < 1e-10) {
            std::cerr << "Singular Matrix: No unique solution exists!" << std::endl;
            return;
        }

        // Eliminate below the pivot
        for (int k = i + 1; k < n; ++k) {
            double factor = matrix[k][i] / matrix[i][i];
            for (int j = i; j < n; ++j) {
                matrix[k][j] -= factor * matrix[i][j];
            }
            b[k] -= factor * b[i];
        }
    }

    // Back Substitution
    for (int i = n - 1; i >= 0; --i) {
        double sum = b[i];
        for (int j = i + 1; j < n; ++j) {
            sum -= matrix[i][j] * solution[j];
        }
        solution[i] = sum / matrix[i][i];
    }
}

// Function to print the system
void printSystem(const std::vector<std::vector<double>>& matrix, const std::vector<double>& b) {
    int n = matrix.size();
    std::cout << "Augmented Matrix: " << std::endl;
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            std::cout << std::setw(8) << matrix[i][j] << " ";
        }
        std::cout << "| " << std::setw(8) << b[i] << std::endl;
    }
}

int main() {
    int n;
    std::cout << "Enter the number of equations: ";
    std::cin >> n;

    std::vector<std::vector<double>> matrix(n, std::vector<double>(n));
    std::vector<double> b(n), solution(n, 0);

    std::cout << "Enter the coefficients of the augmented matrix (A | B):" << std::endl;
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            std::cin >> matrix[i][j];
        }
        std::cin >> b[i];
    }

    printSystem(matrix, b);
    
    gaussianElimination(matrix, b, solution);

    std::cout << "\nSolution:" << std::endl;
    for (int i = 0; i < n; ++i) {
        std::cout << "x" << i + 1 << " = " << solution[i] << std::endl;
    }

    return 0;
}
