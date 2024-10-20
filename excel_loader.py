import pandas as pd

class ExcelLoader:
    def __init__(self, file_path):
        self.file_path = file_path

    def load_data(self, sheet_name, has_header=True):
        try:
            if has_header:
                return pd.read_excel(self.file_path, sheet_name=sheet_name)
            else:
                return pd.read_excel(self.file_path, sheet_name=sheet_name, header=None)  # No header
        except Exception as e:
            print(f"Error loading Excel file: {e}")
            return None
