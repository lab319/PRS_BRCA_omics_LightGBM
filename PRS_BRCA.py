import os
import sys
import joblib
import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings("ignore")


def reduce_mem_usage(df, verbose=True):
    """
    Function to reduce the dataframe size
    :param df: dataframe
    :param verbose: bool
    :return: dataframe
    """
    numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
    # memory_usage calculate the bytes of every columns
    start_mem = df.memory_usage().sum() / 1024**2
    for col in df.columns:
        col_type = df[col].dtypes
        if col_type in numerics:
            c_min = df[col].min()
            c_max = df[col].max()
            if str(col_type)[:3] == 'int':
                if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                    df[col] = df[col].astype(np.int8)
                elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
                    df[col] = df[col].astype(np.int16)
                elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                    df[col] = df[col].astype(np.int32)
                elif c_min > np.iinfo(np.int64).min and c_max < np.iinfo(np.int64).max:
                    df[col] = df[col].astype(np.int64)
            else:
                if c_min > np.finfo(np.float16).min and c_max < np.finfo(np.float16).max:
                    df[col] = df[col].astype(np.float16)
                elif c_min > np.finfo(np.float32).min and c_max < np.finfo(np.float32).max:
                    df[col] = df[col].astype(np.float32)
                else:
                    df[col] = df[col].astype(np.float64)
    end_mem = df.memory_usage().sum() / 1024**2
    if verbose: print('Mem. usage decreased to {:5.2f} Mb ({:.1f}% reduction)'.format(end_mem, 100 * (start_mem - end_mem) / start_mem))
    return df


def bio_var_load(bio_var_path):
    """
    Function to load biological variables
    :param bio_var_path: absolute path
    :return: dateframe of biological variables
    """
    try:
        bio_var = pd.read_csv(bio_var_path, index_col=0)
        return bio_var
    except:
        print("There is no biological variables csv file!")
        print("Please check up!")
        sys.exit(1)


def omics_data_load(omics_data_path, axis=2):
    """
    Function to load omics data
    :param omics_data_path: absolute path
    :param axis: options(int) : "1" or "2", "1" represents that each row is a samples, each column is a biological variable
    :return: dataframe of omics data
    """
    if axis == 1:
        try:
            omics_data = pd.read_csv(omics_data_path, index_col=0)
            omics_data = reduce_mem_usage(omics_data, verbose=True)
            return omics_data
        except:
            print("There is no omics data csv file!")
            print("Please check up!")
            sys.exit(1)
    elif axis == 2:
        try:
            omics_data_reader = pd.read_csv(omics_data_path, index_col=0, chunksize = 5000)
            omics_data = pd.DataFrame()
            for chunk in omics_data_reader:
                chunk = reduce_mem_usage(chunk)
                omics_data = pd.concat([omics_data, chunk], axis=0)
                del chunk
            omics_data = pd.DataFrame(omics_data.values.T, index=omics_data.columns, columns=omics_data.index)
            return omics_data
        except:
            print("There is no omics data csv file!")
            print("Please check up!")
            sys.exit(1)
    else:
            print("The is no paramters \"axis:\"" + str(axis))
            sys.exit(1)


def model_load(model_path):
    """
    Function to load model pkl file
    :param model_path: absolute path
    :return: LightGBM model (.pkl)
    """
    try:
        model = joblib.load(model_path)
        return model
    except:
        print("There is no model pkl file!")
        print("Please check up!")
        sys.exit(1)


def check_up_bio_var(omics_data, bio_var):
    """
    Function to check whether the biological variables of the
    input data meet the requirements of the model
    :param omics_data: dateframe of omics data
    :param bio_var: dateframe of biological variables
    :return: omics data with meeting requirements
    """
    bio_var_index = bio_var.index
    bvis = set(bio_var_index)
    omics_data_columns = omics_data.columns
    odcs = set(omics_data_columns)
    if len(odcs) != len(omics_data_columns):
        order = list(odcs)
        omics_data = omics_data[order]
        print("There are repeat biological variables in input data.")
        print("Don`t worry, we will fix it!")
    if bvis.issubset(odcs):
        order = list(bio_var_index)
        omics_data = omics_data[order]
        return omics_data
    else:
        print("The requested biological variables were not found in the input data.")
        print("Please check the biological variables!")
        sys.exit(1)


if __name__ == "__main__":
    # configuration by user
    status = input("Please input the status of BRCA: ")
    while status not in ["case_control", "cancer_stage"]:
        print("Please input the correct status of BRCA.")
        status = input("Please input status of BRCA: ")

    omics = input("Please input the type of omics data of BRCA: ")
    while omics not in ["methylation", "miRNA", "mRNA", "lncRNA"]:
        print("Please input the correct type of omics data of BRCA.")
        omics = input("Please input the type of omics data of BRCA: ")

    # path
    relative_path = os.path.dirname(os.path.realpath(__file__))
    name = "TCGA_BRCA_" + omics + "_lightgbm"
    bio_var_absolute_path = relative_path + "/biological_variables/" + status + "/" + name + ".csv"
    model_absolute_path = relative_path + "/saved_model/" + status + "/" + name + ".pkl"
    input_absolute_path = relative_path + "/input_data/data.csv"
    output_absolute_path = relative_path + "/output_data/" + "TCGA_BRCA_" + status + "_" + omics + "_prs.csv"

    # load data
    bio_var = bio_var_load(bio_var_absolute_path)
    omics_data = omics_data_load(input_absolute_path, axis=2)
    model = model_load(model_absolute_path)

    # check up the biological variables
    omics_data = check_up_bio_var(omics_data, bio_var)

    # prediction
    prs = model.predict(omics_data)
    prs_df = pd.DataFrame(prs, index=omics_data.index, columns=["prs"])
    print(prs_df)

    # output
    prs_df.to_csv(output_absolute_path)
    print("The prs csv file is gengrated in output_data.")