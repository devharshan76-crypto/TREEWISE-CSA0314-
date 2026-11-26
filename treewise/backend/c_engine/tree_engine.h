#ifndef TREE_ENGINE_H
#define TREE_ENGINE_H

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

/**
 * Node structure for Binary Search Tree and AVL Tree in C.
 */
typedef struct TreeNode {
    int val;
    int height;
    struct TreeNode *left;
    struct TreeNode *right;
} TreeNode;

/**
 * Basic operations
 */
TreeNode* create_node(int val);
TreeNode* bst_insert(TreeNode *root, int val);
TreeNode* bst_delete(TreeNode *root, int val);
TreeNode* bst_search(TreeNode *root, int val);
void free_tree(TreeNode *root);

/**
 * Tree properties
 */
int get_height(TreeNode *node);
int get_balance_factor(TreeNode *node);
int get_node_count(TreeNode *root);

/**
 * Traversals (writes node values into output buffer, returns count)
 */
int traverse_inorder(TreeNode *root, int *buffer, int max_size);
int traverse_preorder(TreeNode *root, int *buffer, int max_size);
int traverse_postorder(TreeNode *root, int *buffer, int max_size);
int traverse_levelorder(TreeNode *root, int *buffer, int max_size);

/**
 * AVL Rotations & Insert
 */
TreeNode* right_rotate(TreeNode *y);
TreeNode* left_rotate(TreeNode *x);
TreeNode* avl_insert(TreeNode *node, int val);

#endif // TREE_ENGINE_H
