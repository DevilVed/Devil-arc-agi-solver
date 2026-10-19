# Bolt's Journal - Critical Learnings

## 2025-05-18 - Concurrent Sandbox Evaluation in ARC-AGI
**Learning:** In candidate evaluation routines, running subprocess-based sandbox calls (`sandbox.run`) sequentially across $N$ training examples and $M$ test examples causes significant latency ($O((N+M) \cdot T)$).
**Action:** Use `asyncio.gather(*train_tasks, *test_tasks)` to evaluate all training and test examples concurrently, reducing solution evaluation time to $O(\max(T))$.
