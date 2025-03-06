import os
import xml.etree.ElementTree as ET
import pandas as pd

xml_folder = 'xml_output'

# Storage for detailed analysis results
analysis_results = []

# Process each XML file
for xml_file in os.listdir(xml_folder):
    if xml_file.endswith('.xml'):
        xml_path = os.path.join(xml_folder, xml_file)
        tree = ET.parse(xml_path)
        root = tree.getroot()

        # Get patient details
        patient_id = root.find('id').text
        diagnosis = root.find('diagnosis').text
        start_time = root.find('./measurement/start_time').text

        # Extract frequency amplitudes
        frequencies = root.findall('.//frequency')
        amplitudes = [float(freq.text) for freq in frequencies]

        # Calculate average, minimum, and maximum amplitude
        avg_amplitude = sum(amplitudes) / len(amplitudes)
        min_amplitude = min(amplitudes)
        max_amplitude = max(amplitudes)

        # Store results clearly
        analysis_results.append({
            'patient_id': patient_id,
            'diagnosis': diagnosis,
            'start_time': start_time,
            'average_amplitude': avg_amplitude,
            'min_amplitude': min_amplitude,
            'max_amplitude': max_amplitude
        })

# Convert results to DataFrame and save as CSV
df_results = pd.DataFrame(analysis_results)
df_results.to_csv('xml_analysis_results_detailed.csv', index=False)

print(df_results)
