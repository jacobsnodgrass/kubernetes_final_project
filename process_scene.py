#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import rasterio
import numpy as np
from utils import apply_scale_factors, compute_lst, apply_cloud_mask, summarize_scene

INPUT_DIR = '/data/input'
OUTPUT_DIR = '/data/output'

def main():
    # The pod will receive the scene index or name via env var
    scene_name = os.environ.get('SCENE_NAME')
    if scene_name is None:
        raise ValueError('SCENE_NAME environment variable not set')
        
    scene_path = os.path.join(INPUT_DIR, f'{scene_name}.tif')
    if not os.path.exists(scene_path):
        raise FineNotFoundError(f'Input scene not foun: {scene_path}')
        
    print(f'Processing scene: {scene_name}')
    
    with rasterio.open(scene_path) as src:
        arr = src.read(1).astype('float32')
        profile = src.profile
        
        # Basic Steps
        arr = apply_scale_factors(arr)
        arr = compute_lst(arr)
        arr = apply_cloud_mask(arr)
        
    output_raster = os.path.join(OUTPUT_DIR, f'{scene_name}_lst.tif')
    profile.update(dtype=rasterio.float32)
    
    with rasterio.open(output_raster, 'w', **profile) as dst:
        dst.write(arr, 1)
        
    # Summaries (mean, median, etc)
    summary = summarize_scene(arr)
    summary_path = os.path.join(OUTPUT_DIR, f'{scene_name}_summary.csv')
    
    with open(summary_path, 'w') as f:
        for k, v in summary.items():
            f.write(f"{k},{v}\n")
            
    print(f'Finished processing {scene_name}')
    
if __name__ == "__main__": 
    main()

