## Jacobean Sensitivity Analysis of 20 Ensemble model:
Size 4,256,6 x 20 
now Jacobean matrix $j$ for the surrogate is $6*4$ 
$$
J_{ij} = \frac{\partial \hat{y}_{i}}{\partial x_{i}}
$$
It describes how much each output changes for a small change in each input - a local, linearized sensitivity.
### Computing Jacobean Sensitivity from 20 Ensemble model

- Normalizing the Jacobean gives Elasticity(percent change):
$$
elasticity_{ij} = \frac{x_i}{y_i} * J_{ij}
$$
- Then answer -> *A 1% increase in beam height reduces the max stress by X%* - this is very meaningful for the design.
---

## Manifold Extraction from 20 Ensemble Model
