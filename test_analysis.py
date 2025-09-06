import pandas as pd
import os
from analysis import *


def test_read_file():
    """Test if read_file function works correctly"""
    # Create a mock CSV file for testing
    data = {"Column 1 ": [1, 2, 3], "Column 2 aux ": [4, 5, 6]}
    test_file = "test_file.csv"
    df = pd.DataFrame(data)
    df.to_csv(test_file, index=False, sep="\t", encoding="utf-16le")

    df_loaded = read_file(test_file)

    assert df_loaded.shape == (3, 2)
    assert "Column 1 " in df_loaded.columns
    assert "Column 2 aux " in df_loaded.columns

    # Clean up
    if os.path.exists(test_file):
        os.remove(test_file)


def test_preprocess_column_names():
    """Test if preprocess_column_names function cleans column names"""
    df = pd.DataFrame({" Column 1 ": [1, 2, 3], " Column 2 aux ": [4, 5, 6]})
    cleaned_df = preprocess_column_names(df)
    assert cleaned_df.columns.tolist() == ["Column_1", "Column_2_aux"]


def test_missing_values():
    """Test if missing_values function works correctly"""
    df = pd.DataFrame({"Column 1": [1, None, 3], "Column 2": [None, "C", "B"]})

    # Test column 'Column 1'
    df_cleaned = missing_values(df, "Column 1")
    assert df_cleaned["Column 1"].isna().sum() == 0
    assert df_cleaned["Column 1"].iloc[1] == -1  # The 2 value from Column 1 was None

    # Test column 'Column 2'
    df_cleaned = missing_values(df, "Column 2")
    assert df_cleaned["Column 2"].isna().sum() == 0
    assert (
        df_cleaned["Column 2"].iloc[0] == "MISSING"
    )  # The 1 value from Column 2 was None


def test_preprocess_dataframe():
    """Test full preprocessing pipeline"""
    df = pd.DataFrame(
        {
            " Column 1 ": [1, 2, 3],
            " Column 2 aux ": [4, None, 6],
            "Column 3": [None, "C", "B"],
        }
    )
    preprocessed_df = preprocess_dataframe(df)
    assert preprocessed_df["Column_2_aux"].isna().sum() == 0
    assert preprocessed_df["Column_3"].isna().sum() == 0


def test_groupby_information():
    """Test groupby_information function for pandas"""
    df = pd.DataFrame(
        {
            "Fiscal_Year": [2020, 2020, 2021, 2021],
            "New_Employment_Approval": [5, 10, 15, 20],
            "Continuation_Approval": [1, 2, 3, 4],
            "New_Employment_Denial": [0, 0, 1, 1],
            "Continuation_Denial": [0, 0, 0, 0],
        }
    )
    result = groupby_information(
        df,
        groupby_col=["Fiscal_Year"],
        aggregate_cols=[
            "New_Employment_Approval",
            "Continuation_Approval",
            "New_Employment_Denial",
            "Continuation_Denial",
        ],
    )
    assert result.shape == (
        2,
        4,
    )  # Two fiscal years, four aggregated columns, plus the groupby column (this doesn't appear)
    assert "Continuation_Denial" in result.columns
    assert "New_Employment_Approval" in result.columns


def test_groupby_information_polars():
    """Test groupby_information_polars function for polars"""
    df = pd.DataFrame(
        {
            "Fiscal_Year": [2020, 2020, 2021, 2021],
            "New_Employment_Approval": [5, 10, 15, 20],
            "Continuation_Approval": [1, 2, 3, 4],
            "New_Employment_Denial": [0, 0, 1, 1],
            "Continuation_Denial": [0, 0, 0, 0],
        }
    )
    result_pl = groupby_information_polars(
        df,
        groupby_col=["Fiscal_Year"],
        aggregate_cols=[
            "New_Employment_Approval",
            "Continuation_Approval",
            "New_Employment_Denial",
            "Continuation_Denial",
        ],
    )
    assert result_pl.shape == (
        2,
        5,
    )  # Two fiscal years, four aggregated columns, plus the groupby column
    assert "Fiscal_Year" in result_pl.columns
    assert "New_Employment_Approval" in result_pl.columns


# Running the tests
if __name__ == "__main__":
    test_read_file()
    test_preprocess_column_names()
    test_missing_values()
    test_preprocess_dataframe()
    test_groupby_information()
    test_groupby_information_polars()
    print("All tests passed!")
