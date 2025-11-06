"""
### FILE EXPECTATIONS
- This script expects CSV files in the format: `xxxxpaviewX.csv` (e.g., `2025-09-16-10cm-0,15t-n-0,1paview2.csv`).
- All files must be placed in the directory defined by `DATA_DIR`.
- Each unique measurement pattern (e.g., `2025-09-16-10cm-0,15t-n-0,1`) can have multiple `paviewX.csv` files.
- The script groups files by their pattern prefix and processes them together.

### HOW TO ADD NEW MATERIALS OR PROCESSES
1. **Add a New Process:**
   - Edit the `get_process_materials()` function.
   - Add a new entry to the `process_materials` dictionary with:
     - A unique key (e.g., `"4"`).
     - A descriptive `"name"`.
     - A list of `"elements"` involved.
     - A `"cohesive_energies"` dictionary for each element (use `0` for background gases).
     - A `"pattern_structure"` list of tuples: `(element, charge, file_index)`.
   - Example:
     ```python
     "4": {
         "name": "CrN (Cr cathode, N₂ gas)",
         "elements": ["Cr", "N", "N₂"],
         "cohesive_energies": {"Cr": 4.10, "N": 0, "N₂": 0},
         "pattern_structure": [
             ("Cr", 1, 0),  # File 1 is Cr 1+
             ("Cr", 2, 1),  # File 2 is Cr 2+
             ("N", 1, 2),   # File 3 is N 1+
             ("N₂", 1, 3),  # File 4 is N₂ 1+
         ]
     }
     ```
2. **Add a New Element:**
   - Add the element to the `ionization_energies` dictionary with its ionization energy levels (in eV).
   - Add the element to the `mass_to_charge` dictionary with its mass-to-charge ratios for charge states 1+ to 6+.
   - Example for adding Chromium (Cr):
     ```python
     ionization_energies = {
         ...
         "Cr": [6.7665, 16.48, 30.96, 49.1, 69.3, 90.6],
     }
     mass_to_charge = {
         ...
         "Cr": [51.9961 / i for i in range(1, 7)],
     }
     ```

3. **Cohesive Energy Guidelines:**
   - For **solid materials** (e.g., Ti, Al, V, Cr), use their cohesive energy (in eV).
   - For **background gases** (e.g., N₂, O₂, Ar), set cohesive energy to `0`.

4. **Ionization and Mass-to-Charge Values:**
   - Ensure the new element is added to both `ionization_energies` and `mass_to_charge` dictionaries.
   - Provide at least the first 3 ionization levels for solids, and as many as available for gases.
   
### OUTPUT STRUCTURE
- The script creates an output folder (user-specified) in `OUTPUT_BASE_DIR`.
- For each pattern and element, it generates:
  - **Plots** (PNG): Saved in `OUTPUT_BASE_DIR/folder_name/element/`, with annotations for average energy (up to 60 eV).
  - **CSV File**:
    - `combined_analysis_results.csv`: Contains mean charge state, average potential energy, average kinetic energy, and average energy (up to 60 eV) for each charge state.

### ANALYSIS DETAILS
- **Average Energy Calculation**: Only energies <= 60 eV are used for the average energy calculation.
- **Mean Charge State**: Calculated for each element across all charge states.
- **Potential Energy**: Includes cohesive energy for solids and ionization energy for all elements.
- **Kinetic Energy**: Weighted average of the energy distribution for each element.
- **Plot Annotations**: Each plot includes the average energy for each charge state.

### CONSTANTS AND PARAMETERS
- `G`, `S`, `MU`: Parameters for the mass transmission function.
- `C_FACTOR`: Estimates how much potential energy ends up in the surface (default: 0.8).

### EXAMPLE WORKFLOW
1. Place all CSV files in `DATA_DIR` and define it.
2. Depending on your naming scheme change the truncate_pattern function (first function below)
3. Run the script and select a process (e.g., "TiAlN").
4. Select the patterns to analyze (or choose 'a' for all).
5. Enter a name for the output folder (e.g., "TiAlN_Analysis").
6. Results are saved in the output folder:
   - Plots for each element and pattern.
   - CSV file with detailed analysis results.

### NOTES
- For background gases (N, O, Ar, etc.), potential energy is based on ionization energy only.
- For cathode materials (including compounds like TiN, VN, AlN), potential energy includes cohesive/bond energy.
- The script automatically applies mass transmission correction and charge state correction.
- Pattern names are truncated for cleaner output filenames (last 4 parts of the pattern name).
"""



