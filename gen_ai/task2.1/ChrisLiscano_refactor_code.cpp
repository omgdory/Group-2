/*
    Name: Christopher Liscano, 5007202091, CS302 1004, Assignment 4
    Description: computing the largest zig zag path in a binary tree
    Input: tree node names
    Output: longest zigzag
*/

#include "binTree.h"
#include <vector>
#include <string>

/*
FUNCTION_IDENTIFIER: default ctor
description: sets root to null
*/
binTree::binTree()
{
    root = nullptr;
}

/*
FUNCTION_IDENTIFIER: dtor
description: calls the deallocateTree function to deallocate the tree
*/
binTree::~binTree()
{
    binTree::deallocateTree(root);
}

/*
FUNCTION_IDENTIFIER: deallocate binary tree
parameters: binary tree pointer
return value: void
description: a function that will recursively delete the binary tree in postorder fashion
*/
void binTree::deallocateTree(binTreeNode *r)
{
    if (r == nullptr) // checks if tree is empty
        return;

    deallocateTree(r->left);  // deallocate left side
    deallocateTree(r->right); // deallocate right side

    delete r; // deallocate root
}

/*
FUNCTION_IDENTIFIER: wrapper buildTree function
parameters: locations
return value: void
description: checks if the locations is empty. If not, assigns the root pointer by calling
             a function that returns the root of the binary tree.
*/
void binTree::buildTree(std::vector<std::string> locations)
{
    if (locations.empty())
        return;

    root = buildTree(new binTreeNode(), locations, 0);
}

/*
FUNCTION_IDENTIFIER: overloaded buildTree function
parameters: binary tree pointer, locations, index
return value: pointer
description: recursive function that builds a tree in preorder fashion. It would then return
             a pointer pointing at the root of the tree.
*/
binTreeNode *binTree::buildTree(binTreeNode *r, std::vector<std::string> locations, int index)
{
    // BASE CASES
    if ((index > (locations.size() - 1) || index < 0) || locations[index] == "_") // if index is out of bounds or if you encounter an "_" at the index
    {
        delete r;       // delete b/c its not needed anymore
        return nullptr; // returning an empty node
    }

    // GENERAL CASES
    r->location = locations[index]; // assigning character to a node

    r->left = buildTree(new binTreeNode(), locations, (index * 2) + 1);  // building left side of tree
    r->right = buildTree(new binTreeNode(), locations, (index + 1) * 2); // building right side of tree

    return r;
}

/*
FUNCTION_IDENTIFIER: wrapper zigzag function
parameters: N/A
return value: vector
description: returns a vector of nodes of the longest zig zag path in the tree
*/
std::vector<std::string> binTree::zigzag()
{
    std::vector<std::string> leftPath;  // left side of tree
    std::vector<std::string> rightPath; // right side of tree
    std::vector<std::string> path;      // stores char at root if zigzag starts at root

    if (root == nullptr) // empty tree
        return path;

    // FINDING IF THE ROOT IS APART OF A ZIGZAG //
    if (root->left->right != nullptr) // checking if left path has a zigzag
    {
        path.push_back(root->location);                     // if zigzag exists, include the root
        leftPath = binTree::zigzag(root->left, true, path); // getting zigzags from left side
    }
    else // if the root isn't a part of the zigzag
        leftPath = binTree::zigzag(root->left, true, path);

    path.clear(); // clearing path in the case of both sides having the root as part of the zigzag

    if (root->right->left != nullptr) // checking if right path has a zigzag
    {
        path.push_back(root->location);
        rightPath = binTree::zigzag(root->right, false, path); // getting zigzags from right side
    }
    else
        rightPath = binTree::zigzag(root->right, false, path);

    if (leftPath.size() > rightPath.size()) // finding out which one is the larger path
        return leftPath;
    else
        return rightPath;

    return path;
}

/*
FUNCTION_IDENTIFIER: overloaded zigzag function
parameters: binary tree pointer, childType, path
return value: vector
description: a function that returns the longest path from node r.
*/
std::vector<std::string> binTree::zigzag(binTreeNode *r, bool childType, std::vector<std::string> path)
{
    if (!r) return path; // Base case: return current path if node is null

    path.push_back(r->location); // Include current node in the path

    std::vector<std::string> leftPath, rightPath;

    if (childType) // Coming from the left, move to the right
        rightPath = zigzag(r->right, false, path);
    else // Coming from the right, move to the left
        leftPath = zigzag(r->left, true, path);

    // Compare and return the longest path
    return (leftPath.size() > rightPath.size()) ? std::move(leftPath) : std::move(rightPath);
}
