class Solution:
    def partition(self, nums, p, r):
        l = p - 1
        while p < r:
            if nums[p] >= nums[r]:
                l += 1
                nums[l], nums[p] = nums[p], nums[l]
            p += 1
        nums[l + 1], nums[r] = nums[r], nums[l + 1]
        return l + 1


    # def quickSort(self, nums, s, e):
    #     if s < e:
    #         mid = self.partition(nums, s, e)
    #         self.quickSort(nums, s, mid - 1)
    #         self.quickSort(nums, mid + 1, e)


    def findKthLargest(self, nums, k):
        if nums:
            pos = self.partition(nums, 0, len(nums) - 1)
            if k < pos + 1:
                return self.findKthLargest(nums[:pos], k)
            elif k > pos + 1:
                return self.findKthLargest(nums[pos + 1:], k - pos - 1)
            else:
                return nums[pos]

if __name__ == "__main__":
    s_instance = Solution()
    nums = [3, 2, 1, 5, 6, 6, 4]
    print(s_instance.findKthLargest(nums, 4))
