import pandas as pd
import pathlib 
import requests

def download_data(destination_folder):
    """
    Download STEM education data into a given destination folder.
    Parameter:
    destination_folder: string that contains the relative path of the folder in which you want to save the excel file.
    Returns:
    string with the location of the excel file.
    """
    url = "https://storage.googleapis.com/piloto_maker_kits/Data_sin_procesar_%3D(/mujeres/Tabla%20de%20STEM%202001-2018%20ET_v2013.xlsx"
    location_path = pathlib.Path(destination_folder)
    location_path.mkdir(exist_ok=True)
    r=requests.get(url, allow_redirects=True)
    name_file= "Tabla_STEM_2001_2018_v2013.xslx"
    location_file = location_path.joinpath(name_file)
    with open(location_file, 'wb') as f:
        f.write(r.content)
    return str(location_file) 

def data_as_dfs_dict(data_path):
    """
    Read de location of an excel file as a dictionary whose keys are the names of each sheet of the excel file and whose values are the content of the sheets as dataframes.
    Parameter: 
    data_path: string with the location of the excel file.
    Returns: the dictionary that contains the information of the excel file with modified keys names, where the white spaces are replaced by underscores.
    """
    data_dict = pd.read_excel(data_path, sheet_name=None)
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

def calligraphy_unification(names_ls):
    """
    Replaces every spanish accentuated vowel by a simple vowel, takes "*" out from the string and turns the strings into uppercase strings.
    Parameters:
    names_ls: List of strings.
    Returns:
    new_names_ls: A list with uppercase clean strings.
    """
    invalid_vowels_dict = {"á":"a", "é":"e", "í":"i", "ó":"o", "ú":"u", "ü":"u", "Á":"A", "É":"E", "Í":"I", "Ó":"O", "Ú":"U", "Ü":"U", "*":"", ","}
    characters_ls = []
    new_characters_ls = []
    "new_names_ls = []"
    names_dict = dict()
    new_name = str()
    for name in names_ls:
        characters_ls = list(name)
        for character in characters_ls:
            if character in invalid_vowels_dict.keys():
                new_char = invalid_vowels_dict[character]
                new_characters_ls.append(new_char)
            else:
                new_characters_ls.append(character)
        new_name = ("".join(new_characters_ls)).upper()
        "new_names_ls.append(new_name)"
        names_dict[name] = new_name
        new_name = str()
        new_characters_ls= []
        characters_ls = []
    return names_dict

def filter_rename_columns(df, columns_names_dict):
    """
    Filter and rename columns that you need in your dataframe.
    Parameters:
    df: Original dataframe with all the columns.
    old_names_ls: List of old dataframe columns names that you want to keep in your dataframe.
    new_names_ls: List of new dataframe columns names that you need.
    Returns:
    filtered_renamed_columns_df : A new dataframe with renamed columns.
    """
    filtered_df = df.filter(columns_names_dict.keys(), axis="columns")
    filtered_renamed_columns_df = filtered_df.rename(columns=columns_names_dict)    
    return filtered_renamed_columns_df

def observation_replace(df_column, orig_obs, new_obs):
    """
    Replaces the value(s) inside a column by new one(s).
    Parameters:
    df_column: Dataframe column that contains the values to be changed.
    orig_obs: string or integer or float or list of observations contained in the dataframe column to be changed.
    new_obs: string or integer or float or list of observations that will replace the original value(s) in the column dataframe.
    Returns:
    The frequency of each value in the modified dataframe column .
    """ 
    replaced_df = df_column.str.replace(orig_obs, new_obs)
    return replaced_df.value_counts()

