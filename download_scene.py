#!/usr/bin/env python
# coding: utf-8

# In[1]:


import boto3
import os
import logging

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')


def download_scene(scene_id, path='034', row='032', local_dir='./data/input', bands=None):
    """
    Download selected bands of a Landsat scene from AWS Open Data.

    Args:
        scene_id (str): Landsat scene ID
        path (str): WRS-2 path
        row (str): WRS-2 row
        local_dir (str): Local directory to store bands
        bands (list): List of bands to download (e.g., ['B10.TIF', 'QA_PIXEL.TIF'])
    """
    if bands is None:
        bands = ['B10.TIF', 'QA_PIXEL.TIF']  # default thermal + QA

    bucket = 'landsat-pds'
    prefix = f'c2/L8/{path}/{row}/{scene_id}/'
    os.makedirs(local_dir, exist_ok=True)
    s3 = boto3.client('s3')

    try:
        response = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)
    except Exception as e:
        logging.error(f"Error accessing S3 bucket: {e}")
        return

    if 'Contents' not in response:
        raise FileNotFoundError(f"Scene {scene_id} not found in S3.")

    for obj in response['Contents']:
        key = obj['Key']
        file_name = os.path.basename(key)
        if file_name not in bands:
            continue  # skip unwanted bands

        local_file = os.path.join(local_dir, f"{scene_id}_{file_name}")
        if not os.path.exists(local_file):
            try:
                s3.download_file(bucket, key, local_file)
                logging.info(f"Downloaded {local_file}")
            except Exception as e:
                logging.error(f"Failed to download {key}: {e}")
        else:
            logging.info(f"File already exists, skipping: {local_file}")

