import pysam
import pandas as pd
from itertools import chain
import sys


class Variant():
    def __init__(self, chromosome, begin, end, svtype):
        self.chromosome = chromosome
        self.begin = begin
        self.id = '.'
        self.ref = 'N'
        self.qual = 0
        self.filter = "PASS"
        self.end = end
        self.svtype = svtype
        self.alt = "<{}>".format(self.svtype)
        self.svlen = -(self.end - self.begin) if self.svtype == "DEL" else self.end - self.begin

    def __str__(self):
        columns = [str(a) for a in [self.chromosome, self.begin, self.id,
                                    self.ref, self.alt, self.qual, self.filter]]
        info = dict(SVLEN=self.svlen,
                    END=self.end,
                    SVTYPE=self.svtype)
        return "{columns}\t{info}\t{vformat}\t{sample}".format(
            columns='\t'.join(columns),
            info=';'.join(["{}={}".format(k, v) for k, v in info.items()]),
            vformat='GT',
            sample="0/1"
        )


def extract_from_record(alignment):
    if alignment.is_reverse:
        cigarstart = alignment.cigartuples[-1][1] if alignment.cigartuples[-1][0] in [4, 5] else 0
    else:
        cigarstart = alignment.cigartuples[0][1] if alignment.cigartuples[0][0] in [4, 5] else 0
    return [
        alignment.query_name, alignment.reference_name, alignment.reference_start,
        alignment.reference_end, cigarstart, alignment.is_reverse, ]


def alignment_to_vars(df):
    variants = []
    for chrom in df["chromosome"].unique():
        df_chrom = df.loc[df["chromosome"] == chrom]
        if len(df_chrom["is_reverse"].unique()) == 1:
            variants.extend(linear_alignment_to_variants(df_chrom.sort_values(by="cigarstart")))
        else:
            variants.extend(alignment_with_inversion(df_chrom.sort_values(by="cigarstart")))
    return variants


def linear_alignment_to_variants(df):
    """For a linear series of alignments, call variants based on gaps"""
    variants = []
    for breakpoint in get_breakpoints(df):
        if breakpoint[1] > breakpoint[0]:  # no overlaps
            variants.append(Variant(chromosome=df["chromosome"].unique()[0],
                                    begin=breakpoint[0],
                                    end=breakpoint[1],
                                    svtype="DEL")
                            )
        else:
            sys.stderr.write("Alignment with overlaps at {} < {}\n".format(
                breakpoint[1], breakpoint[0]))
    return variants


def get_breakpoints(df):
    starts_and_ends = list(
        chain(*df[['ref_start', 'ref_end']].itertuples(index=False, name=None)))[1:-1]
    return list(zip(starts_and_ends[0::2], starts_and_ends[1::2]))


def alignment_with_inversion(df):
    variants = []
    if inversion_is_contained(df):
        for inv_start, inv_end in get_inversion_breakpoints(df):
            variants.append(Variant(chromosome=df["chromosome"].unique()[0],
                                    begin=inv_start,
                                    end=inv_end,
                                    svtype="INV")
                            )
    else:
        sys.stderr.write("Inversion not resolved!\n")
    for linear_chain in break_chains(df):
        variants.extend(linear_alignment_to_variants(linear_chain))
    return variants


def inversion_is_contained(df):
    """Check if inversion is entirely in read and we can thus identify two breakpoints"""
    return True if df["is_reverse"].iloc[0] == df["is_reverse"].iloc[-1] else False


def get_inversion_breakpoints(df):
    breakpoints = []
    last_direction = df["is_reverse"].iloc[0]
    for index, direction in enumerate(df["is_reverse"]):
        # a change in direction which is not a change back to the normal
        if direction != last_direction and direction != df["is_reverse"].iloc[0]:
            breakpoints.append(list(df.iloc[index][["ref_start"]]))
        # a change in direction which is a change back to the normal
        if direction != last_direction and direction == df["is_reverse"].iloc[0]:
            breakpoints[-1].append(df.iloc[index - 1]["ref_end"])
        last_direction = direction
    return breakpoints


def break_chains(df):
    """Break a non-linear alignment in linear parts"""
    dataframes = []
    last_direction = df["is_reverse"].iloc[0]
    initial_index = 0
    for index, direction in enumerate(df["is_reverse"]):
        if direction != last_direction:
            dataframes.append(df.iloc[initial_index:index])
            initial_index = index
        last_direction = direction
    else:
        dataframes.append(df.iloc[initial_index:])
    return dataframes


def main():
    bam = pysam.AlignmentFile(sys.argv[1], "rb")
    df = pd.DataFrame(
        data=[extract_from_record(alignment) for alignment in bam],
        columns=["name", "chromosome", "ref_start", "ref_end", "cigarstart", "is_reverse", ])
    variants = list(chain(*[alignment_to_vars(df[df["name"] == read])
                            for read in df["name"].unique()]))
    print("""##fileformat=VCFv4.2""")
    print("""##source=SVs_from_split_contig_alignments.py from wdecoster""")
    for line in open("GRCh38.fa.fai"):
        print("""##contig=<ID={},length={}>""".format(line.split('\t')[0], line.split('\t')[1]))
    print("""##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">""")
    print("""##INFO=<ID=SVLEN,Number=1,Type=Integer,Description="Length of SV">""")
    print("""##INFO=<ID=END,Number=1,Type=Integer,Description="End coordinate of SV">""")
    print("""##INFO=<ID=SVTYPE,Number=1,Type=String,Description="Type of SV">""")
    print("{}".format("\t".join(['#CHROM', 'POS', 'ID', 'REF',
                                 'ALT', 'QUAL', 'FILTER', 'INFO', 'FORMAT', 'SAMPLE'])))
    for v in variants:
        print(v)


if __name__ == '__main__':
    main()
