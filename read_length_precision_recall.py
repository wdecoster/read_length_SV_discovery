import pandas as pd
from argparse import ArgumentParser
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def main():
    args = get_args()
    df = pd.read_csv(filepath_or_buffer=args.pr,
                     sep="\t",
                     header=None,
                     names=['caller', 'length', 'precision', 'recall', 'opacity'])

    plt.figure()
    ax = plt.gca()
    for feat in ["precision", "recall"]:
        ax.scatter(x=df['length'],
                   y=df[feat],
                   label=feat,
                   s=3)
    ax.set_xscale('log')
    plt.legend(loc="lower right")
    plt.xlabel("Read length (log-transformed)")
    plt.tight_layout()
    plt.show()
    plt.savefig("length-vs-pr.png")


def get_args():
    parser = ArgumentParser(
        description="Plot precision and recall in function of increasing read length")
    parser.add_argument("pr", help="file with 5 columns, of which 3 and 4 are precision and recall")
    return parser.parse_args()


if __name__ == '__main__':
    main()
