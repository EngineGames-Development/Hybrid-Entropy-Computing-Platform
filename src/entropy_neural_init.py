import serial
import hashlib
import torch
import torch.nn as nn
import time
import os

PORT = 'COM3'
BAUD = 115200
LOG_FILE = "quantum_ai_data.csv"

try:
    ser = serial.Serial(PORT, BAUD, timeout=1)
    print(f"[OK] Connecting to Laser {PORT}")
except Exception as e:
    print(f"[ERROR] Hardware not found: {e}")
    exit()

def get_quantum_entropy(num_bits=512):
    raw_data = ""
    while len(raw_data) < num_bits:
        if ser.in_waiting > 0:
            bit = ser.read(1).decode('utf-8', errors='ignore')
            if bit in ['0', '1']:
                raw_data += bit
    
    refined_hash = hashlib.sha256(raw_data.encode()).digest()
    return [b / 255.0 for b in refined_hash]

class QuantumNet(nn.Module):
    def __init__(self):
        super(QuantumNet, self).__init__()
        self.layer = nn.Linear(32, 1)
        self.apply_quantum_weights()

    def apply_quantum_weights(self):
        with torch.no_grad():
            q_seed = get_quantum_entropy()
            q_tensor = torch.tensor(q_seed).reshape(1, 32)
            self.layer.weight.copy_(q_tensor)

    def forward(self, x):
        return torch.sigmoid(self.layer(x))

print("\n--- INITIALISE QUANTUM AI ---")
model = QuantumNet()

if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w") as f:
        f.write("Timestamp,Quantum_Decision,Weight_Entropy\n")

print(f"[INFO] Data is stored in {LOG_FILE}.")
print("-" * 45)

try:
    while True:
        input_vector = torch.randn(1, 32)
        
        decision = model(input_vector).item()
        
        timestamp = time.strftime("%H:%M:%S")
        with open(LOG_FILE, "a") as f:
            f.write(f"{timestamp},{decision:.8f},{model.layer.weight.mean().item():.8f}\n")
        
        print(f"[{timestamp}] Decision: {decision:.6f} | Status: Stable")
        
        if int(time.time()) % 2 == 0:
            model.apply_quantum_weights()
            print("  >> AI-Evolution triggered from Laser-Entropy")
            
        time.sleep(0.5)

except KeyboardInterrupt:
    print("\n[STOP] System shutting down.")
    ser.close()
