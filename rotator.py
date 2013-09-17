#!/usr/bin/python
#coding=utf-8


import csv
import argparse
import os
from decimal import Decimal
import banner_rotator
import itertools
import string
import random

parser = argparse.ArgumentParser()
parser.add_argument('-f', metavar='DATA_FILE', help="File with banners and their weights. (default: %(default)s)", dest='banners_csv_file', type=argparse.FileType('r'), required=True)
parser.add_argument('-b', metavar='BLOCKS', help="Number of banners to show. It must be less than number of unique banners (default: %(default)s)", dest='blocks', type=int, default=1)
parser.add_argument('-s', metavar='STATISTICS_FILE', help="Calculate statistics for given number of blocks and save to file. ONLY FOR len(banners) * blocks < 100", dest='statistics_csv_file', type=argparse.FileType('w'), required=False)
parser.add_argument('-q', metavar='N', help="Use if needed frequency analysis of choosing k banners; %(metavar)s - number of samples", dest='frequencies_samples_number', type=int, required=False)

args = parser.parse_args()

def generate_banners():
    keys = ["".join(x) for x in itertools.permutations(string.ascii_uppercase, 4)]
    banners = zip(keys, xrange(1, len(keys)))
    with open("./huge_number_of_banners.csv", "wb") as file_with_generated_banners:
        banners_writer = csv.writer(file_with_generated_banners, delimiter=",")
        for row in banners:
            banners_writer.writerow(row)
    return banners
        
if __name__=="__main__":
    banners_reader = csv.reader(args.banners_csv_file, delimiter=",")
    all_banners = [(banner, int(weight)) for banner, weight in banners_reader]
    args.banners_csv_file.close()
    
    if args.blocks < 1:
        print "Wrong blocks size"
        exit(1)
    if  args.blocks > len(all_banners):
        print "Number of blocks bigger than number of unique banners"
        exit(1)

    rotator = banner_rotator.BannerRotator(all_banners)
    print "\nRandom", args.blocks, "banners:" if args.blocks > 1 else "banner:" , "\n", rotator.show_banners(args.blocks)
    
    if args.statistics_csv_file:
        if(len(all_banners) * args.blocks > 100):
            print "Sorry, we can't make statistics for huge number of banners"
            exit(1)
        start_weights = rotator.start_weights_of_show_banners()
        start_probabilities = rotator.start_probabilities_of_show_banners()
        resulted_probabilities = rotator.probabilities_of_show_banners(args.blocks)
        resulted_weights = {k: v/min(resulted_probabilities.values()) for k,v in resulted_probabilities.items()}
        
        statistics_data =  [start_weights, start_probabilities, resulted_probabilities, resulted_weights]
        banners_writer = csv.writer(args.statistics_csv_file, delimiter=",")
        
        if args.frequencies_samples_number:
            frequencies = rotator.frequency_test(args.blocks, args.frequencies_samples_number)        
            statistics_data += [frequencies]
            banners_writer.writerow(["banner","start_weights", "start_probabilities", "resulted_probabilities", "resulted_weights", "frequencies"])
        else:
            banners_writer.writerow(["banner","start_weights", "start_probabilities", "resulted_probabilities", "resulted_weights"])
            
        statistics = []
        precision = Decimal('.0000')
        for banner_name in [banner_name for banner_name, weight in all_banners]:
            statistics += [[banner_name] + list( Decimal(dictionary[banner_name]).quantize(precision).normalize() for dictionary in statistics_data)]

        for row in statistics:
            banners_writer.writerow(row)
        args.statistics_csv_file.close()