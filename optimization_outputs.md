# Output from `optimization.py`

**Executed:** 2026-06-02 04:09:18  
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
  f1_min               : min  modal_frequency_1
  f2_max               : max  modal_frequency_2

Running NSGA‑II optimisation...
==========================================================
n_gen  |  n_eval  | n_nds  |      eps      |   indicator  
==========================================================
     1 |      100 |     22 |             - |             -
     2 |      200 |     32 |  0.0097916317 |             f
     3 |      300 |     36 |  0.0304332145 |         ideal
     4 |      400 |     42 |  0.0059365494 |         ideal
     5 |      500 |     44 |  0.0038839582 |         ideal
     6 |      600 |     53 |  0.0060782553 |             f
     7 |      700 |     66 |  0.0040494648 |             f
     8 |      800 |     80 |  0.0095243602 |         ideal
     9 |      900 |    100 |  0.0180234445 |         nadir
    10 |     1000 |    100 |  0.0166856277 |         ideal
    11 |     1100 |    100 |  0.0014442931 |             f
    12 |     1200 |    100 |  0.0039615572 |         ideal
    13 |     1300 |    100 |  0.0017132649 |             f
    14 |     1400 |    100 |  0.0079283615 |         ideal
    15 |     1500 |    100 |  0.0019065200 |             f
    16 |     1600 |    100 |  0.0029049604 |         ideal
    17 |     1700 |    100 |  0.0013290125 |             f
    18 |     1800 |    100 |  0.0045716663 |         ideal
    19 |     1900 |    100 |  0.0009414762 |             f
    20 |     2000 |    100 |  0.0037956075 |         ideal
    21 |     2100 |    100 |  0.0008925641 |             f
    22 |     2200 |    100 |  0.0040900788 |         nadir
    23 |     2300 |    100 |  0.0010268148 |             f
    24 |     2400 |    100 |  0.0019096349 |             f
    25 |     2500 |    100 |  0.0027057192 |             f
    26 |     2600 |    100 |  0.0010544724 |             f
    27 |     2700 |    100 |  0.0017049208 |             f
    28 |     2800 |    100 |  0.0121119767 |         ideal
    29 |     2900 |    100 |  0.0009754797 |             f
    30 |     3000 |    100 |  0.0019153955 |             f
    31 |     3100 |    100 |  0.0027467051 |             f
    32 |     3200 |    100 |  0.0032366208 |         nadir
    33 |     3300 |    100 |  0.0007279752 |             f
    34 |     3400 |    100 |  0.0013663377 |             f
    35 |     3500 |    100 |  0.0018834422 |             f
    36 |     3600 |    100 |  0.0027383398 |             f
    37 |     3700 |    100 |  0.0111619111 |         nadir
    38 |     3800 |    100 |  0.0008236046 |             f
    39 |     3900 |    100 |  0.0013028536 |             f
    40 |     4000 |    100 |  0.0018580531 |             f
    41 |     4100 |    100 |  0.0022461571 |             f
    42 |     4200 |    100 |  0.0029394153 |             f
    43 |     4300 |    100 |  0.0009016991 |             f
    44 |     4400 |    100 |  0.0014203338 |             f
    45 |     4500 |    100 |  0.0020940716 |             f
    46 |     4600 |    100 |  0.0026921268 |             f
    47 |     4700 |    100 |  0.0007223322 |             f
    48 |     4800 |    100 |  0.0015073308 |             f
    49 |     4900 |    100 |  0.0023240120 |             f
    50 |     5000 |    100 |  0.0027377303 |             f

NSGA‑II finished. Pareto front size: 100
Pareto front saved to: C:\Users\Administrator\Desktop\code\momobot\WORKSPACE\output\thesis_02\plots\pareto\pareto_front.csv
Pareto front plot saved to: C:\Users\Administrator\Desktop\code\momobot\WORKSPACE\output\thesis_02\plots\pareto\pareto_front_plot.png and C:\Users\Administrator\Desktop\code\momobot\WORKSPACE\output\thesis_02\plots\pareto\pareto_front_plot.svg

Pareto front summary:
       beam_height  beam_length  ...      f1_min       f2_max
count   100.000000   100.000000  ...  100.000000   100.000000
mean     14.405306    12.481517  ...  173.240162  1184.929511
std       4.195328     2.861426  ...   95.953263   354.686993
min       5.019530    10.001018  ...   64.989694   472.250767
25%      14.592785    10.005183  ...   79.503744   922.526237
50%      16.360912    10.034969  ...  150.766993  1300.196473
75%      16.720577    15.807286  ...  249.405897  1494.258031
max      19.924423    16.999688  ...  365.478271  1625.467191

[8 rows x 6 columns]

Top 3 solutions by each objective:

f1_min (min):
 beam_height  beam_length  fillet_size  beam_width    f1_min     f2_max
    5.019530    16.999688     0.236045    0.400055 64.989694 472.250767
    5.115799    16.994119     0.236045    0.400036 65.331243 479.937501
    5.206087    16.665770     0.181527    0.400214 65.870276 501.376379

f2_max (max):
 beam_height  beam_length  fillet_size  beam_width     f1_min      f2_max
   16.710442    10.003402     0.457196    0.799969 365.478271 1625.467191
   16.361146    10.001018     0.468982    0.789275 359.047972 1618.514094
   16.361146    10.001018     0.489435    0.784916 355.684383 1613.970470

---

## Execution Details

- **Python Interpreter:** `C:\Users\Administrator\Desktop\code\.venv\Scripts\python.exe`
- **Working Directory:** `C:\Users\Administrator\Desktop\code\momobot\WORKSPACE\output\thesis_02`
- **Output File:** `C:\Users\Administrator\Desktop\code\momobot\WORKSPACE\output\thesis_02\optimization_outputs.md`


## ✓ Execution Status

**Script completed successfully** (exit code 0)

