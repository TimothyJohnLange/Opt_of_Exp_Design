
# coding: utf-8

# In[13]:
def calc_T(experiments):

	from scipy.misc import comb
	from numpy import zeros, size
	from math import ceil


	# In[14]:

	deg = [1.0, 2.0, 2.5, 3]
	q = 6.0


	# In[15]:
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
					'TMA':      {'exp_time': None,
								 'sample_prep_time': None,
								 'no_exp_p_day': 12,
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
								 'no_exp_p_day': 14,
								 'no_exp_p_run': 1.0},
					'UL94':     {'exp_time': 10.0, #Need more info
								 'sample_prep_time': 10.0,
								 'no_exp_p_day': None,
								 'no_exp_p_run': 1.0},
					'LOI':      {'exp_time': None, #Need more info
								 'sample_prep_time': None,# As Monique
								 'no_exp_p_day': 14,
								 'no_exp_p_run': 1.0}}


	# In[16]:

	T = zeros([size(experiments), size(deg)]) # In hours
	no_exp_all = zeros([size(experiments), size(deg)])

	for col, n in enumerate(deg):
		# Calculate the number of terms required
		if n == 2.5:
			no_terms = comb(n + q - 0.5, n + 0.5) - comb(q, 3)
		else:
			no_terms = comb(n + q - 1, n)
		
		for row, exp in enumerate(experiments):
			
			# Account for multiple runs done at the same time
			e_p_run = exp_time_data[exp]['no_exp_p_run']
			rem = no_terms%e_p_run
			if rem != 0:
				no_exp = no_terms + e_p_run - rem
			else:
				no_exp = no_terms
			
			# Populate T matrix with the total time required for each experiment degree combination
			# On a time per experiment basis
			
			no_p_day = exp_time_data[exp]['no_exp_p_day']
			e_time = exp_time_data[exp]['exp_time']
			
			if e_time != None and no_p_day != None:
				print 'Error: Entries for both time per experiment and exp per day for experiment %s'%exp
			
			elif e_time != None:
				T[row][col] = e_time*no_exp/(60*e_p_run)
			
			# On a number of experiments per day
			elif no_p_day != None:
				rem = no_terms%no_p_day
				if rem != 0:
					no_exp = no_terms + no_p_day - rem
				else:
					no_exp = no_terms
				T[row][col] = 8.0*ceil(no_exp/no_p_day)
				
			# Add in sample preparation time
			sample_prep = exp_time_data[exp]['sample_prep_time']
			
			if sample_prep != None:
				T[row][col] += sample_prep*no_exp/60
				
			# Populate no of experiments matrix
			no_exp_all[row][col] = no_exp
			
	return T, no_exp_all
            
        






