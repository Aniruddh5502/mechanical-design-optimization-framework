import os
import sys
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
from pathlib                    import Path
from sklearn.preprocessing      import StandardScaler
from sklearn.model_selection    import train_test_split
from sklearn.model_selection    import cross_val_score
from sklearn.neural_network     import MLPRegressor
from sklearn.metrics            import r2_score, mean_absolute_percentage_error


if 'ipykernel' in sys.modules:
    ROOT = Path().resolve().parent  
else:
    ROOT = Path(__file__).parent 

MODEL_PATH      =       ROOT / "models"
DATASET_DIR     =       ROOT / "dataset"
SCALER_PATH     =       ROOT / "models"  / "scalers"
SPLIT_PATH      =       ROOT / "models"  / "split"
DATASET         =       ROOT / "dataset" / "dataset.csv"
OUTPUT_DIR      =       ROOT / "plots"

# Create directories (safe to do at import – just creates folders)
DATASET_DIR.mkdir(parents=True,exist_ok=True)
SCALER_PATH.mkdir(parents=True,exist_ok=True)
SPLIT_PATH.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
MODEL_PATH.mkdir(parents=True, exist_ok=True)


def save_fig(fig, name):
    png_path = OUTPUT_DIR / f"{name}.png"
    svg_path = OUTPUT_DIR / f"{name}.svg"
    fig.savefig(png_path, dpi=1000, bbox_inches='tight', facecolor='white')
    fig.savefig(svg_path, dpi=72,   bbox_inches='tight', facecolor='white')
    print(f"Saved: {png_path} and {svg_path}")


