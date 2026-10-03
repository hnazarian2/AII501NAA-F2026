# AII501NAA-F2026

# AI Activity 1

## Setup
Describe any software, programming language, or dependencies required to run
the implementation.

## Execution
Explain how to run the spam filter agent and breadth-first search implementation.

## Testing
Explain the test cases used to verify the solutions.

For the water-jug problem, testing includes:
- Initial state: (0, 0, 0)
- Goal condition: at least one jug contains exactly 1 gallon
- Fill, empty, and pour actions
- BFS correctly identifies a reachable goal state

## Assumptions
### Spam Filter
- Emails are provided in .eml format.
- Allow-listed domains are always classified as non-spam.
- Restrict-listed domains are classified as spam unless overridden by the
  higher-priority allow-list rule.
- More than 5 bad words means 6 or more bad words.

### Water Jug Search
- The jugs initially contain no water.
- The capacities are 12, 8, and 3 gallons.
- A jug can be filled completely from the faucet.
- A jug can be emptied completely onto the ground.
- When pouring between jugs, pouring continues until the source is empty
  or the destination is full.
- Water amounts are measured in whole gallons.
- A goal is reached when any jug contains exactly 1 gallon.
