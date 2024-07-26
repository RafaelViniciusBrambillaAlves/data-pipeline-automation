import os
import shutil
from datetime import datetime

def is_valid_date_format(name):
    try:
        datetime.strptime(name, '%Y%m%d')
        return True
    except ValueError:
        return False

def organize_csv_and_metrics(directory):
    """
    Organiza os arquivos com base na Data atual e nome da tabela.
    Copia os arquivos para um diretório 'current_data', substituindo se já existir.

    Args:
        directory (str): Diretório onde os arquivos CSV estão localizados.
    """
    # Obtém a data de hoje no formato YYYYMMDD
    today_date = datetime.today().strftime('%Y%m%d')
    # Diretório de destino para os arquivos de hoje
    today_directory = os.path.join(directory, today_date)
    os.makedirs(today_directory, exist_ok=True)

    # Diretório para 'current-data'
    current_data_directory = os.path.join(directory, "current_data")
    os.makedirs(current_data_directory, exist_ok=True)

    # Lista todos os arquivos no diretório que não são diretórios com nomes no formato de data
    files_and_dirs = os.listdir(directory)
    files = [f for f in files_and_dirs if os.path.isfile(os.path.join(directory, f)) and not is_valid_date_format(f)]

    if files:
        for file in files:
            src = os.path.join(directory, file)
            dest_today = os.path.join(today_directory, file)
            dest_current = os.path.join(current_data_directory, file)

            # Move o arquivo para o diretório de destino com a data de hoje
            shutil.move(src, dest_today)

            # Remove o arquivo antigo em 'current-data' se existir
            if os.path.exists(dest_current):
                os.remove(dest_current)

            # Copia o arquivo movido para o diretório 'current-data'
            shutil.copy(dest_today, dest_current)

        # Remove o diretório original, se estiver vazio
        if not os.listdir(directory):
            os.rmdir(directory)
    else:
        print("Nenhum arquivo para mover.")

if __name__ == "__main__":
    # Diretório a ser organizado
    directory_to_organize = "C:\\project\\data"
    organize_csv_and_metrics(directory_to_organize)
