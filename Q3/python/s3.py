import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

gate_voltages = [0.3, 0.6, 0.9, 1.5]
file_names = ["VGS_0.3.txt", "VGS_0.6.txt", "VGS_0.9.txt", "VGS_1.5.txt"]
device_width_um = 1.0
check_voltages = [1.1, 1.5]

drain_voltage_list = []
drain_current_list = []
conductance_list = []

for file_name in file_names:
    table = pd.read_csv(file_name, sep="\t")
    table.columns = ["drain_voltage", "drain_current"]
    table["drain_current"] = table["drain_current"].abs()
    table = table.sort_values("drain_voltage")

    drain_voltage = table["drain_voltage"].to_numpy()
    drain_current = table["drain_current"].to_numpy()

    drain_voltage_list.append(drain_voltage)
    drain_current_list.append(drain_current)
    conductance_list.append(np.gradient(drain_current, drain_voltage))

figure_both, (axis_current, axis_conductance) = plt.subplots(1, 2, figsize=(13, 5))

for i in range(len(gate_voltages)):
    curve_label = f"$V_{{GS}}$ = {gate_voltages[i]} V"
    axis_current.plot(
        drain_voltage_list[i],
        drain_current_list[i] * 1e6 / device_width_um,
        linewidth=1.8,
        label=curve_label,
    )
    axis_conductance.plot(
        drain_voltage_list[i],
        conductance_list[i] * 1e6 / device_width_um,
        linewidth=1.8,
        linestyle="--",
        label=curve_label,
    )

axis_current.set_xlabel("Drain-to-source voltage $V_{DS}$ (V)")
axis_current.set_ylabel("Drain current $I_D$ (µA/µm)")
axis_current.set_title("(a) Output characteristics ($I_D$ vs $V_{DS}$)")
axis_current.grid(True, alpha=0.3)
axis_current.legend()

axis_conductance.set_xlabel("Drain-to-source voltage $V_{DS}$ (V)")
axis_conductance.set_ylabel("Output conductance $g_{ds}$ (µS/µm)")
axis_conductance.set_title("(b) Output conductance ($g_{ds}$ = dI$_D$/dV$_{DS}$)")
axis_conductance.grid(True, alpha=0.3)
axis_conductance.legend()

figure_both.tight_layout()
figure_both.savefig("S3_output_characteristics_and_gds.png", dpi=300)

summary_rows = []
for i in range(len(gate_voltages)):
    for check_voltage in check_voltages:
        if check_voltage > drain_voltage_list[i].max():
            continue
        current_here = np.interp(check_voltage, drain_voltage_list[i], drain_current_list[i])
        conductance_here = np.interp(check_voltage, drain_voltage_list[i], conductance_list[i])
        if conductance_here > 0:
            output_resistance_kohm_um = (1.0 / conductance_here) * device_width_um / 1e3
        else:
            output_resistance_kohm_um = float("inf")
        summary_rows.append(
            {
                "VGS (V)": gate_voltages[i],
                "VDS (V)": check_voltage,
                "ID (µA/µm)": current_here * 1e6 / device_width_um,
                "gds (µS/µm)": conductance_here * 1e6 / device_width_um,
                "ro (kΩ·µm)": output_resistance_kohm_um,
            }
        )

summary_table = pd.DataFrame(summary_rows)
summary_table.to_csv("S3_summary.csv", index=False)
print(summary_table.round(3).to_string(index=False))

plt.show()
