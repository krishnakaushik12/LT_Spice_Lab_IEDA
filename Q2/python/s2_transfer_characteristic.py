import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

width_um = 1.0
length_um = 0.065
criterion_current = 100e-9 * width_um / length_um


def load_transfer_curve(file_name):
    data = pd.read_csv(file_name, sep="\t")
    data = data.iloc[:, 0:2]
    data.columns = ["gate_voltage", "drain_current"]
    data["drain_current"] = data["drain_current"].abs()
    data = data.sort_values("gate_voltage")
    return data["gate_voltage"].to_numpy(), data["drain_current"].to_numpy()


def threshold_max_gm(gate_voltage, drain_current):
    gm = np.gradient(drain_current, gate_voltage)
    peak = np.argmax(gm)
    return gate_voltage[peak] - drain_current[peak] / gm[peak]


def threshold_constant_current(gate_voltage, drain_current):
    return np.interp(criterion_current, drain_current, gate_voltage)


def subthreshold_swing(gate_voltage, drain_current, threshold):
    table = pd.DataFrame({"vg": gate_voltage, "id": drain_current})
    table = table[(table["vg"] < threshold) & (table["id"] > 0)]
    log_current = np.log10(table["id"])
    swing = np.gradient(table["vg"], log_current) * 1000
    return np.min(swing)


def current_at(gate_voltage, drain_current, target_voltage):
    return np.interp(target_voltage, gate_voltage, drain_current)


gate_low, current_low = load_transfer_curve("VDS_50m.txt")
gate_high, current_high = load_transfer_curve("VDS_1.1.txt")

vth_linear = threshold_max_gm(gate_low, current_low)
vth_cc_low = threshold_constant_current(gate_low, current_low)
vth_cc_high = threshold_constant_current(gate_high, current_high)
dibl = (vth_cc_low - vth_cc_high) / (1.1 - 0.05) * 1000
ss_low = subthreshold_swing(gate_low, current_low, vth_cc_low)
ss_high = subthreshold_swing(gate_high, current_high, vth_cc_high)
ion = current_at(gate_high, current_high, 1.1) / width_um
ioff = current_at(gate_high, current_high, 0.0) / width_um

results = pd.DataFrame(
    {
        "Quantity": [
            "VTH,lin (V)", "VTH,cc at 50 mV (V)", "VTH,cc at 1.1 V (V)",
            "DIBL (mV/V)", "SS at 50 mV (mV/dec)", "SS at 1.1 V (mV/dec)",
            "ION (mA/um)", "IOFF (nA/um)",
        ],
        "SPICE": [
            vth_linear, vth_cc_low, vth_cc_high, dibl, ss_low, ss_high,
            ion * 1e3, ioff * 1e9,
        ],
        "Table 5.1": [0.38, 0.27, 0.13, 130, 90, 96, 1.15, 67],
    }
)
print(results.round(3).to_string(index=False))

fig, (linear_axis, log_axis) = plt.subplots(1, 2, figsize=(11, 4.5))

linear_axis.plot(gate_low, current_low / width_um * 1e3, label="VDS = 50 mV")
linear_axis.plot(gate_high, current_high / width_um * 1e3, label="VDS = 1.1 V")
log_axis.semilogy(gate_low, current_low / width_um, label="VDS = 50 mV")
log_axis.semilogy(gate_high, current_high / width_um, label="VDS = 1.1 V")

linear_axis.set_xlabel("VGS (V)")
linear_axis.set_ylabel("ID (mA/um)")
linear_axis.set_title("Linear scale")
log_axis.set_xlabel("VGS (V)")
log_axis.set_ylabel("ID (A/um)")
log_axis.set_title("Logarithmic scale")
for axis in (linear_axis, log_axis):
    axis.grid(True, alpha=0.3)
    axis.legend()

plt.tight_layout()
plt.savefig("s2_transfer_characteristic.png", dpi=200)
plt.show()
