import serial
import time
import numpy as np
import math
import matplotlib.pyplot as plt
from collections import Counter
from scipy import signal
from reportlab.pdfgen import canvas
import argparse
import csv
import os


PORT = "COM3"
BAUD = 115200
DURATION = 30

def capture(label):
    ser = serial.Serial(PORT, BAUD, timeout=1)
    time.sleep(2)

    print(f"[CAPTURE] {label}")

    start = time.time()
    data = []

    while time.time() - start < DURATION:
        bit = ser.read().decode(errors="ignore")
        if bit in ["0", "1"]:
            data.append(bit)

    ser.close()

    print(f"[DONE] {label}: {len(data)} bits")
    return data

def entropy(data):
    c = Counter(data)
    total = len(data)
    return -sum((v/total)*math.log2(v/total) for v in c.values())

def balance(data):
    c = Counter(data)
    return c["1"] / len(data)

def autocorr(data):
    bits = np.array([int(b) for b in data])
    return np.corrcoef(bits[:-1], bits[1:])[0, 1]

def runs(data):
    r = 1
    for i in range(1, len(data)):
        if data[i] != data[i-1]:
            r += 1
    return r

def imbalance(data):
    c = Counter(data)
    return abs(c["1"] - c["0"]) / len(data)

def plot_hist(data, title):
    c = Counter(data)
    plt.figure()
    plt.bar(["0", "1"], [c["0"], c["1"]])
    plt.title(title)
    plt.show()

def plot_fft(data, title):
    bits = np.array([int(b) for b in data])
    bits = bits - np.mean(bits)

    f, pxx = signal.welch(bits, nperseg=256)

    plt.figure()
    plt.semilogy(f, pxx)
    plt.title(title)
    plt.xlabel("Frequency")
    plt.ylabel("Power")
    plt.show()

def entropy_over_time(data, window=500):
    vals = []
    for i in range(0, len(data)-window, window):
        chunk = data[i:i+window]
        vals.append(entropy(chunk))

    plt.figure()
    plt.plot(vals)
    plt.title("Entropy Over Time")
    plt.show()

def analyze(name, data):
    results = {
        "Entropy": entropy(data),
        "Balance": balance(data),
        "Autocorr": autocorr(data),
        "Runs": runs(data),
        "Imbalance": imbalance(data)
    }

    print(f"\n===== {name} =====")
    for k, v in results.items():
        print(f"{k}: {v}")

    plot_hist(data, name + " Histogram")
    plot_fft(data, name + " Spectrum")
    entropy_over_time(data)

    return results

def report(on, off):
    c = canvas.Canvas("qrng_report.pdf")
    c.setFont("Helvetica", 12)

    y = 750
    c.drawString(50, y, "Entropy System Analysis Report")
    y -= 30

    for k in on:
        line = f"ON {k}: {on[k]:.6f} | OFF {off[k]:.6f}"
        c.drawString(50, y, line)
        y -= 20

    c.save()

def benchmark(trials=5):
    os.makedirs("results", exist_ok=True)

    rows = []

    for i in range(trials):
        print(f"\n===== TRIAL {i+1} =====")

        on = capture("LASER ON")
        off = capture("LASER OFF")

        on_results = analyze("LASER ON", on)
        off_results = analyze("LASER OFF", off)

        row = {
            "trial": i + 1,
            "on_entropy": on_results["Entropy"],
            "off_entropy": off_results["Entropy"],
            "on_balance": on_results["Balance"],
            "off_balance": off_results["Balance"],
            "on_autocorr": on_results["Autocorr"],
            "off_autocorr": off_results["Autocorr"]
        }

        rows.append(row)

    with open("results/benchmark.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print("\n[OK] Saved results/benchmark.csv")

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Hybrid Entropy Computing Platform"
    )

    parser.add_argument(
        "mode",
        choices=["test", "onoff", "report"],
        help="Mode to run"
    )

    parser.add_argument(
        "--duration",
        type=int,
        default=30,
        help="Capture duration in seconds"
    )

    args = parser.parse_args()

    DURATION = args.duration

    if args.mode == "test":
        data = capture("TEST RUN")
        analyze("TEST RUN", data)

    elif args.mode == "onoff":
        on = capture("LASER ON")
        off = capture("LASER OFF")

        on_results = analyze("LASER ON", on)
        off_results = analyze("LASER OFF", off)

        print("\n===== COMPARISON =====")
        print("Entropy difference:",
              on_results["Entropy"] - off_results["Entropy"])
        print("Autocorr difference:",
              on_results["Autocorr"] - off_results["Autocorr"])

    elif args.mode == "report":
        on = capture("LASER ON")
        off = capture("LASER OFF")

        on_results = analyze("LASER ON", on)
        off_results = analyze("LASER OFF", off)

        report(on_results, off_results)

        print("\n[REPORT GENERATED: qrng_report.pdf]")