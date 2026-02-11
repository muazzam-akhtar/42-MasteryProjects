import argparse
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def plot_scatter(df: pd.DataFrame, target_label: str,
                 feature1: str, feature2: str):
    plt.figure(figsize=(8, 8))
    sns.scatterplot(
        data=df,
        x=feature1,
        y=feature2,
        hue=target_label,
        legend='auto'
    )
    plt.title("Scatter plot by house")
    plt.legend(
        loc='upper center',
        bbox_to_anchor=(0.9, 1.15),
        ncol=2,
        title=target_label
    )
    plt.show()


def main():
    parser = argparse.ArgumentParser(description="Scatter plot for dataset")
    parser.add_argument("filename", help="Path to CSV dataset")
    parser.add_argument("feature1", help="First feature/column to plot")
    parser.add_argument("feature2", help="Second feature/column to plot")
    args = parser.parse_args()

    try:
        # Load dataset
        df = pd.read_csv(args.filename)

        # Assuming the dataset has a target column like 'Hogwarts House'
        # Adjust to your dataset column
        if 'Hogwarts House' not in df.columns:
            raise ValueError('Missing Hogwarts House Column')
        targetLabel = ('Hogwarts House')

        print(f"Scatter plot for {args.filename}")
        print(f"Features: {args.feature1} vs {args.feature2}")

        plot_scatter(df, targetLabel, args.feature1, args.feature2)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    main()
