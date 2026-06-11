import pandas as pd
import matplotlib.pyplot as plt
import os
from scipy.signal import find_peaks

folder = os.path.dirname(__file__)

sim = pd.read_csv(os.path.join(folder, "simulation.csv"))
test = pd.read_csv(os.path.join(folder, "test.csv"))


freq_sim = sim["Frequency"]
amp_sim = sim["Amplitude"]

freq_test = test["Frequency"]
amp_test = test["Amplitude"]



sim_prominence = 0.05 * amp_sim.max()
test_prominence = 0.05 * amp_test.max()

sim_peaks, _ = find_peaks(
    amp_sim,
    prominence=sim_prominence
)

test_peaks, _ = find_peaks(
    amp_test,
    prominence=test_prominence
)


plt.figure(figsize=(12,7))

plt.plot(
    freq_sim,
    amp_sim,
    linewidth=2,
    label="Simulation"
)

plt.plot(
    freq_test,
    amp_test,
    linewidth=2,
    label="Testing"
)


plt.scatter(
    freq_sim.iloc[sim_peaks],
    amp_sim.iloc[sim_peaks]
)

for peak in sim_peaks:

    plt.annotate(
        f'{freq_sim.iloc[peak]:.1f} Hz',
        (
            freq_sim.iloc[peak],
            amp_sim.iloc[peak]
        )
    )



plt.scatter(
    freq_test.iloc[test_peaks],
    amp_test.iloc[test_peaks]
)

for peak in test_peaks:

    plt.annotate(
        f'{freq_test.iloc[peak]:.1f} Hz',
        (
            freq_test.iloc[peak],
            amp_test.iloc[peak]
        )
    )



plt.xlabel("Frequency (Hz)")
plt.ylabel("Amplitude")
plt.title("FRF Correlation : Simulation vs Testing")
plt.grid(True)
plt.legend()


results_folder = os.path.join(
    os.path.dirname(folder),
    "results"
)

os.makedirs(results_folder, exist_ok=True)

plt.savefig(
    os.path.join(
        results_folder,
        "frf_correlation.png"
    ),
    dpi=300
)

plt.show()

report_path = os.path.join(
    results_folder,
    "correlation_report.txt"
)

with open(report_path, "w") as report:

    report.write("FRF CORRELATION REPORT\n")
    report.write("="*50 + "\n\n")

    report.write("SIMULATION RESONANCE PEAKS\n")
    report.write("-"*50 + "\n")

    for peak in sim_peaks:

        report.write(
            f"Frequency = {freq_sim.iloc[peak]:.2f} Hz"
            f" | Amplitude = {amp_sim.iloc[peak]:.4f}\n"
        )

    report.write("\n")

    report.write("TEST RESONANCE PEAKS\n")
    report.write("-"*50 + "\n")

    for peak in test_peaks:

        report.write(
            f"Frequency = {freq_test.iloc[peak]:.2f} Hz"
            f" | Amplitude = {amp_test.iloc[peak]:.4f}\n"
        )

    report.write("\n")

    report.write("CORRELATION TABLE\n")
    report.write("-"*50 + "\n")

    report.write(
        "Mode\tSimulation(Hz)\tTesting(Hz)\tError(Hz)\n"
    )

    num_modes = min(
        len(sim_peaks),
        len(test_peaks)
    )

    for i in range(num_modes):

        sim_freq = freq_sim.iloc[sim_peaks[i]]
        test_freq = freq_test.iloc[test_peaks[i]]

        error = abs(sim_freq - test_freq)

        report.write(
            f"{i+1}\t"
            f"{sim_freq:.2f}\t\t"
            f"{test_freq:.2f}\t\t"
            f"{error:.2f}\n"
        )

print(f"\nReport Saved : {report_path}")

print("\nGraph Saved Successfully")
print("results/frf_correlation.png")