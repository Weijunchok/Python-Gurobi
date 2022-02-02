import gurobipy as gp
import math
from gurobipy import GRB
try:
    model = gp.Model("model")
    S_B = 100
    X12 = 0.2
    P12_MAX = 1.5
    L2 = 4
    a = [3,4.05]
    b = [20,18.07]
    c = [100,98.87]
    Pmin = [0.28,0.90]
    Pmax = [2.06,2.84]
    Pg = model.addVars(range(1,3), lb = Pmin,ub=Pmax,name='Pg')
    Pl = model.addVars(1,lb = -P12_MAX,ub=P12_MAX,name='PL')
    Delta = model.addVars(range(1,3), lb = -math.pi,ub=math.pi, name='Delta')

    model.update()
    model.setObjective(gp.quicksum(a[i]*Pg[i+1]*Pg[i+1]+b[i]*Pg[i+1]+c[i] for i in range(2)))
    model.addConstr((Delta[1] - Delta[2])/X12 == Pl[0])
    model.addConstr(Delta[1] == 0)
    model.addConstr(Pg[2] + Pl[0] - L2 == 0)
    model.addConstr(Pg[1] - Pl[0] == 0)
    
    model.write('model.lp')


    model.optimize()
    if model.Status == GRB.OPTIMAL:
        for v in model.getVars():
            print(f"{v.varName} -> {v.x}")
        print('Optimal objective: %g' % model.ObjVal)
        model.write('model.sol')
        model.write('model.lp')
    elif model.Status == GRB.INF_OR_UNBD:
        # Turn presolve off to determine whether model is infeasible
        # or unbounded
        model.setParam(GRB.Param.Presolve, 0)
        model.optimize()
    elif model.Status != GRB.INFEASIBLE:
        print('Optimization was stopped with status %d' % model.Status)
except gp.GurobiError:
    print('Error reported')

#m = gp.read('model.lp')