import math
import os
import re

import numpy as np


def loadlog():
    log_data = None
    # 检查'data'文件夹是否存在
    if not os.path.exists('data'):
        print("文件夹 'data' 不存在。")
    else:
        # 'data'文件夹存在，检查'myapp1.log'文件是否存在
        file_path = os.path.join('data', 'myapp6.log')
        if not os.path.exists(file_path):
            print("日志文件不存在。")
        else:
            # 'myapp1.log'文件存在，尝试读取文件内容
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    log_data = file.read()
                    # 这里可以添加处理日志数据的代码
                    print('ready!')
            except UnicodeDecodeError:
                # 如果UTF-8编码失败，尝试使用GBK编码
                with open(file_path, 'r', encoding='gbk') as file:
                    log_data = file.read()
                    # 这里可以添加处理日志数据的代码
                    print('ready!')
    # print(log_data)
    return log_data


def calc_ego_distance(frame_obj):
    vehicle_obj_list = frame_obj['vehicle_obj_list']
    ego_obj_list = frame_obj['ego_obj_list']
    traffic_light_obj_list = frame_obj['traffic_light_obj_list']
    traffic_sign_obj_list = frame_obj['traffic_sign_obj_list']

    ego_obj = ego_obj_list[0]
    ego_loc = ego_obj.get('location3d')

    ego_x = ego_loc.get('x')
    ego_y = ego_loc.get('y')

    for vehicle_obj in vehicle_obj_list:
        vehicle_loc = vehicle_obj.get('location3d')
        if vehicle_loc:
            ego_distance = math.sqrt((vehicle_loc.get('x') - ego_x)**2 + (vehicle_loc.get('y') - ego_y)**2)
            vehicle_obj['ego_distance'] = ego_distance

    for traffic_light_obj in traffic_light_obj_list:
        traffic_light_loc = traffic_light_obj.get('location3d')
        if traffic_light_loc:
            ego_distance = math.sqrt((traffic_light_loc.get('x') - ego_x)**2 + (traffic_light_loc.get('y') - ego_y)**2)
            traffic_light_obj['ego_distance'] = ego_distance

    for traffic_sign_obj in traffic_sign_obj_list:
        traffic_sign_loc = traffic_sign_obj.get('location3d')
        if traffic_sign_loc:
            ego_distance = math.sqrt((traffic_sign_loc.get('x') - ego_x) ** 2 + (traffic_sign_loc.get('y') - ego_y) ** 2)
            traffic_sign_obj['ego_distance'] = ego_distance


def vec_denoise_v3(record_vec, window_size=5):
    new_record_vec = []
    for i in range(len(record_vec) - window_size):
        current_window = record_vec[i:i+window_size]
        major_vec = get_majority(current_window)
        # print(major_vec)
        new_record_vec.append(major_vec)

    # new_record_vec = np.array(new_record_vec)
    return new_record_vec


def get_majority(vec_list):
    unique_vecs = []
    for vec in vec_list:
        # check whether the vec is in the unique vec list
        flag = False
        for i in range(len(unique_vecs)):
            if unique_vecs[i][0] == vec:
                unique_vecs[i][1] += 1
                flag = True
                break

        if not flag:
            unique_vecs.append([vec, 1])

    # find the majority unique vec
    max_count = -1
    majority_vec = None
    for i in range(len(unique_vecs)):
        if unique_vecs[i][1] > max_count:
            max_count = unique_vecs[i][1]
            majority_vec = unique_vecs[i][0]

    # print(vec_list, majority_vec)
    return majority_vec

def dealLocation(obj, fieldname):
    location = obj.get(fieldname)  #  Location(x=32.367764, y=-81.074402, z=0.003042)
    if location:
        # 定义匹配模式
        pattern = r"Location\(x=(-?\d+\.\d+), y=(-?\d+\.\d+), z=(-?\d+\.\d+)\)"

        # 使用正则表达式查找匹配项
        match = re.match(pattern, location)

        # 判断是否符合要求
        if match:
            # 如果匹配成功，提取并返回x, y, z的值
            x = float(match.group(1))
            y = float(match.group(2))
            z = float(match.group(3))
            obj['location3d'] = {
                'x': x,
                'y': y,
                'z': z
            }


def deal_vector3d(obj, src_field_name, target_field_name):
    location = obj.get(src_field_name)  # Vector3D(x=32.367764, y=-81.074402, z=0.003042)
    if location:
        # 定义匹配模式
        pattern = r"Vector3D\(x=(-?\d+\.\d+), y=(-?\d+\.\d+), z=(-?\d+\.\d+)\)"

        # 使用正则表达式查找匹配项
        match = re.match(pattern, location)

        # 判断是否符合要求
        if match:
            # 如果匹配成功，提取并返回x, y, z的值
            x = float(match.group(1))
            y = float(match.group(2))
            z = float(match.group(3))
            obj[target_field_name] = {
                'x': x,
                'y': y,
                'z': z
            }


def create_ego_action_vec(frame_obj_list, map):
    move_state = []
    speed_state = []
    pre_speed_value = None
    for frame_obj in frame_obj_list:
        ego_obj = frame_obj.get('ego_obj_list')[0]
        # turn left,turn right,forward
        vehicle_steering_angle = ego_obj['vehicle_steering_angle']
        vehicle_steering_angle = float(vehicle_steering_angle)
        if vehicle_steering_angle < 0:
            move_state.append([1, 0, 0])
        elif vehicle_steering_angle > 0:
            move_state.append([0, 1, 0])
        else:
            move_state.append([0, 0, 1])
        # speed    equal   speed up   speed down
        vehicle_velocity_value = ego_obj['vehicle_velocity_value']
        vehicle_velocity_value = float(vehicle_velocity_value)
        if pre_speed_value is None:
            speed_state.append([1, 0 ,0])
        elif vehicle_velocity_value > pre_speed_value:
            speed_state.append([0, 1, 0])
        elif vehicle_velocity_value < pre_speed_value:
            speed_state.append([0, 0, 1])
        else:
            speed_state.append([1, 0, 0])
        pre_speed_value = vehicle_velocity_value

    move_state = np.vstack(move_state)
    speed_state = np.vstack(speed_state)
    ego_actions = np.concatenate([move_state, speed_state], axis=1)
    return ego_actions.tolist()


def deal_floor(val, floor_height=5):
    if val <= 0:
        return 0
    return int(val) // floor_height + 1