import os
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# --- USER CONFIGURATION ---
DATA_DIR = "/media/sf_Junk.Paul/Measurements/Massspec2"  # Directory containing CSV files
OUTPUT_BASE_DIR = "/home/bruh/Documents"                # Base directory for output

# --- CONSTANTS ---
G = 226.32
S = 1.27
MU = 5.06
C_FACTOR = 0.8  # Rough estimate of how much potential energy ends up in the surface

# --- FUNCTIONS ---
def truncate_pattern(pattern):
    """Truncate pattern name for cleaner output filenames."""
    parts = pattern.split('-')
    parts = [part.replace(',', '.') for part in parts]
    return '-'.join(parts[-4:])

def MassTransmission(M):
    """Transmission function after Chatain and Rohkamm."""
    return (G / (M * S * np.sqrt(2 * np.pi))) * np.exp(-(np.log(M) - MU) ** 2 / (2 * S ** 2))

def get_process_materials():
    """Define available processes and their associated elements, cohesive energies, and file patterns."""
    process_materials = {
        "1": {
            "name": "TiAl",
            "elements": ["Al", "Ti"],
            "cohesive_energies": {"Al": 3.39, "Ti": 4.85},
            "pattern_structure": [
                ("Al", 1, 0), ("Al", 2, 1), ("Al", 3, 2),
                ("Ti", 1, 3), ("Ti", 2, 4), ("Ti", 3, 5), ("Ti", 4, 6),
            ]
        },
        "2": {
            "name": "TiAlN (Al+Ti cathode, N₂ gas)",
            "elements": ["Al", "Ti", "N", "N₂"],
            "cohesive_energies": {"Al": 3.39, "Ti": 4.85, "N": 0, "N₂": 0},
            "pattern_structure": [
                ("Al", 1, 0), ("Al", 2, 1), ("Al", 3, 2),
                ("Ti", 1, 3), ("Ti", 2, 4), ("Ti", 3, 5), ("Ti", 4, 6),
                ("N", 1, 7), ("N₂", 1, 8),
            ]
        },
        # Add more processes here as needed
    }
    return process_materials

# Element properties (ionization energies and mass-to-charge ratios)
ionization_energies = {
    "Al": [5.98577, 18.8285, 28.4477, 119.992, 153.826, 190.48],
    "Ti": [6.8282, 13.5755, 27.4917, 43.2672, 99.3004, 120.0],
    "V": [6.74, 14.65, 29.31, 46.71, 65.2, 128.1],
    "N": [14.5341, 29.6013, 47.4492, 77.4735, 97.8902, 552.068],
    "N₂": [15.58, 38.5, 65.0],
    "O": [13.6181, 35.1173, 54.9355, 77.4135, 113.899, 138.119],
    "Ar": [15.7596, 27.6297, 40.74, 59.81, 75.02, 91.008]
}

mass_to_charge = {
    "Al": [26.981538 / i for i in range(1, 7)],
    "Ti": [47.867 / i for i in range(1, 7)],
    "V": [50.9415 / i for i in range(1, 7)],
    "N": [14.0067 / i for i in range(1, 7)],
    "N₂": [28.013 / i for i in range(1, 7)],
    "O": [15.999 / i for i in range(1, 7)],
    "Ar": [39.948 / i for i in range(1, 7)]
}

"""
Famous last words, it shouldnt be needed to go below here
"""


def list_unique_patterns_sorted(data_dir):
    """List all unique measurement patterns in the data directory, sorted by length (longest first)."""
    try:
        filenames = os.listdir(data_dir)
    except FileNotFoundError:
        print(f"Error: Directory '{data_dir}' not found.")
        return []
    patterns = set()
    for filename in filenames:
        if filename.endswith(".csv"):
            match = re.match(r"^(.*?)paview\d+\.csv$", filename, re.IGNORECASE)
            if match:
                patterns.add(match.group(1))
    return sorted(patterns, key=len, reverse=True)  # Sort by length, longest first

