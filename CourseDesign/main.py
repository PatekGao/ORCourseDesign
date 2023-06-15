import gurobipy as gp

from CourseDesign.init import NK_C, L_n_plus, L_n_minus, q_w_plus, q_w_minus, NK
from CourseDesign.paramsFromSheet import L, K, p_profits, c, Lc, Lo, M

# 创建模型
m = gp.Model()

# 创建决策变量
x = m.addVars(L, K, vtype=gp.GRB.BINARY, name="x")
q_plus = m.addVars(NK, K, lb=0, name="q_plus")
q_minus = m.addVars(NK, K, lb=0, name="q_minus")

# 创建目标函数
obj = gp.quicksum(p_profits[l][k] * x[l, k] for l in L for k in K) - \
      (gp.quicksum(c[l][k] * x[l, k] for l in Lc for k in K) +
       gp.quicksum(c[k] * q_plus[n, k] for n in NK_C for k in K))

m.setObjective(obj, gp.GRB.MAXIMIZE)

# 创建约束条件
for _l in Lo:
    m.addConstr(gp.quicksum(x[_l, k] for k in K) == 1)

for _l in Lo:
    m.addConstr(gp.quicksum(x[_l, k] for k in K) <= 1)

for n in NK:
    for k in K:
        m.addConstr(gp.quicksum(x[l, k] for l in L_n_plus[n]) + q_plus[n, k] == \
                    gp.quicksum(x[l, k] for l in L_n_minus[n]) + q_minus[n, k])

for k in K:
    m.addConstr(q_w_plus[k] == q_w_minus[k])

for k in K:
    m.addConstr(gp.quicksum(x[l, k] for l in Lc) + gp.quicksum(q_plus[n, k] for n in NK_C) <= M[k])

# 求解模型
m.optimize()
