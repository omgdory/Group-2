// Connect 4
// Repurposed from CS 302.
// Made by Charles Ballesteros.
/* New additions include modifiable board size,
 * two new gamemodes, and colors to more easily
 * distinguish pieces.
 * */
#include <iostream>

/**
 * @brief Ensures the user enters a valid integer greater than a specified minimum value.
 *
 * This function continuously prompts the user until they provide a valid input.
 * It clears any input errors and ignores invalid characters.
 *
 * @param prompt The message displayed to the user when asking for input.
 * @param minValue The minimum allowable value for input.
 * @return A valid integer greater than minValue.
 */
int getValidInput(const std::string& prompt, int minValue) {
    int value;
    while (true) {
        std::cout << prompt;
        std::cin >> value;

        if (!std::cin.fail() && value > minValue) {
            return value; // Return valid input
        }

        // Handle invalid input
        std::cin.clear();
        std::cin.ignore(100, '\n');
        std::cout << "\nInvalid Input. Please try again.\n";
    }
}

/**
 * @brief Prompts the user to input board dimensions with validation.
 *
 * This function asks the user for row and column sizes based on the game mode selected.
 * The values must be greater than the minimum required values.
 *
 * @param rowSize Reference to store the row size input.
 * @param boardSize Reference to store the column size input.
 * @param defaultRows The default number of rows for the selected game mode.
 * @param defaultCols The default number of columns for the selected game mode.
 * @param minRows The minimum required row size.
 * @param minCols The minimum required column size.
 */
void getBoardSize(int& rowSize, int& boardSize, int defaultRows, int defaultCols, int minRows, int minCols) {
    std::cout << "\nChoose the size of the board.\n";
    std::cout << "Default: Rows = " << defaultRows << ", Columns = " << defaultCols << "\n";

    // Get valid input for row and column sizes
    rowSize = getValidInput("\nEnter rows > " + std::to_string(minRows) + ": ", minRows);
    boardSize = getValidInput("\nEnter columns > " + std::to_string(minCols) + ": ", minCols);
}

/**
 * @brief Displays descriptions of the different game modes available.
 */
void displayGameModeInfo() {
    std::cout << "\nClassic: Place four pieces in a row (horizontal, vertical, or diagonal) to win.\n";
    std::cout << "Connect-Five: Similar to Classic, but requires five in a row to win.\n";
    std::cout << "PopOut: Standard four-in-a-row rules, but players can remove their piece from the bottom.\n";
}

int main() {
    int gamemode, rowSize, boardSize;

    // Loop until the user selects a valid game mode (0, 1, or 2)
    do {
        // Display available game modes
        std::cout << "\nWhat game mode would you like to play?\n";
        std::cout << "\nGamemodes: \n(0)Classic \n(1)Connect Five \n(2)PopOut \n(3)More Info\n";
        std::cout << "\nEnter the number corresponding to the gamemode: ";
        std::cin >> gamemode;

        // Handle invalid game mode selection
        if (std::cin.fail() || gamemode < 0 || gamemode > 3) {
            std::cin.clear();
            std::cin.ignore(100, '\n');
            std::cout << "\nInvalid input. Please enter a valid option.\n";
            continue;
        }

        // Handle game mode selection
        switch (gamemode) {
            case 0: // Classic
            case 2: // PopOut
                getBoardSize(rowSize, boardSize, 7, 6, 4, 3);
                break;
            case 1: // Connect-Five
                getBoardSize(rowSize, boardSize, 6, 9, 5, 6);
                break;
            case 3: // More Info
                displayGameModeInfo();
                break;
        }

    } while (gamemode < 0 || gamemode > 2); // Repeat if an invalid game mode is selected

    return 0; // Exit the program successfully
}
