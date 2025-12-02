#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import pandas as pd

OUTPUT_DIR = "/data/output"

def main():
    summaries = []

    for filename in os.listdir(OUTPUT_DIR):
        if filename.endswith("_summary.csv"):
            scene = filename.replace("_summary.csv", "")
            df = pd.read_csv(os.path.join(OUTPUT_DIR, filename), header=None, names=["metric", "value"])
            df["scene"] = scene
            summaries.append(df)

    if summaries:
        full = pd.concat(summaries)
        pivot = full.pivot(index="scene", columns="metric", values="value")
        pivot.to_csv(os.path.join(OUTPUT_DIR, "all_summaries.csv"))

    print("Aggregated all summaries successfully.")

if __name__ == "__main__":
    main()

