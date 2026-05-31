"""
surrogate_jacobian_pca_analysis.py

Comprehensive surrogate model analysis:
1. Jacobian (sensitivity) across the whole dataset (exact via PyTorch autograd).
2. PCA on random predictions to visualise the output manifold.

Strictly follows the graph-design guidelines:
- serif font, L-frame, grid behind data
- Paul Tol colour palette / perceptually uniform colormaps
- markers with white edges
- Outputs to /mnt/user-data/outputs/ (adjustable)
"""

import sys
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.decomposition import PCA
import torch
import torch.nn as nn
import joblib
from predict import SurrogatePredictor

# =============================================================================
# Configuration & Paths
# =============================================================================
# Graph-design skill output directory (adjust if needed)
from model_build import OUTPUT_DIR
from model_build import DATASET
# Dataset path – update to match your location
DATA_PATH = DATASET
# If the above is not available, we can use a random grid; but the Jacobian
# analysis is more informative on the actual training points.
USE_DATASET = DATA_PATH.exists()
OUTPUT_DIR  = OUTPUT_DIR/"jacobean"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
# Input / output names (must match predictor)
input_names = ['beam_height', 'beam_length', 'fillet_size', 'beam_width']
input_short = ['h', 'L', 'f', 'w']
output_names = ['f1', 'f2', 'f3', 'f4', 'deform', 'stress']
output_full = ['modal_frequency_1', 'modal_frequency_2', 'modal_frequency_3',
               'modal_frequency_4', 'max_deformation', 'max_stress']

# =============================================================================
# Publication-quality styling (Graph Design Skill)
# =============================================================================
FIG_WIDTH_SINGLE = 6.0
FIG_HEIGHT_SINGLE = FIG_WIDTH_SINGLE / 1.3   # ~4.6"

FIG_WIDTH_MULTI = 9.0
FIG_HEIGHT_MULTI = 4.0

# Paul Tol colour palette (colorblind-safe)
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
# 1. Load surrogate predictor and extract scaling parameters
# =============================================================================
print("Loading surrogate predictor (ensemble of 20 MLPs)...")
predictor = SurrogatePredictor()
# The scalers are stored inside the predictor
scaler_X = predictor.scaler_X
scaler_Y = predictor.scaler_Y

# Input/output ranges (for real‑unit conversion)
input_min = scaler_X.mean_ - 3 * scaler_X.scale_   # approximate, but exact min/max
input_max = scaler_X.mean_ + 3 * scaler_X.scale_
# More accurate: load from saved scaling_params.json if available, but we can recompute
# from the scaler's inverse transform.
# Actually, the StandardScaler stores mean_ and scale_, so:
#   x_real = x_scaled * scale_ + mean_
# Therefore, the real unit scaling factor for the Jacobian is:
#   ∂y_real/∂x_real = ∂y_scaled/∂x_scaled * (scale_y / scale_x)
scale_x = scaler_X.scale_
scale_y = scaler_Y.scale_

# =============================================================================
# 2. Load dataset (or create a dense grid)
# =============================================================================
if USE_DATASET:
    df = pd.read_csv(DATA_PATH)
    X_real = df[input_names].values
    print(f"Loaded dataset: {len(X_real)} samples")
else:
    print("Dataset not found. Generating 5000 random samples for Jacobian analysis.")
    np.random.seed(42)
    n_samples = 5000
    low = np.array([5.0, 10.0, 0.1, 0.4])
    high = np.array([20.0, 18.0, 0.8, 1.0])   # from model_build.py
    X_real = np.random.uniform(low, high, size=(n_samples, 4))

# Scale inputs using the same scaler (to feed into the predictor)
X_scaled = scaler_X.transform(X_real)

# =============================================================================
# 3. Convert sklearn ensemble to PyTorch for exact autograd
# =============================================================================
class MLPRegressorPyTorch(nn.Module):
    """PyTorch replica of sklearn MLPRegressor for autograd."""
    def __init__(self, sklearn_model):
        super().__init__()
        self.layers = nn.ModuleList()
        for coef, intercept in zip(sklearn_model.coefs_, sklearn_model.intercepts_):
            layer = nn.Linear(coef.shape[0], coef.shape[1])
            # sklearn stores weights as (n_inputs, n_outputs); PyTorch uses (n_outputs, n_inputs)
            layer.weight.data = torch.tensor(coef.T, dtype=torch.float32)
            layer.bias.data = torch.tensor(intercept, dtype=torch.float32)
            self.layers.append(layer)
        self.activation = sklearn_model.activation

    def forward(self, x):
        for layer in self.layers[:-1]:
            x = layer(x)
            if self.activation == 'relu':
                x = torch.relu(x)
            elif self.activation == 'tanh':
                x = torch.tanh(x)
            elif self.activation == 'logistic':
                x = torch.sigmoid(x)
        x = self.layers[-1](x)   # output layer, no activation
        return x

