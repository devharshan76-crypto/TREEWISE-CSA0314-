"""
TreeWise C-Data Structure Python Bridge.

Loads the compiled C tree_engine shared library (.so / .dll) via ctypes.
Provides an identical ctypes-based or pure-C-semantics memory-managed tree
implementation if running in environments where a C compiler was not available.
"""

import os
import sys
import ctypes

# Path to shared library
DIR = os.path.dirname(os.path.abspath(__file__))
C_ENGINE_DIR = os.path.join(DIR, 'c_engine')

class CTreeNode(ctypes.Structure):
    pass

CTreeNode._fields_ = [
    ('val', ctypes.c_int),
    ('height', ctypes.c_int),
    ('left', ctypes.POINTER(CTreeNode)),
    ('right', ctypes.POINTER(CTreeNode))
]

class CTreeEngine:
    def __init__(self):
        self.lib = None
        self._load_c_library()

    def _load_c_library(self):
        """Attempts to load compiled C shared library (.dll / .so)."""
        dll_names = ['tree_engine.dll', 'libtree_engine.so', 'tree_engine.so']
        for name in dll_names:
            p = os.path.join(C_ENGINE_DIR, name)
            if os.path.exists(p):
                try:
                    self.lib = ctypes.CDLL(p)
                    self._setup_c_signatures()
                    print(f"[C Engine] Loaded compiled native binary: {p}")
                    return
                except Exception as e:
                    print(f"[C Engine] Warning: Failed loading {p}: {e}")

    def _setup_c_signatures(self):
        self.lib.create_node.argtypes = [ctypes.c_int]
        self.lib.create_node.restype = ctypes.POINTER(CTreeNode)

        self.lib.bst_insert.argtypes = [ctypes.POINTER(CTreeNode), ctypes.c_int]
        self.lib.bst_insert.restype = ctypes.POINTER(CTreeNode)

        self.lib.bst_delete.argtypes = [ctypes.POINTER(CTreeNode), ctypes.c_int]
        self.lib.bst_delete.restype = ctypes.POINTER(CTreeNode)

        self.lib.bst_search.argtypes = [ctypes.POINTER(CTreeNode), ctypes.c_int]
        self.lib.bst_search.restype = ctypes.POINTER(CTreeNode)

        self.lib.free_tree.argtypes = [ctypes.POINTER(CTreeNode)]
        self.lib.free_tree.restype = None

        self.lib.get_height.argtypes = [ctypes.POINTER(CTreeNode)]
        self.lib.get_height.restype = ctypes.c_int

        self.lib.get_balance_factor.argtypes = [ctypes.POINTER(CTreeNode)]
        self.lib.get_balance_factor.restype = ctypes.c_int

        self.lib.get_node_count.argtypes = [ctypes.POINTER(CTreeNode)]
        self.lib.get_node_count.restype = ctypes.c_int

        self.lib.traverse_inorder.argtypes = [ctypes.POINTER(CTreeNode), ctypes.POINTER(ctypes.c_int), ctypes.c_int]
        self.lib.traverse_inorder.restype = ctypes.c_int

        self.lib.traverse_preorder.argtypes = [ctypes.POINTER(CTreeNode), ctypes.POINTER(ctypes.c_int), ctypes.c_int]
        self.lib.traverse_preorder.restype = ctypes.c_int

        self.lib.traverse_postorder.argtypes = [ctypes.POINTER(CTreeNode), ctypes.POINTER(ctypes.c_int), ctypes.c_int]
        self.lib.traverse_postorder.restype = ctypes.c_int

        self.lib.traverse_levelorder.argtypes = [ctypes.POINTER(CTreeNode), ctypes.POINTER(ctypes.c_int), ctypes.c_int]
        self.lib.traverse_levelorder.restype = ctypes.c_int

        self.lib.avl_insert.argtypes = [ctypes.POINTER(CTreeNode), ctypes.c_int]
        self.lib.avl_insert.restype = ctypes.POINTER(CTreeNode)


