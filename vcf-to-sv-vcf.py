from cyvcf2 import VCF, Writer
from argparse import ArgumentParser


def main():
    args = get_args()
    vcf_in = VCF(args.vcf)
    vcf_in.add_info_to_header({'ID': 'SVLEN', 'Description': 'length of sv', 'Type': 'Integer', 'Number': '1'})
    vcf_in.add_info_to_header({'ID': 'SVTYPE', 'Description': 'type of sv - just DEL or INS based on SVLEN', 'Type': 'String', 'Number': '1'})
    vcf_out = Writer(args.output, vcf_in)
    for v in vcf_in:
        if abs(len(v.REF) - max([len(alt) for alt in v.ALT])) > 49:
            v.INFO["SVLEN"] = max([len(alt) for alt in v.ALT]) - len(v.REF)
            if v.INFO["SVLEN"] > 0:
                v.INFO["SVTYPE"] = "INS"
            else:
                v.INFO["SVTYPE"] = "DEL"
            vcf_out.write_record(v)
    vcf_in.close()
    vcf_out.close()


def get_args():
    parser = ArgumentParser(
        description="convert a general vcf file to one with only structural variants")
    parser.add_argument("vcf", help="vcf to start from")
    parser.add_argument("output", help="vcf to produce")
    return parser.parse_args()


if __name__ == '__main__':
    main()

