# Flexure Beam Ensemble Surrogate Model

This repository implements a high-fidelity probabilistic surrogate model designed to predict the structural and modal characteristics of a flexure beam. By leveraging an ensemble of neural networks trained on Finite Element Analysis (FEA) data, the model provides a computationally efficient alternative to traditional simulations, enabling real-time design exploration and uncertainty quantification.

## Overview

The model maps geometric input parameters to six distinct physical responses. Unlike standard "black-box" regressors, this implementation uses an ensemble approach to provide both a mean prediction and a measure of uncertainty (standard deviation), ensuring the reliability of the surrogate in a design exploration context.

### Model Specifications
- **Inputs**: Beam Height, Beam Length, Fillet Size, Beam Width.
- **Outputs**: First four modal frequencies (Hz), maximum deformation (mm), and maximum von Mises stress (MPa).
- **Architecture**: Ensemble of 20 Multi-Layer Perceptron (MLP) regressors.(Has 1 hidden layer)
- **Data Pipeline**: Standard scaling of inputs and targets to ensure numerical stability and convergence.

## Repository Structure

- `model_build.py`: The complete pipeline for data preprocessing, scaling, ensemble training, and performance evaluation.
- `predict.py`: Implements the `SurrogatePredictor` class, a production-ready API for performing inferences with uncertainty quantification.
- `models/`: Contains the serialized ensemble (`ensemble_20_models.pkl`) and the associated scalers.
- `dataset/`: The FEA-generated dataset used for training and validation.
- `plots/`: Diagnostic visualizations, including correlation heatmaps of the target outputs.

## Usage

### Training the Ensemble
To train the ensemble and evaluate its performance, execute:
```bash
python model_build.py
```
The script performs bootstrap sampling to create 20 diverse models, calculates the ensemble mean, and reports the $R^2$ and MAPE for each target.

### Making Predictions with Uncertainty
The `SurrogatePredictor` class allows for both point predictions and probabilistic inferences.

```python
from predict import SurrogatePredictor

# Initialize the predictor
predictor = SurrogatePredictor()

# Predict with uncertainty (mean and standard deviation)
result = predictor.predict_single_with_uncertainty(
    beam_height=10.0, 
    beam_length=12.5, 
    fillet_size=0.3, 
    beam_width=0.6
)

print(f"Mean: {result['mean']}")
print(f"Uncertainty (std): {result['std']}")
```

## Performance

The model achieves "Detailed Design" grade precision, with all target parameters maintaining an error rate (MAPE) of less than 5%.

| Target Parameter | $R^2$ Score | MAPE (%) |
| :--- | :--- | :--- |
| Modal Frequency 1 | 0.9961 | 1.60% |
| Modal Frequency 2 | 0.9995 | 0.47% |
| Modal Frequency 3 | 0.9987 | 0.61% |
| Modal Frequency 4 | 0.9948 | 1.29% |
| Max Deformation | 0.9849 | 3.56% |
| Max Stress | 0.9686 | 4.00% |

The inclusion of the ensemble standard deviation ($\pm \sigma$) allows for the identification of high-uncertainty regions in the design space, transforming the surrogate from a simple approximation tool into a reliable structural analysis utility.
