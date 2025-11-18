# save as sumo_to_csv.py
import pandas as pd
import xml.etree.ElementTree as ET

def sumo_output_to_csv(xml_file, csv_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    data = []

    for interval in root.findall('interval'):
        data.append({
            'begin': float(interval.get('begin')),
            'end': float(interval.get('end')),
            'id': interval.get('id'),
            'flow': float(interval.get('flow')),
            'occupancy': float(interval.get('occupancy')),
            'speed': float(interval.get('speed')),
            'nVeh': int(interval.get('nVehContrib'))
        })

    df = pd.DataFrame(data)
    df.to_csv(csv_file, index=False)
    print(f"✅ Saved {len(df)} records to {csv_file}")

sumo_output_to_csv('detector_output.xml', 'traffic_data.csv')
