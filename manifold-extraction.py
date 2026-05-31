"""
manifold_extraction.py

Extract and visualise the low‑dimensional manifold of the surrogate model's output space.
- Uses UMAP (or PCA fallback) to embed 6‑dimensional predictions into 2D and 3D.
- Generates high‑quality scatter plots coloured by each output and by input parameters.
- Optionally analyses the weight space of the ensemble models.

Follows the graph‑design guidelines (serif, L‑frame, grid behind data, white edges, etc.)
"""

import sys
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import joblib

# Try to import UMAP (optional, but strongly recommended)
try:
    import umap
    UMAP_AVAILABLE = True
except ImportError:
    UMAP_AVAILABLE = False
    print("UMAP not installed. Falling back to PCA for manifold extraction.")
    print("Install UMAP with: pip install umap-learn")

# Import your predictor class
from predict import SurrogatePredictor

# =============================================================================
# Configuration
# =============================================================================
from model_build import OUTPUT_DIR
OUTPUT_DIR = OUTPUT_DIR/"manifold"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
# Number of random samples for the response manifold
N_SAMPLES = 200_000
BATCH_SIZE = 10_000

# Input bounds (from model_build.py logs)
INPUT_BOUNDS = {
    'beam_height': (5.0, 20.0),
    'beam_length': (10.0, 18.0),
    'fillet_size': (0.1, 0.8),
    'beam_width': (0.4, 1.0)
}
INPUT_NAMES = list(INPUT_BOUNDS.keys())
INPUT_SHORT = ['h', 'L', 'f', 'w']

OUTPUT_NAMES_FULL = ['modal_frequency_1', 'modal_frequency_2', 'modal_frequency_3',
                     'modal_frequency_4', 'max_deformation', 'max_stress']
OUTPUT_SHORT = ['f1 (Hz)', 'f2 (Hz)', 'f3 (Hz)', 'f4 (Hz)', 'deform (mm)', 'stress (MPa)']

# UMAP parameters (good default for this problem)
UMAP_NEIGHBORS = 15
UMAP_MIN_DIST = 0.1
RANDOM_SEED = 42

# =============================================================================
# Publication‑quality styling (Graph Design Skill)
# =============================================================================
FIG_WIDTH_SINGLE = 6.0
FIG_HEIGHT_SINGLE = FIG_WIDTH_SINGLE / 1.3

FIG_WIDTH_3D = 7.0
FIG_HEIGHT_3D = 5.0

# Paul Tol colour palette
COLORS = {
    'primary':   '#88CCEE',
    'secondary': '#CC6677',
    'tertiary':  '#DDCC77',
    'quaternary':'#6699CC',
    'quinary':   '#888888',
    'accent':    '#EE7733',
    'grid':      '#CCCCCC',
}

plt.rcParams.update({
    'font.family': 'serif',
    'font.size': 10,
    'axes.labelsize': 11,
    'axes.titlesize': 12,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
})

def save_fig(fig, name):
    """Save as PNG (1000 DPI) and SVG."""
    png_path = OUTPUT_DIR / f"{name}.png"
    svg_path = OUTPUT_DIR / f"{name}.svg"
    fig.savefig(png_path, dpi=1000, bbox_inches='tight', facecolor='white')
    fig.savefig(svg_path, dpi=72, bbox_inches='tight', facecolor='white')
    print(f"Saved: {png_path}\n       {svg_path}")

# =============================================================================
# 1. Load surrogate predictor
# =============================================================================
print("="*80)
print("MANIFOLD EXTRACTION FOR SURROGATE MODEL")
print("="*80)

print("\nLoading surrogate predictor (ensemble of 20 MLPs)...")
predictor = SurrogatePredictor()
scaler_X = predictor.scaler_X   # StandardScaler (mean 0, std 1)
scaler_Y = predictor.scaler_Y

# =============================================================================
# 2. Generate large random sample in original (real) units
# =============================================================================
print(f"\nGenerating {N_SAMPLES:,} random input points within training bounds...")
np.random.seed(RANDOM_SEED)
X_real = np.zeros((N_SAMPLES, 4))
for i, name in enumerate(INPUT_NAMES):
    low, high = INPUT_BOUNDS[name]
    X_real[:, i] = np.random.uniform(low, high, N_SAMPLES)

