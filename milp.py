# ## Optimisation of the Experimental Design for the Flexible PVC Modelling Experiments
# Allocation of Degree and Student for each experiment

#Actual optimisation

from pulp import *
from calc_constants import calc_T
from report import results
from numpy import size, amax, amin

def solve_milp(p, mm_lambda_1, mm_lambda_2, exp_time_data, experiments):
    # ####Define Design Variables

    #Degree allocation for each Experiment

	#Exp List must be in alphabetical order for the program output to make sense

	#experiments = ['Antistat',
	#			   'Rheometer',
	#			   'Metrastat',
	#			   'Ransomat',
	#			   'Vicat',
	#			   'TMA',
	#			   'Tensile',
	#			   'Impact',
	#			   'Cone_Cal',
	#			   'Micro_Cone',
	#			   'UL94',
	#			   'LOI']
	#experiments.sort()

    no_exp = size(experiments)

    degrees = ['1', '2', '2.5', '3'] 

	#Binary variables for each combination of experiment and degree 
    N = LpVariable.dicts('exp_deg', (experiments, degrees), 0, 1, 'Integer')

	#Allocation of Students to Degree
    no_students = 4
    students = [str(i + 1) for i in range(no_students)]

	#Binary variables for each combination of experiment and student
    S = LpVariable.dicts('exp_stu', (experiments, students), 0, 1, 'Integer')

	#Continuous variable for total time required for each experiment
    tau = LpVariable.dicts('total_time', experiments)

	#Continuous variable introduces in glover formulation, z_ji = S_ij*tau_i
    z = LpVariable.dicts('stu_exp', (students, experiments))


	# ####Define Constants

    d = [1.0, 2.0, 2.5, 3.0] #Degree values

    T_no_exp_all = calc_T(experiments, exp_time_data)
    T = T_no_exp_all[0] #Time required for each experiment degree combination
    no_exp_all = T_no_exp_all[1] #No of experiments required for each experiment degree combination

    U = amax(T)
    L = amin(T)

	# ####Initiate Problem

    prob = LpProblem('Optimisation of Experimental Design', LpMaximize)

	# ####Define Objective function

    obj = []
    for i in experiments:
        obj.append(sum([d[n]*N[i][j] for n, j in enumerate(degrees)]))

    prob += sum(obj)

	# #### Define Constraints
	# Logical Constraints

	#Logical constraint on degrees of experiments

    for i in experiments:
        prob += sum([N[i][j] for j in degrees]) == 1, 'Logic constr on deg of exp %s'%i

	#Logical constraint on allocations of students to experiments

    for i in experiments:
        prob += sum([S[i][j] for j in students]) == 1, 'Logic constr on stu per exp %s'%i

	# Resource Constraints (Glover Constraints)

    for n, j in enumerate(students):
        prob += sum([z[j][i] for i in experiments]) <= p[n], 'Stu %s time constr'%j 
        for i in experiments:
            prob += z[j][i] <= U*S[i][j], 'Glover constr 1 up exp %s stu %s'%(i, j)
            prob += z[j][i] >= L*S[i][j], 'Glover constr 1 low exp %s stu %s'%(i, j)
            prob += z[j][i] <= tau[i] - L*(1 - S[i][j]), 'Glover constr 2 low exp %s stu %s'%(i, j)
            prob += z[j][i] >= tau[i] - U*(1 - S[i][j]), 'Glover constr 2 up exp %s stu %s'%(i, j)
			
	# Calculation of Tau Constraint

    for m, i in enumerate(experiments):
        prob += sum([T[m][n]*N[i][j] for n, j in enumerate(degrees)]) == tau[i],'Calc of tau %s constr'%i 

	# Constraint on the type of experiments a student can do
	
    stu_2_exp = ['Micro_Cone',
                'LOI']
    
    prob += sum([S[i][students[1]] for i in experiments if i not in stu_2_exp]) == 0,'Student 2 exp constr'
    
    for i in [0, 2, 3]:
        prob += sum([S[j][students[i]] for j in stu_2_exp]) == 0,'Student %s germany exp constr'%students[i]
	
    stu_3_exp = ['Rheometer',
                 'Ransomat',
                 'Metrastat']

    prob += sum([S[i][students[2]] for i in experiments if i not in stu_3_exp]) == 0,'Student 3 exp constr'

    stu_4_exp = ['Cone_Cal',
                 'UL94']

    prob += sum([S[i][students[3]] for i in experiments if i not in stu_4_exp]) == 0,'Student 4 exp constr'

	# Minimax Constraint (Minimum Degree)

    for i in experiments:
        prob += sum([d[n]*N[i][j] for n, j in enumerate(degrees)]) >= mm_lambda_1, 'Minimax 1 constr exp %s'%i

	# Minimax Constraint (Minimum no. of Experiments per Student)

    for j in students:
        prob += sum([S[i][j] for i in experiments]) >= mm_lambda_2, 'Minimax 2 constr stu %s'%j

	# ####Write Problem to File

	#prob.writeLP('first_attempt.lp')

	# ####Solve Problem

    prob.solve()

	# ####Report Solution

	# Solution Status

    print 'Status:', LpStatus[prob.status]
    print '_______________________'

	# Detailed Solution Report

    results(prob, degrees, no_exp, no_students, experiments, students, no_exp_all, T)

	# Optimum Objective Function Value

    print 'Objective =', value(prob.objective)
	
    return value(prob.objective), prob.status




