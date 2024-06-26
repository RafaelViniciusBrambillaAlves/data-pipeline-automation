import os
import shutil
from datetime import datetime, timedelta

def is_valid_date_format(name):
    try:
        datetime.strptime(name, '%Y%m%d')
        return True
    except ValueError:
        return False

def organize_csv_and_metrics(directory):
    """
    Organiza os arquivos com base na Data atual e nome da tabela.

    Args:
        directory (str): Diretório onde os arquivos CSV estão localizados.
    """

    # Obtém a data de hoje no formato YYYYMMDD
    today_date = datetime.today().strftime('%Y%m%d')
    today_date = (datetime.today() + timedelta(days=1)).strftime('%Y%m%d')

    # Diretório de destino para os arquivos de hoje
    today_directory = os.path.join(directory, today_date)
    os.makedirs(today_directory, exist_ok=True)

    # Lista todos os arquivos no diretório que não são diretórios com nomes no formato de data
    files_and_dirs = os.listdir(directory)
    files = [f for f in files_and_dirs if os.path.isfile(os.path.join(directory, f)) and not is_valid_date_format(f)]

    if files:
        for file in files:
            src = os.path.join(directory, file)
            dest = os.path.join(today_directory, file)

            # Move o arquivo para o destino (substitui se existir)
            shutil.move(src, dest)

        # Remove o diretório original, se estiver vazio
        if not os.listdir(directory):
            os.rmdir(directory)
    else:
        print("Nenhum arquivo para mover.")

if __name__ == "__main__":
    # Diretório a ser organizado
    directory_to_organize = "/project/data/not-process"
    organize_csv_and_metrics(directory_to_organize)
