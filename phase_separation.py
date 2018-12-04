from Bio import SeqIO
import sys

with open("phase0.fasta", 'w') as phase0, open("phase1.fasta", 'w') as phase1:
    for record in SeqIO.parse(sys.argv[1], "fasta"):
        if record.id.endswith('0'):
            phase0.write(record.format("fasta"))
        elif record.id.endswith('1'):
            phase1.write(record.format("fasta"))
        else:
            print(record.id)
