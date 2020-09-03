# Optimal Travel Plan
Consider the case when you wish to travel on particular days of a month. There are multiple passes available (daily, weekly and monthly, for example), and each one has a different cost. In that case, what would be a cost optimal plan. It is assumed that you would buy a pass (if necessary) on a day you dont wish to travel. This code computes the optimal travel plan (a well known puzzle) by posing it as an ILP and then solving it using a little randomization.

# Use
getOptimalPlan(x=np.array([ 1,  4,  6, 11, 22, 27, 30, 33, 35, 40, 55, 58, 66, 68,
                                72, 74, 81, 82, 83, 84, 90, 91, 93, 95, 97, 99]),
                   validity_period=[1,7,30],costs=[2,7,15],solver='ECOS')
                   

# Package Requirements
1) Numpy 
2) CVXPY