# 生成obs_action_vec
def create_obs_action_vec(frame_obj_list, map, near_distance=5.0):
    obs_type_list = []
    obs_type_set = []
    obs_type_num_list = []
    for frame_obj in frame_obj_list:
        vehicle_obj_list = frame_obj.get('vehicle_obj_list')
        traffic_light_obj_list = frame_obj.get('traffic_light_obj_list')
        traffic_sign_obj_list = frame_obj.get('traffic_sign_obj_list')
        pedestrian_obj_list = frame_obj.get('pedestrian_obj_list')
        obs_type = []
        obs_type_num = {}

        for vehicle_obj in vehicle_obj_list:
            if vehicle_obj.get('ego_distance') is not None and vehicle_obj.get('ego_distance'):
                ego_distance = float(vehicle_obj.get('ego_distance'))
                if ego_distance < near_distance:
                    type_id = vehicle_obj.get('vehicle_type')
                    obs_type.append(type_id)
                    if obs_type_num[obs_type_num] is None:
                        obs_type_num[obs_type_num] = 0
                    obs_type_num[type_id] = obs_type_num[type_id] + 1

        for traffic_light_obj in traffic_light_obj_list:
            if traffic_light_obj.get('ego_distance') is not None:
                ego_distance = float(traffic_light_obj.get('ego_distance'))
                if ego_distance < near_distance:
                    obs_type.append(traffic_light_obj.get('type_id'))
                    type_id = traffic_light_obj.get('type_id')
                    if obs_type_num[obs_type_num] is None:
                        obs_type_num[obs_type_num] = 0
                    obs_type_num[type_id] = obs_type_num[type_id] + 1

        for traffic_sign_obj in traffic_sign_obj_list:
            if traffic_sign_obj.get('ego_distance') is not None:
                ego_distance = float(traffic_sign_obj.get('ego_distance'))
                if ego_distance < near_distance:
                    obs_type.append(traffic_sign_obj.get("type_id"))
                    type_id = traffic_sign_obj.get('type_id')
                    if obs_type_num[obs_type_num] is None:
                        obs_type_num[obs_type_num] = 0
                    obs_type_num[type_id] = obs_type_num[type_id] + 1

        for pedestrian_obj in  pedestrian_obj_list:
            if pedestrian_obj.get("ego_distance") is not None:
                ego_distance = float(pedestrian_obj.get("ego_distance"))
                if ego_distance < near_distance:
                    obs_type.append(pedestrian_obj.get("type_id"))
                    type_id = pedestrian_obj.get('type_id')
                    if obs_type_num[obs_type_num] is None:
                        obs_type_num[obs_type_num] = 0
                    obs_type_num[type_id] = obs_type_num[type_id] + 1
        # 这一帧的 obs_type
        obs_type_set += obs_type
        obs_type = list(set(obs_type))
        obs_type_list.append(obs_type)
        obs_type_num_list.append(obs_type_num)

    obs_type_set = list(set(obs_type_set))
    obs_types_vec = []
    obs_type_num_vec = []
    for t, n in zip(obs_type_list, obs_type_num_list):
        vec = [0 for _ in range(len(obs_type_set) + 1)]
        for v in t:
            vec[obs_type_set.index(v)] = 1
        obs_types_vec.append(vec)

        vec = [0 for _ in range(len(obs_type_set) + 1)]
        for key, value in n.items():
            val = int(value)
            vec[obs_type_set.index(key)] = deal_floor(val)
        obs_type_num_vec.append(vec)

    obs_types_vec = np.vstack(obs_types_vec)
    obs_type_num_vec = np.vstack(obs_type_num_vec)

    obstacle_actions = np.concatenate([obs_types_vec, obs_type_num_vec], axis=1)
    return obstacle_actions.tolist()



def record2vec():
    frame_obj_list, map_obj = buildFrameObjList()
    scene_vec = create_scene_vecs(frame_obj_list, map_obj)
    actor_vec = create_actor_vecs(frame_obj_list, map_obj)
    ego_action_vec = create_ego_action_vec(frame_obj_list, map)
    obs_action_vec = create_obs_action_vec(frame_obj_list, map)

    scene_vec = vec_denoise_v3(scene_vec, 3)
    actor_vec = vec_denoise_v3(actor_vec, 3)
    ego_action_vec = vec_denoise_v3(ego_action_vec, 3)
    obs_action_vec = vec_denoise_v3(obs_action_vec, 3)

    record_data = {
        'scene_vec': scene_vec,
        'actor_vec': actor_vec,
        'ego_action_vec': ego_action_vec,
        'obs_action_vec': obs_action_vec
    }


def buildMapObj(mapstring):
    split_flag = "+" * 70
    mapstringarr = mapstring.split(split_flag)
    map_obj = msg2obj(mapstringarr[0])
    split_flag = "+" * 60
    crosswalks_log = mapstringarr[1].split(split_flag)
    crosswalks = []
    for crosswalk_log in crosswalks_log:
        crosswalk_obj = msg2obj(crosswalk_log)
        crosswalks.append(crosswalk_obj)
    map_obj['crosswalks'] = crosswalks
    # 处理交叉路口
    if len(mapstringarr) > 2:
        junctions_log = mapstringarr[2].split(split_flag)
        junctions = []
        for junction_log in junctions_log:
            junction_obj = msg2obj(junction_log)
            junctions.append(junction_obj)
        map_obj['junctions'] = junctions
    return map_obj


