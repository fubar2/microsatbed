## microsatellites to bed features

### July 11 2024 for the VGP

This code will soon become a Galaxy tool, for building some of the [NIH MARBL T2T assembly polishing](https://github.com/marbl/training) tools as Galaxy workflows.

 
 See https://pytrf.readthedocs.io/en/latest/ for the pytrf documentation. Definition is quoted here:

   *A Tandem repeat (TR) in genomic sequence is a set of adjacent short DNA sequence repeated consecutively. The core sequence or repeat unit is generally called motif. 
   According to the motif length, tandem repeats can be classified as microsatellites and minisatellites. Microsatellites are also known as simple sequence repeats (SSRs) 
   or short tandem repeats (STRs) with motif length of 1-6 bp. Minisatellites are also sometimes referred to as variable number of tandem repeats (VNTRs) has longer motif length than microsatellites.*

Pytrf is a lightweight Python C extension for identification of tandem repeats. The pytrf enables to fastly identify both exact or perfect SSRs.
It also can find generic tandem repeats with any size of motif, such as with maximum motif length of 100 bp. Additionally, it has capability of finding approximate or imperfect tandem repeats. 

A fasta file must be supplied for processing.

Different subsets of STR may be selected for output. Perfect STRs are the default, but any combination with one or more of pefect, approxinate and generic.
  
Designed to build some of the microsatellite tracks from https://github.com/arangrhie/T2T-Polish/tree/master/pattern for the VGP.
 