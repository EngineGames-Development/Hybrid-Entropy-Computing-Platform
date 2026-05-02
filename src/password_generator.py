import serial
import time
import argparse
import sys

PORT = 'COM3'
BAUD = 115200

try:
    ser = serial.Serial(PORT, BAUD, timeout=1)
    print(f"[OK] Connecting to Laser {PORT}")
except Exception as e:
    print(f"[ERROR] Hardware not found: {e}")
    exit()
time.sleep(2)

print("--- QUANTUM DATA STREAM ---")

bit_accumulator = ""
password = ""

def generate_password(ser, length=10, show_bits=True):
    bit_accumulator = ""
    password = ""

    while len(password) < length:
        if ser.in_waiting > 0:
            bit = ser.read(1).decode("utf-8", errors="ignore")

            if bit in ["0", "1"]:
                bit_accumulator += bit

                if show_bits:
                    print(bit, end="", flush=True)

                if len(bit_accumulator) == 8:
                    char_code = int(bit_accumulator, 2) % 94 + 33
                    password += chr(char_code)
                    bit_accumulator = ""

                    print(f" -> Symbol found! Password: {password}")

    return password

def main():
    parser = argparse.ArgumentParser(
        description="Hardware Entropy Password Generator"
    )

    parser.add_argument(
        "--port",
        default="COM3",
        help="Serial port (default: COM3)"
    )

    parser.add_argument(
        "--baud",
        type=int,
        default=115200,
        help="Baud rate (default: 115200)"
    )

    parser.add_argument(
        "--length",
        type=int,
        default=10,
        help="Password length (default: 10)"
    )

    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Hide live bitstream output"
    )

    args = parser.parse_args()

    try:
        ser = serial.Serial(args.port, args.baud, timeout=1)
        print(f"[OK] Connected to {args.port}")
    except Exception as e:
        print(f"[ERROR] Hardware not found: {e}")
        sys.exit(1)

    time.sleep(2)
    print("--- ENTROPY DATA STREAM ---")

    try:
        password = generate_password(
            ser,
            length=args.length,
            show_bits=not args.quiet
        )

    except KeyboardInterrupt:
        print("\nInterrupted.")
        password = ""

    finally:
        ser.close()

    if password:
        print(f"\nGenerated Password: {password}")


if __name__ == "__main__":
    main()