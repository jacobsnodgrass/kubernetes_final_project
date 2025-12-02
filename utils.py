#!/usr/bin/env python
# coding: utf-8

# In[2]:


import numpy as np

def apply_scale_factors(arr, scale=0.0000275, offset=-0.2):
    """
    Applies Landsat Collection 2 Level-2 scale factors.
    """
    return arr * scale + offset
def compute_lst(arr, k1=774.89, k2=1321.08):
    """
    Simplified brightness temperature to LST conversion.
    Replace with full radiance + emissivity LST model later.
    """
    arr = np.where(arr > 0, arr, np.nan)
    
    return k2 / np.log((k1 / arr) + 1)

def apply_cloud_mask(arr, mask_value=np.nan):
    """
    Placeholder: In a full pipeline read QA_PIXEL band instead.
    """
    
    arr[arr < 200] = np.nan
    arr[arr > 400] = np.nan
    
    return arr

def summarize_scene(arr):
    """
    Compute basic statistics for reporting and later aggregation.
    """
    arr_flat = arr[~np.isnan(arr)]
    
    return {
        "mean": float(np.nanmean(arr)),
        "median": float(np.nanmedian(arr)),
        "min": float(np.nanmin(arr_flat)),
        "max": float(np.nanmax(arr_flat)),
        "std": float(np.nanstd(arr_flat)),
        "valid_pixels": int(arr_flat.size)
    }


# In[ ]:




