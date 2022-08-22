#txtreader.py
import sys
import numpy as np
import statistics as stats
import math
import os

print("""  _                        _
 |_) ._ _ _|_  _  o ._    |_) ._ _        _  _  ._
 |   | (_) |_ (/_ | | |   |_) | (_) \/\/ _> (/_ |
                                                     """)

argument_list = sys.argv[1:]

filename = "0"
output_name = "0"

try:
    for arg in argument_list:
        if arg in ("-h"):
            print("\nUsage: peptalk [option] -i [input file] -o [output file] -p [JSON params file]")
            print("\nOptions and arguments: \n-h\t: print the usage manual\n-i\t: name of the input file (currently tab-delimited text only)\n-o\t: name of the output file\n-p\t: path to a JSON custom analysis parameters file\n-v\t: verbose output\n-c\t: parse a cysteine reactivity file")
            quit()
        if arg in ("-o"):
            for i in range(len(argument_list)):
                if argument_list[i] == "-o":
                    output_name = argument_list[i+1]
        if arg in ("-i"):
            for i in range(len(argument_list)):
                if argument_list[i] == "-i" and i != len(argument_list):
                    filename = argument_list[i+1]
        #elif curr_arg in ("-p"):
        #elif curr_arg in ("-v"):
        #elif curr_arg in ("-c"):
except:
    print("Could not load arguments")
    quit()

if filename == "0":
    print("\nInput file name not provided\n")
    quit()

if output_name == "0":
    print("\nOutput file name not provided\n")
    quit()

sheet = open(filename, "r")
text = sheet.read()

proteins = []

text_stripped = text.replace('"','')
sheet2 = open(filename, "w")
sheet2.write(text_stripped)
sheet2.close()
#program throws an error when [], #, are present within the header - square brackets must be escaped as they are used for list declaration and cannot be used inside a list.
header = "Proteins Unique Sequence ID, Protein FDR Confidence: Combined, Score Sequest HT: Sequest HT, Accession, Description, MW, Peptides, PSMs, Abundance1, Abundance2, Abundance3, Abundance4"

accession_data = np.genfromtxt(filename, skip_header=1, names=header, delimiter="\t", usecols=("Accession"), encoding=None, dtype=None)
description_data = np.genfromtxt(filename, skip_header=1, names=header, delimiter="\t", usecols=("Description"), encoding=None, dtype=None)
mw_data = np.genfromtxt(filename, skip_header=1, names=header, delimiter="\t", usecols=("MW"), encoding=None, dtype=None)
peptide_data = np.genfromtxt(filename, skip_header=1, names=header, delimiter="\t", usecols=("Peptides"), encoding=None, dtype=None)
psm_data = np.genfromtxt(filename, skip_header=1, names=header, delimiter="\t", usecols=("PSMs"), encoding=None, dtype=None)
ratio_data = np.genfromtxt(filename, skip_header=1, names=header, delimiter="\t", usecols=("Abundance1", "Abundance2", "Abundance3", "Abundance4"), encoding=None, dtype=None)

medians = []
lens = []
for i in range(len(ratio_data[0])):
    counter = 0
    arr = []
    for j in range(len(ratio_data)):
        if np.isnan(ratio_data[j][i]) == False:
            counter += 1
            arr.append(ratio_data[j][i])
    medians.append(stats.median(arr))
    lens.append(counter)
#Could nans be messing up the data?

