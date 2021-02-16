from pathlib import Path
import xml.etree.ElementTree as ET

import pandas as pd

def get_point(node):
    return {'x': float(node.attrib['x']), 'y': float(node.attrib['y'])}

def create_file_points(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    data = pd.DataFrame({node.attrib['name']: get_point(node) for node in root}).T
    data['File'] = filename.stem
    data = data.set_index('File', append=True).reorder_levels([1,0])
    return data

data_folder = Path('./data')

data = pd.concat([create_file_points(file) for file in data_folder.glob('*.points')], axis=0)

