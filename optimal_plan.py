import numpy as np
import cvxpy as cvx

def getOptimalPlan(x=np.array([ 1,  4,  6, 11, 22, 27, 30, 33, 35, 40, 55, 58, 66, 68,
                                72, 74, 81, 82, 83, 84, 90, 91, 93, 95, 97, 99]),
                   validity_period=[1,7,30],costs=[2,7,15],solver='ECOS'):
    """
    This function computes the minimal cost travel plan given the desired days of travel,
    the validity periods of the available plans and the costs. The method formulates the problem
    as an ILP and then solves it using a little randomziation.
    :param x: Days of travel (list of unique positive integers).
    :param validity_period: List of unique positive integers.
    :param costs: List of floats.
    :param solver: List of solvers from the CVXPY suite (default is 'ECOS').
    :return: Prints the plan, and the optimal total cost.
    """

    x = np.sort(x)

    c = np.array([])

    A = np.zeros([1,np.max(x)+1])

    for l in range(len(validity_period)):
        for k in range(np.max(x)+1):
            A = np.vstack((A, np.hstack((np.zeros(k), np.ones(validity_period[l]), np.zeros(max(0,A.shape[1]-validity_period[l]-k))))[0:np.max(x)+1]))
            c = np.hstack((c, costs[l]))

    A = A[1:,:]
    z = cvx.Variable(A.shape[0])

    c1 = c + (np.min(np.abs(np.diff(np.sort(costs))))/10)*np.random.rand(len(c))
    prob = cvx.Problem(cvx.Minimize(c1@z), [(z@A)[list(x)]==1]+[z>=0, z<=1])
    prob.solve(solver=solver)

    if(prob.status=='optimal_inaccurate'):
        print('The solution is inaccurate. Try another solver!')

    z = z.value
    z[z<=1e-6] = 0

    days = []
    idx = []
    plan_choice = []
    for k in range(len(z)):
        if (z[k] > 0.5):
            idx = idx + [k]
            if (k < (np.max(x)+1)):
                days = days + [k]
                plan_choice = plan_choice + [0]
            for l in range(1,len(validity_period)-1):
                if (k >= l*(np.max(x)+1) and k < (l+1) * (np.max(x)+1)):
                    days = days + [k - l*(np.max(x)+1)]
                    plan_choice = plan_choice + [l]
                    break
            if (k >= (len(validity_period)-1) * (np.max(x)+1)):
                days = days + [k - (len(validity_period)-1) * (np.max(x)+1)]
                plan_choice = plan_choice + [(len(validity_period)-1)]

    coveredx, res = checkValidity(x, plan_choice, days, validity_period)
    if (res):
        pass
    else:
        print('Something went wrong!')
        return

    for k in np.argsort(days):
        print('Buy a PLAN '+ str(plan_choice[k]) +' pass on ' + str(days[k]) + ' day')

    if(np.abs((c @ z)-np.round(c @ z))<=np.min(costs)/10):
        print('The total cost of travel will be: ' + str(np.round(c @ z)))
    else:
        print('The total cost of travel will be: ' + str(c @ z))


def checkValidity(x, plan_choice, days, validity_period):
    """
    This function checks the validity of the generated travel plan.
    :param x: The days of travel (positive integers).
    :param plan_choice: The validity plans chosen on the day of buying (positive indices).
    :param days: The days on which the plans are procured.
    :param validity_period: The validity of the plans (unique positive integers).
    :return: True or False
    """
    coveredx = np.zeros(len(x))
    for k in range(len(plan_choice)):
        for l in range(len(x)):
            if(days[k]<=x[l] and x[l]<=days[k]+validity_period[plan_choice[k]]-1):
                coveredx[l] = 1

    if((coveredx==1).all()):
        return coveredx, True
    else:
        return coveredx, False

