# TreeWise - Full-Stack Tree Algorithms Learning Platform

TreeWise is an interactive full-stack learning platform for Tree Data Structures and Algorithms. It combines an interactive React dashboard with a Python REST API backend and a low-level C Data Structure Engine.

---

## 🏛️ Project Architecture

```text
treewise/
├── backend/
│   ├── c_engine/
│   │   ├── tree_engine.h       # C Data Structure interface (TreeNode struct)
│   │   ├── tree_engine.c       # BST & AVL algorithms, traversals in C
│   │   └── Makefile            # Compiles C shared library (.so / .dll)
│   ├── tree_bridge.py          # Python ctypes bridge interfacing with C engine
│   └── server.py               # Python REST API server (endpoints: /api/tree, /api/traverse, etc.)
├── frontend/
│   └── index.html              # Interactive drag-and-drop SVG tree dashboard
├── index.html                  # Root entry point configured for GitHub Pages
└── README.md                   # Project documentation
```

---

## 🚀 Running the Project Locally

### 1. Run with Python Backend + C Engine

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. (Optional) Compile C engine into a shared library:
   - On Linux/macOS:
     ```bash
     gcc -Wall -O3 -shared -fPIC -o c_engine/libtree_engine.so c_engine/tree_engine.c
     ```
   - On Windows (MinGW / GCC):
     ```bash
     gcc -Wall -O3 -shared -o c_engine/tree_engine.dll c_engine/tree_engine.c
     ```

3. Launch the Python server:
   ```bash
   python server.py
   ```

4. Open **`http://localhost:8000`** in your browser. The status badge will indicate **`Backend Connected`**.

---

## 🌐 Publishing to GitHub & GitHub Pages (Step-by-Step)

### Step 1: Initialize Git and Commit
In your terminal (inside the `treewise` folder):
```bash
git init
git add .
git commit -m "feat: complete TreeWise platform with C algorithms and Python backend"
```

### Step 2: Push to GitHub
1. Create a new public repository on [GitHub](https://github.com/new) named `treewise`.
2. Connect your local repository and push:
```bash
git branch -M main
git remote add origin https://github.com/<your-username>/treewise.git
git push -u origin main
```

### Step 3: Enable Free GitHub Pages Web Hosting
1. Go to your repository on GitHub.
2. Navigate to **Settings** > **Pages** (in the left sidebar).
3. Under **Build and deployment > Branch**:
   - Select **`main`** branch.
   - Select **`/(root)`** folder.
4. Click **Save**.
5. Within 1 minute, GitHub will provide your live website URL:
   `https://<your-username>.github.io/treewise/`

> **Note:** On GitHub Pages (static hosting), the frontend automatically switches to client-side mode so that the interactive tree, draggable nodes, and traversal visualizer work seamlessly without needing a live backend server.
