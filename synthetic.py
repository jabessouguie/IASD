import solution_good

inf = open('pdf.txt','r')
outf = open('out.txt','w')

a=solution_good.PMDAProblem(solution_good.PMDAProblem.load(inf))
inf.close()
if a.search():
    a.save(outf)
    print('Solution found with cost = ' + str(a.state.totalGone))
else:
    print('No solution found')
    
outf.close()