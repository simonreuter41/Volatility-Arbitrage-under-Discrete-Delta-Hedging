from simulation_Env import SimulationEnv
from blackScholesMethods import BlackScholesMethods
import numpy as np
import pandas as pd
from scipy.stats import gaussian_kde, norm
import matplotlib.pyplot as plt
import os

# -------------------------------------------------
# Global plotting style
# -------------------------------------------------
plt.style.use("seaborn-v0_8-whitegrid")
plt.rcParams.update({
    "font.size": 12,
    "axes.titlesize": 13,
    "axes.labelsize": 12,
    "legend.fontsize": 10,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "figure.dpi": 120,
    "savefig.dpi": 300,
})

MAIN_BLUE = "#1f77b4"
DARK_GREY = "#333333"

# -------------------------------------------------
# Output directory for figures
# -------------------------------------------------
FIG_DIR = "bld"
os.makedirs(FIG_DIR, exist_ok=True)

# -------------------------------------------------
# Initialize environment
# -------------------------------------------------
random_seeds= [42, 123, 321, 621]
simEnv = SimulationEnv(1000, 0.05, 1000)

# -------------------------------------------------
# Example graphics for n=252, n=1000, n=100000
# Fixed parameters: sigma=0.2, sigma_iv=0.3, T=1
# -------------------------------------------------
stepsizes = [252, 1000, 100000]

np.random.seed(random_seeds[0])  # Set seed for reproducibility

results = [] 

for n in stepsizes:
    S, B, delta, profit, cumulative_profit, discounted_profit, expected_profit, C_Market, C_Model = simEnv.vol_arb_fast(
        n=n, sigma=0.2, sigma_iv=0.3, T=1
    )


    results.append({
        "n": n,
        "discounted_profit": discounted_profit,
        "expected_profit": expected_profit
    })

    t = np.linspace(0, 1, len(S))

    print(f"Steps: {n}")
    print(f"Discounted Profit: {discounted_profit:.6f}")
    print(f"Expected Profit:    {expected_profit:.6f}")
    print()

    fig, axs = plt.subplots(2, 1, figsize=(9, 5), sharex=True)

    # Underlying price process
    axs[0].plot(t, S, color=MAIN_BLUE, linewidth=1.8)
    axs[0].set_title(f"Underlying Price Process $S_t$ (n = {n} steps)")
    axs[0].set_ylabel("Price (€)")
    axs[0].grid(True, alpha=0.25)

    # Cumulative profit
    axs[1].plot(t, cumulative_profit, color=DARK_GREY, linewidth=1.8)
    axs[1].axhline(0, color="black", linestyle="--", linewidth=1)
    axs[1].set_title(f"Cumulative P&L (n = {n} steps)")
    axs[1].set_xlabel("Time (t)")
    axs[1].set_ylabel("Profit (€)")
    axs[1].grid(True, alpha=0.25)

    plt.tight_layout()
    plt.savefig(f"{FIG_DIR}/price_profit_n{n}.png", dpi=300, bbox_inches="tight")
    plt.savefig(f"{FIG_DIR}/price_profit_n{n}.pdf", bbox_inches="tight")
    plt.show()
    plt.close()

df = pd.DataFrame(results)
df.to_csv(f"{FIG_DIR}/profit_summary.csv", index=False)


# -------------------------------------------------
# Simulations for n=252, n=1000, n=100000 with N=10000 repetitions
# -------------------------------------------------
N = 10000
hedging_errors_array = np.empty((len(stepsizes), N))
expected_profits = np.empty((len(stepsizes), N))
discounted_profits = np.empty((len(stepsizes), N))

for i, n in enumerate(stepsizes):
    np.random.seed(random_seeds[i+1])  # Set seed for reproducibility
    hedging_errors, expected_profit, discounted_profit = simEnv.vol_arb_fast_matrix(
        n=n, N=N, sigma=0.2, sigma_iv=0.3, T=1
    )
    hedging_errors_array[i] = hedging_errors
    expected_profits[i] = expected_profit
    discounted_profits[i] = discounted_profit

# -------------------------------------------------
# Histograms of hedging errors
# -------------------------------------------------
for i, n in enumerate(stepsizes):
    plt.figure(figsize=(7.2, 4.2))
    plt.hist(
        hedging_errors_array[i],
        bins=60,
        color=MAIN_BLUE,
        alpha=0.65,
        edgecolor="white",
        linewidth=0.5
    )
    plt.title(f"Hedging Error Histogram (n={n})")
    plt.xlabel("Hedging Error (€)")
    plt.ylabel("Count")
    plt.grid(True, alpha=0.25)
    plt.tight_layout()
    plt.savefig(f"{FIG_DIR}/hist_hedging_n{n}.png", dpi=300, bbox_inches="tight")
    plt.savefig(f"{FIG_DIR}/hist_hedging_n{n}.pdf", bbox_inches="tight")
    plt.show()
    plt.close()

# -------------------------------------------------
# KDE plots of hedging errors
# -------------------------------------------------
for i, n in enumerate(stepsizes):
    kde = gaussian_kde(hedging_errors_array[i], bw_method="scott")
    x = np.linspace(
        np.min(hedging_errors_array[i]),
        np.max(hedging_errors_array[i]),
        1000
    )

    plt.figure(figsize=(7.2, 4.2))
    plt.plot(x, kde(x), color=MAIN_BLUE, linewidth=2.0, label="KDE")
    plt.title(f"KDE of Hedging Errors (n={n})")
    plt.xlabel("Hedging Error (€)")
    plt.ylabel("Density")
    plt.grid(True, alpha=0.25)
    plt.legend(frameon=False)
    plt.tight_layout()
    plt.savefig(f"{FIG_DIR}/kde_hedging_n{n}.png", dpi=300, bbox_inches="tight")
    plt.savefig(f"{FIG_DIR}/kde_hedging_n{n}.pdf", bbox_inches="tight")
    plt.show()
    plt.close()

# -------------------------------------------------
# KDE vs normal distribution
# -------------------------------------------------
means = np.zeros(len(stepsizes))
stds = np.zeros(len(stepsizes))

for i, n in enumerate(stepsizes):
    means[i] = np.mean(hedging_errors_array[i])
    stds[i] = np.std(hedging_errors_array[i])

    kde = gaussian_kde(hedging_errors_array[i], bw_method="scott")
    x = np.linspace(
        np.min(hedging_errors_array[i]),
        np.max(hedging_errors_array[i]),
        1000
    )

    plt.figure(figsize=(7.2, 4.2))
    plt.plot(x, kde(x), color=MAIN_BLUE, linewidth=2.0, label="KDE")
    plt.plot(
        x,
        norm.pdf(x, means[i], stds[i]),
        color="black",
        linestyle="--",
        linewidth=2.0,
        label="Normal Distribution"
    )
    plt.title(f"KDE vs Normal Distribution (n={n})")
    plt.xlabel("Hedging Error (€)")
    plt.ylabel("Density")
    plt.grid(True, alpha=0.25)
    plt.legend(frameon=False)
    plt.tight_layout()
    plt.savefig(f"{FIG_DIR}/kde_vs_normal_n{n}.png", dpi=300, bbox_inches="tight")
    plt.savefig(f"{FIG_DIR}/kde_vs_normal_n{n}.pdf", bbox_inches="tight")
    plt.show()
    plt.close()

print("Means:", means)
print("Stds: ", stds)

df_stats = pd.DataFrame({
    "stepsize": stepsizes,
    "mean": means,
    "std": stds
})

df_stats.to_csv(f"{FIG_DIR}/hedging_error_stats.csv", index=False)  