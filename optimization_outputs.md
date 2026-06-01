# Output from `optimization.py`

**Executed:** 2026-06-02 02:53:08  
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
  deformation          : max  max_deformation

Running NSGA‑II optimisation...
==========================================================
n_gen  |  n_eval  | n_nds  |      eps      |   indicator  
==========================================================
     1 |      100 |     24 |             - |             -
     2 |      200 |     33 |  0.0136161715 |         ideal
     3 |      300 |     51 |  0.0589593291 |         ideal
     4 |      400 |     69 |  0.0037854199 |         nadir
     5 |      500 |     84 |  0.0048541563 |             f
     6 |      600 |     99 |  0.0233150601 |         ideal
     7 |      700 |    100 |  0.0127872354 |         ideal
     8 |      800 |    100 |  0.0044549206 |         ideal
     9 |      900 |    100 |  0.0237123577 |         ideal
    10 |     1000 |    100 |  0.0230591370 |         ideal
    11 |     1100 |    100 |  0.0026996221 |             f
    12 |     1200 |    100 |  0.0029769202 |         nadir
    13 |     1300 |    100 |  0.0032048419 |             f
    14 |     1400 |    100 |  0.0081609557 |         ideal
    15 |     1500 |    100 |  0.0050623237 |         ideal
    16 |     1600 |    100 |  0.0127117009 |         ideal
    17 |     1700 |    100 |  0.0019442776 |             f
    18 |     1800 |    100 |  0.0035529804 |             f
    19 |     1900 |    100 |  0.0084259104 |         ideal
    20 |     2000 |    100 |  0.0106698783 |         ideal
    21 |     2100 |    100 |  0.0188556165 |         ideal
    22 |     2200 |    100 |  0.0063600660 |         ideal
    23 |     2300 |    100 |  0.0050417035 |         ideal
    24 |     2400 |    100 |  0.0026587130 |             f
    25 |     2500 |    100 |  0.0017962479 |             f
    26 |     2600 |    100 |  0.0034447047 |         ideal
    27 |     2700 |    100 |  0.0016252202 |             f
    28 |     2800 |    100 |  0.0041778889 |         ideal
    29 |     2900 |    100 |  0.0022379957 |             f
    30 |     3000 |    100 |  0.0035917499 |             f
    31 |     3100 |    100 |  0.0018598705 |             f
    32 |     3200 |    100 |  0.0028510184 |             f
    33 |     3300 |    100 |  0.0047835469 |         ideal
    34 |     3400 |    100 |  0.0016143226 |             f
    35 |     3500 |    100 |  0.0028278165 |             f
    36 |     3600 |    100 |  0.0087698213 |         nadir
    37 |     3700 |    100 |  0.0026082477 |         ideal
    38 |     3800 |    100 |  0.0021556107 |             f
    39 |     3900 |    100 |  0.0040125841 |             f
    40 |     4000 |    100 |  0.0022236288 |             f
    41 |     4100 |    100 |  0.0035890316 |             f
    42 |     4200 |    100 |  0.0052828791 |         nadir
    43 |     4300 |    100 |  0.0023300930 |             f
    44 |     4400 |    100 |  0.0035582591 |             f
    45 |     4500 |    100 |  0.0030397980 |         ideal
    46 |     4600 |    100 |  0.0012912876 |             f
    47 |     4700 |    100 |  0.0028008121 |             f
    48 |     4800 |    100 |  0.0017680394 |             f
    49 |     4900 |    100 |  0.0030527561 |             f
    50 |     5000 |    100 |  0.0031187599 |         nadir

NSGA‑II finished. Pareto front size: 100
Pareto front saved to: C:\Users\Administrator\Desktop\code\momobot\WORKSPACE\output\thesis_02\plots\pareto\pareto_front.csv
Pareto front plot saved to: C:\Users\Administrator\Desktop\code\momobot\WORKSPACE\output\thesis_02\plots\pareto\pareto_front_plot.png and C:\Users\Administrator\Desktop\code\momobot\WORKSPACE\output\thesis_02\plots\pareto\pareto_front_plot.svg

Pareto front summary:
       beam_height  beam_length  ...       f2_max  deformation
count   100.000000   100.000000  ...   100.000000   100.000000
mean     14.166966    13.006131  ...  1125.376712     0.225448
std       4.274616     2.801636  ...   341.163318     0.185290
min       5.034550    10.000296  ...   472.116205     0.018199
25%      13.969461    10.014385  ...   911.333117     0.055185
50%      15.913489    13.073030  ...  1125.607595     0.155409
75%      16.773745    15.851372  ...  1443.061383     0.387041
max      19.657850    16.997678  ...  1625.241161     0.580755

[8 rows x 7 columns]

Top 3 solutions by each objective:

f1_min (min):
 beam_height  beam_length  fillet_size  beam_width    f1_min     f2_max  deformation
    5.040326    16.920633     0.212631    0.400366 65.291980 476.984260     0.566553
    5.034550    16.954269     0.136633    0.400181 65.661716 472.116205     0.577666
    5.092195    16.662299     0.136601    0.400864 66.252395 492.456183     0.563495

f2_max (max):
 beam_height  beam_length  fillet_size  beam_width     f1_min      f2_max  deformation
   16.717139    10.002004     0.460366    0.799375 365.066691 1625.241161     0.018199
   16.715761    10.002237     0.460366    0.797698 364.126667 1624.214840     0.018387
   16.595062    10.022695     0.507135    0.762382 342.760097 1597.337821     0.023604

deformation (max):
 beam_height  beam_length  fillet_size  beam_width    f1_min     f2_max  deformation
    5.034550    16.954269     0.100139    0.400181 66.271131 473.511910     0.580755
    5.034550    16.954269     0.136633    0.400181 65.661716 472.116205     0.577666
    5.518497    16.997678     0.123687    0.400428 67.568756 508.060448     0.568832

---

## Execution Details

- **Python Interpreter:** `C:\Users\Administrator\Desktop\code\.venv\Scripts\python.exe`
- **Working Directory:** `C:\Users\Administrator\Desktop\code\momobot\WORKSPACE\output\thesis_02`
- **Output File:** `C:\Users\Administrator\Desktop\code\momobot\WORKSPACE\output\thesis_02\optimization_outputs.md`


## ✓ Execution Status

**Script completed successfully** (exit code 0)

