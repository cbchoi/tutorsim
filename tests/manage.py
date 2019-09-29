with open('student_list.csv', 'r') as f:
	with open('student_list2.csv', 'w') as f2:
		for l in f:
			l = l.strip()
			items = l.split(',')
			f2.write('{0},{1}, https://github.com/hgu-sit22005/daily-commits-{1},\n'.format(items[0], items[1]))
