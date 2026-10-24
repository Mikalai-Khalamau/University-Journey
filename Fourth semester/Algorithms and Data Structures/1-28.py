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


def compute_height(node):
    """Вычисление высоты поддерева."""
    if node is None:
        return -1
    return 1 + max(compute_height(node.left), compute_height(node.right))


def find_equal_height_nodes(root):
    """Поиск всех вершин с равными высотами поддеревьев."""
    result = []

    def dfs(node):
        if node is None:
            return
        left_h = compute_height(node.left)
        right_h = compute_height(node.right)
        if left_h == right_h:
            result.append(node.key)
        dfs(node.left)
        dfs(node.right)

    dfs(root)
    return result


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
    """Решение задачи 28."""
    root = None
    for k in keys:
        root = insert(root, k)

    equal_height_nodes = find_equal_height_nodes(root)
    if not equal_height_nodes:
        return []

    equal_height_nodes.sort()
    median_node = equal_height_nodes[(len(equal_height_nodes) - 1) // 2]

    root = delete_node(root, median_node)
    return preorder(root)


# === Прогон тестов ===
if __name__ == "__main__":
    print("Тест 1:", solve([5, 3, 7, 2, 4, 6, 8]))  # [4, 3, 2, 7, 6, 8]
    print("Тест 2:", solve([10]))  # []
    print("Тест 3:", solve([5, 3, 7, 2]))  # [5, 3, 7]