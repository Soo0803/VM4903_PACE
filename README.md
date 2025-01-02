# Pneumatically Actuated Conforming Ergonomic System for Custom Foot Orthoses (PACE)

**Undergraduate Research Students:** Soo Wei Jie, Krin Muangsiri, Choo Lee Wen  
**Professor:** Dr. Shane Johnson 
**Affiliation:** University of Michigan-Shanghai Jiaotong University Joint Institute, Minhang District, Shanghai, China

## Abstract

Customized orthosis production is crucial for addressing foot-related issues, yet traditional methods are time-consuming and costly. The Pneumatically Actuated Conforming Ergonomic (PACE) system offers an innovative solution, utilizing a human-in-the-loop approach and the Rapid Evaluation and Adjustment Device (READ) prescription method. This repository presents the development, testing, and results of the PACE system, highlighting its efficiency and challenges in capturing arch height reliably.

## Table of Contents

1. [Introduction](#1-introduction)
2. [Materials and Methods](#2-materials-and-methods)
3. [Results and Discussion](#3-results-and-discussion)

## 1. Introduction

Foot orthoses are essential for various foot conditions, but traditional manufacturing methods are slow and costly. PACE reduces production time to approximately 5 minutes by integrating reshaping capabilities and real-time adjustments. This system employs PID control for precise customization and incorporates biomechanical support via an adjustable airbag under the foot arch.

## 2. Materials and Methods

### Materials

- **Thermoplastic (Polycaprolactone - PCL):** Moldable material for orthosis shaping.
- **Airbag and Load Cell:** Flexible support and force measurement under the foot arch.
- **3D Scanner:** High-resolution scanning for precise foot and orthosis geometry.
- **Control System:** Raspberry Pi, motor, pump, ADC converter, and electronic components for system control.

### Methods

- **Subject Selection:** 15 subjects recruited to test orthosis customization.
- **Foot Scanning:** 3D scanning of subjects' feet to capture geometry.
- **Orthosis Shaping:** Airbag application of force under PID control for orthosis molding.
- **Safety System:** Integration of pressure sensor and safety mechanisms for device reliability.

## 3. Results and Discussion

### Data Analysis

- **3D Scanning and Mesh Processing:** Use of MeshLab and MATLAB for processing scanned data.
- **Arch Height Measurement:** Statistical analysis of orthosis geometry to assess reliability.
- **Intraclass Correlation Coefficients (ICCs):** Comparison with benchmark data for validation.

