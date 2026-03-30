# StageShip
<<<<<<< HEAD
A CLI tool to automate the analysis, flattening and packaging of USD stages for efficient transfer and delivery
=======

**StageShip** is a Python-based CLI tool designed to automate the analysis, flattening, and packaging of USD (Universal Scene Description) stages for efficient transfer and delivery.

It helps streamline common pipeline workflows by:
- Detecting external dependencies in USD stages
- Flattening composed scenes into a single deliverable file
- Packaging outputs for transfer (e.g. via torrent)

---

## 🚀 Why StageShip?

In VFX pipelines, delivering assets to clients or between vendors often involves:
- Manually resolving dependencies
- Flattening stages inside DCCs like Houdini
- Transferring large files via external services

StageShip automates this workflow by bringing it into a single CLI tool, making it:
- Faster
- Repeatable
- Less error-prone
- Easier to integrate into pipelines and CI systems

---

## ✨ Features

- 🔍 **USD Stage Analysis**
  - Detects external references, payloads, and sublayers
  - Outputs dependency summaries

- 🧱 **Stage Flattening**
  - Flattens composed USD stages into a single file
  - Removes external dependencies for portability

- 📦 **Packaging**
  - Prepares final deliverables for transfer

- 🌐 **Torrent Generation**
  - Generates `.torrent` files for efficient peer-to-peer distribution

- 🖥️ **CLI-Driven Workflow**
  - Simple command-line interface for all operations

---

## 📦 Installation

> (To be expanded once packaged)

For development:

```bash
git clone <repo-url>
cd StageShip
pip install -e .
>>>>>>> f7670ac (updated readme)
