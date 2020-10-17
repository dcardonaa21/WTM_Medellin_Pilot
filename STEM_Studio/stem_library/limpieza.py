import pandas as pd
from pathlib import Path
import requests

def data_as_df(data_path):
    data_dict = pd.read_excel(data_path, sheet_name=None)
    old_keys = list(data_dict.keys())
    for key in old_keys:
        new_key = key.replace(" ", "_") 
        data_dict[new_key] = data_dict[key]
    for key in old_keys:
        data_dict.pop(key)
    return data_dict

def save_data_as_csv(data_path, save_path):
    data_dict = data_as_df(data_path)
    save_path = Path(save_path)
    for key in data_dict.keys():
        data_dict[key].to_csv(save_path / key + ".csv", index=False)
    return 

def download_data(url, destination_folder):
    # Define dónde se guardan los datos
    # url: string que contiene el sitio web fuente del archivo
    # destination_folder: string que contiene la ruta relativa de la carpeta en la que se quiere guardar el archivo
    r = requests.get(url, allow_redirects=True)
    with open(destination_folder + url[url.rfind('/')+1::], 'wb') as f:
        f.write(r.content)
    return destination_folder+url[url.rfind('/')+1::]