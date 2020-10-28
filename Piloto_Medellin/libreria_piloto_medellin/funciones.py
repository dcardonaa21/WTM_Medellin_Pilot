import pandas as pd
import pathlib 
import requests

def download_data(destination_folder):
    """
    Download graduated students data from 2011 to 2018 into a given destination folder.
    Parameter:
    destination_folder: string that contains the relative path of the folder in which you want to save the excel file.
    Returns:
    string with the location of the folder that contains the excel files.
    """
    url_ls = ["https://storage.googleapis.com/piloto_medellin/GRADUADOS-2001-2017.xlsb", 
    "https://storage.googleapis.com/piloto_medellin/GRADUADOS-2018.xlsx", 
    "https://storage.googleapis.com/piloto_medellin/MATRICULADOS-2014.xlsx", 
    "https://storage.googleapis.com/piloto_medellin/MATRICULADOS-2015.xlsx", 
    "https://storage.googleapis.com/piloto_medellin/MATRICULADOS-2016.xlsx", 
    "https://storage.googleapis.com/piloto_medellin/MATRICULADOS-2017.xlsx", 
    "https://storage.googleapis.com/piloto_medellin/MATRICULADOS-2018.xlsx", 
    "https://storage.googleapis.com/piloto_medellin/MATRICULADOS-HASTA-2013.xlsb"]
    location_path = pathlib.Path(destination_folder)
    location_path.mkdir(exist_ok=True)
    files_ls = []
    
    for url in url_ls:
        r=requests.get(url, allow_redirects=True)
        name_file= url[url.rfind('/') + 1::]
        location_file = location_path.joinpath(name_file)
        with open(location_file, 'wb') as f:
            f.write(r.content)
        files_ls.append(str(location_file))
    return str(files_ls)


def data_as_dfs_dict(data_path):
    """
    Read de location of an excel file as a dictionary whose keys are the names of each sheet of the excel file and whose values are the content of the sheets as dataframes.
    Parameter: 
    data_path: string with the location of the excel file.
    Returns: the dictionary that contains the information of the excel file with modified keys names, where the white spaces are replaced by underscores.
    """
    data_dict = pd.read_excel(data_path, sheet_name=None, engine='pyxlsb')
    old_keys = list(data_dict.keys())
    for key in old_keys:
        new_key = key.replace(" ", "_") 
        data_dict[new_key] = data_dict[key]
    for key in old_keys:
        data_dict.pop(key)
    return data_dict

def save_data_as_csv(data_path, save_path):
    """
    Save each one of the sheets of the excel file as CSV files in the path you give as save_path.
    Parameters: 
    data_path: string with the location of the excel file.
    save_data: string with the path of the file in which you want to save the CSV files.
    """
    data_dict = data_as_dfs_dict(data_path)
    save_path = pathlib.Path(save_path)
    for key in data_dict.keys():
        data_dict[key].to_csv(save_path / key + ".csv", index=False)
    return 