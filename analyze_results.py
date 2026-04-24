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

# Load both datasets
df_cb = process_data("output_exp22_1_4961958.dat")
df_cs = process_data("output_exp22_2_4962019.dat")

# Save tables (optional)
df_cb.to_csv("results_cb.csv", index=False)
df_cs.to_csv("results_cs.csv", index=False)

# Display tables
print("\nResults for cb (benchmark):")
print(df_cb.to_string(index=False))

print("\nResults for cs (student):")
print(df_cs.to_string(index=False))