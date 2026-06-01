#!/usr/bin/env python3
"""
optimization.py – Multi‑objective Pareto optimisation using the surrogate model

Objectives can be configured to:
- Maximise any modal frequency (e.g., f1)
- Minimise max deformation
- Minimise max stress

Uses NSGA‑II (pymoo) if available, otherwise falls back to random sampling + Pareto filtering.

Outputs:
- pareto_front.csv       : all non‑dominated solutions (inputs + objectives)
- pareto_front_plot.png  : pairwise scatter plot matrix
"""

import sys
import numpy as np
import pandas as pd
from pathlib import Path
from typing import List, Tuple, Callable

# Import surrogate predictor
from predict import SurrogatePredictor

# ============================================================================
# Configuration
# ============================================================================

# Input bounds (same as training range – ensure they match your dataset)
INPUT_BOUNDS = {
    'beam_height': (5.0, 20.0),     # mm
    'beam_length': (10.0, 17.0),    # mm
    'fillet_size': (0.1, 0.6),      # mm
    'beam_width': (0.4, 0.8),       # mm
}

# Objective definitions:
# Each objective is a tuple: (name, sense, output_index, transform)
# sense: 'max' or 'min'
# output_index: 0..5 as per predictor.target_names
# transform: function applied to raw output (e.g., lambda x: -x for maximization inside NSGA‑II)
OBJECTIVES = [
    ('f1_min',          'min', 0, None),   # maximise modal frequency 1
    ('f2_max',          'max', 1, None),   # minimise max deformation (index 4)
    ("deformation",     'max', 4, None)
]

# NSGA‑II parameters
POP_SIZE = 100       # population size
N_GEN    = 50        # number of generations
SEED     = 42

# Fallback random sampling (if pymoo not installed)
RANDOM_SAMPLES = 50000

# Output directory (same as plots folder)
OUTPUT_DIR = Path(__file__).parent / "plots"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================================
# Problem definition (pymoo)
# ============================================================================

try:
    from pymoo.algorithms.moo.nsga2 import NSGA2
    from pymoo.core.problem import Problem
    from pymoo.optimize import minimize
    from pymoo.operators.crossover.sbx import SBX
    from pymoo.operators.mutation.pm import PM
    from pymoo.operators.sampling.rnd import FloatRandomSampling
    from pymoo.termination import get_termination
    PYMOO_AVAILABLE = True
except ImportError:
    PYMOO_AVAILABLE = False
    print("pymoo not installed. Falling back to random sampling + Pareto filtering.")
    print("Install pymoo with: pip install pymoo")

if PYMOO_AVAILABLE:
    class SurrogateOptimizationProblem(Problem):
        def __init__(self, predictor: SurrogatePredictor, objectives: List[tuple]):
            self.predictor = predictor
            self.objectives = objectives
            n_obj = len(objectives)
            # Bounds
            xl = np.array([INPUT_BOUNDS[k][0] for k in INPUT_BOUNDS.keys()])
            xu = np.array([INPUT_BOUNDS[k][1] for k in INPUT_BOUNDS.keys()])
            super().__init__(n_var=4, n_obj=n_obj, xl=xl, xu=xu)

        def _evaluate(self, X, out, *args, **kwargs):
            # X shape: (n_pop, 4)
            # Predict outputs (mean only) – shape (n_pop, 6)
            # Use batch prediction for speed
            mean_phys, _ = self.predictor.predict_with_uncertainty(
                X[:, 0], X[:, 1], X[:, 2], X[:, 3],
                return_dataframe=False
            )
            # Build objective array (n_pop, n_obj)
            F = np.zeros((X.shape[0], len(self.objectives)))
            for i, (_, sense, idx, transform) in enumerate(self.objectives):
                val = mean_phys[:, idx]
                if transform is not None:
                    val = transform(val)
                if sense == 'max':
                    val = -val          # NSGA‑II minimises by default
                F[:, i] = val
            out["F"] = F

# ============================================================================
# Fallback: random sampling + Pareto filtering
# ============================================================================

def is_dominated(a: np.ndarray, b: np.ndarray, minimize: List[bool]) -> bool:
    """Return True if a is dominated by b (i.e. b is better on all objectives)."""
    # a and b are 1D arrays of objective values
    # minimize[i] = True means lower is better
    better_or_equal = []
    strictly_better = False
    for i, (av, bv) in enumerate(zip(a, b)):
        if minimize[i]:
            if bv < av:
                better_or_equal.append(True)
                strictly_better = True
            elif bv == av:
                better_or_equal.append(True)
            else:
                better_or_equal.append(False)
        else:   # maximise
            if bv > av:
                better_or_equal.append(True)
                strictly_better = True
            elif bv == av:
                better_or_equal.append(True)
            else:
                better_or_equal.append(False)
    return all(better_or_equal) and strictly_better

