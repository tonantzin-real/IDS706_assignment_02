import pandas as pd
import matplotlib.pyplot as plt
from pandas import DataFrame
import seaborn as sns
from typing import List


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


def groupby_information(df: DataFrame, groupby_col: List[str], aggregate_cols: List[str]) -> DataFrame:
    """Returns a dataframe that has aggregated information given a certain grouped column"""
    return df.groupby(groupby_col)[aggregate_cols].sum()


def plot_rate(df: DataFrame, x_col:str, y_col:str, save_path:str) -> str:
    """Plots a variable's rate"""
    save_path = save_path + f'lineplot_rate_{y_col}.png'
    sns.lineplot(x=df[x_col], y=df[y_col], marker='o', color='g', linestyle='-', linewidth=2)
    plt.title(f'{y_col} by {x_col}')
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.xticks(df[x_col])
    plt.grid(True)
    plt.savefig(save_path, format='png', bbox_inches='tight')


if __name__ == "__main__":
    file_path = "./data/2022_2025_Employer_Information.csv"
    save_path = "./img/"
    df = read_file(file_path)
    df = preprocess_dataframe(df) # Only a very small % of the columns have missing values

    # We create a new variable based on the Industry_NAICS_Code
    df['NAICS_Code'] = df['Industry_NAICS_Code'].str.split('-').str[0]

    # All the Approval columns are objects but they should be int64
    approval_cols = df.filter(like='Approval').columns.tolist()
    for col in approval_cols:
        df[col] = df[col].astype(str).str.replace(',', '').astype(int)

    # We drop certain columns
    rmv_cols = ['Line_by_line', 'Employer_Petitioner_Name', 'Industry_NAICS_Code'] 
    df_ = df.drop(columns=rmv_cols)

    approval_cols_ = df_.filter(like='Approval').columns.tolist()
    denial_cols_ = df_.filter(like='Denial').columns.tolist()

    print(f'df with original columns: {df.shape}')
    print(f'df with dropped columns: {df_.shape}')

    # How many approvals and denials (new and continuation) were there by year?
    appr_cols = ['New_Employment_Approval', 'Continuation_Approval']
    den_cols = ['New_Employment_Denial', 'Continuation_Denial']

    df_approval_denial = groupby_information(df=df_, 
                                            groupby_col=['Fiscal_Year'], 
                                            aggregate_cols=appr_cols + den_cols) 

    # Total number of new and continuation applications (approvals + denials)
    df_approval_denial['Total_Applications'] = df_approval_denial.sum(axis=1)

    # Calculate the approval rate (approvals / total applications)
    df_approval_denial['Approval_Rate'] = df_approval_denial[appr_cols].sum(axis=1) \
                                            / df_approval_denial['Total_Applications']

    # Display the resulting DataFrame
    df_approval_denial = df_approval_denial.reset_index()
    print(df_approval_denial)

    # Plot the rate
    plot_rate(df=df_approval_denial, x_col='Fiscal_Year', y_col='Approval_Rate', save_path=save_path)


    # How do the approvals and denials look by fiscal year and state?
    df_approval_denial = groupby_information(df=df_, 
                        groupby_col=['Fiscal_Year', 'Petitioner_State'], 
                        aggregate_cols=appr_cols + den_cols)

    # Total number of new and continuation applications (approvals + denials)
    df_approval_denial['Total_Applications'] = df_approval_denial.sum(axis=1)

    # Calculate the approval rate (approvals / total applications)
    df_approval_denial['Approval_Rate'] = df_approval_denial[appr_cols].sum(axis=1) \
                                            / df_approval_denial['Total_Applications']

    # Display the resulting DataFrame
    df_approval_denial = df_approval_denial.reset_index()
    print(df_approval_denial)

    # How does it look for:
    #   North Carolina
    state = 'NC'
    print(state)
    print(df_approval_denial[df_approval_denial.Petitioner_State == state], '\n')

    #   California
    state = 'CA'
    print(state)
    print(df_approval_denial[df_approval_denial.Petitioner_State == state], '\n')

    #   New York
    state = 'NY'
    print(state)
    print(df_approval_denial[df_approval_denial.Petitioner_State == state])



# Modeling

    import pdb;pdb.set_trace()