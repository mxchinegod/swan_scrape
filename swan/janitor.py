import os, csv, chardet, docx, PyPDF2, multiprocessing, ast
import xml.etree.ElementTree as ET
from io import BytesIO
from tqdm import tqdm
from bs4 import BeautifulSoup
from .fancy_print import _f

class Janitor:
    def __init__(self, data=None):
        self.data = data 
        _f('fatal', 'no data passed to clean') if data is None else None

    def get_directory_size(directory):
        total_size = 0
        for path, dirs, files in os.walk(directory):
            for file in files:
                filepath = os.path.join(path, file)
                total_size += os.path.getsize(filepath)
        return total_size
    
    def calculate_directory_sizes(directories):
        sizes = {}
        for directory in directories:
            if os.path.isdir(directory):
                size_bytes = get_directory_size(directory)
                size_gb = size_bytes / (1024 ** 3)  # Convert bytes to GB
                sizes[directory] = size_gb
            else:
                print(f"Directory '{directory}' does not exist.")
        return sizes
    
    def remove_html_tags(text):
        soup = BeautifulSoup(text, 'html.parser')
        text_without_tags = soup.get_text(separator=' ')
        return text_without_tags
    
    def xml_to_string(xml_data):
        root = ET.fromstring(xml_data)
        result = ""
        for element in root.iter():
            if element.text and element.tag:
                try:
                    result += f"{element.tag.split('}')[1]}: {element.text}\n"
                except:
                    result += f"{element.tag}: {element.text}\n"
        return remove_html_tags(result)
    
    def process_xml_html(file, file_path):
        with open(file_path, 'rb') as f:
            raw_data = f.read()
            encoding = chardet.detect(raw_data)['encoding']
            if encoding is None:
                encoding = 'utf-8'
            try:
                if file.endswith('.xml'):
                    text = xml_to_string(raw_data.decode(encoding))
                else:
                    text = raw_data.decode(encoding, errors='replace')
                if not text.startswith('linkbase:'):
                    return remove_html_tags(text)
            except Exception as e:
                print(f'markup: {e} | {file}')