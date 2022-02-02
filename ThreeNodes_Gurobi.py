import gurobipy as gp
import math
from gurobipy import GRB
try:
    model = gp.Model("model")
    S_B = 100
    X_Line = [0.2,0.25,0.4]
    P_Line = [0.5,1,1]
    P_Line2 = [-0.5,-1,-1]
    Line = [[1,2],[2,3],[1,3]]
    L2 = 1
    b = [10,11]
    Pmin = [0,0]
    Pmax = [0.65,1.0]
    Pg = model.addVars(range(1,3), lb = Pmin,ub=Pmax,name='Pg')
    Pl = model.addVars(range(1,4),lb = P_Line2, ub=P_Line,name='PL')
    Delta = model.addVars(range(1,4), lb = -math.pi,ub=math.pi, name='Delta')

    model.update()
    model.write('model.lp')
    model.setObjective(gp.quicksum(b[i]*Pg[i+1] for i in range(2)))
    model.addConstrs((Delta[(Line[i][0])] - Delta[(Line[i][1])])/X_Line[i] == Pl[i+1] for i in range(3))
    model.addConstr(Delta[3] == 0)
    model.addConstr(Pg[1] - Pl[1] - Pl[3] == 0)
    model.addConstr(-L2   + Pl[1] - Pl[2] == 0)
    model.addConstr(Pg[2] + Pl[2] + Pl[3] == 0)

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