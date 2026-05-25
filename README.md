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

The script may require a significant amount of RAM (up to 24 GB) for the final simulation with N=100,000 paths. This is due to the process 
being vectorized. If you encounter memory issues, consider reducing the number of paths. This however will of course not perfectly replicate the graphs in the paper.
I will upload a optimized version of the code in C++ in the future, which will be more memory efficient and faster.

---

## License

The code in this repository is released under the MIT License.

The paper remains the intellectual property of the author.

---

## Contact

Simon Paul Reuter

Email: simonreuter41@gmail.com