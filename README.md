This repository contains solutions to four tasks covering fundamental AI concepts. Each assignment builds on the last, progressing from basic search algorithms to advanced probabilistic inference in the Pacman and Ghostbusters domains.

**1. Task 1: Search Algorithms (task1/)**
Topics: Uninformed & Informed Search, Heuristics
Key Files: p1.py–p7.py, parse.py
Tasks:

Implement DFS, BFS, UCS, Greedy Search, and A* for pathfinding in graphs.
Solve the 8-Queens Problem using local search.
Parse graph-based problems (states, transitions, heuristics).

**2. Task 2: Pacman Game Agents (task2/)**
Topics: Adversarial Search, Minimax, Expectimax, Evaluation Functions
Key Files: p1.py–p6.py, parse.py
Tasks:

Design agents for Pacman vs. Ghosts using:
Randomized play (Problem 1–3).
Reflex agents with evaluation functions (Problem 4).
Minimax and Expectimax (Problems 5–6).
Handle multi-ghost scenarios with turn-based mechanics.

**3. Task 3: Markov Decision Processes (task3/)**
Topics: MDPs, Value/Policy Iteration, Q-Learning
Key Files: p1.py–p4.py, parse.py
Tasks:

Model grid-world MDPs with stochastic transitions.
Implement policy evaluation, value iteration, and Q-learning with exploration.
Simulate episodes under noisy policies (e.g., 80% intended action, 20% noise).

**4. Task 4: Ghostbusters Probabilistic Inference (task4/)**
Topics: Bayes Nets, Particle Filtering, Exact/Approximate Inference
Key Files: inference.py, bustersAgents.py
Tasks:

Track invisible ghosts using:
Exact inference (Bayes’ nets).
Particle filters for scalable approximations.
Implement joint particle filters for multi-ghost tracking.
Optimize Pacman’s hunting strategy with belief distributions.

**Setup & Usage**
Requirements: Python 3.6+ (no external libraries needed).

Run Autograders:

bash
python autograder.py -q qX  # For task4 questions
python pX.py -Y             # For A1–A3 (X=problem, Y=test case)
Visualization: Use --no-graphics for faster testing.
