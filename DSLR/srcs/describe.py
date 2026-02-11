from DSLR.math import count, mean, minimum, maximum, std, percentile, cov, var, skew
import pandas as pd
import sys
import os


def load_data(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"The file {path} was not found.")
    df = pd.read_csv(path)
    return df


def statistics(values):
    values = values.dropna()  # remove NaN values
    stats = [
        count(values),
        mean(values),
        std(values),
        minimum(values),
        percentile(values, 0.25),
        percentile(values, 0.5),
        percentile(values, 0.75),
        maximum(values),
        var(values),
        cov(values),
        skew(values)
    ]
    return stats


def describe(df):
    cols_nbrs = df.select_dtypes(include=['number']).columns
    stats_list = [statistics(df[col]) for col in cols_nbrs]
    col_names = ['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max',
                 'Variances', 'COV', 'Skewness']
    describe_df = pd.DataFrame(stats_list, columns=col_names, index=cols_nbrs)
    return describe_df.T


def main():
    if len(sys.argv) != 2:
        print("Usage: python describe.py <dataset_name.csv>")
        sys.exit(1)
    try:
        DATA_FILE_PATH = sys.argv[1]
        df = load_data(DATA_FILE_PATH)
        my_describe_df = describe(df)
        print(f"my describe:\n{my_describe_df}")
        # print(f"original pandas describe:\n{df.describe()}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