def main():
    # ------------------------------------------------------------------
    # All original code from here onward (exactly as provided)
    # ------------------------------------------------------------------
    df = pd.read_csv(DATASET).dropna()

    feature_columns = ['beam_height', 'beam_length', 'fillet_size', 'beam_width']
    target_columns  = [col for col in df.columns if col not in feature_columns]

    # informations about the dataset
    print("\n"*4)
    print("="*90)
    print("                                BASIC DATA PROPERTIES ")
    print("="*90)
    print(f"1. Number of samples        : {len(df)}")
    print(f"2. Number of input features : {len(feature_columns)}")
    print(f"3. Number of output targets : {len(target_columns)}")
    print(f"\n4. Input features: \n{feature_columns}")
    print(f"5. Output targets: \n{target_columns}")
    print(f"\n6. Input value ranges: ")
    for col in feature_columns:
        print(f"    {col:<40}   :   {df[col].min():<10.4f}, {df[col].max():<10.4f}")

    print(f"\n7. Output value ranges: ")
    for col in target_columns:
        print(f"    {col:<40}   :   {df[col].min():<10.4f}, {df[col].max():<10.4f}")

    # Data scaling stratagy
    # Seperate Features and Targets
    X = df[feature_columns].values
    Y = df[target_columns].values

    # Creating scales
    scaler_X = StandardScaler()
    scaler_Y = StandardScaler()

    # Fit Scalers
    X_scaled = scaler_X.fit_transform(X)
    Y_scaled = scaler_Y.fit_transform(Y)

    # Dumping scaling informations
    joblib.dump(scaler_X, SCALER_PATH / "scaler_X.pkl")
    joblib.dump(scaler_Y, SCALER_PATH / "scaler_Y.pkl")

    # Printing out scaling informations
    print("\n"*4)
    print("="*90)
    print("                                SCALING PARAMETERS SAVED ")
    print("="*90)
    print("Input scaler (X) parameters: ")
    print(f"    Mean  : {scaler_X.mean_}")
    print(f"    Std   : {scaler_X.scale_}")
    print(f"    Shape : {scaler_X.mean_.shape}")

    print(f"\nOutput scaler (y) parameters:")
    print(f"  Mean : {scaler_Y.mean_}")
    print(f"  Std  :  {scaler_Y.scale_}")
    print(f"  Shape: {scaler_Y.mean_.shape}")

    print(f"\nScalers saved to: {SCALER_PATH}")
    print(f"  - scaler_X.pkl (for inputs)")
    print(f"  - scaler_Y.pkl (for outputs)")

    # Verify scaling worked
    print("\n\n")
    print("="*90)
    print("                                     VEIFICATION")
    print("="*90)
    print(f"Original X[0]: {X[0]}")
    print(f"Scaled X[0]:   {X_scaled[0]}")
    print(f"Mean of scaled X: {X_scaled.mean(axis=0)} (should be ~0)")
    print(f"Std of scaled X:  {X_scaled.std(axis=0)} (should be ~1)")

    # split the scaled data
    X_train, X_test, Y_train, Y_test = train_test_split(
        X_scaled, Y_scaled,
        test_size    = 0.02,     # 20% for testing
        random_state = 42       # Reproducable split
    )
    print("\n\n")
    print("="*90)
    print("                                DATA SPLIT CONFIG ")
    print("="*90)
    print(f"Training set size:      {len(X_train):<5} samples ({len(X_train)/len(X_scaled)*100:<5.4f}%)")
    print(f"Test set size    :      {len(X_test):<5} samples ({len(X_test)/len(X_scaled)*100:<5.4f}%)")
    print(f"\nInput dimension:     {X_train.shape[1]}")
    print(f"Output dimension:    {Y_train.shape[1]}")

    # Check the split is representative
    print("="*90)
    print(f"                             SPLIT QUALITY CHECK ")
    print("="*90)
    print(f"Training X mean:     {X_train.mean(axis=0)}")
    print(f"Test X mean:         {X_test.mean(axis=0)}")
    print(f"\nTraining Y mean:     {Y_train.mean(axis=0)}")
    print(f"Test Y mean:         {Y_test.mean(axis=0)}")

    np.save(SPLIT_PATH / "X_train.npy", X_train)
    np.save(SPLIT_PATH / "X_test.npy", X_test)
    np.save(SPLIT_PATH / "Y_train.npy", Y_train)
    np.save(SPLIT_PATH / "Y_test.npy", Y_test)

    print(f"\n[DONE] Split data saved to: {SPLIT_PATH}")

    # =======================================================================
    #                 MODEL ARCHITECTURE
    # =======================================================================

    # ----------------------------------------------------------------------
    #  Typography & style (serif, clean L‑frame)
    # ----------------------------------------------------------------------
    plt.rcParams.update({
        'font.family': 'serif',
        'font.size': 10,
        'axes.labelsize': 11,
        'axes.titlesize': 12,
        'xtick.labelsize': 9,
        'ytick.labelsize': 9,
    })

    # Figure dimensions (single column, 6" width)
    FIG_WIDTH = 6.0
    FIG_HEIGHT = FIG_WIDTH / 1.3   # ~4.6" height

    # ----------------------------------------------------------------------
    #  Compute correlation matrix
    # ----------------------------------------------------------------------
    output_corr = df[target_columns].corr()
    n_vars = len(target_columns)

    # ----------------------------------------------------------------------
    #  Pure matplotlib heatmap (no seaborn)
    # ----------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(FIG_WIDTH, FIG_HEIGHT))

    # Diverging colormap (Paul Tol 'coolwarm' equivalent)
    cmap = plt.cm.coolwarm

    # Plot the matrix
    im = ax.imshow(output_corr, cmap=cmap, vmin=-1, vmax=1, aspect='auto', zorder=1)

    # Add text annotations
    for i in range(n_vars):
        for j in range(n_vars):
            text = ax.text(j, i, f'{output_corr.iloc[i, j]:.2f}',
                           ha="center", va="center",
                           color="white" if abs(output_corr.iloc[i, j]) > 0.5 else "black",
                           fontsize=8, zorder=3)

    # Tick labels (shortened for readability)
    short_labels = [col for col in target_columns]
    ax.set_xticks(np.arange(n_vars))
    ax.set_yticks(np.arange(n_vars))
    ax.set_xticklabels(short_labels, rotation=45, ha='right', rotation_mode='anchor')
    ax.set_yticklabels(short_labels)

    # L‑frame: remove top/right spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

    # Grid behind data (only ticks, no grid lines needed for heatmap)
    ax.grid(False)

    # Colorbar
    cbar = fig.colorbar(im, ax=ax, shrink=0.8, pad=0.02)
    cbar.set_label('Pearson correlation', fontsize=10)

    ax.set_title('Output Correlations – Modal vs Static Results', fontweight='bold', pad=12)

    plt.tight_layout()
    save_fig(fig, 'output_correlation_heatmap')

    print("="*90)
    print("                             OUTPUT CORRELATION ANALYSIS ")
    print("="*90)
    print("\nModal frequencies (0-3) correlations: ")
    for i in range(4):
        for j in range(i+1, 4):
            print(f"   {target_columns[i][:20]} vs {target_columns[j][:20]} : {output_corr.iloc[i,j]:.3f}")

    print("\nModal vs Static correlations:")
    for i in range(4):  # modal outputs
        for j in range(4, 6):  # static outputs
            print(f"  {target_columns[i][:20]} vs {target_columns[j][:20]}: {output_corr.iloc[i,j]:.3f}")

    # Test larger architectures for maximum accuracy
    architectures_max = [
        (4, 5,  6),           # baseline 0.9246
        (4, 32, 6),           # 358 params
        (4, 64, 6),           # 646 params  
        (4, 128, 6),          # 1350 params
        (4, 64, 32, 6),       # 2598 params
        (4, 128, 64, 6),      # 10310 params
        (4, 256, 128, 6),     # 41158 params
    ]
    print("="*90)
    print("                     MAXIMUM ACCURACY (INTERPOLATION) ")
    print("="*90)
    # Get baseline from smallest model we tested earlier
    baseline_r2 = 0.9346  # from (4,8,6) architecture

    for arch in architectures_max:
        params = 0
        for i in range(len(arch)-1):
            params += arch[i] * arch[i+1] + arch[i+1]
        
        model = MLPRegressor(
            hidden_layer_sizes=arch[1:-1],
            activation='relu',
            max_iter=2000,  # More iterations
            random_state=42,
            early_stopping=True,
            validation_fraction=0.1,
            tol=1e-8  # Tighter tolerance
        )
        
        scores = cross_val_score(model, X_train, Y_train, 
                                 cv=5, scoring='r2')
        
        print(f"Arch: {arch}")
        print(f"  Params: {params}")
        print(f"  CV R²: {scores.mean():.6f} (±{scores.std():.6f})")
        print(f"  Improvement: {(scores.mean() - baseline_r2)*100:.2f}%")
        
        # Check if improvement plateaus
        if params > 5000 and scores.std() < 0.001:
            print(f"  → Plateau reached, diminishing returns beyond this")
        print()
        
    # The results indicate that (4,128,6) is better in cost efficiency and output accuracy
    # This will be the selected architecture for the surrogate model
    # as it produces close enough result to Arch: (4, 256, 128, 6) with 4.51%
    # but with very much less parameter count effecting the inference

    # ======================================================================
    #                            ENSEMBLE TRAINING (20 models)
    # ======================================================================
    print("\n"*5)
    print("="*90)
    print("                         TRAINING ENSEMBLE OF 20 MODELS")
    print("="*90)

    n_ensemble = 20
    ensemble_models = []

    for i in range(n_ensemble):
        # Bootstrap sample from training set
        np.random.seed(i)   # ensure reproducibility of bootstrap indices
        idx = np.random.choice(len(X_train), len(X_train), replace=True)
        X_boot = X_train[idx]
        Y_boot = Y_train[idx]
        
        model = MLPRegressor(
            hidden_layer_sizes=(256,),      # same as final model
            activation='relu',
            solver='adam',
            max_iter=20000,
            random_state=i,                 # different seed for init / shuffle
            early_stopping=True,
            validation_fraction=0.2,
            tol=1e-10,
            verbose=False,
            n_iter_no_change=1000
        )
        model.fit(X_boot, Y_boot)
        ensemble_models.append(model)
        print(f"Trained model {i+1}/{n_ensemble}")

    # Evaluate ensemble on test set
    y_pred_scaled_ensemble = np.mean(
        [model.predict(X_test) for model in ensemble_models], axis=0
    )
    y_pred = scaler_Y.inverse_transform(y_pred_scaled_ensemble)
    y_test_original = scaler_Y.inverse_transform(Y_test)

    print("\n=== ENSEMBLE MODEL PERFORMANCE ===")
    for i, target_name in enumerate(target_columns):
        r2 = r2_score(y_test_original[:, i], y_pred[:, i])
        mape = mean_absolute_percentage_error(y_test_original[:, i], y_pred[:, i])
        print(f"{target_name[:35]:35} | R²: {r2:.4f} | MAPE: {mape:.2%}")

    # Save the entire ensemble
    joblib.dump(ensemble_models, MODEL_PATH / "ensemble_20_models.pkl")
    print(f"\n[DONE] Ensemble saved to: {MODEL_PATH/'ensemble_20_models.pkl'}")


if __name__ == "__main__":
    main()