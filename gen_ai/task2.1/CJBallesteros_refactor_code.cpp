// Connect 4
// Repurposed from CS 302.
// Made by Charles Ballesteros.
/* New additions include modifiable board size,
 * two new gamemodes, and colors to more easily
 * distinguish pieces.
 * */

#include <iostream>
#include "LL.h"

/*
Game States:
0 = Ongoing
1 = Player win
2 = Tie
3 = Exit
*/

int main() {
    // Declaring all the variables.
    int boardSize = 7; // Column size
    int rowSize = 6;
    int gamemode = 0;

    std::cout << "\nWelcome to Terminal Connect 4. o/\n";

    // While loop that asks player for gamemode and board size.
    do {
        if (gamemode < 0 || gamemode > 3 || std::cin.fail()) {
            std::cin.clear();
            std::cin.ignore(100, '\n');
            std::cout << "\nInvalid input";
        }

        std::cout << "\nWhat game mode would you like to play?\n";
        std::cout << "\nGamemodes: \n(0)Classic \n(1)Connect Five \n(2)PopOut";
        std::cout << "\n(3)More Info\n";

        std::cout << "\nEnter the number corresponding to the gamemode: ";
        std::cin >> gamemode;

        if (gamemode == 0 || gamemode == 2) {
            std::cout << "\nChoose the size of the board.\n";
            std::cout << "Rows default = 7, Columns default = 6\n";

            std::cout << "\nEnter rows > 4: ";
            std::cin >> rowSize;

            while (rowSize <= 3 || std::cin.fail()) {
                std::cin.clear();
                std::cin.ignore(100, '\n');
                std::cout << "\nInvalid Input";
                std::cout << "\nEnter rows > 4: ";
                std::cin >> rowSize;
            }

            std::cout << "Enter columns > 3: ";
            std::cin >> boardSize;

            while (boardSize <= 4 || std::cin.fail()) {
                std::cin.clear();
                std::cin.ignore(100, '\n');
                std::cout << "\nInvalid Input";
                std::cout << "\nEnter columns > 3: ";
                std::cin >> boardSize;
            }
        }

        if (gamemode == 1) {
            std::cout << "\nChoose the size of the board.\n";
            std::cout << "Rows default = 6, Columns default = 9\n";

            std::cout << "Enter columns > 5: ";
            std::cin >> boardSize;

            std::cout << "\nEnter rows > 6: ";
            std::cin >> rowSize;

            while (rowSize <= 3 || std::cin.fail()) {
                std::cin.clear();
                std::cin.ignore(100, '\n');
                std::cout << "\nInvalid Input";
                std::cout << "\nEnter rows > 5: ";
                std::cin >> rowSize;
            }

            while (boardSize <= 4 || std::cin.fail()) {
                std::cin.clear();
                std::cin.ignore(100, '\n');
                std::cout << "\nInvalid Input";
                std::cout << "Enter columns > 6: ";
                std::cin >> boardSize;
            }
        }

        if (gamemode == 3) {
            std::cout << "\nClassic: The original game rules where one" <<
                      "\ntries to place four of their colored pieces, " <<
                      "\nin a row, whether that's horizontally, " <<
                      "\nvertically, or diagonally\n";
            std::cout << "\nConnect-Five: Same rules as classic, but you" <<
                      "\nneed five in a row to win.\n";
            std::cout << "\nPopOut: Four-in-a-row rules, but on your turn" <<
                      "\nyou get the opportunity to remove your " <<
                      "\ncolored piece from the bottom. (But only" <<
                      "\na piece of your color!)\n";
        }

    } while (gamemode < 0 || gamemode > 2 || std::cin.fail());

    return 0;
}
