# Volatility Arbitrage under Discrete Delta Hedging

This repository contains the replication code for the paper:

> Volatility Arbitrage under Discrete Delta Hedging  
> by Simon Paul Reuter (SSRN ID: 6778301)

Paper: https://ssrn.com/abstract=6778301

---

## Citation

If you use this work, please cite the corresponding paper in accordance with standard academic practice.

---

## Repository Structure

```text
bld/       Figures and simulation results
src/       Python classes and script
LICENSE    License file
README.md  README file
requirements.txt  Python dependencies
```

---

## Setup

Create and activate a virtual environment:

```bash
# Create environment
python -m venv venv
# or
py -m venv venv

# Activate (Windows)
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Usage

Run the main script:

```bash
python src/script.py
# or
py src/script.py
```

All outputs will be generated in the `bld/` directory.

### Remark on RAM Usage

The script may require a significant amount of memory in the full simulation setup with \(n = 100{,}000\) rebalancing time steps.

This is due to the fully vectorized implementation, which stores and processes all simulated paths across the entire time grid simultaneously.

If memory limitations are encountered, the number of rebalancing steps can be reduced. However, this will not perfectly replicate the results presented in the paper.

A more memory-efficient and computationally faster implementation in C++ is planned for a future release. Results will not be bitwise identical due to differences in numerical precision and random number generation, but the main results will remain unchanged.

---

## License

The code in this repository is released under the MIT License.

The paper remains the intellectual property of the author.

---

## Contact

Simon Paul Reuter

Email: simonreuter41@gmail.com