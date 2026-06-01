# Accelerometer Flexure Surrogate Model

This repository contains a probabilistic surrogate model for a single-degree-of-freedom (SDOF) accelerometer flexure geometry. The model is designed to predict modal and structural responses based on geometric parameters, facilitating the analysis of cross-axis modal separation and structural integrity without requiring repeated high-cost Finite Element Analysis (FEA).

## Project Objective

The goal is to replace computationally expensive FEA simulations with a fast, accurate surrogate model. By training an ensemble of neural networks, the system predicts the first four modal frequencies, maximum deformation, and maximum stress, while providing a measure of uncertainty to ensure the predictions are reliable for engineering decisions.

## Geometry and Design
The surrogate model focuses on a flexure beam geometry intended for a MEMS accelerometer. The primary design objectives include:
- **Single Degree of Freedom (SDOF)**: Ensuring the structure responds primarily along the intended axis.
- **Cross-Axis Modal Separation**: Maximizing the frequency gap between the primary mode and transverse/torsional modes to avoid signal interference.

## Input and Output Parameters

### Input Geometric Parameters
- **Beam Height**: Vertical dimension of the flexure.
- **Beam Length**: Longitudinal dimension of the flexure.
- **Fillet Size**: Radius of the fillets to reduce stress concentrations.
- **Beam Width**: Lateral dimension of the flexure.

### Output Physical Responses
- **Modal Frequencies (1-4)**: The first four natural frequencies of the structure (Hz).
- **Maximum Deformation**: The peak displacement under design load (mm).
- **Maximum Stress**: The peak von Mises stress to ensure the material remains within the elastic limit (MPa).

## Repository Structure

### Core Scripts
- `model_build.py`: Full pipeline for data loading, scaling, ensemble training, and performance metrics.
- `predict.py`: Contains the `SurrogatePredictor` class for making fast inferences with uncertainty.
- `dataset_gen.py`: Generates the input parameter grid based on design bounds.
- `sweep.py`: Automates the execution of Ansys Workbench to populate the dataset.
- `ansys_runner.py`: Handles the communication and parameter updates within Ansys Workbench.
- `clean_logs.py`: Maintenance script to clear temporary log files.
- `process_runner.py`: Utility to execute scripts and save their terminal output to markdown files.

### Analysis and Visualization
- `manifold-extraction.py`: Uses UMAP/PCA to visualize the output manifold and weight space.
- `model-analysis.py`: Conducts Jacobian sensitivity analysis to see how inputs affect outputs.

### Folders
- `models/`: Stores the trained ensemble (`ensemble_20_models.pkl`) and scaling parameters.
- `dataset/`: Contains the `dataset.csv` used for training and validation.
- `ansys_files/`: Project files and parameter definitions for Ansys Workbench.
- `plots/`: Stores all generated figures and analysis results.

## Installation and Setup

### Prerequisites
- Python 3.x
- Required Libraries: `numpy`, `pandas`, `scikit-learn`, `matplotlib`, `joblib`
- Optional: `umap-learn` (for manifold extraction), `termcolor` (for formatted logs).
### Running the Pipeline
1. **Data Generation**:
   Run `dataset_gen.py` to create the input grid in `dataset/dataset.csv`.
   ```bash
   python dataset_gen.py
   ```
2. **FEA Data Collection**:
   Ensure Ansys Workbench is open and the server port is known. Run `sweep.py` and enter the port number when prompted.
   ```bash
   python sweep.py
   ```

3. **Model Training**:
   Train the ensemble of 20 MLP regressors.
   ```bash
   python model_build.py
   ```

4. **Inference**:
   Use the `SurrogatePredictor` in `predict.py` to get results for new geometries.

## Performance Metrics

The model is evaluated using $R^2$ and Mean Absolute Percentage Error (MAPE).

| Target Parameter  | R2 Score | MAPE (%) |
| :---------------- | :------- | :------- |
| Modal Frequency 1 | 0.9961   | 1.60%    |
| Modal Frequency 2 | 0.9995   | 0.47%    |
| Modal Frequency 3 | 0.9987   | 0.61%    |
| Modal Frequency 4 | 0.9948   | 1.29%    |
| Max Deformation   | 0.9849   | 3.56%    |
| Max Stress        | 0.9686   | 4.00%    |
