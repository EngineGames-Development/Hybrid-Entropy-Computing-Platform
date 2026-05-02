import serial
import time
import logging
from qiskit import QuantumCircuit
from qiskit_aer import Aer

PORT = 'COM3'
BAUDRATE = 115200
TIMEOUT = 1

logging.basicConfig( level=logging.INFO,format="%(asctime)s [%(levelname)s] %(message)s")

try:
    ser = serial.Serial(PORT, BAUDRATE, timeout=TIMEOUT)
    logging.info(f"Connected to serial port {PORT}")
except serial.SerialException as e:
    logging.error(f"Failed to open serial port: {e}")
    exit(1)

try:
    simulator = Aer.get_backend('qasm_simulator')
except Exception as e:
    logging.error(f"Failed to initialize simulator: {e}")
    ser.close()
    exit(1)

def run_quantum_op(bit):
    try:
        qc = QuantumCircuit(1, 1)

        if bit == '1':
            qc.h(0)
            logging.info("Laser-Bit 1 → Hadamard applied (superposition)")
        elif bit == '0':
            qc.x(0)
            logging.info("Laser-Bit 0 → Pauli-X applied (NOT)")
        else:
            raise ValueError(f"Invalid bit: {bit}")

        qc.measure(0, 0)

        job = simulator.run(qc, shots=1)
        result = job.result().get_counts()

        return list(result.keys())[0]

    except Exception as e:
        logging.error(f"Quantum operation failed: {e}")
        return None

logging.info("--- QUANTUM CIRCUIT CONTROLLER START ---")

try:
    while True:
        try:
            if ser.in_waiting > 0:
                raw = ser.read(1)

                if not raw:
                    continue

                try:
                    bit = raw.decode('utf-8').strip()
                except UnicodeDecodeError:
                    logging.warning("Received undecodable byte")
                    continue

                if bit not in ['0', '1']:
                    logging.warning(f"Ignoring invalid input: {bit}")
                    continue

                final_state = run_quantum_op(bit)

                if final_state is not None:
                    logging.info(f"Final Quantum State: |{final_state}>")

                time.sleep(0.2) 

        except serial.SerialException as e:
            logging.error(f"Serial communication error: {e}")
            break

except KeyboardInterrupt:
    logging.info("User interrupted. Shutting down...")

finally:
    if ser.is_open:
        ser.close()
        logging.info("Serial port closed.")