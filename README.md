# LTspice Lab – EC2L104

Krishna Kaushik D (25EC01016)

This is my repo for the LTspice exercise of EC2L104 (Introduction to EDA Tools, Dr. Akshay K). It has the LTspice files, the exported data and the Python scripts for all the questions on the exercise sheet, and my report is in here too.

## How the repo is organised

There is one folder per question, so `Q1` is S1, `Q2` is S2, and so on up to `Q7`.

| Folder | Question |
| --- | --- |
| `Q1` | S1, reading the model card and the `.op` results |
| `Q2` | S2, ID–VG at VDS = 50 mV and 1.1 V |
| `Q3` | S3, ID–VD curves, gds and ro |
| `Q4` | S4, the UA = UB = 0 and VSAT × 100 runs |
| `Q5` | S5, the 14 parameter sweeps |
| `Q6` | S6, fitting `nfit` to the TCAD curves |
| `Q7` | S7, the CMOS inverter |

Inside each folder:
- the LTspice schematic (`.asc`) or netlist (`.cir`) and its log file
- a copy of the model card it uses (`65nm_bulk.pm`, or `nfit.pm` in Q6)
- a `python` folder with the data I exported from LTspice, the script that plots it, and the figures it makes

Outside the folders:
- `65nm_bulk.pm` is the original PTM 65 nm card
- `LTspice_Exercises.pdf` is the exercise sheet
- `REPORT.pdf` is the Lab Report

- Every folder has its own copy of the model card because LTspice looks for the `.include` file next to the schematic. The copies in Q1 to Q4 are the same as the one in the main folder. Q5 has a version where the parameters are written as `{vth0}`, `{toxe}` and so on so that they can be stepped, Q6 has the fitted `nfit.pm`, and in Q7 the pmos model is renamed `pmos0`.
- The nmos model is called `nmos0` and not `nmos`, because LTspice already has a built-in `nmos` that would be used instead of the PTM card.
- Q4 has two extra model files, `uaubzero.pm` and `vsat100.pm`, which are the card with only UA/UB or only VSAT changed.

## Running the Python scripts

The scripts read their data files by name, so run each one from inside its own `python` folder. For example:

```
cd Q2/python
python s2_transfer_characteristic.py
```

The scripts use numpy, pandas and matplotlib. If you want to make new data, run the netlist in LTspice, plot `Id(M1)` and use File → Export data as text to save it in that `python` folder.
