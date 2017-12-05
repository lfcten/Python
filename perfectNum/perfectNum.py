import math
def helper(n):
    if n == 1:
        return 1

    end = int(math.sqrt(n))

    if end * end == n:
        return 1

    return min([1 + helper(n - i * i) for i in range(1, end + 1) if i * i <= n // 2])

print(helper(16))

from functools import lru_cache
"""
public class Solution {
    public int numSquares(int n) {
        int[] dp = new int[n + 1];
    	Arrays.fill(dp, Integer.MAX_VALUE);
    	dp[0] = 0;
    	for(int i = 1; i <= n; ++i) {
    		int min = Integer.MAX_VALUE;
    		int j = 1;
    		while(i - j*j >= 0) {
    			min = Math.min(min, dp[i - j*j] + 1);
    			++j;
    		}
    		dp[i] = min;
    	}		
    	return dp[n];  
    }
}"""