def list_unique_patterns_ordered(data_dir):
    """List all unique measurement patterns in the data directory, in the order they appear in the folder."""
    try:
        filenames = os.listdir(data_dir)
    except FileNotFoundError:
        print(f"Error: Directory '{data_dir}' not found.")
        return []
    patterns = []
    for filename in filenames:
        if filename.endswith(".csv"):
            match = re.match(r"^(.*?)paview\d+\.csv$", filename, re.IGNORECASE)
            if match:
                pattern = match.group(1)
                if pattern not in patterns:
                    patterns.append(pattern)
    return patterns 
def select_patterns(data_dir):
    """Prompt user to select patterns for analysis."""
    patterns = list_unique_patterns_ordered(data_dir)
    if not patterns:
        print("No patterns found. Check the data directory.")
        return []
    print("\nAvailable patterns:")
    for i, pattern in enumerate(patterns, 1):
        print(f"{i}. {pattern}")
    print("\nEnter the numbers of the patterns you want to analyze (comma-separated) or 'a' for all:")
    while True:
        selection = input().strip().lower()
        if selection == 'a':
            return patterns
        try:
            selections = selection.split(",")
            selected_indices = [int(s.strip()) - 1 for s in selections]
            selected_patterns = [patterns[i] for i in selected_indices]
            return selected_patterns
        except (ValueError, IndexError):
            print("Invalid input. Please enter valid numbers (e.g., 1,3,5) or 'a' for all.")

def assign_charge_states(data_dir, pattern, elements, pattern_structure):
    """Assign CSV files to charge states based on pattern structure, ensuring exact matching."""
    files = [f for f in os.listdir(data_dir) if f.startswith(pattern) and f.endswith(".csv")]
    # Remove files that belong to longer patterns
    patterns_sorted = list_unique_patterns_sorted(data_dir)
    files = [f for f in files if not any(
        p.startswith(pattern) and p != pattern and f.startswith(p)
        for p in patterns_sorted
    )]
    if not files:
        print(f"No files found for pattern: {pattern}")
        return {}
    assignments = {element: {} for element in elements}
    for element, charge, file_index in pattern_structure:
        if file_index < len(files):
            if charge not in assignments[element]:
                assignments[element][charge] = []
            assignments[element][charge].append(files[file_index])
    return assignments



def setup_process(data_dir):
    """Set up the analysis process by selecting a process and patterns."""
    process_materials = get_process_materials()
    print("Available processes:")
    for key, process in process_materials.items():
        print(f"{key}. {process['name']}")
    while True:
        process_key = input("Enter the number of the process: ").strip()
        if process_key in process_materials:
            selected_process = process_materials[process_key]
            break
        else:
            print("Invalid input. Please try again.")
    selected_patterns = select_patterns(data_dir)
    if not selected_patterns:
        print("No patterns selected. Exiting.")
        return None
    selected_ionization_energies = {element: ionization_energies[element] for element in selected_process["elements"]}
    selected_mass_to_charge = {element: mass_to_charge[element] for element in selected_process["elements"]}
    selected_cohesive_energies = selected_process["cohesive_energies"]
    process = {
        "name": selected_process["name"],
        "elements": selected_process["elements"],
        "patterns": selected_patterns,
        "file_assignments": {},
        "ionization_energies": selected_ionization_energies,
        "mass_to_charge": selected_mass_to_charge,
        "cohesive_energies": selected_cohesive_energies,
        "pattern_structure": selected_process["pattern_structure"]
    }
    for pattern in selected_patterns:
        process["file_assignments"][pattern] = assign_charge_states(
            data_dir, pattern, process["elements"], process["pattern_structure"]
        )
    return process

def find_average_energy(energy, iedf):
    """Calculate the average energy for energies <= 65 eV."""
    mask = energy <= 65
    energy_range = energy[mask]
    iedf_range = iedf[mask]
    if np.sum(iedf_range) > 0:
        average_energy = np.average(energy_range, weights=iedf_range)
    else:
        average_energy = energy[np.argmax(iedf)]
    return average_energy

