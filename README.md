Dante's HELL "o" World

"Abandon all sanity, ye who compile here."

Winner: "Gloriously Over-Engineered" Award

How to Gloriously Over-Engineer a Simple Concept: A 'Hello World' That Makes Your Brain IMPLODE.

HackoberFest 2026 — Fort Monroe, VA (October 17, 2026)

Overview

Dante’s HELL "o" World is an intentionally unhinged, multi-tiered esoteric computing architecture engineered and showcased at HackoberFest 26 at historic Fort Monroe, Virginia. Instead of printing a standard string with a single print("Hello, World") statement, this project descends through all nine computational circles of the underworld—running independent, hyper-complex esoteric programs and over-engineered systems across disparate paradigms to assemble the greeting's characters.

From stack-based baking recipes in physical mixing bowls and 59,049-trit ternary virtual machines to raw Linux hardware syscalls, compile-time template recursion, and a quantum Proof-of-Work consensus ledger, every character is forged in its own circle of torment:

  <img src="Dantes%20Circles%201st%20image.jpg" alt="Dante's Circles Architecture" width="80%" />    

System Architecture & File Structure

├── assets/
│   ├── dantes_hell_o_world.gif     # Looping visual identity
│   └── intro_cerberus.mp4          # Hackathon showcase video
├── src/
│   ├── fibonacci_l.bf              # Brainfuck tape routine -> 'L'
│   ├── soufle_o.chef               # Chef stack-based recipe -> 'O'
│   └── circle9_r.mal               # Malbolge ternary VM code -> 'R'
├── scripts/
│   ├── malbolge_vm_trace.py        # Malbolge VM trace emulator
│   └── orchestrate.py              # Automated pipeline execution runner
└── README.md


The Circles of Execution

1. Circle I: The Memory Tape (.bf)

Target Output: L (ASCII 76)

Engine: Brainfuck

Design Pattern: Bypasses basic multiplication loops (8 * 9 + 4) in favor of dynamic cell allocation, calculating intermediate Fibonacci-spaced offsets across memory pointers before consolidating the target accumulator.

2. Circle II: The Culinary Stack (.chef)

Target Output: O (ASCII 79)

Engine: Chef Esolang

Design Pattern: Treats computational storage as physical kitchenware. Utilizes multiple mixing bowls, ingredient-based integer assignments, and conditional sub-recipes to manipulate the runtime stack before liquefying and pouring the result into the output vessel.

3. Circle IX: The Frozen Abyss (.mal)

Target Output: R (ASCII 82)

Engine: Malbolge

Design Pattern: A 1,033-byte routine operating on base-3 trits. Employs pointer encryption, the ternary "crazy" operator table, and self-modifying memory loops to coerce execution into emitting a single valid register state without triggering an immediate crash or infinite memory fault. Validated using the accompanying Python trace emulator (scripts/malbolge_vm_trace.py).

Local Execution & Verification

Prerequisites

Ensure you have Python 3.10+ installed, along with your chosen esoteric interpreters:

Brainfuck: beef or any standard C-based runner

Chef: chef-py or an equivalent Chef compiler

Malbolge: Run natively via scripts/malbolge_vm_trace.py

Manual Execution

# Circle I: Brainfuck
beef src/fibonacci_l.bf

# Circle II: Chef
chef-py src/soufle_o.chef

# Circle IX: Malbolge (Trace & Verification)
python3 scripts/malbolge_vm_trace.py src/circle9_r.mal


Automated Pipeline Orchestration

To run all circles sequentially and assemble the final output in a single pass:

python3 scripts/orchestrate.py


Pipeline Flow:

Spawns child subshells targeting each esoteric file (.bf, .chef, .mal).

Buffers standard stream channels to avoid cross-circle memory pollution.

Evaluates intermediate register snapshots against ASCII verification matrices.

Aggregates the character buffers into the final output banner.

Team & Credits

Engineered with dark arts and excessive enthusiasm by:

Debs Kernstock

Vanessa Gerardo

Camden Carr
