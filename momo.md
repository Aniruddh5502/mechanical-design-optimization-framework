# Project Analysis: Mechanical Design Optimization Framework

## 1. Current Codebase Structure
The current repository is organized as a research project with a flat structure. Most logic resides in standalone scripts at the root level.

### Directory Tree
- `dataset/`: Input parameter grids and FEA results (`dataset.csv`).
- `models/`: Trained ensemble weights (`ensemble_20_models.pkl`) and scaling factors.
- `plots/`: Generated visualization files.
- `verification/`: Verification scripts/data.

### Script Mapping
| Script | Purpose |
| :--- | :--- |
| `dataset_gen.py` | Generates input parameter grid. |
| `sweep.py` | Automates ANSYS Workbench execution. |
| `ansys_runner.py` | Communication interface for ANSYS. |
| `model_build.py` | Training pipeline for the MLP ensemble. |
| `predict.py` | Inference engine with uncertainty estimation. |
| `optimization.py` | Design optimization logic. |
| `manifold-extraction.py` | UMAP/PCA dimensionality reduction. |
| `model-analysis.py` | Jacobian sensitivity analysis. |
| `process_runner.py` | Execution utility to capture logs to markdown. |
| `clean_logs.py` | Maintenance utility for temporary files. |
| `main.py` | General entry point. |

---

## 2. Proposed Standard Restructuring
To transition this from a research script collection to a maintainable software framework, I propose the following structure.

### Target Structure
```text
project_root/
├── data/                   # Data storage
│   ├── raw/                # Initial generated grids
│   └── processed/          # FEA results and cleaned datasets
├── models/                 # Model artifacts (pkl, scalars)
├── plots/                  # Visualization outputs
├── src/                    # Core source code
│   ├── __init__.py
│   ├── core/               # Model logic
│   │   ├── predictor.py    # (from predict.py)
│   │   └── trainer.py      # (from model_build.py)
│   ├── simulation/         # FEA/ANSYS integration
│   │   ├── runner.py       # (from ansys_runner.py)
│   │   └── sweep.py        # (from sweep.py)
│   ├── analysis/           # Post-processing & Optimization
│   │   ├── manifold.py     # (from manifold-extraction.py)
│   │   ├── sensitivity.py   # (from model-analysis.py)
│   │   └── optimization.py  # (from optimization.py)
│   └── utils/               # Helper utilities
│       ├── logging.py      # (from process_runner.py)
│       └── cleanup.py      # (from clean_logs.py)
├── tests/                  # Unit and integration tests (from verification/)
├── scripts/                # CLI Entry points
│   ├── generate_data.py    # (from dataset_gen.py)
│   ├── train.py            # Wrapper for src.core.trainer
│   ├── predict.py         # Wrapper for src.core.predictor
│   └── main.py             # Top-level coordinator
├── config/                  # Configuration files (yaml/json)
├── .gitignore
├── requirements.txt        # Dependency list
└── README.md
```

### Rationale for Changes
1. **Separation of Concerns**: Decouples the *logic* (in `src/`) from the *execution* (in `scripts/`).
2. **Modularity**: Grouping related functionality (e.g., all ANSYS logic in `simulation/`) makes it easier to update the FEA backend without touching the ML model.
3. **Testability**: Moving verification to a dedicated `tests/` folder allows for the use of standard frameworks like `pytest`.
4. **Data Integrity**: Distinguishing between `raw` and `processed` data prevents accidental overwrites of the original design grids.
5. **Maintainability**: Using a `config/` directory avoids hard-coding paths and parameters inside the Python scripts.

---

## 3. Implementation Roadmap (Future)
1. **Phase 1**: Setup the directory hierarchy and move files.
2. **Phase 2**: Refactor imports from absolute root paths to package-relative imports (`from src.core...`).
3. **Phase 3**: Extract hard-coded constants into `config/settings.yaml`.
4. **Phase 4**: Implement a proper `requirements.txt` and `setup.py` for environment reproducibility.
