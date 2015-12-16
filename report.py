from numpy import size

def results(prob, degrees, no_exp, no_students, experiments, students, no_exp_all, T):
	# Converts the output from the lp solver into a report
	
	# Converting List of Variables to Design Variable Matrices
	no_deg = size(degrees)
	N_result = []
	S_result = []
	z_result = []
	tau_result = []
	row = []
	v_no_N = no_exp*no_deg - 1
	v_no_S = v_no_N + no_exp*no_students
	v_no_z = v_no_S + no_students*no_exp

	for n, v in enumerate(prob.variables()):
		if n <= v_no_N:
			row.append(v.varValue)
			if size(row) == no_deg:
				N_result.append(row)
				row = []
		elif n <= v_no_S:
			row.append(v.varValue)
			if size(row) == no_students:
				S_result.append(row)
				row = []
		elif n <= v_no_z:
			row.append(v.varValue)
			if size(row) == no_exp:
				z_result.append(row)
				row = []
		else:
			tau_result.append(v.varValue)
			
	# Printing results
	print 'Degree allocation for each experiment'
	print '_______________________'
	for exp_no, row in enumerate(N_result):
		for deg_no, val in enumerate(row):
			if val == 1:
				print 'Experiment', experiments[exp_no].ljust(10, ' '), '|', 'Degree', degrees[deg_no].ljust(3, ' '), '|', 'No. Exp', no_exp_all[exp_no][deg_no], '|', 'Time Req.', T[exp_no][deg_no]
				
	print '_______________________'
	print ''
	print 'Student allocation for each experiment'
	print '_______________________'

	for exp_no, row in enumerate(S_result):
		for stu_no, val in enumerate(row):
			if val == 1:
				print 'Experiment', experiments[exp_no].ljust(10, ' '), '|', 'Student', students[stu_no] 
	print '_______________________'        
	print ''
	print 'Total time required from each student'
	print '_______________________'

	for stu_no, row in enumerate(z_result):
		print 'Student', students[stu_no], '|', 'Total time', sum(row)
	print '_______________________'
	return