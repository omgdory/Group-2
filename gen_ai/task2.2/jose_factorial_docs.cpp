/**
 * @file factorial.cpp
 * @author Jose Alarcon
 * @NSHE 5005581810
 * @course CS202, Section 1001
 * @brief This program calculates the factorial of an integer using recursion.
 *
 * The program defines a recursive function to compute the factorial of a given
 * integer and demonstrates its usage in the `main` function.
 */

 #include <iostream>

 using namespace std;
 
 /**
  * @brief Computes the factorial of a non-negative integer recursively.
  * 
  * @param n The integer for which the factorial is computed. Must be non-negative.
  * @return The factorial of the input integer.
  * 
  * @note If n is 0 or 1, the function returns 1 as the base case.
  * @note Function assumes n is non-negative; behavior is undefined for negative inputs.
  */
 int factorial(int n) {
     if (n == 0 || n == 1) 
         return 1;
     return n * factorial(n - 1);
 }
 
 /**
  * @brief Main function to demonstrate the factorial computation.
  * 
  * @return int Exit status of the program.
  */
 int main() {
     int num = 5; ///< The number whose factorial will be computed.
     
     // Display the result
     cout << "Factorial of " << num << " is: " << factorial(num) << endl;
     
     return 0;
 }
 