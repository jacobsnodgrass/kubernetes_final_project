#!/usr/bin/env python
# coding: utf-8

# In[2]:


import os
import logging
import rasterio
from utils import apply_scale_factors, compute_lst, apply_cloud_mask, summarize_scene
from download_scene import download_scene

# Directories (mounted PVCs in Kubernetes)
INPUT_DIR = '/data/input'
OUTPUT_DIR = '/data/output'

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')


def process_scene(scene_id, path='034', row='032'):
    """
    Process a single Landsat scene:
    1. Download if missing
    2. Apply scaling, LST conversion, cloud mask
    3. Write LST raster and summary CSV
    """
    thermal_file = os.path.join(INPUT_DIR, f"{scene_id}_B10.TIF")  # Thermal band
    qa_file = os.path.join(INPUT_DIR, f"{scene_id}_QA_PIXEL.TIF")  # QA_PIXEL band

    # Step 1: Download if missing
    if not os.path.exists(thermal_file) or not os.path.exists(qa_file):
        logging.info(f"Scene bands not found locally. Downloading from AWS...")
        try:
            download_scene(scene_id, path=path, row=row, local_dir=INPUT_DIR)
        except FileNotFoundError as e:
            logging.error(str(e))
            return

    logging.info(f"Processing scene: {scene_id}")

    # Step 2: Load raster bands
    try:
        with rasterio.open(thermal_file) as src:
            arr = src.read(1).astype('float32')
            profile = src.profile
    except Exception as e:
        logging.error(f"Failed to read {thermal_file}: {e}")
        return

    qa_arr = None
    if os.path.exists(qa_file):
        try:
            with rasterio.open(qa_file) as src:
                qa_arr = src.read(1).astype('uint16')
        except Exc

