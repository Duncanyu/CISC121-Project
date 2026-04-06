# Binary Search Visualizer & Challenge

## Demos

### Working Binary Search Demo
![working_compressed](https://github.com/user-attachments/assets/8be6364f-1a79-4ba6-98b8-0133f860c807)

### Broken Binary Search Demo
![broken_compressed](https://github.com/user-attachments/assets/1495e670-3da0-4eef-a756-22369a2ca9f4)

### Human vs Binary Challenge Demo
![challenge_compressed](https://github.com/user-attachments/assets/4f95d8c5-e6db-44ba-83fb-8579e81b15a1)

---

## Problem Breakdown & Computational Thinking

### Decomposition

* Parse user input into a list of integers
* Check if the list is sorted
* Perform binary search and record each step
* Visualize each step (low, high, midpoint, decisions)
* Provide controls to step through the algorithm
* Create a challenge mode where the user reveals values manually
* Compare user performance against binary search efficiency

### Pattern Recognition

* Binary search repeatedly divides the search space in half
* Each step compares the midpoint with the target
* The search continues in either the left or right half depending on the comparison

### Abstraction

* The internal binary search process is simplified into visual steps
* Users do not need to understand implementation details like loops or indices
* In challenge mode, the full array is hidden to simulate decision-making

### Algorithm Design

* Input: List of numbers and a target value
* Process: Binary search algorithm determines position step-by-step
* Output: Found index (or not found) and visual explanation of each step

---

## How It Works

This app has two main modes:

### 1. Visualizer

* Users input a list and a target
* The app runs binary search and displays each step
* Shows:

  * Current search range
  * Midpoint selection
  * Decision (left or right)
* Includes playback controls (pause, resume, next, previous)

### 2. Challenge Mode

* The array is hidden
* The user reveals values one at a time
* The goal is to find the target using as few reveals as possible
* The app compares the user’s steps to binary search

This demonstrates why binary search is more efficient than guessing randomly.

---

## Steps to Run

1. Clone the repository

2. Install dependencies:
   ```pip install -r requirements.txt```

4. Run the app:
   ```python app.py```

---

## Hugging Face Link

https://huggingface.co/spaces/duncanfr/cisc121_project

---

## Testing & Verification

* Tested with sorted and unsorted lists
* Verified correct behavior when:

  * Target is at beginning
  * Target is at end
  * Target is in the middle
  * Target is not in the list
* Confirmed binary search step count matches expected results
* Verified visualizer correctly updates each step
* Tested challenge mode logic for:

  * Game completion conditions
  * Prevention of already selected/out of range indices

---

## Author

Duncan

---

## Acknowledgement

* AI was used to build Gradio interface and help with HTML. However, the majority of the backend/binary search was done without AI help.
* Gradio for UI development
* Inspired by algorithm visualization tools such as VisuAlgo
