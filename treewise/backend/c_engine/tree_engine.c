#include "tree_engine.h"

static int max(int a, int b) {
    return (a > b) ? a : b;
}

TreeNode* create_node(int val) {
    TreeNode *node = (TreeNode*)malloc(sizeof(TreeNode));
    if (!node) return NULL;
    node->val = val;
    node->height = 1;
    node->left = NULL;
    node->right = NULL;
    return node;
}

int get_height(TreeNode *node) {
    if (!node) return 0;
    return node->height;
}

int get_balance_factor(TreeNode *node) {
    if (!node) return 0;
    return get_height(node->left) - get_height(node->right);
}

static void update_height(TreeNode *node) {
    if (node) {
        node->height = 1 + max(get_height(node->left), get_height(node->right));
    }
}

TreeNode* bst_insert(TreeNode *root, int val) {
    if (!root) return create_node(val);
    if (val < root->val) {
        root->left = bst_insert(root->left, val);
    } else if (val > root->val) {
        root->right = bst_insert(root->right, val);
    }
    update_height(root);
    return root;
}

static TreeNode* min_value_node(TreeNode *node) {
    TreeNode *curr = node;
    while (curr && curr->left != NULL) {
        curr = curr->left;
    }
    return curr;
}

TreeNode* bst_delete(TreeNode *root, int val) {
    if (!root) return NULL;

    if (val < root->val) {
        root->left = bst_delete(root->left, val);
    } else if (val > root->val) {
        root->right = bst_delete(root->right, val);
    } else {
        // Node with only one child or no child
        if (!root->left) {
            TreeNode *temp = root->right;
            free(root);
            return temp;
        } else if (!root->right) {
            TreeNode *temp = root->left;
            free(root);
            return temp;
        }

        // Node with two children: Get inorder successor (smallest in the right subtree)
        TreeNode *temp = min_value_node(root->right);
        root->val = temp->val;
        root->right = bst_delete(root->right, temp->val);
    }
    update_height(root);
    return root;
}

TreeNode* bst_search(TreeNode *root, int val) {
    if (!root || root->val == val) return root;
    if (val < root->val) return bst_search(root->left, val);
    return bst_search(root->right, val);
}

void free_tree(TreeNode *root) {
    if (!root) return;
    free_tree(root->left);
    free_tree(root->right);
    free(root);
}

int get_node_count(TreeNode *root) {
    if (!root) return 0;
    return 1 + get_node_count(root->left) + get_node_count(root->right);
}

/* --- Traversals --- */
static int inorder_helper(TreeNode *root, int *buffer, int *idx, int max_size) {
    if (!root || *idx >= max_size) return *idx;
    inorder_helper(root->left, buffer, idx, max_size);
    if (*idx < max_size) {
        buffer[(*idx)++] = root->val;
    }
    inorder_helper(root->right, buffer, idx, max_size);
    return *idx;
}

int traverse_inorder(TreeNode *root, int *buffer, int max_size) {
    int idx = 0;
    return inorder_helper(root, buffer, &idx, max_size);
}

static int preorder_helper(TreeNode *root, int *buffer, int *idx, int max_size) {
    if (!root || *idx >= max_size) return *idx;
    if (*idx < max_size) {
        buffer[(*idx)++] = root->val;
    }
    preorder_helper(root->left, buffer, idx, max_size);
    preorder_helper(root->right, buffer, idx, max_size);
    return *idx;
}

int traverse_preorder(TreeNode *root, int *buffer, int max_size) {
    int idx = 0;
    return preorder_helper(root, buffer, &idx, max_size);
}

static int postorder_helper(TreeNode *root, int *buffer, int *idx, int max_size) {
    if (!root || *idx >= max_size) return *idx;
    postorder_helper(root->left, buffer, idx, max_size);
    postorder_helper(root->right, buffer, idx, max_size);
    if (*idx < max_size) {
        buffer[(*idx)++] = root->val;
    }
    return *idx;
}

int traverse_postorder(TreeNode *root, int *buffer, int max_size) {
    int idx = 0;
    return postorder_helper(root, buffer, &idx, max_size);
}

int traverse_levelorder(TreeNode *root, int *buffer, int max_size) {
    if (!root || max_size <= 0) return 0;
    TreeNode **queue = (TreeNode**)malloc(sizeof(TreeNode*) * 1024);
    int front = 0, rear = 0, idx = 0;

    queue[rear++] = root;
    while (front < rear && idx < max_size) {
        TreeNode *curr = queue[front++];
        buffer[idx++] = curr->val;

        if (curr->left && rear < 1024) queue[rear++] = curr->left;
        if (curr->right && rear < 1024) queue[rear++] = curr->right;
    }

    free(queue);
    return idx;
}

/* --- AVL Rotations & Insert --- */
TreeNode* right_rotate(TreeNode *y) {
    TreeNode *x = y->left;
    TreeNode *T2 = x->right;

    x->right = y;
    y->left = T2;

    update_height(y);
    update_height(x);

    return x;
}

TreeNode* left_rotate(TreeNode *x) {
    TreeNode *y = x->right;
    TreeNode *T2 = y->left;

    y->left = x;
    x->right = T2;

    update_height(x);
    update_height(y);

    return y;
}

TreeNode* avl_insert(TreeNode *node, int val) {
    if (!node) return create_node(val);

    if (val < node->val) {
        node->left = avl_insert(node->left, val);
    } else if (val > node->val) {
        node->right = avl_insert(node->right, val);
    } else {
        return node; // Duplicate keys not allowed
    }

    update_height(node);
    int balance = get_balance_factor(node);

    // Left Left Case
    if (balance > 1 && val < node->left->val)
        return right_rotate(node);

    // Right Right Case
    if (balance < -1 && val > node->right->val)
        return left_rotate(node);

    // Left Right Case
    if (balance > 1 && val > node->left->val) {
        node->left = left_rotate(node->left);
        return right_rotate(node);
    }

    // Right Left Case
    if (balance < -1 && val < node->right->val) {
        node->right = right_rotate(node->right);
        return left_rotate(node);
    }

    return node;
}
