# 根据您提供的信息，您可以按照以下步骤来初始化NK_C、NK、L_n_plus、L_n_minus、q_w_plus和q_w_minus：
from CourseDesign.second.paramsFromSheet import flightSheet, K, NC

# 创建空字典NK_C和NK，用于存储航班和机型之间的映射关系。
# 创建空字典L_n_plus和L_n_minus，用于存储每个节点的正向和反向邻居节点。
# 创建空字典q_w_plus和q_w_minus，用于存储每个节点的正向和反向邻居节点的转移时间。
# 以下是一个示例代码，用于实现上述步骤：

NK_C = {}
NK = {}
L_n_plus = {}
L_n_minus = {}
q_w_plus = {}
q_w_minus = {}


def flight_time(d_t, a_t):
    """
    计算从一个时间到另一个时间的飞行时间
    :param d_t: 起飞时间，格式为'HH:MM'
    :param a_t: 降落时间，格式为'HH:MM'
    :return: 飞行时间，单位为分钟
    """
    d_t = int(d_t[:2]) * 60 + int(d_t[3:])
    a_t = int(a_t[:2]) * 60 + int(a_t[3:])
    f_t = a_t - d_t
    return max(0, f_t)


for flight in flightSheet:
    flight_id, flight_no, origin, departure_time, destination, arrival_time, is_required = flight
    for k in K:
        if is_required:
            # 如果是必要航班，则将其起飞节点和到达节点添加到NK_C和NK中
            takeoff_node = (origin, k, departure_time)
            landing_node = (destination, k, arrival_time)
            if takeoff_node not in NK_C:
                NK_C[takeoff_node] = []
            if landing_node not in NK_C:
                NK_C[landing_node] = []
            NK_C[takeoff_node].append((flight_id, landing_node))
            NK_C[landing_node].append((flight_id, takeoff_node))
            if takeoff_node not in NK:
                NK[takeoff_node] = []
            if landing_node not in NK:
                NK[landing_node] = []
            NK[takeoff_node].append(landing_node)
            NK[landing_node].append(takeoff_node)
        # 将所有节点添加到L_n_plus、L_n_minus、q_w_plus和q_w_minus中
        if takeoff_node not in L_n_plus:
            L_n_plus[takeoff_node] = []
        if landing_node not in L_n_minus:
            L_n_minus[landing_node] = []
        if takeoff_node not in q_w_plus:
            q_w_plus[takeoff_node] = {}
        if landing_node not in q_w_minus:
            q_w_minus[landing_node] = {}
        for j in NC:
            if j != origin:
                # 将起飞节点的正向邻居节点添加到L_n_plus和q_w_plus中
                takeoff_node_plus = (j, k, departure_time)
                L_n_plus[takeoff_node].append(takeoff_node_plus)
                q_w_plus[takeoff_node][takeoff_node_plus] = flight_time(departure_time, arrival_time)
            if j != destination:
                # 将到达节点的反向邻居节点添加到L_n_minus和q_w_minus中
                landing_node_minus = (j, k, arrival_time)
                L_n_minus[landing_node].append(landing_node_minus)
                q_w_minus[landing_node][landing_node_minus] = flight_time(departure_time, arrival_time)

print(L_n_plus)