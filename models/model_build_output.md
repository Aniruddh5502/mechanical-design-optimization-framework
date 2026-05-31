## Output from model_build.py

```text

==========================================================================================
                                BASIC DATA PROPERTIES 
==========================================================================================
1. Number of samples        : 1295
2. Number of input features : 4
3. Number of output targets : 6

4. Input features: 
['beam_height', 'beam_length', 'fillet_size', 'beam_width']
5. Output targets: 
['modal_frequency_1', 'modal_frequency_2', 'modal_frequency_3', 'modal_frequency_4', 'max_deformation', 'max_stress ']

6. Input value ranges: 
    beam_height                                :   5.0000    , 20.0000   
    beam_length                                :   10.0000   , 17.0000   
    fillet_size                                :   0.1000    , 0.6000    
    beam_width                                 :   0.4000    , 0.8000    

7. Output value ranges: 
    modal_frequency_1                          :   65.5096   , 449.0734  
    modal_frequency_2                          :   462.6255  , 1628.6322 
    modal_frequency_3                          :   531.9205  , 1691.9936 
    modal_frequency_4                          :   559.3348  , 1921.3576 
    max_deformation                            :   0.0139    , 0.5923    
    max_stress                                 :   0.8409    , 6.6401    





==========================================================================================
                                SCALING PARAMETERS SAVED 
==========================================================================================
Input scaler (X) parameters: 
    Mean  : [12.4965251  13.49837838  0.34980695  0.60009266]
    Std   : [5.12392634 2.39116562 0.17070703 0.13663804]
    Shape : (4,)

Output scaler (y) parameters:
  Mean : [1.87695684e+02 1.09124181e+03 1.17531541e+03 1.36266992e+03
 1.10859572e-01 2.53754280e+00]
  Std  :  [7.00140653e+01 2.43518304e+02 2.50077707e+02 2.64834243e+02
 9.38064383e-02 1.19334188e+00]
  Shape: (6,)

Scalers saved to: C:\Users\Administrator\Desktop\code\momobot\WORKSPACE\obsidian\thesis_02\models\scalers
  - scaler_X.pkl (for inputs)
  - scaler_Y.pkl (for outputs)



==========================================================================================
                                     VEIFICATION
==========================================================================================
Original X[0]: [ 5.  10.   0.1  0.4]
Scaled X[0]:   [-1.4630431  -1.4630431  -1.46336652 -1.46439945]
Mean of scaled X: [-1.52259158e-16 -6.47787272e-16  2.63367192e-16  4.49918952e-16] (should be ~0)
Std of scaled X:  [1. 1. 1. 1.] (should be ~1)



==========================================================================================
                                DATA SPLIT CONFIG 
==========================================================================================
Training set size:      1269  samples (97.9923%)
Test set size    :      26    samples (2.0077%)

Input dimension:     4
Output dimension:    6
==========================================================================================
                             SPLIT QUALITY CHECK 
==========================================================================================
Training X mean:     [ 0.00367713 -0.01293247  0.00274656  0.00232078]
Test X mean:         [-0.17947214  0.63120426 -0.13405349 -0.11327212]

Training Y mean:     [ 0.00969526  0.01091075  0.01069207  0.01349021 -0.00797286 -0.00391285]
Test Y mean:         [-0.47320336 -0.53252861 -0.52185511 -0.65842595  0.38913681  0.19097717]

[DONE] Split data saved to: C:\Users\Administrator\Desktop\code\momobot\WORKSPACE\obsidian\thesis_02\models\split
Saved: C:\Users\Administrator\Desktop\code\momobot\WORKSPACE\obsidian\thesis_02\plots\output_correlation_heatmap.png and C:\Users\Administrator\Desktop\code\momobot\WORKSPACE\obsidian\thesis_02\plots\output_correlation_heatmap.svg
==========================================================================================
                             OUTPUT CORRELATION ANALYSIS 
==========================================================================================

Modal frequencies (0-3) correlations: 
   modal_frequency_1 vs modal_frequency_2 : 0.740
   modal_frequency_1 vs modal_frequency_3 : 0.672
   modal_frequency_1 vs modal_frequency_4 : 0.759
   modal_frequency_2 vs modal_frequency_3 : 0.979
   modal_frequency_2 vs modal_frequency_4 : 0.839
   modal_frequency_3 vs modal_frequency_4 : 0.789

Modal vs Static correlations:
  modal_frequency_1 vs max_deformation: -0.796
  modal_frequency_1 vs max_stress : -0.766
  modal_frequency_2 vs max_deformation: -0.672
  modal_frequency_2 vs max_stress : -0.540
  modal_frequency_3 vs max_deformation: -0.626
  modal_frequency_3 vs max_stress : -0.505
  modal_frequency_4 vs max_deformation: -0.750
  modal_frequency_4 vs max_stress : -0.525
==========================================================================================
                     MAXIMUM ACCURACY (INTERPOLATION) 
==========================================================================================
Arch: (4, 5, 6)
  Params: 61
  CV R²: 0.935871 (±0.006815)
  Improvement: 0.13%

Arch: (4, 32, 6)
  Params: 358
  CV R²: 0.960515 (±0.007175)
  Improvement: 2.59%

Arch: (4, 64, 6)
  Params: 710
  CV R²: 0.970675 (±0.005225)
  Improvement: 3.61%

Arch: (4, 128, 6)
  Params: 1414
  CV R²: 0.976777 (±0.004566)
  Improvement: 4.22%

Arch: (4, 64, 32, 6)
  Params: 2598
  CV R²: 0.970305 (±0.003395)
  Improvement: 3.57%

Arch: (4, 128, 64, 6)
  Params: 9286
  CV R²: 0.981162 (±0.001843)
  Improvement: 4.66%

Arch: (4, 256, 128, 6)
  Params: 34950
  CV R²: 0.981397 (±0.005478)
  Improvement: 4.68%







==========================================================================================
                         TRAINING ENSEMBLE OF 20 MODELS
==========================================================================================
Trained model 1/20
Trained model 2/20
Trained model 3/20
Trained model 4/20
Trained model 5/20
Trained model 6/20
Trained model 7/20
Trained model 8/20
Trained model 9/20
Trained model 10/20
Trained model 11/20
Trained model 12/20
Trained model 13/20
Trained model 14/20
Trained model 15/20
Trained model 16/20
Trained model 17/20
Trained model 18/20
Trained model 19/20
Trained model 20/20

=== ENSEMBLE MODEL PERFORMANCE ===
modal_frequency_1                   | R²: 0.9961 | MAPE: 1.60%
modal_frequency_2                   | R²: 0.9995 | MAPE: 0.47%
modal_frequency_3                   | R²: 0.9987 | MAPE: 0.61%
modal_frequency_4                   | R²: 0.9948 | MAPE: 1.29%
max_deformation                     | R²: 0.9849 | MAPE: 3.56%
max_stress                          | R²: 0.9686 | MAPE: 4.00%

[DONE] Ensemble saved to: C:\Users\Administrator\Desktop\code\momobot\WORKSPACE\obsidian\thesis_02\models\ensemble_20_models.pkl
```