def extract_parameters(pattern):
    """Extract distance, magnetic field, pressure, and version from the pattern."""
    distance = None
    magnetic_field = None
    pressure = None
    version = None

    distance_match = re.search(r'(\d+\.?\d*)\s*cm', pattern, re.IGNORECASE)
    magnetic_field_match = re.search(r'(\d+\.?\d*)\s*t', pattern, re.IGNORECASE)
    pressure_match = re.search(r'n-(\d+\.?\d*)', pattern, re.IGNORECASE)
    version_match = re.search(r'v(\d+)', pattern, re.IGNORECASE)

    if distance_match:
        distance = float(distance_match.group(1))
    if magnetic_field_match:
        magnetic_field = float(magnetic_field_match.group(1))
    if pressure_match:
        pressure = float(pressure_match.group(1))
    if version_match:
        version = int(version_match.group(1))

    return distance, magnetic_field, pressure, version


# --- MAIN EXECUTION ---
if __name__ == "__main__":
    process = setup_process(DATA_DIR)
    if process:
        folder_name = input("Enter a name for the output folder (in Documents): ").strip()
        output_dir = os.path.join(OUTPUT_BASE_DIR, folder_name)
        os.makedirs(output_dir, exist_ok=True)
        # Initialize a list to collect all results
        all_results = []
        # Process each pattern
        for pattern in process["patterns"]:
            truncated_pattern = truncate_pattern(pattern)
            print(f"\nProcessing pattern: {pattern}")

            # Extract parameters from the pattern
            distance, magnetic_field, pressure, version = extract_parameters(pattern)

            # Update pattern_results with the extracted parameters
            pattern_results = {
                "pattern": truncated_pattern,
                "distance (cm)": distance,
                "magnetic_field (T)": magnetic_field,
                "pressure (Pa)": pressure,
                "version": version,
                "elements": {}
            }

            df_set = pd.DataFrame()
            csv_files = []
            for element, charge_states in process["file_assignments"][pattern].items():
                for charge, files in charge_states.items():
                    csv_files.extend(files)
            for jdx, csv_file in enumerate(csv_files):
                df_raw = pd.read_csv(os.path.join(DATA_DIR, csv_file), header=None, names=['Energy', 'IEDF'])
                for element in process["elements"]:
                    for charge, files in process["file_assignments"][pattern][element].items():
                        if csv_file in files:
                            mass = process["mass_to_charge"][element][charge-1]
                            df_raw['IEDF'] = df_raw['IEDF'] * MassTransmission(mass)
                            if charge > 1:
                                df_raw['Energy'] = df_raw['Energy'] * charge
                            break
                df_set[f'E{jdx+1}'] = df_raw['Energy']
                df_set[f'IEDF{jdx+1}'] = df_raw['IEDF']
            # Calculate results for each element
            for element in process["elements"]:
                iedf_sum = []
                avg_energy = []
                avg_energy_60eV = {}  # Store average energy (up to 60 eV) for each charge state
                individual_kinetic_energies = {}  # Store individual kinetic energies for each charge state
                for charge in sorted(process["file_assignments"][pattern][element].keys()):
                    if process["file_assignments"][pattern][element][charge]:
                        col_idx = csv_files.index(process["file_assignments"][pattern][element][charge][0]) + 1
                        iedf_sum.append(df_set[f'IEDF{col_idx}'].sum())
                        individual_kinetic_energy = (df_set[f'E{col_idx}'] * df_set[f'IEDF{col_idx}']).sum() / df_set[f'IEDF{col_idx}'].sum()
                        avg_energy.append(individual_kinetic_energy)
                        individual_kinetic_energies[charge] = individual_kinetic_energy  # Store the individual kinetic energy
                        # Calculate average energy (up to 60 eV) for this charge state
                        energy = df_set[f'E{col_idx}']
                        iedf = df_set[f'IEDF{col_idx}']
                        avg_energy_60eV[charge] = find_average_energy(energy, iedf)
                    else:
                        iedf_sum.append(0)
                        avg_energy.append(0)
                        avg_energy_60eV[charge] = 0
                        individual_kinetic_energies[charge] = 0

                total_iedf = sum(iedf_sum)
                if total_iedf > 0:
                    if process["cohesive_energies"][element] > 0:
                        epot = [process["cohesive_energies"][element] + C_FACTOR * sum(process["ionization_energies"][element][:i]) for i in range(1, len(iedf_sum)+1)]
                    else:
                        epot = [C_FACTOR * sum(process["ionization_energies"][element][:i]) for i in range(1, len(iedf_sum)+1)]
                    avg_epot = np.sum(np.array(iedf_sum) * np.array(epot)) / total_iedf
                    avg_ekin = np.sum(np.array(iedf_sum) * np.array(avg_energy)) / total_iedf
                    qmean = np.sum(np.array(iedf_sum) * np.array(range(1, len(iedf_sum)+1))) / total_iedf
                else:
                    avg_epot, avg_ekin, qmean = 0, 0, 0
                pattern_results["elements"][element] = {
                    "mean_charge_state": qmean,
                    "avg_potential_energy": avg_epot,
                    "avg_kinetic_energy": avg_ekin,
                    "avg_energy_60eV": avg_energy_60eV,
                    "individual_kinetic_energies": individual_kinetic_energies
                }
            # Add pattern results to the list
            for element, data in pattern_results["elements"].items():
                row = {
                    "Pattern": truncated_pattern,
                    "Distance (cm)": pattern_results["distance (cm)"] if pattern_results["distance (cm)"] is not None else "",
                    "Magnetic Field (T)": pattern_results["magnetic_field (T)"] if pattern_results["magnetic_field (T)"] is not None else "",
                    "Pressure (Pa)": pattern_results["pressure (Pa)"] if pattern_results["pressure (Pa)"] is not None else "",
                    "Version": pattern_results["version"] if pattern_results["version"] is not None else "",
                    "Element": element,
                    "Mean Charge State": data["mean_charge_state"],
                    "Average Potential Energy (eV)": data["avg_potential_energy"],
                    "Average Kinetic Energy (eV)": data["avg_kinetic_energy"]
                }
                # Add average energy (up to 60 eV) for each charge state
                for charge in sorted(data["avg_energy_60eV"].keys()):
                    row[f"Avg Energy (≤60 eV) {element}{'+' * charge}"] = data["avg_energy_60eV"][charge]
                # Add individual kinetic energies for each charge state
                for charge in sorted(data["individual_kinetic_energies"].keys()):
                    row[f"Kinetic Energy {element}{'+' * charge}"] = data["individual_kinetic_energies"][charge]
                all_results.append(row)
            # Plot and save figures
            for element in process["elements"]:
                if any(process["file_assignments"][pattern][element].values()):
                    plt.figure(figsize=(8, 6))
                    annotations = []
                    for charge in sorted(process["file_assignments"][pattern][element].keys()):
                        if process["file_assignments"][pattern][element][charge]:
                            col_idx = csv_files.index(process["file_assignments"][pattern][element][charge][0]) + 1
                            energy = df_set[f'E{col_idx}']
                            iedf = df_set[f'IEDF{col_idx}']
                            average_energy = find_average_energy(energy, iedf)
                            annotations.append(f'{element}{"+"*charge}: {average_energy:.2f} eV')
                            plt.plot(energy, iedf, label=f'{element}{"+"*charge}')
                    plt.xlim([0, 300])
                    plt.yscale("log")
                    plt.ylim([10, 10**6])
                    plt.title(f"{truncated_pattern} - {element}")
                    plt.xlabel('Energy (eV)')
                    plt.ylabel('Counts per second')
                    plt.legend()
                    plt.annotate("\n".join(annotations), xy=(0.02, 0.98), xycoords='axes fraction',
                                 verticalalignment='top', horizontalalignment='left',
                                 bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
                    plt.tight_layout()
                    element_dir = os.path.join(output_dir, element)
                    os.makedirs(element_dir, exist_ok=True)
                    filename = f"{truncated_pattern}_{element}.png"
                    plt.savefig(os.path.join(element_dir, filename), dpi=300, bbox_inches='tight')
                    plt.close()
                    print(f"Saved: {os.path.join(element, filename)}")
        # Convert the list of results to a DataFrame and save to CSV
        df_results = pd.DataFrame(all_results)
        output_csv = os.path.join(output_dir, "combined_analysis_results.csv")
        df_results.to_csv(output_csv, index=False)
        print(f"\nCombined results saved to: {output_csv}")
    else:
        print("Process setup failed. Exiting.")