def buildFrameObjList():
    # 1、读取数据，从data文件夹下面读取数据
    log_data = loadlog()
    # 使用 "*" * 90 分离map数据
    splitflag = "*" * 90
    log_arr = log_data.split(splitflag)
    mapstring = log_arr[0]
    map_obj = buildMapObj(mapstring)
    # 使用 "*" * 80 分离每一帧的数据
    splitflag = "*" * 80
    frams = log_arr[1].split(splitflag)
    # frams = frams[1:]
    # 用来存储string[]
    frames_msg = []
    frames_obj_list = []

    for fram in frams:
        frame_msg = {}

        frame_obj = {}

        vehicle_obj_list = []
        ego_obj_list = []
        traffic_light_obj_list = []
        traffic_sign_obj_list = []
        pedestrian_obj_list = []

        frame_obj['vehicle_obj_list'] = vehicle_obj_list
        frame_obj['ego_obj_list'] = ego_obj_list
        frame_obj['traffic_light_obj_list'] = traffic_light_obj_list
        frame_obj['traffic_sign_obj_list'] = traffic_sign_obj_list
        frame_obj['pedestrian_obj_list'] = pedestrian_obj_list
        frames_obj_list.append(frame_obj)
        vehicle_msg = []

        frame_msg['vehicle_msg'] = vehicle_msg

        splitflag = "*" * 70
        msg = fram.split(splitflag)
        v_msgs = msg[0]
        tl_msgs = msg[1]
        ts_msgs = msg[2]
        pedestrians_msgs = msg[3]

        # 对汽车进行处理
        splitflag = "-" * 60
        v_msg_arr = v_msgs.split(splitflag)
        for v_msg in v_msg_arr:
            obj = msg2obj(v_msg)
            # 处理location对象
            dealLocation(obj, "vehicle_location")
            # 是ego还是背景车
            if obj.get('role_name') == 'hero':
                print('ego:')
                print(obj)
                ego_obj_list.append(obj)
            else:
                vehicle_obj_list.append(obj)

        # 对信号灯进行处理
        splitflag = "+" * 40
        tl_msg_arr = tl_msgs.split(splitflag)
        for tl_msg in tl_msg_arr:
            obj = msg2obj(tl_msg)
            dealLocation(obj, "location")
            traffic_light_obj_list.append(obj)
        # 处理交通标识
        splitflag = "+" * 50
        ts_msg_arr = ts_msgs.split(splitflag)
        for ts_msg in ts_msg_arr:
            obj = msg2obj(ts_msg)
            dealLocation(obj, "location")
            traffic_sign_obj_list.append(obj)
        # 处理行人
        splitflag = "+" * 40
        pedestrians_arr = pedestrians_msgs.split(splitflag)
        for pedestrian in pedestrians_arr:
            obj = msg2obj(pedestrian)
            dealLocation(obj, "location")
            pedestrian_obj_list.append(obj)

        # 计算与ego之间的距离
        calc_ego_distance(frame_obj)
        break
    print('frames_obj_list:')
    print(frames_obj_list)
    return frames_obj_list, map_obj


def msg2obj(v_msg):
    # 解析日志行的正则表达式
    log_line_pattern = re.compile(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) - DEBUG - (\w+): (.+)",
                                  re.UNICODE)
    subpattern = r"(\w+_+\w+): (\S+)"
    # 结果字典
    obj = {}
    # 遍历日志中的每一行
    for line in v_msg.strip().split("\n"):
        match = log_line_pattern.match(line)
        if match:
            # 提取属性名和值
            key, value = match.group(2), match.group(3)

            # 跳过以get_或set_开头的属性
            if key.startswith("get_") or key.startswith("set_") or key.startswith("add_") or key.startswith("apply_"):
                continue

            # 如果值是一个对象
            if value.startswith("{") and value.endswith('}'):
                val = value.replace("'", "")
                val = val.strip('{}')
                matches = re.findall(subpattern, val)
                for k, v in matches:
                    obj[k] = v
            else:
                obj[key.lower()] = value
    return obj


