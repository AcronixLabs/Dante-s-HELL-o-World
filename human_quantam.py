import hashlib
import math
import time
import json
import numpy as np

class QuantumQubitSimulator:
    """Simulates 1-Qubit Quantum State Vectors and Hadamard Superposition."""
    def __init__(self):
        self.state = np.array([1.0, 0.0], dtype=np.complex128)
        self.Hadamard = (1.0 / math.sqrt(2)) * np.array([[1.0, 1.0], [1.0, -1.0]], dtype=np.complex128)

    def apply_hadamard_gate(self):
        self.state = np.dot(self.Hadamard, self.state)

    def collapse_wavefunction(self, target_ascii):
        prob_0 = float(np.abs(self.state[0])**2)
        prob_1 = float(np.abs(self.state[1])**2)
        phase_angle = float(np.angle(self.state[0] * np.conj(self.state[0])))
        return target_ascii, prob_0, prob_1, phase_angle

class QuantumBlock:
    def __init__(self, index, category, name, greeting, prev_hash, quantum_entropy):
        self.index = index
        self.timestamp = time.time()
        self.category = category
        self.name = name
        self.greeting = greeting
        self.prev_hash = prev_hash
        self.quantum_entropy = quantum_entropy
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        content = f"{self.index}{self.timestamp}{self.category}{self.name}{self.greeting}{self.prev_hash}{self.quantum_entropy}{self.nonce}"
        return hashlib.sha256(content.encode('utf-8')).hexdigest()

    def mine(self, difficulty=3):
        target = "0" * difficulty
        start = time.time()
        while not self.hash.startswith(target):
            self.nonce += 1
            self.hash = self.calculate_hash()
        return (time.time() - start) * 1000

def run_multilingual_quantum_pipeline():
    print("=" * 85)
    print("  MULTILINGUAL, REGIONAL, DUNE & STAR WARS QUANTUM PoW PIPELINE")
    print("=" * 85)
    
    with open("human_languages.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        
    q_sim = QuantumQubitSimulator()
    prev_hash = "0" * 64
    difficulty = 3
    blockchain = []
    
    # Process samples from National, Regional, and Fictional (Dune / Star Wars)
    samples = []
    for item in data.get("national_languages", [])[:4]:
        samples.append(("National", item["language"], item["greeting"]))
    for item in data.get("regional_dialects", [])[:4]:
        samples.append(("Regional", f"{item['region']} ({item['dialect']})", item["greeting"]))
    for item in data.get("fictional_languages", [])[:8]:
        samples.append(("Fictional", f"{item['universe']} - {item['language']}", item["greeting"]))
        
    for cat, name, greeting in samples:
        print(f"\n>>> MINING [{cat.upper()}] {name} -> '{greeting}'")
        print("-" * 85)
        
        mode_nonces = 0
        for idx, char in enumerate(greeting):
            q_sim.apply_hadamard_gate()
            _, p0, _, phase = q_sim.collapse_wavefunction(ord(char))
            entropy = f"P0:{p0:.2f}|Phase:{phase:.4f}"
            
            block = QuantumBlock(
                index=len(blockchain),
                category=cat,
                name=name,
                greeting=greeting,
                prev_hash=prev_hash,
                quantum_entropy=entropy
            )
            block.mine(difficulty=difficulty)
            prev_hash = block.hash
            mode_nonces += block.nonce
            blockchain.append(block)
            
        print(f"✔ [MINED BLOCK] {name:<45} | Nonces: {mode_nonces:<7} | Hash: {prev_hash[:24]}...")

    print("\n" + "=" * 85)
    print(f"[✔] Total Multilingual Quantum Blocks Mined: {len(blockchain)}")
    print(f"[✔] Total Nonces Computed: {sum(b.nonce for b in blockchain)}")
    print(f"[✔] Final Multilingual Chain Hash: {prev_hash}")
    print("=" * 85)

if __name__ == "__main__":
    run_multilingual_quantum_pipeline()
