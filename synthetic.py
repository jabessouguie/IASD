import solution_good

inf = open('pdf.txt','r')
outf = open('out.txt','w')

a=solution_good.PMDAProblem(list())
a.load(inf)
if a.search():
    a.save(outf)
    print('Solution found with cost = ' + str(a.state))
else:
    print('No solution found')