class Protein:
    def __init__(self, accession, description, mw, peptides, PSMs, ratios_raw):
        self.accession = accession.tolist()
        self.description = description.tolist()
        self.peptides = peptides.tolist()
        self.PSMs = PSMs.tolist()
        self.mw = mw.tolist()
        self.ratios_raw = ratios_raw
        self.ratios_corrected = ratios_raw
        self.rraw = ratios_raw.tolist()

    def N(self):
        n = 0
        for i in range(len(self.ratios_raw)):
            if np.isnan(self.ratios_raw[i]) == False:
                n += 1
        return n

    def correction(self):
        #print(self.ratios_raw)
        for i in range(len(self.ratios_raw)):
                if self.ratios_raw[i] == 6.64:
                    self.ratios_corrected[i] = 6.64
                elif self.ratios_raw[i] == -6.64:
                    self.ratios_corrected[i] = -6.64
                elif np.isnan(self.ratios_raw[i]):
                    self.ratios_corrected[i] = 'nan'
                elif self.ratios_raw[i] > 6.64:
                    self.ratios_corrected[i] = 6.64
                elif self.ratios_raw[i] < -6.64:
                    self.ratios_corrected[i] = -6.64
                else:
                    self.ratios_corrected[i] = self.ratios_raw[i] - medians[i]
        #print(self.ratios_corrected)

    def avg(self):
        sum = 0
        n = self.N()
        for i in self.ratios_corrected:
            if np.isnan(i) == False:
                sum += i
        if n != 0:
            return sum / n
        else:
            return 0

    def std_dev(self):
        self.ratios_notnan = []
        for i in self.ratios_corrected:
            if np.isnan(i) == False:
                self.ratios_notnan.append(i)
        return np.std(self.ratios_notnan)

    def std_error(self):
        self.n = self.N()
        self.dev = self.std_dev()
        return (self.dev / math.sqrt(self.n))

    '''def round(self):
        self.round_raw = []
        self.round_corr = []
        for i in self.rraw:
            self.round_raw.append(round(i, 2))
        self.ratios_corrected = self.ratios_corrected.tolist()
        for i in self.ratios_corrected:
            self.round_corr.append(round(i,2)) '''

    def display(self):
        print('------------------------------\n')
        print('***** PROTEIN DATA *****\n')
        print('Accession number: {}\n'.format(self.accession[0]))
        print('Description: {}\n'.format(self.description[0]))
        print('Molecular weight: {}\n'.format(self.mw[0]))
        print('No. PSMs: {}\n'.format(self.PSMs[0]))
        print('No. peptides: {}\n'.format(self.peptides[0]))
        print('Raw light/heavy ratio values: {}\n'.format(self.rraw))
        print('Corrected light/heavy ratio values: {}\n'.format(self.ratios_corrected))
        print('Average light/heavy ratio value: {}\n'.format(self.avg()))
        print('N-value: {}\n'.format(self.N()))
        print('Standard deviation: {}\n'.format(self.std_dev()))
        print('Standard error: {}\n'.format(self.std_error()))

    def strformat(self):
        self.round_raw = []
        self.round_corr = []
        for i in self.rraw:
            self.round_raw.append(round(i, 2))
        self.ratios_corrected = self.ratios_corrected.tolist()
        for i in self.ratios_corrected:
            self.round_corr.append(round(i,2))
        self.str_rraw_concat = str(self.round_raw)
        self.str_rraw = self.str_rraw_concat.replace(',','\t')
        self.rcorr = self.ratios_corrected
        self.str_rcorr_concat = str(self.round_corr)
        self.str_rcorr = self.str_rcorr_concat.replace(',','\t')
        if np.isnan(self.avg()) == False:
            self.avg_val = str(round(self.avg()))
        else:
            self.avg_val = str(self.avg())
        if np.isnan(self.std_dev()) == False:
            self.std_dev_val = str(round(self.std_dev()))
        else:
            self.std_dev_val = str(self.std_dev())
        if np.isnan(self.std_error()) == False:
            self.std_error_val = str(round(self.std_error()))
        else:
            self.std_error_val = str(self.std_error())
        ls = [str(self.accession[0]), str(self.description[0]), str(round(self.mw[0])), str(self.PSMs[0]), str(self.peptides[0]), self.avg_val, self.std_dev_val, self.std_error_val]
        ls.append(self.str_rraw)
        ls.append(self.str_rcorr)
        string = "\t".join(ls)
        string2 = string.replace('[','')
        string3 = string2.replace(']','')
        return string3

num_rows = accession_data.size
for i in range(num_rows):
    accession = accession_data[i]
    description = description_data[i]
    mw = mw_data[i]
    peptides = peptide_data[i]
    PSMs = psm_data[i]
    ratios_raw = ratio_data[i]

    proteins.append(Protein(accession, description, mw, peptides, PSMs, ratios_raw))

for i in proteins:
    i.correction()
    #i.round()
    i.display()

print("Reading data from file {} ...".format(filename))

print("Median ratio values for raw data: {}".format(medians))
print("Number of valid repeats in each column: {}".format(lens))

print("Output data saved to {}".format(output_name))

handle = open(output_name, 'w')
for i in proteins:
    handle.write(i.strformat())
    handle.write("\n")

#Print out median correction value?
#Implement std/serror calculation
#Print the header line into output files
#Print out avg, stddev, stderror, 3-letter name
#CLI tool
#Load top line from file as header
#Fix floating point issue
#COMMENT
