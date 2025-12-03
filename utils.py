#!/usr/bin/env python
# coding: utf-8

# In[2]:


import numpy as np
import logging

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')


def apply_scale_factors(arr, scale=0.0000275, offset=-0.2):
    """
    Applies Landsat Collection 2 Level-2 scale factors.
    """
    logging.info("Applying scale factors...")
    return arr * scale + offset


def compute_lst(arr, k1=774.89, k2=1321.08):
    """
    Simplified brightness temperature to LST conversion.
    Replace with full radiance + emissivity LST model later.
    """
    logging.info("Computing LST...")
    arr = np.where(arr > 0, arr, np.nan)
    with np.errstate(divide='ignore', invalid='ignore'):
        lst = k2 / np.log((k1 / arr) + 1)
    return lst


def apply_cloud_mask(arr, qa_arr=None, mask_value=np.nan):
    """
    Apply a cloud mask using the QA_PIXEL band if available.
    Falls back to thresholding if QA band not provided.
    
    Landsat QA_PIXEL example (bits):
      - Bit 3 = Cloud
      - Bit 4 = Cloud shadow
      - Bit 5 = Snow
    """
    logging.info("Applying cloud mask...")

    if qa_arr is not None:
        # Mask clouds, shadows, and snow
        cloud_mask = ((qa_arr & (1 << 3)) > 0) | ((qa_arr & (1 << 4)) > 0) | ((qa_arr & (1 << 5)) > 0)
        arr = np.where(cloud_mask, mask_value, arr)
    else:
        # Fallback: simple thresholds
        arr = np.where((arr < 200) | (arr > 400), mask_value, arr)

    return arr


def summarize_scene(arr):
    """
    Compute basic statistics for reporting and aggregation.
    """
    logging.info("Summarizing scene...")
    arr_flat = arr[~np.isnan(arr)]
    if arr_flat.size == 0:
        logging.warning("No valid pixels found in array.")
        return {
            "mean": np.nan,
            "median": np.nan,
            "min": np.nan,
            "max": np.nan,
            "std": np.nan,
            "valid_pixels": 0
        }

    return {
        "mean": float(np.nanmean(arr_flat)),
        "median": float(np.nanmedian(arr_flat)),
        "min": float(np.nanmin(arr_flat)),
        "max": float(np.nanmax(arr_flat)),
        "std": float(np.nanstd(arr_flat)),
        "valid_pixels": int(arr_flat.size)
    }


# In[ ]:




