wBannerRotator
==============


Баннерная крутилка

Необходимо из n различных взвешенных баннеров выбрать k различных баннеров в соответствии с весами.
```
usage: rotator.py [-h] -f DATA_FILE [-b BLOCKS] [-s STATISTICS_FILE] [-q N]

optional arguments:
  -h, --help          show this help message and exit
  -f DATA_FILE        File with banners and their weights. (default: None)
  -b BLOCKS           Number of banners to show. It must be less than number
                      of unique banners (default: 1)
  -s STATISTICS_FILE  Calculate statistics for given number of blocks and save
                      to file. ONLY FOR len(banners) * blocks < 100
  -q N                Use if needed frequency analysis of choosing k banners;
                      N - number of samples
```
Пример:
```
$python rotator.py -f generated_banners.csv -s stat.csv -b 3 -q 10000
```
```
$python rotator.py -f huge_number_of_banners.csv -b 2000
```
