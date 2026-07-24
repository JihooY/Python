# longest_factor_multiple_sequence.py

import time
import sys

N = 100
TIME_LIMIT_SEC = None  # None으로 바꾸면 끝까지 탐색. 오래 걸릴 수 있음.

nums = list(range(1, N + 1))
idx = {v: i for i, v in enumerate(nums)}
ALL = (1 << N) - 1

# 그래프 만들기:
# a와 b 중 하나가 다른 하나의 약수/배수이면 연결
adj = [0] * N

for i, a in enumerate(nums):
    for j in range(i + 1, N):
        b = nums[j]
        if a % b == 0 or b % a == 0:
            adj[i] |= 1 << j
            adj[j] |= 1 << i

degree = [adj[i].bit_count() for i in range(N)]

# 시작 가능 숫자: even and < 50
starts = [idx[x] for x in range(2, 50, 2)]


def bit_iter(mask):
    while mask: 
        lsb = mask & -mask
        yield lsb.bit_length() - 1
        mask ^= lsb


def reachable_count(cur, unused):
    """
    현재 cur에서 아직 안 쓴 숫자들만 이용해서
    이론상 더 갈 수 있는 숫자 개수 upper bound.
    이걸로 불가능한 가지를 잘라냄.
    """
    allowed = unused | (1 << cur)
    seen = 0
    stack = 1 << cur

    while stack:
        lsb = stack & -stack
        stack ^= lsb
        node = lsb.bit_length() - 1

        if seen & (1 << node):
            continue

        seen |= 1 << node
        stack |= adj[node] & allowed & ~seen

    return (seen & unused).bit_count()


def is_valid_sequence(seq):
    if not seq:
        return False

    if seq[0] % 2 != 0 or seq[0] >= 50:
        return False

    if len(seq) != len(set(seq)):
        return False

    for a, b in zip(seq, seq[1:]):
        if not (a % b == 0 or b % a == 0):
            return False

    return True


# 초반 best를 빨리 만들기 위한 greedy
def greedy_path(start):
    used = 1 << start
    path = [start]
    cur = start

    while True:
        candidates = adj[cur] & ~used
        if not candidates:
            break

        # 다음 선택지가 적은 숫자를 먼저 고름
        nxt = min(
            bit_iter(candidates),
            key=lambda x: ((adj[x] & ~used).bit_count(), degree[x])
        )

        path.append(nxt)
        used |= 1 << nxt
        cur = nxt

    return path


best_path = []

for s in starts:
    p = greedy_path(s)
    if len(p) > len(best_path):
        best_path = p


start_time = time.time()
calls = 0
finished = True

sys.setrecursionlimit(10000)


def dfs(cur, used, path):
    global best_path, calls, finished

    calls += 1

    if TIME_LIMIT_SEC is not None and time.time() - start_time > TIME_LIMIT_SEC:
        finished = False
        raise TimeoutError

    if len(path) > len(best_path):
        best_path = path[:]
        result = [nums[i] for i in best_path]
        print(f"\nNew best length = {len(result)}")
        print(result)

    unused = ALL ^ used

    # 남은 연결 가능 숫자를 다 써도 best를 못 넘으면 중단
    if len(path) + reachable_count(cur, unused) <= len(best_path):
        return

    candidates = adj[cur] & ~used
    if not candidates:
        return

    # 선택지가 적은 쪽부터 탐색하면 긴 경로를 빨리 찾는 경우가 많음
    ordered = list(bit_iter(candidates))
    ordered.sort(
        key=lambda x: (
            (adj[x] & ~used).bit_count(),
            degree[x],
            nums[x]
        )
    )

    for nxt in ordered:
        dfs(nxt, used | (1 << nxt), path + [nxt])


try:
    for s in starts:
        dfs(s, 1 << s, [s])
except TimeoutError:
    pass


answer = [nums[i] for i in best_path]

print("\n========== RESULT ==========")
print("Finished exact search:", finished)
print("DFS calls:", calls)
print("Best length:", len(answer))
print("Best sequence:")
print(answer)
print("Valid:", is_valid_sequence(answer))


