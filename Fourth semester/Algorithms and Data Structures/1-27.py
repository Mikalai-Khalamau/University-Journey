class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None


def insert(root, key):
    """Вставка ключа в BST."""
    if root is None:
        return Node(key)
    if key < root.key:
        root.left = insert(root.left, key)
    elif key > root.key:
        root.right = insert(root.right, key)
    return root


def find_leaves(root):
    """Сбор всех листьев дерева."""
    leaves = []
    def dfs(node):
        if node is None:
            return
        if node.left is None and node.right is None:
            leaves.append(node.key)
        dfs(node.left)
        dfs(node.right)
    dfs(root)
    return leaves


def find_parent(root, target, parent=None):
    """Поиск родителя вершины с заданным ключом."""
    if root is None:
        return None
    if root.key == target:
        return parent
    left_res = find_parent(root.left, target, root)
    if left_res is not None:
        return left_res
    return find_parent(root.right, target, root)


def tree_size(root):
    """Количество вершин в дереве."""
    if root is None:
        return 0
    return 1 + tree_size(root.left) + tree_size(root.right)


def find_max_and_parent(node):
    """Поиск максимального элемента в поддереве и его родителя."""
    parent = None
    current = node
    while current.right is not None:
        parent = current
        current = current.right
    return current, parent


def delete_node(root, key):
    """Правое удаление вершины: замена на максимум левого поддерева."""
    if root is None:
        return None
    if key < root.key:
        root.left = delete_node(root.left, key)
    elif key > root.key:
        root.right = delete_node(root.right, key)
    else:
        # Вершина найдена
        if root.left is None:
            return root.right
        if root.right is None:
            return root.left
        # Два потомка: заменяем на максимум левого поддерева
        max_node, max_parent = find_max_and_parent(root.left)
        root.key = max_node.key
        if max_parent is None:
            root.left = max_node.left
        else:
            max_parent.right = max_node.left
    return root


def preorder(root):
    """Прямой (левый) обход дерева."""
    result = []
    def dfs(node):
        if node is None:
            return
        result.append(node.key)
        dfs(node.left)
        dfs(node.right)
    dfs(root)
    return result


def solve(keys):
    """Решение задачи 27."""
    root = None
    for k in keys:
        root = insert(root, k)

    leaves = find_leaves(root)
    if not leaves:
        return []

    leaves.sort()
    median_leaf = leaves[(len(leaves) - 1) // 2]

    # Если дерево из одной вершины — удаляем её
    if tree_size(root) == 1:
        return []

    parent = find_parent(root, median_leaf)
    if parent is None:
        return []

    root = delete_node(root, parent.key)
    return preorder(root)


# === Прогон тестов ===
if __name__ == "__main__":
    print("Тест 1:", solve([5, 3, 7, 2, 4, 6, 8]))  # [5, 2, 4, 7, 6, 8]
    print("Тест 2:", solve([10]))                     # []
    print("Тест 3:", solve([5, 3, 7, 4]))            # [5, 4, 7]