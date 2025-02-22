#include <iostream>
#include <string>
#include <algorithm>  // For std::transform, std::equal, std::remove_if
#include <cctype>     // For std::isalnum, std::tolower

using namespace std;

bool isPalindrome(string str) {
    // Remove non-alphanumeric characters (punctuation, spaces, etc.)
    str.erase(remove_if(str.begin(), str.end(), [](char c) { return !isalnum(c); }), str.end());

    // Convert all characters to lowercase for case-insensitive comparison
    transform(str.begin(), str.end(), str.begin(), ::tolower);

    // Compare the string with its reverse using std::equal
    return equal(str.begin(), str.begin() + str.size() / 2, str.rbegin());
}

int main() {
    string word;

    // Prompt user to enter a string
    cout << "Enter a string: ";
    getline(cin, word);  // Using getline to allow multi-word inputs

    // Check if the input string is a palindrome and display the result
    if (isPalindrome(word)) {
        cout << "\"" << word << "\" is a palindrome." << endl;
    } else {
        cout << "\"" << word << "\" is not a palindrome." << endl;
    }

    return 0;
}
