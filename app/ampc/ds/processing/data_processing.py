import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from app.ampc.ds.common.enums import DatasetExtensionChoices
from app.ampc.ds.common.enums import DelimiterChoices


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

    # NOTE if normalization == True input data is normalized, optional

    if normalization:
        scaler = StandardScaler()
        scaler.fit(X_array)
        X = scaler.transform(X_array)
    else:
        X = X_array

    X_train, X_test, y_train, y_test = train_test_split(X, y_vector, test_size=0.30, random_state=101)
    return {'X_train': X_train, 'X_test': X_test, 'y_train': y_train, 'y_test': y_test}
