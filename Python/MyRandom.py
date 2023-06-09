#! /usr/bin/env python

import math
import numpy as np

#################
# Random class
#################
# class that can generate random numbers
class Random:
    """A random number generator class"""

    # initialization method for Random class
    def __init__(self, seed = 5555):
        self.seed = seed
        self.m_v = np.uint64(4101842887655102017)
        self.m_w = np.uint64(1)
        self.m_u = np.uint64(1)
        
        self.m_u = np.uint64(self.seed) ^ self.m_v
        self.int64()
        self.m_v = self.m_u
        self.int64()
        self.m_w = self.m_v
        self.int64()

    # function returns a random 64 bit integer
    def int64(self):
        with np.errstate(over='ignore'):
            self.m_u = np.uint64(self.m_u * np.uint64(2862933555777941757) + np.uint64(7046029254386353087))
        self.m_v ^= self.m_v >> np.uint64(17)
        self.m_v ^= self.m_v << np.uint64(31)
        self.m_v ^= self.m_v >> np.uint64(8)
        self.m_w = np.uint64(np.uint64(4294957665)*(self.m_w & np.uint64(0xffffffff))) + np.uint64((self.m_w >> np.uint64(32)))
        x = np.uint64(self.m_u ^ (self.m_u << np.uint64(21)))
        x ^= x >> np.uint64(35)
        x ^= x << np.uint64(4)
        with np.errstate(over='ignore'):
            return (x + self.m_v)^self.m_w

    # function returns a random floating point number between (0, 1) (uniform)
    def rand(self):
        return 5.42101086242752217E-20 * self.int64()

    # function returns a random integer (0 or 1) according to a Bernoulli distr.
    def Bernoulli(self, p=0.5):
        if p < 0. or p > 1.:
            return 1
        
        R = self.rand()

        if R < p:
            return 1
        else:
            return 0

    # function returns a random double (0 to infty) according to an exponential distribution
    def Exponential(self, beta=1.):
      # make sure beta is consistent with an exponential
      if beta <= 0.:
        beta = 1.

      R = self.rand();

      while R <= 0.:
        R = self.rand()

      X = -math.log(R)/beta

      return X

    # returns a truncated poisson distribution based on a uniform RNG [0,1]
    def DiscretePoisson(self, beta=2):
        # Resiliance against users
        if beta <= 0:
            beta = 1
        
        R = self.rand();
        while R <= 0:
            R = self.rand();
            
        cdf = 0
        x = 0
        
        while cdf < R:
            cdf += beta**x * math.e**(-beta)/math.factorial(x)
            
            if R <= cdf:
                return x
            x +=1


    def DiscretePoissonProb(slef, beta, x):
        return beta**x * math.e**(-beta)/math.factorial(x)
        
    # If the step chance is below the probability, returns a random number in [-100,100]. Otherwise returns a random number in [-1,1]
    def LevyFlight(self, p=0.01):
        if p < 0. or p > 1.:
            return 1
        
        
        stepchance = self.rand()
        while stepchance < 0 or stepchance > 1:
            stepchance = self.rand()
            
        if stepchance <= p:
            step = (self.rand() - 0.5) * 200
        
        else:
            step = (self.rand() - 0.5) * 2
            
        return step
                
        