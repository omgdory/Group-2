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
    std::vector<std::string> empty; // used for clearing the zigzag
    std::vector<std::string> leftPath;
    std::vector<std::string> rightPath;
    std::vector<std::string> result; // for storing the longest zigzag

    if (!(path.empty())) // if a path exists
    {
        for (unsigned int i = 0; i < path.size(); i++)
        {
            result.push_back(path[i]); // getting paths from previous iterations
        }
    }

    // BASE CASE //
    if (r == nullptr) // if zigzag reaches the end OR if zigzag is empty
        return result;

    // GENERAL CASES //
    if (childType) // LEFT SIDE
    {
        if (r->left == nullptr && r->right == nullptr && result.size() > 2) // checks if end of zigzag. We check size because a zigzag at minimum is 3 nodes
        {
            result.push_back(r->location);                        // push the last character in zigzag
            rightPath = binTree::zigzag(r->right, false, result); // getting zigzag
            return rightPath;
        }

        if (r->right != nullptr) // checking for zigzag on the right b/c we're on the left
        {
            result.push_back(r->location);                        // adding a potential zigzag
            rightPath = binTree::zigzag(r->right, false, result); // since we're on the right node, check the left node
        }
        else
            rightPath = binTree::zigzag(r->right, false, empty); // if no node, return empty list

        if (r->left != nullptr) // checking for a left node, if one exists, create a new zigzag
        {
            result.clear();
            result.push_back(r->location);                     // potential zigzag
            leftPath = binTree::zigzag(r->left, true, result); // checking left nodes
        }
        else
            leftPath = binTree::zigzag(r->left, true, empty); // empty list

        // finding out which one is the larger path
        if (leftPath.size() > rightPath.size())
            return leftPath;
        else
            return rightPath;
    }
    else // RIGHT SIDE
    {
        if (r->left == nullptr && r->right == nullptr && result.size() > 2) // checking if at end
        {
            result.push_back(r->location);
            leftPath = binTree::zigzag(r->left, true, result);
            return leftPath;
        }

        if (r->left != nullptr) // checking for zigzag on the left b/c we're on the right
        {
            result.push_back(r->location);
            leftPath = binTree::zigzag(r->left, true, result);
        }
        else
            leftPath = binTree::zigzag(r->left, true, empty); // empty list

        if (r->right != nullptr) // checking for a right node, if one exists, create a new zigzag
        {
            result.clear();
            result.push_back(r->location);
            rightPath = binTree::zigzag(r->right, false, result);
        }
        else
            rightPath = binTree::zigzag(r->right, false, empty);

        // finding out which one is the larger path
        if (leftPath.size() > rightPath.size())
            return leftPath;
        else
            return rightPath;
    }

    return empty; // if left and right nodes are empty
}