class EnsembleTorch(nn.Module):
    """Ensemble of PyTorch models, returns mean prediction."""
    def __init__(self, sklearn_models):
        super().__init__()
        self.models = nn.ModuleList([MLPRegressorPyTorch(m) for m in sklearn_models])

    def forward(self, x):
        preds = torch.stack([model(x) for model in self.models])
        return torch.mean(preds, dim=0)

print("Converting ensemble to PyTorch...")
ensemble_torch = EnsembleTorch(predictor.models)
ensemble_torch.eval()

# =============================================================================
# 4. Compute Jacobian (exact) using PyTorch autograd
# =============================================================================
def compute_jacobian_torch(model, X_scaled):
    """
    model: PyTorch ensemble (returns mean)
    X_scaled: numpy array (n_samples, 4), already scaled
    Returns: J_scaled (n_samples, 6, 4)  where J[s,o,i] = ∂y_o / ∂x_i (scaled space)
    """
    n_samples = X_scaled.shape[0]
    n_outputs = 6
    n_inputs = 4
    J_scaled = np.zeros((n_samples, n_outputs, n_inputs))

    print(f"Computing Jacobian for {n_samples} samples using autograd...")
    for idx in range(n_samples):
        if (idx + 1) % 500 == 0:
            print(f"  Progress: {idx+1}/{n_samples}")

        x = torch.tensor(X_scaled[idx:idx+1], dtype=torch.float32, requires_grad=True)
        y = model(x)                     # shape (1,6)
        for out in range(n_outputs):
            # Zero previous gradients
            if x.grad is not None:
                x.grad.zero_()
            y[0, out].backward(retain_graph=True)
            J_scaled[idx, out, :] = x.grad.detach().cpu().numpy()[0]

    print("Jacobian computation finished.")
    return J_scaled

# Compute scaled Jacobian
J_scaled = compute_jacobian_torch(ensemble_torch, X_scaled)

# Convert to real units: J_real = J_scaled * (scale_y / scale_x)  (elementwise per input/output)
scale_ratio = scale_y[:, np.newaxis] / scale_x[np.newaxis, :]   # shape (6,4)
J_real = J_scaled * scale_ratio

print(f"Jacobian shapes: scaled {J_scaled.shape}, real {J_real.shape}")

# =============================================================================
# 5. Visualisation A: Global mean absolute Jacobian heatmap (6×4)
# =============================================================================
mean_abs_J = np.mean(np.abs(J_real), axis=0)   # (6,4)

fig, ax = plt.subplots(figsize=(FIG_WIDTH_SINGLE, FIG_HEIGHT_SINGLE))
im = ax.imshow(mean_abs_J, cmap='viridis', aspect='auto')

# Annotations
for i in range(6):
    for j in range(4):
        val = mean_abs_J[i, j]
        text_color = 'white' if val > mean_abs_J.max() * 0.5 else 'black'
        ax.text(j, i, f'{val:.2e}', ha='center', va='center', color=text_color, fontsize=8)

ax.set_xticks(range(4))
ax.set_yticks(range(6))
ax.set_xticklabels(input_short, rotation=45, ha='right')
ax.set_yticklabels(output_names)
ax.set_xlabel('Input parameters')
ax.set_ylabel('Output quantities')
ax.set_title('Global mean absolute sensitivity |∂output/∂input|', fontweight='bold')

# L‑frame (remove top/right spines)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.grid(False)

cbar = plt.colorbar(im, ax=ax, shrink=0.8, pad=0.02)
cbar.set_label('Sensitivity (real units)')
plt.tight_layout()
save_fig(fig, 'global_jacobian_heatmap')

# Print summary
print("\nGlobal sensitivity summary (mean |J|):")
for i, out in enumerate(output_names):
    max_idx = np.argmax(mean_abs_J[i])
    print(f"  {out:6s} most sensitive to {input_short[max_idx]:2s} : {mean_abs_J[i, max_idx]:.2e}")

# =============================================================================
# 6. Visualisation B: Per‑output 2D colormaps (variation across input pairs)
# =============================================================================
input_pairs = [(0,1), (0,2), (0,3), (1,2), (1,3), (2,3)]
pair_labels = [f'{input_short[i]} vs {input_short[j]}' for i,j in input_pairs]

