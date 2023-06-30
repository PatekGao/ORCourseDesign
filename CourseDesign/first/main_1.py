import gurobipy as gp
from CourseDesign.first.paramsFromSheet import K, p_profits, c, L_plus, L, M, S, LA, LD, L_Linar

m = gp.Model('Airline Profit Maximization')

# m.Params.LogToConsole = 1

x = m.addVars(L_plus, L_plus, K, vtype=gp.GRB.BINARY, name="x")

m.update()

obj = gp.quicksum(x[i, j, k] * p_profits[j, k] for k in K for j in L for i in L_plus) \
      - gp.quicksum(x[0, j, k] * c[k] for k in K for j in L)
m.setObjective(obj, gp.GRB.MAXIMIZE)
# i_num = 0
# j_num = 0
# # 添加约束条件
# for i in L_plus:
#     for j in L_plus:
#         if i != 0:
#             i_num = int(str(i)[1:])
#         else:
#             i_num = i
#         if j != 0:
#             j_num = int(str(j)[1:])
#         else:
#             j_num = j
#             # 添加约束条件：如果j>i，则x[i, j, k] = 0
#         if j_num > i_num:
#             m.addConstrs(x[i, j, k] == 0 for k in K)

for i in L_plus:
    for j in L_plus:
        if i != 0:
            tmp = L_Linar[i]
            if j in tmp:
                continue
            else:
                m.addConstrs(x[i, j, k] == 0 for k in K)

# 添加约束条件
for i in L_plus:
    for j in L_plus:
        if i != 0 and j != 0:
            if j in L_Linar.get(i, []):
                m.addConstrs(x[i, j, k] == 0 for k in K)

m.addConstrs((x[i, j, k] == 0 for i in L_plus for j in L_plus for k in K if i == j), name="constraint_name")

for j in L:
    m.addConstr(gp.quicksum(x[i, j, k] for i in L_plus for k in K) == 1,
                f'Flight {j} is covered by exactly one aircraft')

for _l in L:
    for k in K:
        m.addConstr(gp.quicksum(x[i, _l, k] for i in L_plus) - gp.quicksum(x[_l, j, k] for j in L_plus) == 0,
                    f'Flow balance constraint for flight {_l} and fleet {k}')

for s in S:
    LA_S = LA[s]
    LD_S = LD[s]
    for k in K:
        m.addConstr(gp.quicksum(x[0, _l, k] for _l in LD_S) - gp.quicksum(x[_l, 0, k] for _l in LA_S) == 0,
                    f'Flow balance constraint for airport {s} and fleet {k}')

for k in K:
    m.addConstr(gp.quicksum(x[0, _l, k] for _l in L) <= M[k],
                f'Fleet {k} does not exceed the total number of available aircraft')

    m.optimize()

if m.status == gp.GRB.OPTIMAL:
    print("最优解已找到")
    print("目标函数值: ", m.objVal)

    # 输出变量值
    for v in m.getVars():
        print(v.varName, v.x)
else:
    print("模型无可行解")
