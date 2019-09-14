import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from app.apmc.ds.common.enums import DatasetExtensionChoices
from app.apmc.ds.common.enums import DelimiterChoices


def load_data(dataset_path):
    """
    Load data in csv, xls or xlsx format as data set for model training
    and evaluation
    """
    if dataset_path.endswith(DatasetExtensionChoices.csv):
        data_set = pd.read_csv(dataset_path, delimiter=DelimiterChoices.comma)
    else:
        data_set = pd.read_excel(dataset_path)

    col_names = data_set.columns
    dim = len(col_names)
    X_columns = col_names[: dim - 1]
    y_column = col_names[-1]

    X_array = np.array(data_set[X_columns])
    y_vector = np.array(data_set[y_column]).ravel()

    return {'X_names': X_columns, 'y_name': y_column, 'X_array': X_array, 'y_vector': y_vector}


def data_set_split(X_array, y_vector, normalization=False):
    """
    User need to determine what are X variables and y in input data set
    bellow is just temporary.
    Temporary solution is that last column in data set is always y-variable
    return dict:{"X_train": self.X_train, "X_test": self.X_test,
    "y_train": self.y_train, "y_test": self.y_test}
    """

    if normalization:
        scaler = StandardScaler()
        scaler.fit(X_array)
        X = scaler.transform(X_array)

        mean_array = scaler.mean_  # data used for scaling user input
        std_array = scaler.scale_
    
    else:
        X = X_array

        mean_array = np.mean(X, axis=0)
        std_array = np.std(X, axis=0)

    X_train, X_test, y_train, y_test = train_test_split(X, y_vector, test_size=0.30, random_state=101)

    return {
        'X_train': X_train,
        'X_test': X_test,
        'y_train': y_train,
        'y_test': y_test,
        'X_mean': mean_array,
        'X_std': std_array,
    }


def extrapolation_risk(X_array, mean_list, std_list, values_to_predict, X_names):
    n_columns = X_array.shape[1]

    input_values = np.reshape(values_to_predict, (n_columns, 1))

    warnings = []
    
    for counter, input_value in enumerate(input_values):
        
        if input_value < (mean_list[counter] - (3 * (std_list[counter]))):
            
            warnings.append(
                f"Risk of extrapolation predictor [{X_names[counter]}] value is SMALLER than 3 std from mean!"
            )

        if input_value > (mean_list[counter] + (3 * (std_list[counter]))):
            
            warnings.append(
                f"Risk of extrapolation predictor [{X_names[counter]}] value is BIGGER than 3 std from mean!"
            )

    return warnings


def prepare_data_for_report(dataset_path):
    if dataset_path.endswith(DatasetExtensionChoices.csv):
        data_set = pd.read_csv(dataset_path, delimiter=DelimiterChoices.comma)
    else:
        data_set = pd.read_excel(dataset_path)

    col_names = list(data_set.columns)
    col_number = len(col_names)

    predictors_names = col_names[: (col_number - 1)]
    classes = list(data_set[col_names[-1]].unique())
    classes = [str(target) for target in classes]

    return {
        'data': data_set,
        'col_names': col_names,
        'col_number': col_number,
        'predictors_names': predictors_names,
        'classes': classes,
    }
