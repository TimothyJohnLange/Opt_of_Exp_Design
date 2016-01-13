
# coding: utf-8

# ## Optimisation of the Experimental Design for the Flexible PVC Modelling Experiments
# Allocation of Degree and Student for each experiment

# In[1]:

from milp import solve_milp
from numpy import linspace
from matplotlib.pyplot import plot, show, legend, xlim, ylim
#get_ipython().magic(u'pylab inline')


# ####Define Constants

# In[2]:

p = [45*8, 45*8, 80, 80] #Time limit for each student
#p = [i*0.7 for i in p] #Scale factor for time (safety factor) might not be necessary
# Use working day calculator (south-africa.workingdays.org) 
# to calculate number of hours available for p[0] which is R Fechter
# from 1 Feb to 6 April

mm_lambda_1 = 1.0 #Minimax constraint minimum degree value
mm_lambda_2 = 1.0 #Minimax constraint minimum no. experiments per student


# ####Sensitivity Analysis

# In[3]:

#student = 1 #which student is analysed
p_reset = p

increase = 100 #Amount of increase in hrs
#no_pnts = 100

#all_obj_val = zeros([size(p), no_pnts])
all_p_adjust_per_stu = []
all_obj_val_per_stu = []

for student in range(4):
    p = p_reset
    p_current = p[student]
#     all_p_adjusted = linspace(0, p_current + dev_range, no_pnts)
    all_p_adjusted = range(0, p_current + increase, 10) #DO NOT go under 2 for last value, program crashes??
    all_p_adjust_per_stu.append(all_p_adjusted)
    all_obj_val = []
    for n, i in enumerate(all_p_adjusted):
        p[student] = i
        print '***********************************'
        print 'Student %s Time Limit %s'%(student + 1, i)
        [obj_val, status] = solve_milp(p, mm_lambda_1, mm_lambda_2)

        if status == 1:
            all_obj_val.append(obj_val)
        else:
            all_obj_val.append(0.0)
            
    all_obj_val_per_stu.append(all_obj_val)


# In[9]:

for student in range(4):
    plot(all_p_adjust_per_stu[student], all_obj_val_per_stu[student], '.', label='Student %s'%(student + 1))

legend(loc='lower right')
xlim([0, 400])
ylim([20, 37])
show()


# In[ ]:



