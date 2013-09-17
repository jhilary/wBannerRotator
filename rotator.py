#!/usr/bin/python
#coding=utf-8


import csv
import argparse
import os
from decimal import Decimal
import banner_rotator

parser = argparse.ArgumentParser()
parser.add_argument('-f', metavar='DATA_FILE', help="File with banners and their weights", dest='banners_csv_file', type=argparse.FileType('r'), required=True)
parser.add_argument('-b', metavar='BLOCKS', help="Number of banners to show. It must be less than number of unique banners (default: %(default)s)", dest='blocks', type=int, default=1)
parser.add_argument('-s', metavar='STATISTICS_FILE', help="Calculate statistics for given number of blocks and save to %(metavar)s", dest='statistics_csv_file', type=argparse.FileType('w'), required=False)

args = parser.parse_args()
    
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

    #print "Banners:\n", all_banners
    rotator = banner_rotator.BannerRotator(list(all_banners))
    print "\nRandom", args.blocks, "banners:" if args.blocks > 1 else "banner:" , "\n", rotator.show_banners(args.blocks)
    
    if args.statistics_csv_file:
        
        start_weights = rotator.start_weights_of_show_banners()
        start_probabilities = rotator.start_probabilities_of_show_banners()
        probabilities = rotator.probabilities_of_show_banners(args.blocks)
        frequencies = rotator.frequency_test(args.blocks)        
        
        statistics_data =  (start_weights, start_probabilities, probabilities, frequencies)
        statistics = []
        precision = Decimal('.0000')
        for banner_name in [banner_name for banner_name, weight in all_banners]:
            statistics += [[banner_name] + list( Decimal(dictionary[banner_name]).quantize(precision).normalize() for dictionary in statistics_data)]

        banners_writer = csv.writer(args.statistics_csv_file, delimiter=",")
        banners_writer.writerow(["banner","start_weights", "start_probabilities", "probabilities", "frequencies"])
        for row in statistics:
            banners_writer.writerow(row)
        args.statistics_csv_file.close()