for out_idx in range(6):
    fig, axes = plt.subplots(2, 3, figsize=(FIG_WIDTH_MULTI, FIG_HEIGHT_MULTI))
    axes = axes.flatten()
    out_name = output_names[out_idx]

    for sub_idx, (i, j) in enumerate(input_pairs):
        ax = axes[sub_idx]
        # Sensitivity w.r.t input i (absolute)
        sens = np.abs(J_real[:, out_idx, i])

        # Scatter plot – colour by sensitivity, size fixed
        sc = ax.scatter(X_real[:, i], X_real[:, j],
                        c=sens, cmap='viridis', s=20,
                        edgecolors='white', linewidths=0.5,
                        alpha=0.7, norm=plt.matplotlib.colors.LogNorm(vmin=1e-6, vmax=sens.max()))

        ax.set_xlabel(input_short[i])
        ax.set_ylabel(input_short[j])
        ax.set_title(f'|∂{out_name}/∂{input_short[i]}|', fontsize=9)

        # L‑frame + grid behind
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.grid(True, linestyle='-', alpha=0.3, zorder=0)

        # Colour bar for each subplot (optional, but can add a common one later)
        cbar = plt.colorbar(sc, ax=ax, fraction=0.046, pad=0.04)
        cbar.ax.tick_params(labelsize=7)

    fig.suptitle(f'Output: {out_name} — Jacobian variation across input space', fontweight='bold')
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    save_fig(fig, f'jacobian_maps_output_{out_name}')
    plt.close(fig)

# =============================================================================
# 7. PCA on random predictions (manifold mapping)
# =============================================================================
print("\n" + "="*60)
print("PCA MANIFOLD ANALYSIS")
print("="*60)

# Generate random inputs
np.random.seed(42)
n_pca = 5000
X_pca_real = np.random.uniform(low=[5,10,0.1,0.4], high=[20,18,0.8,1.0], size=(n_pca,4))
df_pca = pd.DataFrame(X_pca_real, columns=input_names)
Y_pred = predictor.predict_batch(df_pca).values   # (n_pca,6)

pca = PCA(n_components=6)
Y_pca = pca.fit_transform(Y_pred)

print("PCA explained variance ratio:")
for i, ev in enumerate(pca.explained_variance_ratio_):
    print(f"  PC{i+1}: {ev:.4f}")
print(f"Cumulative first two: {np.sum(pca.explained_variance_ratio_[:2]):.4f}")

# 7a: Explained variance bar plot + cumulative line
fig, ax = plt.subplots(figsize=(FIG_WIDTH_SINGLE, FIG_HEIGHT_SINGLE))
components = np.arange(1, 7)
ax.bar(components, pca.explained_variance_ratio_, color=COLORS['primary'],
       edgecolor='black', linewidth=0.5, label='Individual')
ax.plot(components, np.cumsum(pca.explained_variance_ratio_),
        color=COLORS['secondary'], marker='o', markersize=6, linewidth=2, label='Cumulative')

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(True, axis='y', linestyle='-', alpha=0.5, zorder=0)

ax.set_xlabel('Principal component')
ax.set_ylabel('Explained variance ratio')
ax.set_title('PCA explained variance', fontweight='bold')
ax.legend(frameon=False, loc='lower right')

# Annotate cumulative
for i, cum in enumerate(np.cumsum(pca.explained_variance_ratio_), start=1):
    ax.text(i, cum + 0.02, f'{cum:.2f}', ha='center', fontsize=8)

plt.tight_layout()
save_fig(fig, 'pca_explained_variance')

# 7b: Manifold (PC1 vs PC2) coloured by beam height
fig, ax = plt.subplots(figsize=(FIG_WIDTH_SINGLE, FIG_HEIGHT_SINGLE))
sc = ax.scatter(Y_pca[:, 0], Y_pca[:, 1],
                c=X_pca_real[:, 0],   # beam height
                cmap='viridis', s=10,
                edgecolors='white', linewidths=0.8,
                alpha=0.7, zorder=3)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(True, linestyle='-', alpha=0.5, zorder=0)

ax.set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.1%} var)')
ax.set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.1%} var)')
ax.set_title('Output manifold (first two principal components)', fontweight='bold')

cbar = fig.colorbar(sc, ax=ax, pad=0.02)
cbar.set_label('Beam height (mm)')

plt.tight_layout()
save_fig(fig, 'manifold_pc1_pc2_coloured_by_height')

print("\nAll analyses complete. Figures saved to:", OUTPUT_DIR)