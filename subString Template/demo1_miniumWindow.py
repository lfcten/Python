class Solution:
    def minWindow(self, s, t):
        counter = len(t)
        min_dis = counter + 1
        start = 0
        window_start = 0
        need = {}


        for char in t:
            need[char] = need.get(char, 0) + 1

        for end, val in enumerate(s):
            if s[end] in need:
                if need[val] > 0:
                    counter -= 1
                need[val] -= 1

            while not counter:
                if s[start] in need:
                    need[s[start]] += 1
                    if need[s[start]] > 0:
                        counter += 1

                start += 1

            if min_dis > end - start:
                min_dis = end - start + 1
                window_start = start - 1
        return "" if min_dis == len(t) else s[window_start: window_start + min_dis + 1]


a = Solution()

print(a.minWindow('faisnda', 'sda'))