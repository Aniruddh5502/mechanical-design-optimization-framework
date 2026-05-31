this thesis will be a thesis of a design optimizer.
- learn from Ansys simulations -> Ground reality for physics
- train ml model to capture the design space and predict outputs with fractionof compute cost
- run the optimizer with required parameteric range and reverse ml model runs that
- gives you input parameter sets for the expected outputs/properties you want
- use Ansys sims to see if the predictions work, update models if it doesn't
- DONE

## Novelity
- Jacobean Analysis + Physical interpretation, comparison to analytical beam theory(flexure theory)(e.g., gradients should have expected signs: longer beam → lower frequency → negative derivative), that becomes a verification and explainability contribution.

- PCA on the predicted outputs(for many random inputs)
    - See how many components explain 99 percent variance.
    - If its 2 or 3  that indicates a low dimensional output manifold.

- Manifold Extraction(learning lowrer dimensional structure of the input-output mapping)
    - Can involve Autoencoder on inputs + outputs to find intrinsic dimension.
    - PCA(Principle Component Analysis) on joint space
    - Find intrinsic lower-dimensional representation, show it matches 