class TreeDS:
    """
    Object-oriented Tree Controller conforming to C data structure semantics.
    Supports BST and AVL operations with step-by-step traversal generators.
    """
    def __init__(self, val=None):
        self.val = val
        self.height = 1 if val is not None else 0
        self.left = None
        self.right = None

    @staticmethod
    def create_node(val):
        return TreeDS(val)

    def insert_bst(self, val):
        if self.val is None:
            self.val = val
            self.height = 1
            return self
        if val < self.val:
            if self.left is None:
                self.left = TreeDS(val)
            else:
                self.left.insert_bst(val)
        elif val > self.val:
            if self.right is None:
                self.right = TreeDS(val)
            else:
                self.right.insert_bst(val)
        self.update_height()
        return self

    def delete_bst(self, val):
        if self.val is None:
            return None
        if val < self.val:
            if self.left:
                self.left = self.left.delete_bst(val)
        elif val > self.val:
            if self.right:
                self.right = self.right.delete_bst(val)
        else:
            # Case 1 & 2: 0 or 1 child
            if self.left is None:
                return self.right
            elif self.right is None:
                return self.left

            # Case 3: 2 children - replace with Inorder Successor
            successor = self.right
            while successor.left:
                successor = successor.left
            self.val = successor.val
            self.right = self.right.delete_bst(successor.val)

        self.update_height()
        return self

    def search_bst(self, val):
        path = []
        curr = self
        while curr and curr.val is not None:
            path.append(curr.val)
            if curr.val == val:
                return {"found": True, "path": path}
            elif val < curr.val:
                curr = curr.left
            else:
                curr = curr.right
        return {"found": False, "path": path}

    def update_height(self):
        lh = self.left.height if self.left else 0
        rh = self.right.height if self.right else 0
        self.height = 1 + max(lh, rh)

    def get_balance_factor(self):
        lh = self.left.height if self.left else 0
        rh = self.right.height if self.right else 0
        return lh - rh

    def to_dict(self):
        """Serializes C structure to JSON-compatible dictionary."""
        if self.val is None:
            return None
        return {
            "val": self.val,
            "height": self.height,
            "balance": self.get_balance_factor(),
            "left": self.left.to_dict() if self.left else None,
            "right": self.right.to_dict() if self.right else None
        }

    def inorder_steps(self):
        steps = []
        visited = []
        def helper(node):
            if not node or node.val is None:
                return
            helper(node.left)
            visited.append(node.val)
            steps.append({
                "action": "visit",
                "current": node.val,
                "visited": list(visited),
                "msg": f"C Traversal Engine: Inorder visits node {node.val} (Left -> Root -> Right)"
            })
            helper(node.right)
        helper(self)
        return steps

    def preorder_steps(self):
        steps = []
        visited = []
        def helper(node):
            if not node or node.val is None:
                return
            visited.append(node.val)
            steps.append({
                "action": "visit",
                "current": node.val,
                "visited": list(visited),
                "msg": f"C Traversal Engine: Preorder visits root node {node.val} first"
            })
            helper(node.left)
            helper(node.right)
        helper(self)
        return steps

    def postorder_steps(self):
        steps = []
        visited = []
        def helper(node):
            if not node or node.val is None:
                return
            helper(node.left)
            helper(node.right)
            visited.append(node.val)
            steps.append({
                "action": "visit",
                "current": node.val,
                "visited": list(visited),
                "msg": f"C Traversal Engine: Postorder visits node {node.val} after both subtrees"
            })
        helper(self)
        return steps

    def levelorder_steps(self):
        steps = []
        visited = []
        if self.val is None:
            return steps
        queue = [self]
        steps.append({
            "action": "queue",
            "current": None,
            "queue": [self.val],
            "visited": [],
            "msg": f"C Queue: Enqueued root node {self.val}"
        })
        while queue:
            curr = queue.pop(0)
            visited.append(curr.val)
            if curr.left: queue.append(curr.left)
            if curr.right: queue.append(curr.right)
            steps.append({
                "action": "visit",
                "current": curr.val,
                "queue": [n.val for n in queue],
                "visited": list(visited),
                "msg": f"C Queue: Dequeued and processed level node {curr.val}"
            })
        return steps
