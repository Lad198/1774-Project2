from circuit import Circuit
from jacobian import Jacobian
from power_flow import Power_Flow
import numpy as np

# Creating Circuit for 7-bus powerworld system
circuit1 = Circuit("circuit1")

# Creating all buses for the circuit
circuit1.add_bus("Bus1", 20)
circuit1.add_bus("Bus2", 230)
circuit1.add_bus("Bus3", 230)
circuit1.add_bus("Bus4", 230)
circuit1.add_bus("Bus5", 230)
circuit1.add_bus("Bus6", 230)
circuit1.add_bus("Bus7", 18)

# Creating Conductor used in the T-Lines of the circuit
circuit1.add_conductor("Partridge", 0.642, 0.0217, 0.385, 460)

# Creating the geometry of the lines used in the circuit
circuit1.add_geometry("Geometry 1", 0, 0, 19.5, 0, 39, 0)

# Creating the Bundling used by the T-Lines in the circuit
circuit1.add_bundle("Bundle 1", 2, 1.5, circuit1.conductors["Partridge"].name)

# Creating the transformers used in the circuit
circuit1.add_transformer("T1", circuit1.buses["Bus1"].name, circuit1.buses["Bus2"].name, 125, 8.5, 10,'delta-y',(100/230**2),'yes')
circuit1.add_transformer("T2", circuit1.buses["Bus6"].name, circuit1.buses["Bus7"].name, 200, 10.5, 12,'y-delta',0,'no')

# Printing the values for the transformers
print("T1 Impedance pu: ", circuit1.transformers["T1"].zseries, "Admittance: ", circuit1.transformers["T1"].yseries)
print(circuit1.transformers["T1"].y_matrix)
print("T2 Impedance pu: ", circuit1.transformers["T2"].zseries, "Admittance: ", circuit1.transformers["T2"].yseries)
print(circuit1.transformers["T2"].y_matrix)

# Creating the T-Lines used in the circuit
circuit1.add_transmission_line("Line 1", circuit1.buses["Bus2"].name, circuit1.buses["Bus4"].name,
                               circuit1.bundles["Bundle 1"].name, circuit1.geometry["Geometry 1"].name, 10)
circuit1.add_transmission_line("Line 2", circuit1.buses["Bus2"].name, circuit1.buses["Bus3"].name,
                               circuit1.bundles["Bundle 1"].name, circuit1.geometry["Geometry 1"].name, 25)
circuit1.add_transmission_line("Line 3", circuit1.buses["Bus3"].name, circuit1.buses["Bus5"].name,
                               circuit1.bundles["Bundle 1"].name, circuit1.geometry["Geometry 1"].name, 20)
circuit1.add_transmission_line("Line 4", circuit1.buses["Bus4"].name, circuit1.buses["Bus6"].name,
                               circuit1.bundles["Bundle 1"].name, circuit1.geometry["Geometry 1"].name, 20)
circuit1.add_transmission_line("Line 5", circuit1.buses["Bus5"].name, circuit1.buses["Bus6"].name,
                               circuit1.bundles["Bundle 1"].name, circuit1.geometry["Geometry 1"].name, 10)
circuit1.add_transmission_line("Line 6", circuit1.buses["Bus4"].name, circuit1.buses["Bus5"].name,
                               circuit1.bundles["Bundle 1"].name, circuit1.geometry["Geometry 1"].name, 35)

circuit1.add_generator_element("Generator 1", circuit1.buses["Bus1"].name, 100, circuit1.buses["Bus1"].vpu,0.12,0.05,0.14,0,'yes' )
circuit1.add_generator_element("Generator 2", circuit1.buses["Bus7"].name, 200, circuit1.buses["Bus7"].vpu, 0.12,0.05,0.14,(100/18**2),'yes')

circuit1.add_load_element("Load 1", circuit1.buses["Bus3"].name, 110, 50)
circuit1.add_load_element("Load 2", circuit1.buses["Bus4"].name, 100, 70)
circuit1.add_load_element("Load 3", circuit1.buses["Bus5"].name, 100, 65)

print("\nLine 1 Impedance pu: ", circuit1.transmission_lines["Line 1"].impedance_pu, "Series Admittance pu: ", circuit1.transmission_lines["Line 1"].series_admittance,
      "\nShunt Admittance pu: ", circuit1.transmission_lines["Line 1"].shunt_admittance, "\n",circuit1.transmission_lines["Line 1"].y_matrix)
