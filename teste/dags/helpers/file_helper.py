import os
from datetime import datetime

def copy_to_current_data(source_path: str, dest_path: str):
    """
    Copy csv file to current data folder

    Args:
        source_path (str): csv file source path
        dest_path (str): csv file destiny path
    """
    try:
        # Garantir que o diretório de destino exista
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        with open(source_path, 'r') as src_file:
            with open(dest_path, 'w') as dest_file:
                dest_file.write(src_file.read())
    except Exception as e:
        raise ValueError(f"Error copying data: {e}")