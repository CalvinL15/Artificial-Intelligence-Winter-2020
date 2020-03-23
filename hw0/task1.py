# AI20S - HW0
# Student ID                : B06902100
# English Name              : Calvin Liusnando
# Chinese Name (optional)   : 劉益瑋


class Node(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class Solution(object):
    def sum_of_left_leaves(self, _root):
        """
        :type _root: Node
        :return type: int
        """
        # your code
        def dfs(Node, is_left):
        	if not Node:
        		return 0
        	if not Node.left and not Node.right:
        		if(is_left):
        			return Node.val
        		return 0
        	return dfs(Node.right, False) + dfs(Node.left, True)
        return dfs(_root, False)			


if __name__ == '__main__':
    # build tree
    roota = Node(3)
    roota.left = Node(9)
    roota.right = Node(20)
    roota.right.left = Node(15)
    roota.right.left.left = Node(-100)
    roota.right.left.left.left = Node(-30)
    roota.right.right = Node(7)
    sol = Solution()
    print(sol.sum_of_left_leaves(roota))


