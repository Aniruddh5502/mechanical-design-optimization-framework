# Output from `optimization.py`

**Executed:** 2026-06-03 01:51:52  
**Script Path:** `C:\Users\Administrator\Desktop\code\momobot\WORKSPACE\output\thesis_02\optimization.py`  
**Exit Code:** 0

---

## Terminal Output

Loading surrogate predictor...
Loading ensemble from : C:\Users\Administrator\Desktop\code\momobot\WORKSPACE\output\thesis_02\models
Loaded 20 models in ensemble

Input bounds:
  beam_height  : [7.00, 18.00]
  beam_length  : [10.50, 16.00]
  fillet_size  : [0.20, 0.40]
  beam_width   : [0.50, 0.60]

Objectives:
  f1_min               : min  modal_frequency_1
  f2_max               : max  modal_frequency_2

Running NSGA‑II optimisation...
==========================================================
n_gen  |  n_eval  | n_nds  |      eps      |   indicator  
==========================================================
     1 |      100 |     25 |             - |             -
     2 |      200 |     37 |  0.0555855521 |         ideal
     3 |      300 |     51 |  0.0107717750 |             f
     4 |      400 |     61 |  0.0061100891 |         nadir
     5 |      500 |     65 |  0.0048435156 |             f
     6 |      600 |     87 |  0.0077282424 |         ideal
     7 |      700 |     90 |  0.0031884778 |             f
     8 |      800 |    100 |  0.0027459059 |         ideal
     9 |      900 |    100 |  0.0074607166 |         nadir
    10 |     1000 |    100 |  0.0051084892 |         nadir
    11 |     1100 |    100 |  0.0068519396 |         ideal
    12 |     1200 |    100 |  0.0018966380 |             f
    13 |     1300 |    100 |  0.0040780694 |             f
    14 |     1400 |    100 |  0.0008847569 |             f
    15 |     1500 |    100 |  0.0154924299 |         ideal
    16 |     1600 |    100 |  0.0013331674 |             f
    17 |     1700 |    100 |  0.0023692398 |             f
    18 |     1800 |    100 |  0.0034756508 |             f
    19 |     1900 |    100 |  0.0235014209 |         nadir
    20 |     2000 |    100 |  0.0008626655 |             f
    21 |     2100 |    100 |  0.0021034236 |             f
    22 |     2200 |    100 |  0.0105507892 |         nadir
    23 |     2300 |    100 |  0.0040867852 |         nadir
    24 |     2400 |    100 |  0.0010216940 |             f
    25 |     2500 |    100 |  0.0022645942 |             f
    26 |     2600 |    100 |  0.0038396575 |             f
    27 |     2700 |    100 |  0.0011357271 |             f
    28 |     2800 |    100 |  0.0075521068 |         ideal
    29 |     2900 |    100 |  0.0078009662 |         nadir
    30 |     3000 |    100 |  0.0010950471 |             f
    31 |     3100 |    100 |  0.0039794458 |         nadir
    32 |     3200 |    100 |  0.0010933551 |             f
    33 |     3300 |    100 |  0.0021704942 |             f
    34 |     3400 |    100 |  0.0035330315 |             f
    35 |     3500 |    100 |  0.0008874721 |             f
    36 |     3600 |    100 |  0.0021509613 |             f
    37 |     3700 |    100 |  0.0031228067 |             f
    38 |     3800 |    100 |  0.0012549984 |             f
    39 |     3900 |    100 |  0.0018765261 |             f
    40 |     4000 |    100 |  0.0028105928 |             f
    41 |     4100 |    100 |  0.0010579034 |             f
    42 |     4200 |    100 |  0.0019847766 |             f
    43 |     4300 |    100 |  0.0030101435 |             f
    44 |     4400 |    100 |  0.0007279414 |             f
    45 |     4500 |    100 |  0.0015241179 |             f
    46 |     4600 |    100 |  0.0020207838 |             f
    47 |     4700 |    100 |  0.0023581138 |             f
    48 |     4800 |    100 |  0.0029636996 |             f
    49 |     4900 |    100 |  0.0007072609 |             f
    50 |     5000 |    100 |  0.0026990672 |         nadir

NSGA‑II finished. Pareto front size: 100
Pareto front saved to: C:\Users\Administrator\Desktop\code\momobot\WORKSPACE\output\thesis_02\plots\pareto\pareto_front.csv
Pareto front plot saved to: C:\Users\Administrator\Desktop\code\momobot\WORKSPACE\output\thesis_02\plots\pareto\pareto_front_plot.png and C:\Users\Administrator\Desktop\code\momobot\WORKSPACE\output\thesis_02\plots\pareto\pareto_front_plot.svg

Pareto front summary:
       beam_height  beam_length  ...      f1_min       f2_max
count   100.000000   100.000000  ...  100.000000   100.000000
mean     14.788033    12.937928  ...  158.273704  1166.847773
std       3.598748     2.016118  ...   44.411068   203.892165
min       7.208440    10.500183  ...   99.971978   746.919824
25%      13.224299    10.551320  ...  117.163537  1021.181184
50%      16.377089    13.102790  ...  158.241326  1179.613543
75%      17.822797    15.023652  ...  193.685994  1359.759697
max      17.999649    15.988833  ...  244.294764  1442.655807

[8 rows x 6 columns]

Top 3 solutions by each objective:

f1_min (min):
 beam_height  beam_length  fillet_size  beam_width     f1_min     f2_max
    7.208440    15.975841     0.245565    0.500457  99.971978 746.919824
    7.483398    15.975841     0.245966    0.500401 100.463422 763.397162
    7.634427    15.910890     0.230959    0.500600 100.931949 777.040168

f2_max (max):
 beam_height  beam_length  fillet_size  beam_width     f1_min      f2_max
   17.506530    10.500600     0.381809    0.598987 244.294764 1442.655807
   17.608562    10.500600     0.365438    0.598987 243.871650 1441.583028
   17.613609    10.538283     0.364974    0.596024 241.737052 1436.374061

---

## Execution Details

- **Python Interpreter:** `C:\Users\Administrator\Desktop\code\.venv\Scripts\python.exe`
- **Working Directory:** `C:\Users\Administrator\Desktop\code\momobot\WORKSPACE\output\thesis_02`
- **Output File:** `C:\Users\Administrator\Desktop\code\momobot\WORKSPACE\output\thesis_02\optimization_outputs.md`


## ✓ Execution Status

**Script completed successfully** (exit code 0)

