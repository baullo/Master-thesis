import pandas as pd


file_path = "/media/sf_Junk.Paul/Measurements/measurements.xlsx"   
sheet_name = "Sheet1"                          
NA = 6.022e23
molar_mass_approx   = 37.424        #need to change it      
threshold = 1e-4 


first_row = 8
last_row = 49

#%%
MM = {"Ti": 47.867, "Al": 26.982, "N": 14.0067} #g/mol

#need molar mass

skiprows = first_row - 1
nrows = last_row - first_row + 1

df = pd.read_excel(
    file_path, 
    sheet_name="Sheet1", 
    usecols="B,F,R,J",
    skiprows= skiprows,
    nrows= nrows
    )
df.columns = ["Distance_cm", "Pressure_Pa","Magnetic_field_T", "Mass_g"]

df_sorted = df.sort_values(by=["Pressure_Pa", "Magnetic_field_T"]).reset_index(drop=True)


df_sorted.loc[df_sorted["Pressure_Pa"].abs() < threshold, "Pressure_Pa"] = 0

# Optional: rebuild the label after sorting
df_sorted["Label"] = (
    df_sorted["Magnetic_field_T"].astype(str) + "T_" +
    df_sorted["Distance_cm"].astype(str) + "cm_" +
    df_sorted["Pressure_Pa"].astype(str) + "Pa_N2"
)


# Compute atoms
df_sorted["Atoms"] = df_sorted["Mass_g"] / molar_mass_approx * NA #need to be changed


result = df_sorted[["Label", "Mass_g", "Atoms"]]
print(result)