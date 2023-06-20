import gurobipy as gp

from CourseDesign.init import NK, NK_C, L_n_plus, L_n_minus
from CourseDesign.paramsFromSheet import L, K, c, M, Lc, p_profits, Lm, Lo

# 创建模型
m = gp.Model()

# 定义变量
x = m.addVars(L, K, vtype=gp.GRB.BINARY, name="x")
q_plus = m.addVars(NK_C, K, vtype=gp.GRB.INTEGER, name="q_plus")
q_minus = m.addVars(NK_C, K, vtype=gp.GRB.INTEGER, name="q_minus")
q_w_plus = m.addVars(K, vtype=gp.GRB.INTEGER, name="q_w_plus")
q_w_minus = m.addVars(K, vtype=gp.GRB.INTEGER, name="q_w_minus")

# 定义目标函数
obj = gp.quicksum(p_profits[_l, k] * x[_l, k] for _l in L for k in K) - gp.quicksum(
    c[k] * x[_l, k] for _l in Lc for k in K) - gp.quicksum(
    c[k] * q_plus[n, k] for n in NK_C for k in K) - gp.quicksum(c[k] * q_w_plus[k] for k in K)
m.setObjective(obj, gp.GRB.MAXIMIZE)

# 定义约束条件
for _l in Lm:
    m.addConstr(gp.quicksum(x[_l, k] for k in K) == 1, name="assign_must_flight_{}".format(_l))

for _l in Lo:
    m.addConstr(gp.quicksum(x[_l, k] for k in K) <= 1, name="assign_optional_flight_{}".format(_l))

for n in NK:
    for k in K:
        m.addConstr(
            gp.quicksum(x[_l, k] for _l in L_n_plus[n]) + q_plus[n, k] == gp.quicksum(x[_l, k] for _l in L_n_minus[n]) +
            q_minus[n, k], name="flow_balance_{}_{}".format(n, k))

for k in K:
    m.addConstr(q_w_plus[k] == q_w_minus[k], name="overnight_balance_{}".format(k))

for k in K:
    m.addConstr(gp.quicksum(x[_l, k] for _l in Lc) + gp.quicksum(q_plus[n, k] for n in NK_C) <= M[k],
                name="capacity_{}".format(k))

# 求解模型
m.optimize()
