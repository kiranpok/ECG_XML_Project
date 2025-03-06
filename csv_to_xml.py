import pandas as pd
import os
import xml.etree.ElementTree as ET

input_folder = 'data'
output_folder = 'xml_output'

os.makedirs(output_folder, exist_ok=True)

for csv_file in os.listdir(input_folder):
    if csv_file.endswith('.csv'):
        csv_path = os.path.join(input_folder, csv_file)
        df = pd.read_csv(csv_path, header=None)

        filename_parts = csv_file.replace('.csv', '').split('_')
        patient_id = filename_parts[0] + "_" + filename_parts[1]
        diagnosis = filename_parts[2]
        start_time = filename_parts[3]

        patient = ET.Element('patient')

        ET.SubElement(patient, 'id').text = patient_id
        ET.SubElement(patient, 'diagnosis').text = diagnosis

        measurement = ET.SubElement(patient, 'measurement')
        ET.SubElement(measurement, 'start_time').text = start_time

        spectrum = ET.SubElement(measurement, 'spectrum')

        frequency_interval = 0.5
        frequency = frequency_interval

        for value in df.iloc[:, 0]:
            freq_element = ET.SubElement(spectrum, 'frequency')
            freq_element.set('hz', f"{frequency:.1f}")
            freq_element.text = str(value)
            frequency += frequency_interval

        tree = ET.ElementTree(patient)
        xml_filename = csv_file.replace('.csv', '.xml')
        xml_path = os.path.join(output_folder, xml_filename)
        tree.write(xml_path, encoding='utf-8', xml_declaration=True)

        print(f"XML created: {xml_filename}")
