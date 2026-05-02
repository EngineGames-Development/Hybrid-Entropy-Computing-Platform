# Hardware Overview

The Hybrid Entropy Computing Platform uses an optical sensing setup to generate binary data from small fluctuations in detected laser light intensity.

A laser beam illuminates two light-sensitive sensors positioned in parallel. The Arduino continuously samples both analog sensor values and compares their voltage levels in real time. If Sensor A reads higher than Sensor B, the system outputs a `1`; if Sensor B reads higher than Sensor A, it outputs a `0`.

Because microscopic variations occur in light intensity, sensor response time, thermal noise, and analog electronics, the measured differences create a dynamic entropy source that can be analyzed as a random bitstream.

---

# Core Principle

1. Laser emits constant light toward both sensors  
2. Sensors convert light intensity into changing analog voltage values  
3. Arduino reads both inputs using ADC sampling  
4. Relative differences are converted into binary bits  
5. Bitstream is sent over USB serial to the host computer for analysis

---

# Hardware Components

## Microcontroller

- **Arduino Uno**
- Responsible for analog sampling, comparison logic, and serial transmission

## Optical Sensors

- **2x GL5528 Photoresistors**
- Detect incoming laser intensity changes as resistance variations

## Light Source

- **KY-008 Laser Module (5V)**
- Provides stable optical input for both sensors

## Passive Components

- **2x 5.1kΩ Resistors**
- Used in voltage divider circuits with the photoresistors

## Prototyping Components

- Breadboard  
- Jumper wires  
- USB Type A-Type B cable for power + serial communication

---

# Pin Configuration

| Component | Arduino Pin |
|---|---|
| Sensor A Output | A0 |
| Sensor B Output | A1 |
| Laser Module VCC | Digital Pin 7 |
| Laser Module GND | GND |
| USB Serial | USB Port |

---

# Entropy Sources (Possible)

The system may derive randomness from:

- sensor electrical noise  
- ADC quantization noise  
- thermal fluctuations  
- microscopic laser intensity variation  
- resistor noise  
- ambient environmental interference  
- timing jitter during sampling

---

# Notes

This setup is an **experimental entropy generator**, not a certified hardware random number generator. Output quality should be validated using statistical randomness tests.