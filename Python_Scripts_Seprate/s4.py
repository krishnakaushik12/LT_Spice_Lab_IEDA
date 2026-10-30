import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

device_width_um = 1.0
criterion_current_a = 100e-9 * device_width_um / 0.065

model_labels = ["Nominal (nmos0)", "UA = UB = 0 (nmos1)", "VSAT x 100 (nmos2)"]
files_50mv = ["VDS_50m.txt", "uaub0_VDS_50m.txt", "vsat100_VDS_50m.txt"]
files_1v1 = ["VDS_1.1.txt", "uaub0_VDS_1.1.txt", "vsat100_VDS_1.1.txt"]
drain_voltages = [0.05, 1.1]


def load_transfer_curve(file_name):
    table = pd.read_csv(file_name, sep="\t")
    table = table.iloc[:, 0:2]
    table.columns = ["gate_voltage", "drain_current"]
    table["drain_current"] = table["drain_current"].abs()
    table = table.sort_values("gate_voltage")
    return table["gate_voltage"].to_numpy(), table["drain_current"].to_numpy()


def plot_row(linear_axis, log_axis, curves, title_text):
    for i in range(len(model_labels)):
        gate_voltage, drain_current = curves[i]
        current_density = drain_current / device_width_um
        linear_axis.plot(gate_voltage, current_density * 1e3, linewidth=1.8, label=model_labels[i])
        log_axis.semilogy(gate_voltage, current_density, linewidth=1.8, label=model_labels[i])

    linear_axis.set_title(f"Linear scale, {title_text}")
    linear_axis.set_xlabel("Gate-to-source voltage $V_{GS}$ (V)")
    linear_axis.set_ylabel("Drain current $I_D$ (mA/µm)")
    log_axis.set_title(f"Logarithmic scale, {title_text}")
    log_axis.set_xlabel("Gate-to-source voltage $V_{GS}$ (V)")
    log_axis.set_ylabel("Drain current $I_D$ (A/µm)")
    for axis in (linear_axis, log_axis):
        axis.grid(True, alpha=0.3)
        axis.legend()


curves_50mv = []
for file_name in files_50mv:
    curves_50mv.append(load_transfer_curve(file_name))

curves_1v1 = []
for file_name in files_1v1:
    curves_1v1.append(load_transfer_curve(file_name))

figure, axes = plt.subplots(2, 2, figsize=(12, 9))
plot_row(axes[0][0], axes[0][1], curves_50mv, "$V_{DS}$ = 50 mV")
plot_row(axes[1][0], axes[1][1], curves_1v1, "$V_{DS}$ = 1.1 V")

figure.tight_layout()
figure.savefig("S4_physics_check.png", dpi=300)

all_curves = [curves_50mv, curves_1v1]
summary_rows = []
for i in range(len(model_labels)):
    for k in range(len(drain_voltages)):
        gate_voltage, drain_current = all_curves[k][i]
        threshold_voltage = np.interp(criterion_current_a, drain_current, gate_voltage)
        summary_rows.append(
            {
                "Model": model_labels[i],
                "VDS (V)": drain_voltages[k],
                "VTH,cc (V)": threshold_voltage,
                "ION at VGS = 1.1 V (mA/µm)": np.interp(1.1, gate_voltage, drain_current) * 1e3 / device_width_um,
                "IOFF at VGS = 0 (nA/µm)": np.interp(0.0, gate_voltage, drain_current) * 1e9 / device_width_um,
            }
        )

summary_table = pd.DataFrame(summary_rows)
summary_table.to_csv("S4_summary.csv", index=False)
print(summary_table.round(3).to_string(index=False))

plt.show()
