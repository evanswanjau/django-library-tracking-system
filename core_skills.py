import random
# random list of 10 numbers between 1 and 20
rand_list = random.sample(range(1, 20), 10)

# numbers below 10
list_comprehension_below_10 = []
for i in rand_list:
  if i < 10:
    list_comprehension_below_10.append(i)

# numbers below 10 using filter
def belowTen(x):
  return x < 10

list_comprehension_below_10_filter = list(filter(belowTen, rand_list))