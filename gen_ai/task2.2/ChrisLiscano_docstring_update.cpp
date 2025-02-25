/*
    Name: Christopher Liscano, 5007202091, CS302 1004, Assignment 4
    Description: Computes the longest zig-zag path in a binary tree.
    Input: Binary tree node names provided in a vector.
    Output: A vector representing the longest zig-zag path.
*/

#include "binTree.h"
#include <vector>
#include <string>

/*
    Constructor: binTree
    Description: Initializes the binary tree with a null root.
*/
binTree::binTree()
{
    root = nullptr;
}

/*
    Destructor: ~binTree
    Description: Calls the deallocateTree function to free memory used by the tree.
*/
binTree::~binTree()
{
    binTree::deallocateTree(root);
}

/*
    Function: deallocateTree
    Parameters: Pointer to a binary tree node.
    Return Value: None (void)
    Description: Recursively deletes the binary tree nodes in postorder fashion.
                 Base Case: If the node is null, return immediately (empty tree or end of branch).
*/
void binTree::deallocateTree(binTreeNode *r)
{
    if (r == nullptr)
        return;

    deallocateTree(r->left);
    deallocateTree(r->right);

    delete r;
}

/*
    Function: buildTree (Wrapper)
    Parameters: Vector of strings representing node locations.
    Return Value: None (void)
    Description: Builds a binary tree from a given vector of node names.
                 If the input vector is empty, the function returns without modifying the tree.
*/
void binTree::buildTree(std::vector<std::string> locations)
{
    if (locations.empty())
        return;

    root = buildTree(new binTreeNode(), locations, 0);
}

/*
    Function: buildTree (Recursive)
    Parameters: Pointer to a binary tree node, vector of node locations, index.
    Return Value: Pointer to the root of the newly constructed subtree.
    Description: Recursively constructs a binary tree in a preorder manner.
                 Base Case: If the index is out of bounds or the node is marked "_", return nullptr.
*/
binTreeNode *binTree::buildTree(binTreeNode *r, std::vector<std::string> locations, int index)
{
    if (index >= locations.size() || index < 0 || locations[index] == "_")
    {
        delete r;
        return nullptr;
    }

    r->location = locations[index];

    r->left = buildTree(new binTreeNode(), locations, (index * 2) + 1);
    r->right = buildTree(new binTreeNode(), locations, (index + 1) * 2);

    return r;
}

/*
    Function: zigzag (Wrapper)
    Parameters: None
    Return Value: A vector of strings representing the longest zig-zag path in the tree.
    Description: Finds the longest zig-zag path starting from the root.
                 Handles edge cases where the tree is empty or contains a single node.
*/
std::vector<std::string> binTree::zigzag()
{
    std::vector<std::string> leftPath, rightPath, path;

    if (root == nullptr)
        return path;

    if (root->left && root->left->right)
    {
        path.push_back(root->location);
        leftPath = binTree::zigzag(root->left, true, path);
    }
    else
        leftPath = binTree::zigzag(root->left, true, path);

    path.clear();

    if (root->right && root->right->left)
    {
        path.push_back(root->location);
        rightPath = binTree::zigzag(root->right, false, path);
    }
    else
        rightPath = binTree::zigzag(root->right, false, path);

    return (leftPath.size() > rightPath.size()) ? leftPath : rightPath;
}

/*
    Function: zigzag (Recursive)
    Parameters: Pointer to a binary tree node, boolean indicating direction (true = left, false = right), current path vector.
    Return Value: A vector representing the longest zig-zag path from the given node.
    Description: Recursively explores the longest zig-zag path from a given node.
                 Base Case: If the node is null, return the current path.
                 Uses std::move to optimize return values and avoid unnecessary copies.
*/
std::vector<std::string> binTree::zigzag(binTreeNode *r, bool childType, std::vector<std::string> path)
{
    if (!r) return path;

    path.push_back(r->location);

    std::vector<std::string> leftPath, rightPath;

    if (childType)
        rightPath = zigzag(r->right, false, path);
    else
        leftPath = zigzag(r->left, true, path);

    return (leftPath.size() > rightPath.size()) ? std::move(leftPath) : std::move(rightPath);
}
