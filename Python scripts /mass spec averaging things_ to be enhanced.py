import pandas as pd
import matplotlib.pyplot as plt

def plot_data(x_axis, filter_vars, filter_values, data):
    # Filter data based on selected parameters
    filtered_data = data.copy()
    for var, values in zip(filter_vars, filter_values):
        filtered_data = filtered_data[filtered_data[var].isin(values)]

    # Create a figure with secondary y-axis
    fig, ax1 = plt.subplots()

    # Plot IonCurrent on the left y-axis
    for pressure in filter_values[0]:
        for magfield in filter_values[1]:
            subset = filtered_data[
                (filtered_data[filter_vars[0]] == pressure) &
                (filtered_data[filter_vars[1]] == magfield)
            ]
            ax1.plot(subset[x_axis], subset['IonCurrent (A)'],
                     label=f'IonCurrent (A) - P: {pressure} Pa, B: {magfield} T')
    ax1.set_xlabel(x_axis)
    ax1.set_ylabel('IonCurrent (A)', color='#1f77b4')
    ax1.tick_params(axis='y', labelcolor='#1f77b4')

    # Create a second y-axis for Mass
    ax2 = ax1.twinx()
    for pressure in filter_values[0]:
        for magfield in filter_values[1]:
            subset = filtered_data[
                (filtered_data[filter_vars[0]] == pressure) &
                (filtered_data[filter_vars[1]] == magfield)
            ]
            ax2.plot(subset[x_axis], subset['Mass (g)'],
                     linestyle='--',
                     label=f'Mass (g) - P: {pressure} Pa, B: {magfield} T')
    ax2.set_ylabel('Mass (g)', color='#ff7f0e')
    ax2.tick_params(axis='y', labelcolor='#ff7f0e')

    # Combine legends from both axes
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right')

    plt.title(f'Plot of IonCurrent and Mass vs {x_axis}')
    plt.show()

def main():
    # Load the data
    data = pd.read_csv('/home/bruh/Documents/ioncurrent+mass.csv')
    # Prompt for x-axis
    print("Choose the x-axis:")
    print("1. Distance (cm)")
    print("2. Pressure (Pa)")
    print("3. MagField (T)")
    x_axis_choice = input("Enter your choice (1, 2, or 3): ")

    x_axis_map = {
        '1': 'Distance (cm)',
        '2': 'Pressure (Pa)',
        '3': 'MagField (T)'
    }

    x_axis = x_axis_map.get(x_axis_choice)
    if x_axis is None:
        raise ValueError("Invalid choice. Please enter 1, 2, or 3.")

    # Determine remaining parameters
    all_params = ['Distance (cm)', 'Pressure (Pa)', 'MagField (T)']
    remaining_params = [param for param in all_params if param != x_axis]

    # Prompt for filtering
    print(f"\nWhich of the remaining parameters do you want to filter multiple values for?")
    print(f"1. {remaining_params[0]}")
    print(f"2. {remaining_params[1]}")
    filter_choice = input("Enter your choice (1 or 2): ")

    if filter_choice == '1':
        filter_var1 = remaining_params[0]
        filter_var2 = remaining_params[1]
    elif filter_choice == '2':
        filter_var1 = remaining_params[1]
        filter_var2 = remaining_params[0]
    else:
        raise ValueError("Invalid choice. Please enter 1 or 2.")

    # Prompt for values
    filter_values1 = list(map(float, input(f"Enter the {filter_var1} values you want to filter by, separated by spaces: ").split()))
    filter_value2 = float(input(f"Enter the {filter_var2} value you want to filter by: "))

    # Call the plotting function
    plot_data(x_axis, [filter_var1, filter_var2], [filter_values1, [filter_value2]], data)

if __name__ == "__main__":
    main()
