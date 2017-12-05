class Solution:
    def combinationSum(self, candidates, target):
        """
        :type candidates: List[int]
        :type target: int
        :rtype: List[List[int]]
        """
        candidates.sort()
        dp = [[[]]] + [[] for i in range(target)]
        for i in range(1, target + 1):
            for number in candidates:
                if number > i: break
                for L in dp[i - number]:
                    if not L or number >= L[-1]:
                        # print(dp[i] + L +[number])
                        dp[i] += L + [number],

        return dp[target]

if __name__ == "__main__":
    s_instance = Solution()
    print(s_instance.combinationSum([2,3,6,7], 4))
