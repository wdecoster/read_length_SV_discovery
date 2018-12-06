from argparse import ArgumentParser
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


class Flagstat(object):
    def __init__(self, flagstatfile):
        """
        Not the cleanest approach, probably breaks on slightly different scenarios"""
        self.read_length = int(flagstatfile.split('.')[0].split('-')[1])
        with open(flagstatfile) as flagstatf:
            for line in flagstatf:
                if "total" in line:
                    self.total = int(line.split(' ')[0])
                if "mapped (" in line:
                    self.mapped = int(line.split(' ')[0])
                if "secondary" in line:
                    self.secondary = int(line.split(' ')[0])
                if "supplementary" in line:
                    self.supplementary = int(line.split(' ')[0])
            self.uniquely = self.mapped - self.secondary - self.supplementary
            self.unique_frac = self.uniquely / (self.total - self.secondary - self.supplementary)


def main():
    args = get_args()
    stats = [Flagstat(f) for f in args.flagstat]
    plt.figure()
    ax = plt.gca()
    ax.scatter(x=[s.read_length for s in stats],
               y=[s.unique_frac * 100 for s in stats],
               s=3)
    ax.set_xscale('log')
    plt.xlabel("Read length (log-transformed)")
    plt.ylabel("Percentage of reads uniquely aligned")
    plt.tight_layout()
    plt.savefig("length-vs-uniquely_aligned_fraction.png")


def get_args():
    parser = ArgumentParser(
        description="Plot uniquely aligned fraction for multiple read lengths")
    parser.add_argument("flagstat", nargs="+", help="flagstat output files")
    return parser.parse_args()


if __name__ == '__main__':
    main()