print("\nLine 2 Impedance pu: ", circuit1.transmission_lines["Line 2"].impedance_pu, "Series Admittance pu: ", circuit1.transmission_lines["Line 2"].series_admittance,
      "\nShunt Admittance pu: ", circuit1.transmission_lines["Line 2"].shunt_admittance, "\n",circuit1.transmission_lines["Line 2"].y_matrix)
print("\nLine 3 Impedance pu: ", circuit1.transmission_lines["Line 3"].impedance_pu, "Series Admittance pu: ", circuit1.transmission_lines["Line 3"].series_admittance,
      "\nShunt Admittance pu: ", circuit1.transmission_lines["Line 3"].shunt_admittance, "\n",circuit1.transmission_lines["Line 3"].y_matrix)
print("\nLine 4 Impedance pu: ", circuit1.transmission_lines["Line 4"].impedance_pu, "Series Admittance pu: ", circuit1.transmission_lines["Line 4"].series_admittance,
      "\nShunt Admittance pu: ", circuit1.transmission_lines["Line 4"].shunt_admittance, "\n",circuit1.transmission_lines["Line 4"].y_matrix)
print("\nLine 5 Impedance pu: ", circuit1.transmission_lines["Line 5"].impedance_pu, "Series Admittance pu: ", circuit1.transmission_lines["Line 5"].series_admittance,
      "\nShunt Admittance pu: ", circuit1.transmission_lines["Line 5"].shunt_admittance, "\n",circuit1.transmission_lines["Line 5"].y_matrix)
print("\nLine 6 Impedance pu: ", circuit1.transmission_lines["Line 6"].impedance_pu, "Series Admittance pu: ", circuit1.transmission_lines["Line 6"].series_admittance,
      "\nShunt Admittance pu: ", circuit1.transmission_lines["Line 6"].shunt_admittance, "\n",circuit1.transmission_lines["Line 6"].y_matrix)

circuit1.calc_ybus()
print("Ybus Matrix:\n",circuit1.ybus,"\n")
jacobian = Jacobian(circuit1)
print("Jacobian Matrix:\n",jacobian.compute_jacobian())

# Solve the power flow and print results
powerflow = Power_Flow(circuit1, jacobian)
print("\n--- Solving Power Flow ---")
powerflow.solve(circuit1.buses, circuit1.ybus)

circuit1.modify_y_bus()
circuit1.calc_zero_negative_ybus()
#fault_current,fault_voltage = circuit1.calculate_fault("Bus1")

print("\npositive ybus:\n",circuit1.ybus,"\n")
print("\nnegative ybus:\n", circuit1.negative_ybus,"\n")
print("\nzero ybus:\n", circuit1.zero_ybus,"\n")
#print("\nfault_current:\n",fault_current)
#print("\nfault_voltage:\n",fault_voltage)

print(circuit1.ybus)

# === Stabilize ALL sequence Ybuses ===
epsilon = .28
for idx in range(len(circuit1.zero_ybus)):
    circuit1.zero_ybus.iloc[idx, idx] += epsilon
    circuit1.ybus.iloc[idx, idx] += epsilon   # <<< Add to positive sequence too
    circuit1.negative_ybus.iloc[idx, idx] += epsilon  # <<< Add to negative sequence too

# === Run asymmetrical fault ===
asym_fault_current, sequence_currents = circuit1.calculate_asym_fault("slg", "Bus3", Zf=0.0)
print("\nAsymmetrical Fault Currents (SLG) at Bus3:")
print(f"Ia: {asym_fault_current['Ia']}")
print(f"Ib: {asym_fault_current['Ib']}")
print(f"Ic: {asym_fault_current['Ic']}")

# === Run LINE-TO-LINE (LL) fault at Bus3 ===
print("\n=== LINE-TO-LINE (LL) FAULT at Bus3 ===")
ll_fault_current, _ = circuit1.calculate_asym_fault("ll", "Bus3", Zf=0.0)
print("\nAsymmetrical Fault Currents (LL) at Bus3:")
print(f"Ia: {ll_fault_current['Ia']}")
print(f"Ib: {ll_fault_current['Ib']}")
print(f"Ic: {ll_fault_current['Ic']}")

# === Run DOUBLE LINE-TO-GROUND (DLG) fault at Bus3 ===
print("\n=== DOUBLE LINE-TO-GROUND (DLG) FAULT at Bus3 ===")
dlg_fault_current, _ = circuit1.calculate_asym_fault("dlg", "Bus3", Zf=0.0, dlg_phases="bc")
print("\nAsymmetrical Fault Currents (DLG) at Bus3:")
print(f"Ia: {dlg_fault_current['Ia']}")
print(f"Ib: {dlg_fault_current['Ib']}")
print(f"Ic: {dlg_fault_current['Ic']}")