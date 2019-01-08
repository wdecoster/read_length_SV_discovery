from argparse import ArgumentParser
from pyfaidx import Fasta
import gzip
from collections import defaultdict, namedtuple


def main():
    args = get_args()
    genome = Fasta(args.fasta)
    gc_content = defaultdict(list)
    for line in mosdepth_generator(args.mosdepth):
        gc_content[seq_to_gc(genome[line.chr][line.start:line.end].seq.upper())].append(line.cov)
    print(gc_content)


def mosdepth_generator(region_file):
    mosdepth_line = namedtuple('Line', 'chr start end cov')
    for line in gzip.open(region_file, 'rt'):
        yield mosdepth_line(chr=line.split()[0],
                            start=int(line.split()[1]),
                            end=int(line.split()[2]),
                            cov=line.strip().split()[3])


def seq_to_gc(seq):
    return round((seq.count('G') + seq.count('C')) / len(seq))


def get_args():
    parser = ArgumentParser(description="Plot GC content vs coverage")
    parser.add_argument("fasta", help="genome fasta")
    parser.add_argument("mosdepth", help="mosdepth .region.bed.gz file")
    return parser.parse_args()


if __name__ == '__main__':
    main()
