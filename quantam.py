import hashlib
import math
import time
import numpy as np

class QuantumQubitSimulator:
    def __init__(self):
        self.state = np.array([1.0, 0.0], dtype=np.complex128)
        self.Hadamard = (1.0 / math.sqrt(2)) * np.array([[1.0, 1.0], [1.0, -1.0]], dtype=np.complex128)

    def apply_hadamard_gate(self):
        self.state = np.dot(self.Hadamard, self.state)

    def collapse_wavefunction(self, target_ascii):
        prob_0 = float(np.abs(self.state[0])**2)
        prob_1 = float(np.abs(self.state[1])**2)
        phase_angle = float(np.angle(self.state[0] * np.conj(self.state[1])))
        return target_ascii, prob_0, prob_1, phase_angle

class Block:
    def __init__(self, index, char, prev_hash, quantum_entropy):
        self.index = index
        self.timestamp = time.time()
        self.char = char
        self.prev_hash = prev_hash
        self.quantum_entropy = quantum_entropy
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        payload = f"{self.index}{self.timestamp}{self.char}{self.prev_hash}{self.quantum_entropy}{self.nonce}"
        return hashlib.sha256(payload.encode('utf-8')).hexdigest()

    def mine_block(self, difficulty=4):
        target_prefix = "0" * difficulty
        start_time = time.time()
        while not self.hash.startswith(target_prefix):
            self.nonce += 1
            self.hash = self.calculate_hash()
        return (time.time() - start_time) * 1000

def main():
    target_string = "Hello World"
    difficulty = 4
    
    print("=" * 75)
    print("  QUANTUM-ENHANCED PROOF-OF-WORK DISPATCHER v4.2.0-ENTERPRISE")
    print("=" * 75)
    
    blockchain = []
    prev_hash = "0" * 64
    q_sim = QuantumQubitSimulator()

    for idx, char in enumerate(target_string):
        q_sim.apply_hadamard_gate()
        _, p0, p1, phase = q_sim.collapse_wavefunction(ord(char))
        entropy_str = f"P0:{p0:.2f}|P1:{p1:.2f}|Phase:{phase:.4f}"

        block = Block(index=idx, char=char, prev_hash=prev_hash, quantum_entropy=entropy_str)
        mine_time_ms = block.mine_block(difficulty=difficulty)
        
        blockchain.append(block)
        prev_hash = block.hash
        print(f"Index {idx} | Char '{char}' | Nonce {block.nonce} | Mined Hash {block.hash[:24]}...")

    reconstructed_msg = "".join([b.char for b in blockchain])
    print(f"\n[FINAL SYSTEM STDOUT OUTPUT]: {reconstructed_msg}\n")

if __name__ == "__main__":
    main()
