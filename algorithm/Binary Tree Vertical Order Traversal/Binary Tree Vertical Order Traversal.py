class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class Solution:
    def verticalOrder(self, root):
        """
        :type root: TreeNode
        :rtype: List[int]
        """
        if not root:
            return None
        self.res = [[root.val]]
        self.pos = 0
        self.helper(root)
        return self.res

    """

       def helper(self, node):
           if node.left:
               if self.pos == 0:
                   self.res.insert(self.pos, [node.left.val])
                   self.pos += 1
               else:
                   self.res[self.pos - 1].append(node.left.val)

           if node.right:
               if self.pos + 1 == len(self.res):
                   self.res.insert(len(self.res), [node.right.val])
               else:
                   self.res[self.pos + 1].append(node.right.val)

           if node.left:
               self.pos -= 1
               self.helper(node.left)
               self.pos += 1

           if node.right:
               self.pos += 1
               self.helper(node.right)
               self.pos -= 1
    """

    def helper(self, node):
        if node.left:
            if self.pos == 0:
                self.res.insert(self.pos, [node.left.val])
            else:
                self.res[self.pos - 1].append(node.left.val)
                self.pos -= 1
            self.helper(node.left)

        if node.right:
            print(self.res, self.pos)
            if self.pos + 1 == len(self.res):
                self.res.insert(len(self.res), [node.right.val])
                self.pos += 1
            else:
                self.res[self.pos + 1].append(node.right.val)
            self.helper(node.right)
        else:
            self.pos += 1
