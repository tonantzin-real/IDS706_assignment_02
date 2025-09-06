import pandas as pd
import matplotlib.pyplot as plt
from pandas import DataFrame


def read_file(file_path: str) -> DataFrame:
    """Reads a .csv or .parquet file, print its size and a head
        and cleans column names"""
    file_extension = file_path.split(".")[-1]
    if file_extension == "csv":
        df = pd.read_csv(file_path, encoding='utf-16le', sep='\t', low_memory=False)
    elif file_extension == "parquet":
        df = pd.read_parquet(file_path)
    else:
        raise ValueError(
            f"The extension can only be .csv or .parquet and it is {file_extension}"
        )
    print(f"Size: {df.shape}")
    print(df.head().to_string())
    return df


def preprocess_column_names(df: DataFrame) -> DataFrame:
    """Reads a dataframe and cleans the column names """
    print(f"Original column names: {df.columns}")
    df.columns = df.columns.str.strip().str.replace('(', '').str.replace(')', '').str.replace(' ', '_')
    print(f"\nPreprocessed column names: {df.columns}")
    print(f"\nThere are {len(df.columns)} columns\n")
    print(df.info())
    return df


def missing_values(df: DataFrame, column:str) -> DataFrame:
    """Returns the percentage of missing values for a given column
        and imputes them with 'MISSING' if the dtype is object or -1 otherwise"""
    if df[column].dtype == 'object':
        imput = 'MISSING'
    else:
        imput = -1
    n = df.shape[0]
    missing_vals = df[column].isna().sum()
    print(f'{missing_vals/n:.2}% are missing values')
    df[column] = df[column].fillna(imput)
    assert df[column].isna().sum() == 0
    return df

def preprocess_dataframe(df: DataFrame) -> DataFrame:
    """For a given dataframe it cleans the column names, fills in the missing values,
        describes its values, and checks that there're no duplicates"""
    df = preprocess_column_names(df)
    for col in df.columns:
        print(f'\n{col}')
        df = missing_values(df=df, column=col)
        print(df[col].describe())
    assert df.duplicated().sum() == 0
    return df


def describe_column(df: DataFrame, column:str) -> str:
    """Describes a column's distribution"""
    return df[column].describe()



if __name__ == "__main__":
    file_path = "./data/2018_2025_Employer_Information.csv"
    df = read_file(file_path)
    df = preprocess_dataframe(df) # Only a very small % of the columns have missing values
    import pdb;pdb.set_trace()

    # df['Petitioner State'].hist(bins=10)  # Adjust bins as needed
    # plt.xlabel('Value')
    # plt.ylabel('Frequency')
    # plt.title('Histogram of your_column')
    # plt.show()


    # df['Fiscal Year   '].hist(bins=10)  # Adjust bins as needed
    # plt.xlabel('Value')
    # plt.ylabel('Frequency')
    # plt.title('Histogram of your_column')
    # plt.show()