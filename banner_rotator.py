import random
import numpy
import itertools

import structure

class BannerRotator:
    def __init__(self, banners):
        self.banners = banners
        self.banners_tree = structure.IntervalsTree([weight for (banner, weight) in banners])
        
    def swap(self, i, j):
        self.banners[i], self.banners[j] = self.banners[j], self.banners[i]
        self.banners_tree.swap(i, j)
        
    def show_banners(self, k):
        sum_weights = self.banners_tree.get_sum()
        uniq_banners_total = len(self.banners)
        banners_to_show = [0]*k
        
        for i in xrange(k):
            generated_number = random.random() * sum_weights
            #interval = self.find_interval_naive(generated_number)
            interval = self.banners_tree.find_interval(generated_number)
            value, weight = self.banners[interval]
            self.swap(interval, uniq_banners_total - 1)
            uniq_banners_total -= 1
            sum_weights -= weight
            banners_to_show[i] = value
            
        return banners_to_show
    
    def find_interval_naive(self, value):
        sum = 0
        for i in range(len(self.banners)):
            sum += self.banners[i][1]
            if(sum >=value):
                return i
    
    def __probabilities_of_banners(self, banners):
        total_weight = sum(weight for (value, weight) in banners)
        return [float(weight)/total_weight for (value, weight) in banners]
        
    def __probability_of_show_banner(self, banners, target_banner_index, k_blocks):
        if len(banners) == 0 or k_blocks == 0:
            return 0

        probabilities_of_banners = self.__probabilities_of_banners(banners)
        total_probability_of_show_banner = probabilities_of_banners[target_banner_index]
        
        for other_banner_index in xrange(len(banners)):
            if other_banner_index != target_banner_index:
                shifted_target_banner_index = target_banner_index
                if(other_banner_index < shifted_target_banner_index):
                    shifted_target_banner_index -= 1
                
                prob_select_another_banner_first = probabilities_of_banners[other_banner_index] * self.__probability_of_show_banner(banners[0:other_banner_index] + banners[other_banner_index+1:], shifted_target_banner_index, k_blocks-1)
                total_probability_of_show_banner += prob_select_another_banner_first
                
        return total_probability_of_show_banner
              
    def probabilities_of_show_banners(self, k_blocks):
        probabilities = [0]*len(self.banners)
        
        for banner_index in xrange(len(self.banners)):
            probabilities[banner_index] = self.__probability_of_show_banner(self.banners, banner_index, k_blocks)
            
        return dict(zip([banner for (banner, _ ) in self.banners], probabilities))
    
    def start_probabilities_of_show_banners(self):
        return self.probabilities_of_show_banners(1)
    
    def start_weights_of_show_banners(self):
        return dict(self.banners)
    
    def frequency_test(self, k_blocks, amount_of_sampling):
        frequencies = {banner: 0 for banner, weight in self.banners}
        
        for _ in xrange(amount_of_sampling):
            sampled_banners = self.show_banners(k_blocks)
            for banner in sampled_banners:
                frequencies[banner] += 1
                
        return {banner: float(frequency)/amount_of_sampling for banner, frequency in frequencies.items()}
        