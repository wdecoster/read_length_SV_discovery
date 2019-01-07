import pandas as pd
from argparse import ArgumentParser
from scipy.stats import pearsonr


def main():
    args = get_args()
    df1 = pd.read_csv(filepath_or_buffer=args.pr1,
                      sep="\t",
                      header=None,
                      names=['caller', 'length', 'precision', 'recall', 'opacity'])
    df2 = pd.read_csv(filepath_or_buffer=args.pr2,
                      sep="\t",
                      header=None,
                      names=['caller', 'length', 'precision', 'recall', 'opacity'])
    shared_lengths = set(df1["length"]).intersection(set(df2["length"]))
    for feat in ['precision', 'recall']:
        cc, p = pearsonr(df1[df1["length"].isin(shared_lengths)].sort_values('length')[feat],
                         df2[df2["length"].isin(shared_lengths)].sort_values('length')[feat])
        print("Correlation for {}: {} ; p-value {}".format(feat, cc, p))


def get_args():
    parser = ArgumentParser(
        description="Plot precision and recall in function of increasing read length")
    parser.add_argument(
        "pr1", help="file with 5 columns, of which 3 and 4 are precision and recall")
    parser.add_argument(
        "pr2", help="file with 5 columns, of which 3 and 4 are precision and recall")
    return parser.parse_args()


if __name__ == '__main__':
    main()
