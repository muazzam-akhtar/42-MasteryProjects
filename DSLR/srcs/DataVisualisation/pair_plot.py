import argparse
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def plot_pair(df: pd.DataFrame, targetLabel: str, feature1: str,
              feature2: str, feature3: str, feature4: str):
    plot_df = df[[feature1, feature2, feature3, feature4, targetLabel]]

    sns.pairplot(
        plot_df,
        hue=targetLabel,
        diag_kind='hist',  # histogram on the diagonal
        palette='bright'
    )
    plt.suptitle(
        f"Pair Plot: {feature1} vs {feature2} vs {feature3} vs "
        f"{feature4} by {targetLabel}", y=1.02)

    plt.show()


def main():
    parser = argparse.ArgumentParser(description="Pair plot for dataset")
    parser.add_argument("filename", help="Path to CSV dataset")
    parser.add_argument("feature1", help="First feature / column to plot")
    parser.add_argument("feature2", help="Second feature / column to plot")
    parser.add_argument("feature3", help="Third feature / column to plot")
    parser.add_argument("feature4", help="Fourth feature / column to plot")
    args = parser.parse_args()

    try:
        df = pd.read_csv(args.filename)
        if 'Hogwarts House' not in df.columns:
            raise ValueError('Missing Hogwarts House Column')
        targetLabel = ('Hogwarts House')

        print(f"Pair plot for {args.filename}")
        print(f"Features for {args.feature1} vs {args.feature2}")
        plot_pair(df, targetLabel, args.feature1, args.feature2, args.feature3,
                  args.feature4)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    main()