def create_scene_vecs(frame_obj_list, map):
    has_crosswalk = []
    has_intersection = []
    has_stop_sign = []

    signal_color_vec = []
    signal_type_vec = []
    subsignal_type_vec = []
    for frame_obj in frame_obj_list:
        ego_obj = frame_obj.get('ego_obj_list')[0]
        # Red
        # Yellow
        # Green
        # Off
        # Unknown
        traffic_light_state = ego_obj.get('traffic_light_state')
        if traffic_light_state == 'Red':
            signal_color_vec.append([1, 0, 0, 0, 0])
        elif traffic_light_state == 'Yellow':
            signal_color_vec.append([0, 1, 0, 0, 0])
        elif traffic_light_state == 'Green':
            signal_color_vec.append([0, 0, 1, 0, 0])
        elif traffic_light_state == 'Off':
            signal_color_vec.append([0, 0, 0, 1, 0])
        elif traffic_light_state == 'Unknown':
            signal_color_vec.append([0, 0, 0, 0, 1])

        signal_type_vec.append([0])
        subsignal_type_vec.append([0])

        ego_loc = ego_obj.get('location3d')
        has_crosswalk.append(near_crosswalk(ego_loc, map))
        has_intersection.append(near_junction(ego_loc, map))
        has_stop_sign.append(0)

    signal_color_vec = np.vstack(signal_color_vec)
    signal_type_vec = np.vstack(signal_type_vec)
    subsignal_type_vec = np.vstack(subsignal_type_vec)
    has_crosswalk_vec = np.array(has_crosswalk).reshape(-1, 1)
    has_stop_sign_vec = np.array(has_stop_sign).reshape(-1, 1)
    has_intersection_vec = np.array(has_intersection).reshape(-1, 1)
    scene_vec = np.hstack([signal_color_vec, signal_type_vec, subsignal_type_vec, has_crosswalk_vec,
                           has_stop_sign_vec, has_intersection_vec])
    return scene_vec.tolist()


def near_crosswalk(ego_loc, map):
    crosswalks = map['crosswalks']
    closet_dis = 999999
    ego_x = ego_loc.get('x')
    ego_y = ego_loc.get('y')
    for crosswalk in crosswalks:
        # print(lane_polygon)
        dis = calc_dis(ego_x, ego_y, crosswalk.get('x'), crosswalk.get('y'))
        if dis < closet_dis:
            closet_dis = dis
    if closet_dis <= 3:
        return 1
    else:
        return 0


# 计算两个二维点之间的距离
def calc_dis(x0, y0, x1, y1):
    return math.sqrt((x1-x0)**2 + (y1-y0)**2)


def near_junction(ego_loc, map):
    junctions = map['junctions']
    ego_x = ego_loc.get('x')
    closet_dis = 999999
    ego_y = ego_loc.get('y')
    for junction in junctions:
        dis = calc_dis(ego_x, ego_y, junction.get('x'), junction.get('y'))
        if dis < closet_dis:
            closet_dis = dis
    if closet_dis <= 3:
        return 1
    else:
        return 0


def on_crosswalk(loc, map, on_distance=1.0):
    if loc is None:
        return 0
    crosswalks = map['crosswalks']
    x = loc.get('x')
    y = loc.get('y')
    closet_dis = 999999
    for crosswalk in crosswalks:
        dis = calc_dis(x, y, crosswalk.get('x'), crosswalk.get('y'))
        if dis < closet_dis:
            closet_dis = dis
    if closet_dis <= on_distance:
        return 1
    else:
        return 0


def calc_angle_2d(v1, v2):
    x1 = v1['x']
    y1 = v1['y']
    x2 = v2['x']
    y2 = v2['y']

    dot_product = x1 * x2 + y1 * y2
    # 计算两个向量的模长
    magnitude_vec1 = math.sqrt(x1 ** 2 + y1 ** 2)
    magnitude_vec2 = math.sqrt(x2 ** 2 + y2 ** 2)
    # 计算cosθ
    cos_theta = dot_product / (magnitude_vec1 * magnitude_vec2)
    # 确保cosθ的值在有效范围内，避免数学域错误
    cos_theta = max(min(cos_theta, 1), -1)

    # 计算并返回角度θ，转换为度
    angle_rad = math.acos(cos_theta)
    angle_deg = math.degrees(angle_rad)
    return angle_deg


