# Hybrid Entropy Computing Platform

A hardware/software system using optical entropy generation for randomness experiments, security applications, and AI initialization research.

![Picture of the Build without Laser on](/docs/Entropy1.jpeg)
![Picture of the Build with Laser on](/docs/Entropy2.jpeg)
![EntropyCheck](/docs/EntropyCheck.jpeg)

## Features

- Arduino photodiode entropy generator
- Live serial bitstream capture
- Statistical randomness tests
- Password generation
- Neural network entropy initialization
- Quantum simulation experiments

## Hardware

Uses dual photodiodes + laser source + Arduino Uno.

## Example Results

Entropy: 0.998  
Autocorrelation: 0.0012

## Limitations

- Not a certified quantum random generator
- Arduino ADC noise may contribute entropy
- Ambient light can affect sensors
- Small sample size compared to industrial RNG testing
- Qiskit simulator uses classical hardware

## Run

python main.py test
python main.py password
