import random
import numpy
import itertools
import structure
class BannerRotator:
    def __init__(self, banners):
        self.banners = banners
        self.banners_size = len(banners)
        self.banners_tree = structure.IntervalsTree([weight for (value, weight) in banners])
        
    def swap(self, i, j):
        self.banners[i], self.banners[j] = self.banners[j], self.banners[i]
        self.banners_tree.swap(i, j)
        
    def find_interval_naive(self, value):
        sum = 0
        for i in range(len(self.banners)):
            sum += self.banners[i][1]
            if(sum >=value):
                return i
        
    def show_banners(self, k):
        sum_weights = self.banners_tree.get_sum()
        uniq_banners_total = len(self.banners)
        banners_to_show = [0]*k
        for i in range(k):
            generated_number = random.random() * sum_weights
            interval = self.banners_tree.find_interval(generated_number)
            value, weight = self.banners[interval]
            self.swap(interval, uniq_banners_total - 1)
            uniq_banners_total -= 1
            sum_weights -= weight
            banners_to_show[i] = value
        return banners_to_show
    
    def __probability_of_banner(self, banners, i):
        return float(banners[i][1])/sum([weight for (value, weight) in banners])
        
    def __probability_of_show_banner(self, banners, i, k):
        if len(banners) == 0 or k == 0:
            return 0
        probability = self.__probability_of_banner(banners, i)
        for banner_index in range(len(banners)):
            if banner_index != i:
                new_index = i
                if(banner_index < new_index):
                    new_index-=1
                prob_select_another_banner_first = (self.__probability_of_banner(banners, banner_index)) * self.__probability_of_show_banner(banners[0:banner_index] + banners[banner_index+1:], new_index, k-1)
                probability += prob_select_another_banner_first
        return probability
              
    def probabilities_of_show_banners(self, k):
        probabilities = [0]*len(self.banners)
        for i in range(len(self.banners)):
            probabilities[i] = self.__probability_of_show_banner(self.banners, i, k)
        return dict(zip([value for (value, _ ) in self.banners], probabilities))
    
    def start_probabilities_of_show_banners(self):
        return self.probabilities_of_show_banners(1)
    
    def start_weights_of_show_banners(self):
        return dict(self.banners)
    
    def frequency_test(self,k):
        frequencies = {banner: 0 for banner, weight in self.banners}
        total_sum_weights = self.banners_tree.get_sum()
        n = 100000
        for _ in range(n):
            sum_weights = self.banners_tree.get_sum()
            uniq_banners_total = len(self.banners)
            for i in range(k):
                generated_number = numpy.random.uniform() * sum_weights
                interval = self.banners_tree.find_interval(generated_number)
                banner, weight = self.banners[interval]
                self.swap(interval, uniq_banners_total - 1)
                frequencies[banner] += 1
                uniq_banners_total -= 1
                sum_weights -= weight    
        return {banner: float(frequency)/n for banner, frequency in frequencies.items()}
        
        
        
        
        
        