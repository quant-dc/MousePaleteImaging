from pathlib import Path
import xml.etree.ElementTree as ET

import pandas as pd

point_pairing = (
    ('Ant shelf L', 'Post shelf L'),
    ('Ant shelf R', 'Post shelf R'),
    ('Ant shelf L', 'Ant lip L'),
    ('Ant shelf R', 'Ant lip R'),
    ('Post shelf L', 'Ant lip L'),
    ('Post shelf R', 'Ant lip R'),
)

def get_point(node):
    return {'x': float(node.attrib['x']), 'y': float(node.attrib['y'])}

def create_file_points(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    data = pd.DataFrame({node.attrib['name']: get_point(node) for node in root})
    data['File'] = filename.stem
    data = data.set_index('File', append=True).reorder_levels([1,0])
    return data

def measure_distances(data):
    return pd.DataFrame(
        {f'Dist({x}, {y})': ((data[x] - data[y]) ** 2).sum() ** .5 for x, y in point_pairing},
        index=data.index.levels[0]
    )

data_folder = Path('./data')

data = [create_file_points(file) for file in data_folder.glob('*.points')]
distances = pd.concat(map(measure_distances, data))
data = pd.concat(data)

writer = pd.ExcelWriter('results/data.xlsx')
data.to_excel(writer, sheet_name='Points')
distances.to_excel(writer, sheet_name='Distances')
writer.save()
