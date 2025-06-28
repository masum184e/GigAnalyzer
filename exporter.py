import pandas as pd
from typing import List, Dict, Any
from datetime import datetime
from processor import DataProcessor
import json
import os
import config
import shutil


class DataExporter:
    def __init__(self, processor: DataProcessor):
        self.processor = processor
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        self._clear_output_dir()
        os.makedirs(config.OUTPUT_DIR, exist_ok=True)
    
    def export_to_excel(self, filename: str = None) -> str:
        if filename is None:
            filename = f"gig_analysis_{self.timestamp}.xlsx"
        
        filepath = os.path.join(config.OUTPUT_DIR, filename)

        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            df = self.processor.get_dataframe()
            df.to_excel(writer, sheet_name='Gig_Data', index=False)
            
        return filepath

    def export_text_reports(self, filename: str = None) -> List[str]:
        if filename is None:
            filename = f"unique_tags_{self.timestamp}.txt"
    
        filepath = os.path.join(config.OUTPUT_DIR, filename)

        unique_tags = sorted(self.processor.get_unique_tags())
        report = ",".join(unique_tags)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report)

        return [filepath]

    def _clear_output_dir(self):
        for filename in os.listdir(config.OUTPUT_DIR):
            filepath = os.path.join(config.OUTPUT_DIR, filename)
            try:
                if os.path.isfile(filepath) or os.path.islink(filepath):
                    os.unlink(filepath)
                elif os.path.isdir(filepath):
                    shutil.rmtree(filepath) 
            except Exception as e:
                print(f"Failed to delete {filepath}: {e}")