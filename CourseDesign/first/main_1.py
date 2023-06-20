import gurobipy as gp
from CourseDesign.first.paramsFromSheet import K, p_profits, c, L_plus, L, M  # L与L_plus是否定义正确

m = gp.Model('Airline Profit Maximization')

x = m.addVars(L_plus, L, K, vtype=gp.GRB.BINARY, name="x")

m.update()

obj = gp.quicksum(x[i, j, k] * p_profits[j, k] for k in K for j in L for i in L_plus) \
      - gp.quicksum(x[0, j, k] * c[k] for k in K for j in L)
m.setObjective(obj, gp.GRB.MAXIMIZE)

for j in L:
    m.addConstr(gp.quicksum(x[i, j, k] for i in L_plus for k in K) == 1,
                f'Flight {j} is covered by exactly one aircraft')

for _l in L:
    for k in K:
        m.addConstr(gp.quicksum(x[i, _l, k] for i in L_plus) - gp.quicksum(x[_l, j, k] for j in L_plus) == 0,
                    f'Flow balance constraint for flight {_l} and fleet {k}')

for s in S:  # S undefined
    for k in K:
        m.addConstr(gp.quicksum(x[0, _l, k] for _l in L_plus if _l[-1] == s) -  # 是否正确
                    gp.quicksum(x[_l, 0, k] for _l in L_plus if _l[0] == s) == 0,  # 是否正确
                    f'Flow balance constraint for airport {s} and fleet {k}')

for k in K:
    m.addConstr(gp.quicksum(x[0, _l, k] for _l in L_plus) <= M[k],
                f'Fleet {k} does not exceed the total number of available aircraft')

m.optimize()

print(f'Total profit: {m.objVal}')
for v in m.getVars():
    if v.x == 1:
        print(f'{v.varName}: {v.x}')
