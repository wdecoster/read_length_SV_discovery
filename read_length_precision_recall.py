import matplotlib.pyplot as plt
import pandas as pd
from argparse import ArgumentParser
import itertools


def main():
    args = get_args()
    df = pd.read_csv(filepath_or_buffer=args.pr,
                     sep="\t",
                     header=None,
                     names=['caller', 'length', 'precision', 'recall', 'F-measure', 'opacity']) \
        .groupby("length").mean()
    plt.figure()
    ax = plt.gca()
    for feat, marker, size in zip(["precision", "recall", "F-measure"],
                                  ['.', 'x', 'D'],
                                  [16, 16, 12]):
        ax.scatter(x=df.index,
                   y=df[feat],
                   label=feat,
                   marker=marker,
                   s=size)
    ax.set_xscale('log')
    plt.legend(loc="lower right")
    plt.xlabel("Read length (log-transformed)")
    plt.ylim(0, 1)
    xlines = [100, 1000, 10000, 100000]
    for xcoord in xlines:
        plt.axvline(xcoord, alpha=0.7, color='grey', linestyle='--', linewidth=0.5)
    for xcoord in itertools.chain.from_iterable([range(i, i * 10, i) for i in xlines]):
        plt.axvline(xcoord, alpha=0.4, color='grey', linestyle='--', linewidth=0.4)
    plt.tight_layout()
    plt.savefig("length-vs-prf.png")


def get_args():
    parser = ArgumentParser(
        description="Plot precision and recall in function of increasing read length")
    parser.add_argument("pr", help="file with 5 columns, of which 3 and 4 are precision and recall")
    return parser.parse_args()


if __name__ == '__main__':
    main()
