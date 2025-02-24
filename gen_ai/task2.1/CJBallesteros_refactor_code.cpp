// Connect 4
// Repurposed from CS 302.
// Made by Charles Ballesteros.
/* New additions include modifiable board size,
 * two new gamemodes, and colors to more easily
 * distinguish pieces.
 * */
#include <iostream>

// Function to validate numeric input within a range
int getValidInput(const std::string& prompt, int minValue) {
    int value;
    while (true) {
        std::cout << prompt;
        std::cin >> value;

        if (!std::cin.fail() && value > minValue) {
            return value;
        }

        std::cin.clear();
        std::cin.ignore(100, '\n');
        std::cout << "\nInvalid Input. Please try again.\n";
    }
}

// Function to get board size based on game mode
void getBoardSize(int& rowSize, int& boardSize, int defaultRows, int defaultCols, int minRows, int minCols) {
    std::cout << "\nChoose the size of the board.\n";
    std::cout << "Default: Rows = " << defaultRows << ", Columns = " << defaultCols << "\n";

    rowSize = getValidInput("\nEnter rows > " + std::to_string(minRows) + ": ", minRows);
    boardSize = getValidInput("\nEnter columns > " + std::to_string(minCols) + ": ", minCols);
}

void displayGameModeInfo() {
    std::cout << "\nClassic: Place four pieces in a row (horizontal, vertical, or diagonal) to win.\n";
    std::cout << "Connect-Five: Similar to Classic, but requires five in a row to win.\n";
    std::cout << "PopOut: Standard four-in-a-row rules, but players can remove their piece from the bottom.\n";
}

int main() {
    int gamemode, rowSize, boardSize;

    do {
        std::cout << "\nWhat game mode would you like to play?\n";
        std::cout << "\nGamemodes: \n(0)Classic \n(1)Connect Five \n(2)PopOut \n(3)More Info\n";
        std::cout << "\nEnter the number corresponding to the gamemode: ";
        std::cin >> gamemode;

        if (std::cin.fail() || gamemode < 0 || gamemode > 3) {
            std::cin.clear();
            std::cin.ignore(100, '\n');
            std::cout << "\nInvalid input. Please enter a valid option.\n";
            continue;
        }

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

    } while (gamemode < 0 || gamemode > 2); // Loop until a valid gamemode is selected

    return 0;
}
