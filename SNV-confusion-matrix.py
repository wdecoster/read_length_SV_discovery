from argparse import ArgumentParser
from cyvcf2 import VCF
import pandas as pd


def main():
    args = get_args()
    confusion_matrix(args.vcf)


def confusion_matrix(vcff):
    """
    First level of the dict is the "first" call, second level is the "second" sample
    0: hom_ref
    1: heterozygous
    2: unknown/nocall
    3: hom_alt
    """
    zygosities = {0: {0: 0, 1: 0, 2: 0, 3: 0},
                  1: {0: 0, 1: 0, 2: 0, 3: 0},
                  2: {0: 0, 1: 0, 2: 0, 3: 0},
                  3: {0: 0, 1: 0, 2: 0, 3: 0},
                  }
    for v in VCF(vcff):
        zygosities[v.gt_types[0]][v.gt_types[1]] += 1
    zygs = [2, 0, 1, 3]
    df = pd.DataFrame(index=zygs, columns=zygs)
    for tr in zygs:
        for te in zygs:
            df.loc[tr, te] = zygosities[tr][te]
    df.columns = ['nocall', 'hom_ref', 'het', 'hom_alt']
    df.index = ['nocall', 'hom_ref', 'het', 'hom_alt']
    print(df)


def get_args():
    parser = ArgumentParser(description="Create confusion matrix of SNV calls")
    parser.add_argument("vcf", help="vcf containing two samples")
    return parser.parse_args()


if __name__ == '__main__':
    main()