def pareto_front_random(predictor: SurrogatePredictor, n_samples: int, objectives: List[tuple]) -> pd.DataFrame:
    """Generate random inputs, evaluate objectives, keep non‑dominated solutions."""
    # Input names
    input_names = list(INPUT_BOUNDS.keys())
    # Generate random inputs
    np.random.seed(SEED)
    X = np.zeros((n_samples, 4))
    for i, key in enumerate(input_names):
        low, high = INPUT_BOUNDS[key]
        X[:, i] = np.random.uniform(low, high, n_samples)

    # Batch predict
    print(f"Evaluating {n_samples} random designs...")
    mean_phys, _ = predictor.predict_with_uncertainty(
        X[:, 0], X[:, 1], X[:, 2], X[:, 3],
        return_dataframe=False
    )

    # Compute objective values (raw, not flipped)
    obj_raw = np.zeros((n_samples, len(objectives)))
    for i, (_, sense, idx, transform) in enumerate(objectives):
        val = mean_phys[:, idx]
        if transform is not None:
            val = transform(val)
        obj_raw[:, i] = val

    # Determine minimisation direction for each objective (True = lower better)
    minimize = [sense == 'min' for _, sense, _, _ in objectives]

    # Pareto filter
    pareto_mask = np.ones(n_samples, dtype=bool)
    for i in range(n_samples):
        if not pareto_mask[i]:
            continue
        for j in range(n_samples):
            if i == j or not pareto_mask[j]:
                continue
            if is_dominated(obj_raw[i], obj_raw[j], minimize):
                pareto_mask[i] = False
                break
            if is_dominated(obj_raw[j], obj_raw[i], minimize):
                pareto_mask[j] = False

    pareto_idx = np.where(pareto_mask)[0]
    print(f"Found {len(pareto_idx)} Pareto‑optimal solutions out of {n_samples} random samples.")

    # Build DataFrame
    df = pd.DataFrame()
    for i, key in enumerate(input_names):
        df[key] = X[pareto_idx, i]
    for j, (name, sense, _, _) in enumerate(objectives):
        df[name] = obj_raw[pareto_idx, j]
    return df

# ============================================================================
# Plotting utilities
# ============================================================================

def plot_pareto_front(df: pd.DataFrame, objectives: List[tuple], output_path: Path):
    """Create a publication‑quality scatter plot matrix of the Pareto front."""
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib not available – skipping plot.")
        return

    # ---------- Graph‑design standards ----------
    plt.rcParams.update({
        'font.family': 'serif',
        'font.size': 10,
        'axes.labelsize': 11,
        'axes.titlesize': 12,
        'xtick.labelsize': 9,
        'ytick.labelsize': 9,
    })

    # Paul Tol colour palette (colorblind‑safe)
    COLORS = {
        'primary':   '#88CCEE',
        'secondary': '#CC6677',
        'tertiary':  '#DDCC77',
        'quaternary':'#6699CC',
        'quinary':   '#888888',
        'accent':    '#EE7733',
        'grid':      '#CCCCCC',
    }

    obj_names = [name for name, _, _, _ in objectives]
    n_obj = len(obj_names)

    # ----- Single objective: histogram -----
    if n_obj == 1:
        fig, ax = plt.subplots(figsize=(6.0, 6.0/1.3))  # width 6", height 4.6"
        ax.hist(df[obj_names[0]], bins=20, color=COLORS['primary'], edgecolor='black')
        ax.set_xlabel(obj_names[0])
        ax.set_ylabel('Count')
        ax.set_title('Pareto front – single objective', fontweight='bold')
        # L‑frame & grid behind
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.grid(True, linestyle='-', alpha=0.5, zorder=1)
        plt.tight_layout()
        plt.savefig(output_path, dpi=1000, bbox_inches='tight', facecolor='white')
        # Also save SVG (optional, but standard)
        svg_path = output_path.with_suffix('.svg')
        plt.savefig(svg_path, dpi=1000, bbox_inches='tight', facecolor='white')
        plt.close()
        print(f"Pareto front plot saved to: {output_path} and {svg_path}")
        return

    # ----- Two or more objectives: scatter plot matrix -----
    fig, axes = plt.subplots(n_obj, n_obj,
                             figsize=(4.0 * n_obj, 4.0 * n_obj))
    if n_obj == 2:
        axes = np.array([[axes[0,0], axes[0,1]],
                         [axes[1,0], axes[1,1]]])

    for i in range(n_obj):
        for j in range(n_obj):
            ax = axes[i, j]
            if i == j:
                # Diagonal: histogram
                ax.hist(df[obj_names[i]], bins=20,
                        color=COLORS['primary'], edgecolor='black')
                ax.set_xlabel(obj_names[i])
                ax.set_ylabel('Count')
            else:
                # Off‑diagonal: scatter
                ax.scatter(df[obj_names[j]], df[obj_names[i]],
                           s=10,                # marker size
                           alpha=0.7,
                           edgecolors='white',  # white edge (skill requirement)
                           linewidths=1.5,
                           color=COLORS['secondary'])
                ax.set_xlabel(obj_names[j])
                ax.set_ylabel(obj_names[i])

            # L‑frame & grid behind data (applies to all subplots)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.grid(True, linestyle='-', alpha=0.5, zorder=1)

    plt.suptitle("Pareto front – pairwise objective space", fontweight='bold', y=1.02)
    plt.tight_layout()
    # Save high‑res PNG and SVG
    plt.savefig(output_path, dpi=1000, bbox_inches='tight', facecolor='white')
    svg_path = output_path.with_suffix('.svg')
    plt.savefig(svg_path, dpi=72, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"Pareto front plot saved to: {output_path} and {svg_path}")


