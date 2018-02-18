import os
from tqdm import tqdm
from time import sleep

quiet = False
brands = ['Nike', 'Patagonia', 'Coke', 'Netflix']
for brand in tqdm(brands, ncols = 130, desc='Analyzing brands', unit=" media", disable=quiet):
    sleep(0.5)
for brand in tqdm(brands, ncols = 130, desc='Analyzing brands', unit=" media", disable=quiet):
    sleep(0.2)