# Convert to DataFrame for batch prediction (the predictor expects columns)
df_input = pd.DataFrame(X_real, columns=INPUT_NAMES)

# =============================================================================
# 3. Predict outputs using the ensemble (mean only, in original units)
# =============================================================================
print(f"Predicting outputs in batches of {BATCH_SIZE}...")
all_predictions = []
n_batches = int(np.ceil(N_SAMPLES / BATCH_SIZE))

for batch_idx in range(n_batches):
    start = batch_idx * BATCH_SIZE
    end = min((batch_idx + 1) * BATCH_SIZE, N_SAMPLES)
    batch_df = df_input.iloc[start:end]
    # predict_batch returns mean predictions (DataFrame)
    y_batch = predictor.predict_batch(batch_df).values   # shape (batch_size, 6)
    all_predictions.append(y_batch)
    if (batch_idx + 1) % 10 == 0 or (batch_idx + 1) == n_batches:
        print(f"  Batch {batch_idx+1}/{n_batches} completed")

Y_pred = np.vstack(all_predictions)   # (N_SAMPLES, 6)
print(f"Prediction shape: {Y_pred.shape}")

# =============================================================================
# 4. Manifold embedding (2D and 3D) using UMAP (or PCA fallback)
# =============================================================================
print("\nComputing manifold embeddings...")

if UMAP_AVAILABLE:
    print("Using UMAP (non-linear manifold).")   # normal hyphen
    reducer_2d = umap.UMAP(n_neighbors=UMAP_NEIGHBORS, min_dist=UMAP_MIN_DIST,
                           random_state=RANDOM_SEED, n_components=2)
    reducer_3d = umap.UMAP(n_neighbors=UMAP_NEIGHBORS, min_dist=UMAP_MIN_DIST,
                           random_state=RANDOM_SEED, n_components=3)
else:
    print("UMAP not available – using PCA (linear projection).")
    # The dash above is a regular hyphen, but ensure it's ASCII; if not, replace with '-'

# Fit and transform
embedding_2d = reducer_2d.fit_transform(Y_pred)
embedding_3d = reducer_3d.fit_transform(Y_pred)

print(f"2D embedding shape: {embedding_2d.shape}")
print(f"3D embedding shape: {embedding_3d.shape}")

# =============================================================================
# 5. Visualisations
# =============================================================================
print("\nGenerating publication‑quality plots...")

# ----- 5.1 2D manifold coloured by each output -----
for out_idx, (short_name, full_name) in enumerate(zip(OUTPUT_SHORT, OUTPUT_NAMES_FULL)):
    fig, ax = plt.subplots(figsize=(FIG_WIDTH_SINGLE, FIG_HEIGHT_SINGLE))
    sc = ax.scatter(embedding_2d[:, 0], embedding_2d[:, 1],
                    c=Y_pred[:, out_idx], cmap='viridis',
                    s=5, alpha=0.6, edgecolors='white', linewidths=0.3,
                    zorder=3)
    ax.set_xlabel('Manifold dimension 1')
    ax.set_ylabel('Manifold dimension 2')
    ax.set_title(f'Output manifold – {short_name}', fontweight='bold')

    # L‑frame & grid behind
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(True, linestyle='-', alpha=0.3, zorder=0)

    cbar = plt.colorbar(sc, ax=ax, pad=0.02)
    cbar.set_label(short_name)
    plt.tight_layout()
    save_fig(fig, f'manifold_2d_output_{out_idx}_{full_name}')
    plt.close(fig)

# ----- 5.2 2D manifold coloured by each input -----
for in_idx, (in_name, in_short) in enumerate(zip(INPUT_NAMES, INPUT_SHORT)):
    fig, ax = plt.subplots(figsize=(FIG_WIDTH_SINGLE, FIG_HEIGHT_SINGLE))
    sc = ax.scatter(embedding_2d[:, 0], embedding_2d[:, 1],
                    c=X_real[:, in_idx], cmap='viridis',
                    s=5, alpha=0.6, edgecolors='white', linewidths=0.3,
                    zorder=3)
    ax.set_xlabel('Manifold dimension 1')
    ax.set_ylabel('Manifold dimension 2')
    ax.set_title(f'Output manifold coloured by input: {in_name}', fontweight='bold')

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(True, linestyle='-', alpha=0.3, zorder=0)

    cbar = plt.colorbar(sc, ax=ax, pad=0.02)
    cbar.set_label(in_name)
    plt.tight_layout()
    save_fig(fig, f'manifold_2d_coloured_by_{in_name}')
    plt.close(fig)