# ============================================================================
# Main
# ============================================================================

def main():
    # Load predictor
    print("Loading surrogate predictor...")
    predictor = SurrogatePredictor()

    print("\nInput bounds:")
    for k, (low, high) in INPUT_BOUNDS.items():
        print(f"  {k:12} : [{low:.2f}, {high:.2f}]")

    print("\nObjectives:")
    for name, sense, idx, _ in OBJECTIVES:
        target = predictor.target_names[idx]
        print(f"  {name:20} : {sense:3}  {target}")

    if PYMOO_AVAILABLE:
        print("\nRunning NSGA‑II optimisation...")
        problem = SurrogateOptimizationProblem(predictor, OBJECTIVES)
        algorithm = NSGA2(
            pop_size=POP_SIZE,
            sampling=FloatRandomSampling(),
            crossover=SBX(prob=0.9, eta=15),
            mutation=PM(prob=0.1, eta=20),
            eliminate_duplicates=True
        )
        termination = get_termination("n_gen", N_GEN)
        res = minimize(problem,
                       algorithm,
                       termination,
                       seed=SEED,
                       verbose=True)

        # Extract results
        X_opt = res.X
        F_opt = res.F   # these are the *minimised* values (negated for maximisation)

        # Convert back to actual objective values (undo negation)
        obj_actual = np.zeros_like(F_opt)
        for i, (name, sense, _, _) in enumerate(OBJECTIVES):
            if sense == 'max':
                obj_actual[:, i] = -F_opt[:, i]
            else:
                obj_actual[:, i] = F_opt[:, i]

        # Build DataFrame
        input_names = list(INPUT_BOUNDS.keys())
        df_pareto = pd.DataFrame(X_opt, columns=input_names)
        for i, (name, _, _, _) in enumerate(OBJECTIVES):
            df_pareto[name] = obj_actual[:, i]

        print(f"\nNSGA‑II finished. Pareto front size: {len(df_pareto)}")
    else:
        # Fallback
        df_pareto = pareto_front_random(predictor, RANDOM_SAMPLES, OBJECTIVES)

    # Save CSV
    pareto_path = OUTPUT_DIR / "pareto"
    pareto_path.mkdir(parents=True, exist_ok=True)
    csv_path  = pareto_path / "pareto_front.csv"
    df_pareto.to_csv(csv_path, index=False)
    print(f"Pareto front saved to: {csv_path}")

    # Plot
    plot_pareto_front(df_pareto, OBJECTIVES, pareto_path / "pareto_front_plot.png")

    # Print some statistics
    print("\nPareto front summary:")
    print(df_pareto.describe())

    # Show a few best solutions for each objective
    print("\nTop 3 solutions by each objective:")
    for name, sense, _, _ in OBJECTIVES:
        if sense == 'max':
            top = df_pareto.nlargest(3, name)
        else:
            top = df_pareto.nsmallest(3, name)
        print(f"\n{name} ({sense}):")
        print(top.to_string(index=False))

if __name__ == "__main__":
    main()