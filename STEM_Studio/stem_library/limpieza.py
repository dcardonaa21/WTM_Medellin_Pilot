import pandas as pd
import pathlib 
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
    save_path = pathlib.Path(save_path)
    for key in data_dict.keys():
        data_dict[key].to_csv(save_path / key + ".csv", index=False)
    return 

def download_data(destination_folder):
    """
    Define donde se guardan los datos
    url: string que contiene el sitio web fuente del archivo
    destination_folder: string que contiene la ruta relativa de la carpeta en la que se quiere guardar el archivo
    """
    url = "https://github.com/colombia-dev/data/raw/master/salaries/2020/raw.csv"
    location_path = pathlib.Path(destination_folder)
    location_path.mkdir(exist_ok=True)
    r=requests.get(url, allow_redirects=True)
    name_file= url[url.rfind('/')+1::]
    location_file = location_path.joinpath(name_file)
    with open(location_file, 'wb') as f:
        f.write(r.content)
    return str(location_file)        