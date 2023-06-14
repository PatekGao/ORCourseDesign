import gurobipy as gp
from gurobipy import GRB

# production rate of machine k at facility m
pro_rate = [5, 5, 5, 4, 4, 4, 3, 3, 3, 3]

# total capicity of machine k at facility m
capicity = [30, 30, 30, 30, 30, 30, 30, 30, 30, 30]

# usage cost per unit of machine k
usage_cost = [3, 3, 3, 2, 2, 2, 1, 1, 1, 1]

# number of worker required for machine k
woker_req = [3, 3, 3, 3, 3, 3, 3, 3, 3, 3]

# energy consume cost of factory m
energy_cost = 20

# number of fixed worker at factory m
fixed_worker = 21

# labor cost per unit time of fixed worker
fixed_cost = 0.3

# labor cost per unit time of flexible worker
flexible_cost = 0.5


# output value per unit product
unit_value = 3

# earning per output value when the required value is satisfied
earning_value = 1

# penalty cost per output value when the required value is not satisfied
penalty_cost_value = 3

# the objective output value
req_value = 1900

# the reqiured production quantity
req_quantity = 800

# a big real value number
big_m = 100000

# Range of machines
machines = range(len(capicity))

# build an empty model named factory_decision model
m = gp.Model("factory_decision_model")

# decision variable of machine production time：X[k]
pro_time = m.addVars(machines, lb=0, vtype=GRB.CONTINUOUS, name="pro_time")

# decision variable of fixed worker:Y[k]
fix_worker = m.addVars(machines, lb=0, vtype=GRB.INTEGER, name="fix_worker")

# decision variable of flexible worker:Z[k]
flex_worker = m.addVars(machines, lb=0, vtype=GRB.INTEGER, name="flex_worker")

# decision variable of machine setup: \beta[k]
beta = m.addVars(machines, lb=0, ub=1, vtype=GRB.BINARY, name="beta")

# decison variable of maximum production time:T
max_time = m.addVar(lb=0, ub=30, vtype=GRB.CONTINUOUS, name="max_time")

# decision variable of quantity of output value which beyond the requirement
sup_value = m.addVar(lb=0, ub=float("inf"), vtype=GRB.CONTINUOUS, name="sup_value")

# decision variable of quantity of output value which not satisfy the requirement
blow_value = m.addVar(lb=0, ub=float("inf"), vtype=GRB.CONTINUOUS, name="blow_value")

# set objective function: usage cost of machine + labor cost + enerry cost + output value
m.setObjective(gp.quicksum(usage_cost[k] * pro_time[k] for k in machines)
               + gp.quicksum(
    (fixed_cost * fix_worker[k] + flexible_cost * flex_worker[k]) * pro_time[k] for k in machines)
               + energy_cost * max_time + penalty_cost_value * blow_value, GRB.MINIMIZE)

# Add constraint: production quantity
m.addConstr(gp.quicksum(pro_rate[k] * pro_time[k] for k in machines) == req_quantity, "production")

# Add constraint: output value
m.addConstr(req_quantity * unit_value == req_value + sup_value - blow_value, "output_value")

# Add constrains: capacity
m.addConstrs((pro_time[k] <= capicity[k] for k in machines), "capacity")

# Add constrains: labor requirement
m.addConstrs((fix_worker[k] + flex_worker[k] == woker_req[k] * beta[k] for k in machines), "labor")

# Add constrains: machine setup
m.addConstrs((beta[k] * big_m >= pro_time[k] for k in machines), "setup")

# Add constrains: machine setup_1
m.addConstrs((beta[k] <= pro_time[k] * big_m for k in machines), "setup_1")

# Add constraint: max_time
m.addConstrs((max_time >= pro_time[k] for k in machines), "max_time")

# Add constraint: fixed_worker
m.addConstr(gp.quicksum(fix_worker[k] for k in machines) <= fixed_worker, "fixed_worker")

# save model
m.write('factory_decision_modelPY_2.lp')

m.setParam('NonConvex', 2)
# Optimize
m.optimize()

# Print solution
print('\nTotal costs:%g' % m.objVal)
print('SOLUTION:')
total_production = 0
for k in machines:
    if beta[k].x > 0.99:
        print('machine %s is setup' % k)
        print('Machine %s production time is %g' % (k, pro_time[k].x))
        total_production += pro_time[k].x * pro_rate[k]
print('The total production amount is %g' % total_production)
print('---------------------------------------')
total_fix_worker = 0
total_flex_worker = 0
for k in machines:
    if beta[k].x > 0.99:
        print('machine %s is setup' % k)
        print('Machine %s need %g fixed worker' % (k, fix_worker[k].x))
        print('Machine %s need %g flexiable worker' % (k, flex_worker[k].x))
        total_fix_worker += fix_worker[k].x
        total_flex_worker += flex_worker[k].x
print('The total fixed worker is %g' % total_fix_worker)
print('The total flexible worker is %g' % total_flex_worker)
print('---------------------------------------')
print('The maximum production time is %g' % max_time.x)
