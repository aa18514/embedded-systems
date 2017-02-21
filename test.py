import random



class RandomGen(object):

  _random_nums = [-1,0,1,2,3]
  _probabilities = [0.01, 0.3, 0.58, 0.1, 0.01]
  
  cum=0;
  _cdf =[]
  for prob in _probabilities:
    cum +=prob;
    _cdf.append(cum)
  #print(_cdf)
  
  def next_num(self):
     r= random.random()
     return RandomGen._random_nums[[ n for n,i in enumerate(RandomGen._cdf) if i>r ][0]]     #return filter(lambda x,i:x>r,RandomGen._cdf)
     
a =RandomGen()
for i in range(100):
  print(a.next_num())

