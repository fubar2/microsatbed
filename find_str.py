import argparse
import copy

from pyfastx import Fastx  # 0.5.2

import pytrf  # 1.3.0


"""
Allows all STR or those for a subset of motifs to be written to a bed file
Designed to build some of the microsatellite tracks from https://github.com/arangrhie/T2T-Polish/tree/master/pattern for the VGP.
Could make a collection with each of multiple single motif beds, but for first iteration
the downside of discover datasets not being available in workflows makes it useless for this purpose.
"""


def write_ssrs(args):
    """
    The integers in the call change the minimum repeats for mono-, di-, tri-, tetra-, penta-, hexa-nucleotide repeats
    ssrs = pytrf.STRFinder(name, seq, 10, 6, 4, 3, 3, 3)
    but let's just filter here.
    NOTE: STRs with dinucleotides GA and AG are reported separately by https://github.com/marbl/seqrequester.
    The reversed pair STRs are about as common according to the samples shown.
    So, that's what we do here. Only 'GC,AT,GA,TC' are reported in VGP mode.
    """
    beds = {}
    bednames = args.bed.split(',')
    report = args.reportme.lower()
    if report == "all":
        reportMe = "ALL"
        beds["ALL"] = []
    elif report == "vgp":
        reportMe = 'GC,AT,GA,TC'.split(',')
        assert len(bednames) == len(
            reportMe
        ), f"beds={bednames}, motifs={reportMe} - they do not match up - cannot proceed"
        for motif in reportMe:
            beds[motif] = []
    else:
        beds['ALL'] = []
        reportMe = report    
    fa = Fastx(args.fasta, uppercase=True)
    for name, seq in fa:
        trs = []
        if args.perfect:
            trs += pytrf.STRFinder(name, seq)
        if args.approximate:
            trs += pytrf.ATRFinder(name, seq)
        if args.generic:
            trs += pytrf.GTRFinder(name, seq)
        for ssr in trs:
            row = "%s\t%d\t%d\t%s_%d\t%d" % (
                ssr.chrom,
                ssr.start,
                ssr.end,
                ssr.motif,
                ssr.repeat,
                ssr.length,
            )
            if report == "all":
                beds["ALL"].append(row)
            elif report == "vgp" and ssr.motif in reportMe:
                if ssr.motif in reportMe:
                    beds[ssr.motif].append(row)
            elif report == "nomono" and len(ssr.motif) > 1:
                beds["ALL"].append(row)
            elif report == "di" and len(ssr.motif) == 2:
                beds["ALL"].append(row)
            elif report == "tri" and len(ssr.motif) == 3:
                beds["ALL"].append(row)
            elif report == "tetra" and len(ssr.motif) == 4:
                beds["ALL"].append(row)
            elif report == "penta" and len(ssr.motif) == 5:
                beds["ALL"].append(row)
            elif report == "hepta" and len(ssr.motif) == 6:
                beds["ALL"].append(row)
            
    if args.reportme.lower() == "vgp":
        for i, bf in enumerate(bednames):
            bed = beds[reportMe[i]]
            with open(bf, "w") as outbed:
                outbed.write("\n".join(bed))
                outbed.write("\n")
    else:
        bedres = []
        for k in beds:
            if len(beds[k]) > 0:
                bedres += beds[k]
        bedres.sort()
        with open(args.bed, "w") as ob:
            ob.write("\n".join(bedres))
            ob.write("\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    a = parser.add_argument
    a("-p", "--perfect", action="store_true")
    a("-a", "--approximate", action="store_true")
    a("-g", "--generic", action="store_true")
    a("-f", "--fasta", default="mouse5bit.fa")
    a("-b", "--bed", default="mouse.GC.bed,mouse.AT.bed,mouse.GA.bed,mouse.TC.bed")
    a("-r", "--reportme", default="VGP")
    args = parser.parse_args()
    write_ssrs(args)