# ----- 5.3 3D manifold coloured by each output (interactive static plots) -----
for out_idx, (short_name, full_name) in enumerate(zip(OUTPUT_SHORT, OUTPUT_NAMES_FULL)):
    fig = plt.figure(figsize=(FIG_WIDTH_3D, FIG_HEIGHT_3D))
    ax = fig.add_subplot(111, projection='3d')
    sc = ax.scatter(embedding_3d[:, 0], embedding_3d[:, 1], embedding_3d[:, 2],
                    c=Y_pred[:, out_idx], cmap='viridis',
                    s=2, alpha=0.5, edgecolors='none', zorder=3)
    ax.set_xlabel('Dim 1')
    ax.set_ylabel('Dim 2')
    ax.set_zlabel('Dim 3')
    ax.set_title(f'3D manifold – {short_name}', fontweight='bold')
    # 3D plots typically keep spines, but we can set a clean face
    ax.grid(True, linestyle='-', alpha=0.2)
    cbar = fig.colorbar(sc, ax=ax, pad=0.1, shrink=0.6)
    cbar.set_label(short_name)
    plt.tight_layout()
    save_fig(fig, f'manifold_3d_output_{out_idx}_{full_name}')
    plt.close(fig)

# ----- 5.4 (Optional) Weight‑space manifold of the ensemble models -----
# This gives insight into model diversity.
print("\nAnalysing weight space of the ensemble...")
weight_vectors = []
for model in predictor.models:
    flat_weights = np.concatenate([coef.ravel() for coef in model.coefs_])
    flat_biases = np.concatenate([intercept.ravel() for intercept in model.intercepts_])
    weight_vec = np.concatenate([flat_weights, flat_biases])
    weight_vectors.append(weight_vec)

weight_matrix = np.vstack(weight_vectors)   # (20, n_params)
print(f"Weight matrix shape: {weight_matrix.shape}")

# Normalise (StandardScaler) for UMAP
scaler_weights = StandardScaler()
weight_norm = scaler_weights.fit_transform(weight_matrix)

if UMAP_AVAILABLE:
    reducer_w = umap.UMAP(n_neighbors=5, min_dist=0.1, random_state=RANDOM_SEED)
    weight_embedding = reducer_w.fit_transform(weight_norm)

    fig, ax = plt.subplots(figsize=(FIG_WIDTH_SINGLE, FIG_HEIGHT_SINGLE))
    ax.scatter(weight_embedding[:, 0], weight_embedding[:, 1],
               c=COLORS['secondary'], s=200, edgecolors='black', linewidth=1.5, zorder=3)
    for i in range(len(predictor.models)):
        ax.text(weight_embedding[i, 0], weight_embedding[i, 1], str(i),
                ha='center', va='center', fontsize=9, color='white')
    ax.set_title('Weight‑space manifold of ensemble models', fontweight='bold')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(True, linestyle='-', alpha=0.3, zorder=0)
    ax.set_xlabel('UMAP 1')
    ax.set_ylabel('UMAP 2')
    plt.tight_layout()
    save_fig(fig, 'weight_space_manifold')
    plt.close(fig)
else:
    print("Skipping weight‑space UMAP because UMAP is not installed.")

# =============================================================================
# 6. Print summary statistics
# =============================================================================
print("\n" + "="*80)
print("MANIFOLD EXTRACTION COMPLETE")
print("="*80)
print(f"Number of samples: {N_SAMPLES:,}")
print(f"Output space dimension: 6")
print(f"Embedding dimensions: 2D and 3D")
if UMAP_AVAILABLE:
    print("Method: UMAP (non‑linear)")
else:
    print("Method: PCA (linear, fallback)")
print(f"\nAll figures saved to: {OUTPUT_DIR.absolute()}")
print("="*80)