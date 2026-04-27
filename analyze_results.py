import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def process_data(filename):
    # Read the raw data
    data = []
    with open(filename, 'r') as f:
        for line in f:
            size, patch, nprocs, time = line.strip().split(';')
            data.append((int(size), int(nprocs), float(time)))

    # Create DataFrame
    df = pd.DataFrame(data, columns=["size", "nprocs", "time"])

    # Group by size and nprocs and compute mean time
    grouped = df.groupby(["size", "nprocs"])["time"].mean().reset_index()
    grouped = grouped.sort_values(["size", "nprocs"])

    # Compute speed-up and parallel efficiency
    results = []

    for size in grouped["size"].unique():
        df_size = grouped[grouped["size"] == size]
        t1 = df_size[df_size["nprocs"] == 1]["time"].values[0]
        for _, row in df_size.iterrows():
            p = row["nprocs"]
            t = row["time"]
            speedup = t1 / t
            efficiency = speedup / p
            results.append({
                "size": size,
                "nprocs": p,
                "mean_time": t,
                "speedup": speedup,
                "efficiency": efficiency
            })

    return pd.DataFrame(results)



def process_patch_experiment(filename):
    data = []
    with open(filename, "r") as f:
        for line in f:
            size, patch, nprocs, time = line.strip().split(";")
            data.append((int(size), int(patch), int(nprocs), float(time)))

    df = pd.DataFrame(data, columns=["size", "patch", "nprocs", "time"])

    grouped = (
        df.groupby(["size", "nprocs", "patch"])["time"]
        .mean()
        .reset_index()
        .rename(columns={"time": "mean_time"})
        .sort_values(["size", "nprocs", "patch"])
    )

    return df, grouped


#2.3 and 2.4 data: 

df_23, grouped_2_3 = process_patch_experiment("output_exp23_5116564.dat")
df_24, grouped_2_4 = process_patch_experiment("output_exp24_5116759.dat")

print(df_23.head() )
print(df_24.head())
#save to csv 
grouped_2_3.to_csv("results_patch_2_3.csv", index=False)
grouped_2_4.to_csv("results_patch_2_4.csv", index=False)    



# Load both datasets
df_cb = process_data("output_exp22_1_5116562.dat")
df_cs = process_data("output_exp22_2_5116563.dat")  

# Save tables (optional)
df_cb.to_csv("results_cb.csv", index=False)
df_cs.to_csv("results_cs.csv", index=False)

# Display tables
print("\nResults for cb (benchmark):")
print(df_cb.to_string(index=False))

print("\nResults for cs (student):")
print(df_cs.to_string(index=False))

