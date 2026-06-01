# Output from `optimization.py`

**Executed:** 2026-06-02 01:21:21  
**Script Path:** `C:\Users\Administrator\Desktop\code\momobot\WORKSPACE\output\thesis_02\optimization.py`  
**Exit Code:** 0

---

## Terminal Output

Loading surrogate predictor...
Loading ensemble from : C:\Users\Administrator\Desktop\code\momobot\WORKSPACE\output\thesis_02\models
Loaded 20 models in ensemble

Input bounds:
  beam_height  : [5.00, 20.00]
  beam_length  : [10.00, 17.00]
  fillet_size  : [0.10, 0.60]
  beam_width   : [0.40, 0.80]

Objectives:
  f1_max               : max  modal_frequency_1
  deformation_min      : min  max_deformation
  stress_min           : min  max_stress

Running NSGA‑II optimisation...
==========================================================
n_gen  |  n_eval  | n_nds  |      eps      |   indicator  
==========================================================
     1 |      100 |      2 |             - |             -
     2 |      200 |      4 |  0.9687758596 |         ideal
     3 |      300 |      3 |  0.0731123231 |         ideal
     4 |      400 |      4 |  0.4933259325 |         ideal
     5 |      500 |      5 |  0.2592515059 |         ideal
     6 |      600 |      1 |  2.270245E+01 |         ideal
     7 |      700 |      1 |  0.000000E+00 |             f
     8 |      800 |      2 |  2.7249878165 |         ideal
     9 |      900 |      1 |  5.3088645134 |         ideal
    10 |     1000 |      2 |  8.745331E+01 |         ideal
    11 |     1100 |      1 |  3.7892885001 |         ideal
    12 |     1200 |      3 |  1.0162117559 |         ideal
    13 |     1300 |      7 |  0.5822377194 |         ideal
    14 |     1400 |      1 |  1.2925991386 |         ideal
    15 |     1500 |      1 |  4.9944941069 |         ideal
    16 |     1600 |      1 |  1.9323043422 |         ideal
    17 |     1700 |      1 |  0.000000E+00 |             f
    18 |     1800 |      1 |  0.000000E+00 |             f
    19 |     1900 |      1 |  0.000000E+00 |             f
    20 |     2000 |      1 |  0.3917358651 |         ideal
    21 |     2100 |      2 |  2.1080522788 |         ideal
    22 |     2200 |      2 |  4.7864040775 |         ideal
    23 |     2300 |      1 |  0.1025823904 |         ideal
    24 |     2400 |      1 |  0.0446323695 |         ideal
    25 |     2500 |      1 |  0.0775815907 |         ideal
    26 |     2600 |      2 |  1.0000000000 |         ideal
    27 |     2700 |      2 |  1.9318873084 |         ideal
    28 |     2800 |      4 |  0.3625623280 |         ideal
    29 |     2900 |      5 |  0.7325207726 |         ideal
    30 |     3000 |      1 |  0.1583700751 |         ideal
    31 |     3100 |      1 |  0.0086766406 |         ideal
    32 |     3200 |      2 |  1.0000000000 |         ideal
    33 |     3300 |      1 |  0.0741732417 |         ideal
    34 |     3400 |      1 |  0.000000E+00 |             f
    35 |     3500 |      1 |  0.0245436590 |         ideal
    36 |     3600 |      1 |  0.0076697534 |         ideal
    37 |     3700 |      1 |  0.000000E+00 |             f
    38 |     3800 |      1 |  0.0041162467 |         ideal
    39 |     3900 |      2 |  1.0000000000 |         ideal
    40 |     4000 |      3 |  0.9002119397 |         ideal
    41 |     4100 |      1 |  0.0061116606 |         ideal
    42 |     4200 |      1 |  0.0009947795 |             f
    43 |     4300 |      2 |  7.530268E+02 |         ideal
    44 |     4400 |      2 |  6.8993242625 |         ideal
    45 |     4500 |      1 |  0.0053190424 |         ideal
    46 |     4600 |      1 |  0.0002692087 |             f
    47 |     4700 |      2 |  4.8976938623 |         ideal
    48 |     4800 |      1 |  0.0003405325 |             f
    49 |     4900 |      2 |  1.185674E+01 |         ideal
    50 |     5000 |      2 |  0.0030728077 |         ideal

NSGA‑II finished. Pareto front size: 2
Pareto front saved to: C:\Users\Administrator\Desktop\code\momobot\WORKSPACE\output\thesis_02\plots\pareto_front.csv
Pareto front plot saved to: C:\Users\Administrator\Desktop\code\momobot\WORKSPACE\output\thesis_02\plots\pareto_front_plot.png

Pareto front summary:
       beam_height  beam_length  ...  deformation_min    stress_min
count     2.000000     2.000000  ...     2.000000e+00  2.000000e+00
mean     19.999953    10.000002  ...     9.264828e-03  7.891430e-01
std       0.000028     0.000002  ...     3.823410e-08  9.240565e-07
min      19.999933    10.000000  ...     9.264801e-03  7.891424e-01
25%      19.999943    10.000001  ...     9.264815e-03  7.891427e-01
50%      19.999953    10.000002  ...     9.264828e-03  7.891430e-01
75%      19.999963    10.000003  ...     9.264842e-03  7.891434e-01
max      19.999973    10.000004  ...     9.264855e-03  7.891437e-01

[8 rows x 7 columns]

Top 3 solutions by each objective:

f1_max (max):
 beam_height  beam_length  fillet_size  beam_width     f1_max  deformation_min  stress_min
   19.999973    10.000000     0.599998         0.8 462.184012         0.009265    0.789144
   19.999933    10.000004     0.600000         0.8 462.183901         0.009265    0.789142

deformation_min (min):
 beam_height  beam_length  fillet_size  beam_width     f1_max  deformation_min  stress_min
   19.999973    10.000000     0.599998         0.8 462.184012         0.009265    0.789144
   19.999933    10.000004     0.600000         0.8 462.183901         0.009265    0.789142

stress_min (min):
 beam_height  beam_length  fillet_size  beam_width     f1_max  deformation_min  stress_min
   19.999933    10.000004     0.600000         0.8 462.183901         0.009265    0.789142
   19.999973    10.000000     0.599998         0.8 462.184012         0.009265    0.789144

---

## Execution Details

- **Python Interpreter:** `C:\Users\Administrator\Desktop\code\.venv\Scripts\python.exe`
- **Working Directory:** `C:\Users\Administrator\Desktop\code\momobot\WORKSPACE\output\thesis_02`
- **Output File:** `C:\Users\Administrator\Desktop\code\momobot\WORKSPACE\output\thesis_02\optimization_outputs.md`


## ✓ Execution Status

**Script completed successfully** (exit code 0)

