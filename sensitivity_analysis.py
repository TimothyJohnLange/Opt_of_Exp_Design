# ## Optimisation of the Experimental Design for the Flexible PVC Modelling Experiments
# Allocation of Degree and Student for each experiment

from milp import solve_milp
from numpy import linspace
from matplotlib.pyplot import plot, xlim, ylim, legend, figure, show, xlabel, ylabel
#get_ipython().magic(u'pylab inline')

# ####Define Constants

p = [45*8, 45*8, 80, 80] #Time limit for each student
#p = [i*0.7 for i in p] #Scale factor for time (safety factor) might not be necessary
# Use working day calculator (south-africa.workingdays.org) 
# to calculate number of hours available for p[0] which is R Fechter
# from 1 Feb to 6 April

mm_lambda_1 = 1.0 #Minimax constraint minimum degree value
mm_lambda_2 = 2.0 #Minimax constraint minimum no. experiments per student

# Experimental time requirements
exp_time_data = {'Antistat': {'exp_time': 5.0,
                             'sample_prep_time': 25.0,
                             'no_exp_p_day': None,
                             'no_exp_p_run': 1.0},
                    'Rheometer':{'exp_time': 210.0,
								 'sample_prep_time': None,
								 'no_exp_p_day': None,
								 'no_exp_p_run': 1.0}, 
					'Metrastat':{'exp_time': 180.0,
								 'sample_prep_time': 25.0,
								 'no_exp_p_day': None,
								 'no_exp_p_run': 3.0},
					'Ransomat': {'exp_time': 300.0,
								 'sample_prep_time': 20.0,
								 'no_exp_p_day': None,
								 'no_exp_p_run': 8.0},
					'Vicat':    {'exp_time': 20.0, #Need more info
								 'sample_prep_time': None,
								 'no_exp_p_day': None,
								 'no_exp_p_run': 5.0},
					'TMA':      {'exp_time': 30,
								 'sample_prep_time': None,
								 'no_exp_p_day': None,
								 'no_exp_p_run': 1.0},
					'Tensile': {'exp_time': 15.0, #Need more info
								 'sample_prep_time': 25.0,
								 'no_exp_p_day': None,
								 'no_exp_p_run': 1.0},
					'Impact':  {'exp_time': 15.0, #Need more info
								 'sample_prep_time': 25.0,
								 'no_exp_p_day': None,
								 'no_exp_p_run': 1.0},
					'Cone_Cal': {'exp_time': None,
								 'sample_prep_time': 25.0,
								 'no_exp_p_day': 14,
								 'no_exp_p_run': 1.0},
					'Micro_Cone':{'exp_time': None, #Need more info
								 'sample_prep_time': None, # Ask Monique
								 'no_exp_p_day': 12,
								 'no_exp_p_run': 1.0},
					'UL94':     {'exp_time': 10.0, #Need more info
								 'sample_prep_time': 10.0,
								 'no_exp_p_day': None,
								 'no_exp_p_run': 1.0},
					'LOI':      {'exp_time': None, #Need more info
								 'sample_prep_time': None,# Ask Monique
								 'no_exp_p_day': 12,
                                 'no_exp_p_run': 1.0}}


experiments = ['Antistat',
               'Rheometer',
               'Metrastat',
               'Ransomat',
               'Vicat',
               'TMA',
               'Tensile',
               'Impact',
               'Cone_Cal',
               'Micro_Cone',
               'UL94',
               'LOI'] 

experiments.sort() #experiment list must be alphabetical for output to make sense

# ####Sensitivity Analysis

# Varying experiment time requirements

data_types = ['exp_time', 'sample_prep_time', 'no_exp_p_day']

