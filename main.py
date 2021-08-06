from pathlib import Path
import xml.etree.ElementTree as ET

import pandas as pd

data_folder = Path('./data/raw')

point_pairing = (
    ('Ant shelf L', 'Post shelf L'),
    ('Ant shelf R', 'Post shelf R'),
    ('Post shelf L', 'Ant whis L'),
    ('Post shelf R', 'Ant whis R'),
    ('Post shelf L', 'Ant nare L'),
    ('Post shelf R', 'Ant nare R'),
    ('Ant shelf L', 'Post whis L'),
    ('Ant shelf R', 'Post whis R'),
    ('Post whis L', 'Post whis R'),
    ('Med shelf L', 'Post whis L'),
    ('Med shelf R', 'Post whis R'),
    ('Left', 'Right')
)

def get_point(node):
    return {'x': float(node.attrib['x']), 'y': float(node.attrib['y'])}

def create_file_points(filename):
    try:
        tree = ET.parse(filename)
        root = tree.getroot()
        data = pd.DataFrame({node.attrib['name']: get_point(node) for node in root})
    except Exception as e:
        print(f'I failed on this name: {filename}. Come on Cathy! Sort it out!!!')
        raise e
    data['File'] = filename.stem
    data.loc[:, ['Info', 'Culture', 'Time']] = parse_filename(data['File'])
    data = data.set_index('File', append=True).reorder_levels([1,0])
    return data

def parse_filename(filename: pd.Series):
    mapping = {
        'E12.5': 0.0,
        'E13': 12.0,
        'E13.5': 24.0,
        'E14': 36.0,
        'E14.5': 48.0,
        'E15': 60.0,
    }
    result = (
        filename
            .str
            .split(' ', expand=True)
            .iloc[:, :3]
            .rename(columns={
            ix: name
            for ix, name in enumerate(['Info', 'Culture', 'Time'])
        })
    )
    result['Time'] = result['Time'].str.replace('[A-z]*', '', regex=True).astype(float)
    result.loc[filename.str.contains('Fix', regex=False), 'Time'] = result['Info'].map(mapping).astype(float)
    return result

def measure_distances(data):
    return pd.DataFrame(
        {f'Dist({x}, {y})': ((data[x] - data[y]) ** 2).sum() ** .5
         for x, y in point_pairing
         if x in data.columns and y in data.columns},
        index=data.index.levels[0]
    )

if __name__ == '__main__':
    data = [create_file_points(file) for file in data_folder.glob('*.points')]
    distances = pd.concat(map(measure_distances, data))
    distances = pd.concat([distances, parse_filename(pd.Series(distances.index, index=distances.index))], axis=1)
    data = pd.concat(data)

    writer = pd.ExcelWriter('results/data.xlsx')
    data.to_excel(writer, sheet_name='Points')
    distances.to_excel(writer, sheet_name='Distances')
    writer.save()
