import pandas as pd # Importing pandas library in the name as pd
import requests # The requests library is used to send HTTP requess in python and helps to interact with web APIs
from io import StringIO # StringIO used to treat a text as file


# function to load data from CSV file
def data_from_csv(filepath, delimiter=';'):
    try:
        df = pd.read_csv(filepath, sep=delimiter)
        print(f"Data loaded successfully! Shape: {df.shape}")
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

# function to load data from excel
def data_from_excel(filepath, s_n=0):
    try:
        df = pd.read_excel(filepath, sheet_name=s_n)
        print(f"Data loaded successfully! Shape: {df.shape}")
        return df
    except Exception as e:
        print(f"Error loading data: {e}")


# function to load data from APIs
def data_from_api(url,params=None, headers=None,to_dataframe=True):
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        content_type = response.headers.get('content-type','')

        # for JSON
        if 'application/json' in content_type:
            d = response.json()
            if to_dataframe:
                try:
                    df = pd.json_normalize(d)
                    print(f"data from json loaded successfully! Shape: {df.shape}")
                    return df
                except Exception as e:
                    print(f"failed to load data from json: {e}")
                    print(f"returning raw data")
                    return d
            else:
                return d
        elif 'text/csv' in content_type:
            if to_dataframe:
                df = pd.read_csv(StringIO(response.text))
                print(f"data from csv loaded successfully! Shape: {df.shape}")
                return df
            else:
                return response.text
        elif 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' in content_type \
         or 'application/vnd.ms-excel' in content_type \
         or url.endswith(('.xlsx', '.xls')):
            if to_dataframe:
                # Convert response content (bytes) to DataFrame
                df = pd.read_excel(BytesIO(response.content))
                print(f"Excel data loaded successfully! Shape: {df.shape}")
                return df
            else:
                return response.text
        else:
            print("return raw text")
            return response.text
    except Exception as e:
        print(f"Error loading data: {e}")
        return None