def create_actor_vecs(frame_obj_list,  map, near_distance=5.0):
    has_vehicle = []
    has_bicycle = []
    has_pedestrian = []
    has_other = []
    has_on_road_person = []
    has_on_crosswalk_person = []
    has_opposing_direction_vehicle = []
    has_crossing_direction_vehicle = []

    for frame_obj in frame_obj_list:
        ego_obj = frame_obj.get('ego_obj_list')[0]
        deal_vector3d(ego_obj, "forward_vector", "forward_vector_3d")

        near_pedestrian_count = 0
        on_road_pedestrian_count = 0
        on_crosswalk_pedestrian_count = 0

        pedestrian_obj_list = frame_obj.get('pedestrian_obj_list')
        for pedestrian_obj in pedestrian_obj_list:
            if pedestrian_obj.get("ego_distance") is not None:
                ego_distance = float(pedestrian_obj.get("ego_distance"))
                if ego_distance < near_distance:
                    near_pedestrian_count += 1
                    if pedestrian_obj.get("is_walker_on_road") is not None and pedestrian_obj.get("is_walker_on_road"):
                        on_road_pedestrian_count += 1
                    if on_crosswalk(pedestrian_obj.get("location"), map) == 1:
                        on_crosswalk_pedestrian_count += 1

        near_vehicle_count = 0
        near_bicycle_count = 0
        opposing_direction_count = 0
        crossing_direction_count = 0

        vehicle_obj_list = frame_obj.get('vehicle_obj_list')
        for vehicle_obj in vehicle_obj_list:
            if vehicle_obj.get("ego_distance") is not None:
                ego_distance = float(vehicle_obj.get("ego_distance"))
                if ego_distance < near_distance:
                    type_id = vehicle_obj.get('type_id')
                    if type_id == "vehicle.bh.crossbike": # bicycle
                        near_bicycle_count += 1
                    else:
                        near_vehicle_count += 1

                    deal_vector3d(vehicle_obj, "forward_vector", "forward_vector_3d")
                    ego_angle = calc_angle_2d(ego_obj.get("forward_vector_3d"), vehicle_obj.get("forward_vector_3d"))
                    if 135 > ego_angle > 45:
                        crossing_direction_count += 1
                    elif ego_angle >= 135:
                        opposing_direction_count += 1

        if near_vehicle_count > 0:
            has_vehicle.append(1)
        else:
            has_vehicle.append(0)

        if near_bicycle_count > 0:
            has_bicycle.append(1)
        else:
            has_bicycle.append(0)

        if near_pedestrian_count > 0:
            has_pedestrian.append(1)
        else:
            has_pedestrian.append(0)

        has_other.append(0)

        if on_road_pedestrian_count > 0:
            has_on_road_person.append(1)
        else:
            has_on_road_person.append(0)

        if on_crosswalk_pedestrian_count > 0:
            has_on_crosswalk_person.append(1)
        else:
            has_on_crosswalk_person.append(0)

        if opposing_direction_count > 0:
            has_opposing_direction_vehicle.append(1)
        else:
            has_opposing_direction_vehicle.append(0)

        if crossing_direction_count > 0:
            has_crossing_direction_vehicle.append(1)
        else:
            has_crossing_direction_vehicle.append(0)

    if len(has_vehicle) != 0:
        has_vehicle = np.vstack(has_vehicle)
        has_bicycle = np.vstack(has_bicycle)
        has_pedestrian = np.vstack(has_pedestrian)
        has_other = np.vstack(has_other)
        has_on_road_person = np.vstack(has_on_road_person)
        has_on_crosswalk_person = np.vstack(has_on_crosswalk_person)
        has_opposing_direction_vehicle = np.vstack(has_opposing_direction_vehicle)
        has_crossing_direction_vehicle = np.vstack(has_crossing_direction_vehicle)

        actor_vec = np.hstack([has_vehicle, has_bicycle, has_pedestrian, has_other,
                               has_on_road_person, has_on_crosswalk_person,
                               has_opposing_direction_vehicle, has_crossing_direction_vehicle])
    else:
        actor_vec = np.zeros((len(frame_obj_list), 8))

    return actor_vec.tolist()

if __name__ == '__main__':
    record2vec()
