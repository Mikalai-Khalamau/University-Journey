class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.parent = None


def insert(root, key):
    """Вставка ключа в BST с поддержкой ссылок на родителей."""
    if root is None:
        return Node(key)
    curr = root
    while True:
        if key < curr.key:
            if curr.left is None:
                curr.left = Node(key)
                curr.left.parent = curr
                break
            curr = curr.left
        elif key > curr.key:
            if curr.right is None:
                curr.right = Node(key)
                curr.right.parent = curr
                break
            curr = curr.right
        else:
            break
    return root


def compute_heights(node, heights):
    """Вычисление высот поддеревьев для всех вершин."""
    if node is None:
        return -1
    left_h = compute_heights(node.left, heights)
    right_h = compute_heights(node.right, heights)
    heights[node.key] = (left_h + 1, right_h + 1)
    return max(left_h, right_h) + 1


def find_diameter_and_paths(root):
    """Поиск диаметра и подсчёт путей максимальной длины."""
    if root is None:
        return 0, {}

    heights = {}
    compute_heights(root, heights)

    D = 0
    for key, (lh, rh) in heights.items():
        D = max(D, lh + rh)

    path_count = {}

    if D == 0:
        path_count[root.key] = 1
        return D, path_count

    def get_nodes_at_depth(node, depth, target_depth, result):
        if node is None:
            return
        if depth == target_depth:
            result.append(node)
            return
        get_nodes_at_depth(node.left, depth + 1, target_depth, result)
        get_nodes_at_depth(node.right, depth + 1, target_depth, result)

    def get_path_nodes(u, v, lca):
        path = []
        curr = u
        while curr != lca:
            path.append(curr)
            curr = curr.parent
        path.append(lca)
        path_v = []
        curr = v
        while curr != lca:
            path_v.append(curr)
            curr = curr.parent
        path.extend(reversed(path_v))
        return path

    def dfs(node):
        if node is None:
            return
        lh, rh = heights[node.key]

        if lh + rh == D and lh > 0 and rh > 0:
            left_nodes = []
            right_nodes = []
            get_nodes_at_depth(node.left, 1, lh, left_nodes)
            get_nodes_at_depth(node.right, 1, rh, right_nodes)
            for u in left_nodes:
                for w in right_nodes:
                    path = get_path_nodes(u, w, node)
                    for v in path:
                        path_count[v.key] = path_count.get(v.key, 0) + 1

        if lh == D and lh > 0:
            left_nodes = []
            get_nodes_at_depth(node.left, 1, lh, left_nodes)
            for u in left_nodes:
                path = get_path_nodes(u, node, node)
                for v in path:
                    path_count[v.key] = path_count.get(v.key, 0) + 1

        if rh == D and rh > 0:
            right_nodes = []
            get_nodes_at_depth(node.right, 1, rh, right_nodes)
            for w in right_nodes:
                path = get_path_nodes(node, w, node)
                for v in path:
                    path_count[v.key] = path_count.get(v.key, 0) + 1

        dfs(node.left)
        dfs(node.right)

    dfs(root)
    return D, path_count


def find_max_and_parent(node):
    """Поиск максимального элемента в поддереве и его родителя."""
    parent = None
    current = node
    while current.right is not None:
        parent = current
        current = current.right
    return current, parent


def delete_node(root, key):
    """Правое удаление вершины по ключу."""
    if root is None:
        return None

    curr = root
    parent = None
    while curr is not None and curr.key != key:
        parent = curr
        if key < curr.key:
            curr = curr.left
        else:
            curr = curr.right

    if curr is None:
        return root

    if curr.left is None:
        replacement = curr.right
    elif curr.right is None:
        replacement = curr.left
    else:
        max_node, max_parent = find_max_and_parent(curr.left)
        curr.key = max_node.key
        if max_parent is None:
            curr.left = max_node.left
            if max_node.left:
                max_node.left.parent = curr
        else:
            max_parent.right = max_node.left
            if max_node.left:
                max_node.left.parent = max_parent
        return root

    if replacement:
        replacement.parent = parent

    if parent is None:
        return replacement
    elif parent.left == curr:
        parent.left = replacement
    else:
        parent.right = replacement

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
    """Решение задачи 10."""
    root = None
    for k in keys:
        root = insert(root, k)

    D, path_count = find_diameter_and_paths(root)

    if not path_count:
        return []

    max_count = max(path_count.values())
    to_delete = sorted([k for k, v in path_count.items() if v == max_count])

    for k in to_delete:
        root = delete_node(root, k)

    return preorder(root)


# === Прогон тестов ===
if __name__ == "__main__":
    print("Тест 1:", solve([5, 3, 7, 2, 4, 6, 8]))  # [4, 2, 6, 8]
    print("Тест 2:", solve([10]))  # []
    print("Тест 3:", solve([5, 3, 7, 2, 4]))  # [4, 2]