all_obj_val_per_data_type = []
all_adj_val_per_data_type = []
for data_type in data_types[:1]:
    new_data_type = 1 
    if data_type == 'no_exp_p_day':
        start = 1
        interval = 1
        end_1 = 25
    else:
        start = 0
        interval = 5
        end_1 = 100
        end_2 = 600
		
    all_obj_val_per_exp = []
    all_adj_val_per_exp = []
    for n, experiment in enumerate(experiments):
        if n == 0 and data_type == 'exp_time':
            new_data_type = 0
        elif new_data_type == 1:
            exp_time_data[prev_exp][prev_data_type] = prev_val
        else:
            exp_time_data[prev_exp][data_type] = prev_val
			
   
        val = exp_time_data[experiment][data_type]
        if val != None:
            new_data_type = 0
            if val <= 30:
                all_adjusted_val = range(start, end_1, interval)#int(val)*2 + 1, interval)
            else:
                all_adjusted_val = range(start, end_2, 10)#int(val)*2 + 1, 10)
            
            all_obj_val = []
            for i in all_adjusted_val:
                exp_time_data[experiment][data_type] = i
                
                print '***********************************'
                print 'Experiment %s, Data Type %s, Value %s'%(experiment, data_type, i)
                [obj_val, status] = solve_milp(p, mm_lambda_1, mm_lambda_2, exp_time_data, experiments)
                
                if status == 1:
                    all_obj_val.append(obj_val)
                else:
                    all_obj_val.append(0.0)
				
            all_obj_val_per_exp.append(all_obj_val)
            all_adj_val_per_exp.append(all_adjusted_val)
            prev_exp = experiment
            prev_val = val
        else:
            all_obj_val_per_exp.append(None)
            all_adj_val_per_exp.append(None)
        
    all_obj_val_per_data_type.append(all_obj_val_per_exp)
    all_adj_val_per_data_type.append(all_adj_val_per_exp)
    prev_data_type = data_type

exp_time_data[prev_exp][data_type] = prev_val 

print '*******************'

# Plotting sensitivity

colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
col_cntr = 0
for n, (obj_val_per_data_type, adj_val_per_data_type) in enumerate(zip(all_obj_val_per_data_type, all_adj_val_per_data_type)):
    fig = figure()
    fig.suptitle(data_types[n])
    for m, (all_obj_val_per_exp, all_adj_val_per_exp) in enumerate(zip(obj_val_per_data_type, adj_val_per_data_type)):
		if all_obj_val_per_exp != None:# and m in [2, 9, 10]:
			plot(all_adj_val_per_exp, all_obj_val_per_exp, colors[col_cntr], label=experiments[m])
			ori_val = exp_time_data[experiments[m]][data_types[n]]
			index = all_adj_val_per_exp.index(ori_val)
			plot(all_adj_val_per_exp[index], all_obj_val_per_exp[index], 'o' + colors[col_cntr])
			if col_cntr != 6:
				col_cntr += 1
			else:
				col_cntr = 0
		legend()
    if n == 2:
        xlabel('No. of Exp. per Day')
        legend(loc='lower right')
        ylim([26, 37])
    else:
        xlabel('Time (min)')
        ylim([32, 35.5])
        xlim([0, 100])
    ylabel('Optimum Objective Function')

# Varying the amount of time available per student

# increase = 50 #Amount of increase in hrs

# all_p_adjust_per_stu = []
# all_obj_val_per_stu = []

# for student in range(4):
    # p_current = p[student]
    # all_p_adjusted = range(0, p_current + increase, 10) 
    # all_p_adjust_per_stu.append(all_p_adjusted)
    # all_obj_val = []
    # for n, i in enumerate(all_p_adjusted):
        # p[student] = i
        # print '***********************************'
        # print 'Student %s Time Limit %s'%(student + 1, i)
        # [obj_val, status] = solve_milp(p, mm_lambda_1, mm_lambda_2, exp_time_data, experiments)

        # if status == 1:
            # all_obj_val.append(obj_val)
        # else:
            # all_obj_val.append(0.0)
            
    # all_obj_val_per_stu.append(all_obj_val)
	
    # p[student] = p_current

# Plot sensitivity
# fig = figure()
# fig.suptitle('Student Time Limit Adjust')
# col_cntr = 0
# for student in range(4):
    # plot(all_p_adjust_per_stu[student], all_obj_val_per_stu[student], colors[col_cntr], label='Student %s'%(student + 1))
    # index = all_p_adjust_per_stu[student].index(p[student])
    # plot(all_p_adjust_per_stu[student][index], all_obj_val_per_stu[student][index], colors[col_cntr] + 'o')
    # if col_cntr != 6:
        # col_cntr += 1
    # else:
        # col_cntr = 0
# legend(loc='lower right')
# xlim([0, 400])
# ylim([20, 37])
# xlabel('Time (h)')
# ylabel('Optimum Objective Function')

show()




