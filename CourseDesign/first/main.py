import gurobipy as gp
from CourseDesign.first.paramsFromSheet import K, p_profits, c, L,L_plus

# Create the model
model = gp.Model('Airline Profit Maximization')

# Define the decision variables
S = ['a', 'b']
M = {k: 2 for k in K}
x = {}
for i in L_plus:
    for j in L_plus:
        for k in K:
            x[i, j, k] = model.addVar(vtype=gp.GRB.BINARY, name=f'x_{i}_{j}_{k}')

# Define the objective function
profit = gp.quicksum(x[i, j, k] * p_profits[j][k] for k in K for j in L for i in L_plus) \
         - gp.quicksum(x[0, j, k] * c[k] for k in K for j in L)
model.setObjective(profit, gp.GRB.MAXIMIZE)

# Define the constraints
for j in L:
    model.addConstr(gp.quicksum(x[i, j, k] for i in L_plus for k in K) == 1,
                    f'Flight {j} is covered by exactly one aircraft')
for l in L:
    for k in K:
        model.addConstr(gp.quicksum(x[i, l, k] for i in L_plus) - gp.quicksum(x[l, j, k] for j in L_plus) == 0,
                        f'Flow balance constraint for flight {l} and fleet {k}')
for s in S:
    for k in K:
        model.addConstr(gp.quicksum(x[0, l, k] for l in L_plus if l[-1] == s) -
                        gp.quicksum(x[l, 0, k] for l in L_plus if l[0] == s) == 0,
                        f'Flow balance constraint for airport {s} and fleet {k}')
for k in K:
    model.addConstr(gp.quicksum(x[0, l, k] for l in L_plus) <= M[k],
                    f'Fleet {k} does not exceed the total number of available aircraft')

# Optimize the model
model.optimize()

# Print the results
print(f'Total profit: {model.objVal}')
for v in model.getVars():
    if v.x == 1:
        print(f'{v.varName}: {v.x}')
