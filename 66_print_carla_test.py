import carla
import time
import logging
import inspect


def main():
    try:
        # 连接到CARLA服务器
        client = carla.Client('localhost', 2000)
        client.set_timeout(2.0)

        # 获取世界和蓝图库
        world = client.get_world()
        blueprint_library = world.get_blueprint_library()
        map_instance = world.get_map()

        # 配置日志级别、格式和文件名
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s',
                            filename='myapp6.1.log')

        # 记录一条日志
        logging.debug('这是一条debug日志')
        for key, value in inspect.getmembers(map_instance):
            if not key.startswith('__'):
                logging.debug(f"{key}: {value}")

        map_crosswalks = map_instance.get_crosswalks()
        logging.debug(f"map_crosswalks_length: {len(map_crosswalks)}")
        # 分隔 map_crosswalks
        logging.debug("+" * 70)
        for crosswalk in map_crosswalks:
            for key, value in inspect.getmembers(crosswalk):
                if not key.startswith('__'):
                    logging.debug(f"{key}: {value}")

            # 使用 "+" * 60 分隔每一个crosswalk的信息
            logging.debug("+" * 60)
        # 分隔 junctions
        logging.debug("+" * 70)
        # 获取地图的拓扑结构
        topology = map_instance.get_topology()
        # 遍历交叉路口并打印信息
        # for waypoint in topology:
        #     print("waypoint:")
        #     print(waypoint)
        #     # 检查是否是交叉路口
        #     if waypoint.is_junction:
        #         for key, value in inspect.getmembers(waypoint):
        #             if not key.startswith('__'):
        #                 logging.debug(f"{key}: {value}")
        #         # 使用 "+" * 60 分隔每一个junctions的信息
        #         logging.debug("+" * 60)
            
        # 创建一个字典来存储每个Waypoint的连接数
        waypoint_connections ={}
        # 遍历拓扑结构，统计每个Waypoint的连接数
        for waypoint_pair in topology:
            for waypoint in waypoint_pair:
                if waypoint in waypoint_connections: 
                    waypoint_connections[waypoint]+=1
                else: 
                    waypoint_connections[waypoint]=1
        # 识别连接数大于2的Waypoint作为交叉路口
        intersections ={wp for wp, count in waypoint_connections.items()if count >2}
        for waypoint in intersections:
            for key, value in inspect.getmembers(waypoint):
                if not key.startswith('__'):
                    logging.debug(f"{key}: {value}")
            # 使用 "+" * 60 分隔每一个junctions的信息
            logging.debug("+" * 60)

        logging.debug("*" * 90)

        # 设置一个持续5分钟的计时器 5 * 60
        duration = 1 * 20
        start_time = time.time()

        step_time = 0.5

        while time.time() - start_time < duration:
            # 时间信息
            pt = time.time() - start_time
            print(f"Time: {pt:.2f}s")
            logging.debug(f"Time: {pt:.2f}s")

            # 获取所有车辆、行人和交通信号灯
            vehicles = world.get_actors().filter('vehicle.*')
            pedestrians = world.get_actors().filter('walker.pedestrian.*')
            traffic_lights = world.get_actors().filter('traffic.traffic_light')
            traffic_signs = world.get_actors().filter('traffic.sign.*')

            # 输出信息
            print(f"Vehicles: {len(vehicles)}")
            print(f"Pedestrians: {len(pedestrians)}")
            print(f"Traffic Lights: {len(traffic_lights)}")
            print(f"Traffic Signs: {len(traffic_signs)}")

            # 循环输出车辆信息
            for vehicle in vehicles:
                logging.debug(f"Vehicle_ID: {vehicle.id}")
                logging.debug(f"Vehicle_Type: {vehicle.type_id}")
                logging.debug(f"Vehicle_Location: {vehicle.get_location()}")
                logging.debug(f"Vehicle_Velocity: {vehicle.get_velocity()}")
                logging.debug(f"Vehicle_Acceleration: {vehicle.get_acceleration()}")
                logging.debug(f"Vehicle_Angular_Velocity: {vehicle.get_angular_velocity()}")
                logging.debug(f"traffic_light: {vehicle.get_traffic_light()}")
                logging.debug(f"traffic_light_state: {vehicle.get_traffic_light_state()}")
                transform = vehicle.get_transform()
                logging.debug(f"transform: {transform}")
                logging.debug(f"forward_vector: {transform.get_forward_vector()}")
                # logging.debug(f"wheel_steer_angle: {vehicle.get_wheel_steer_angle()}")
                # 是否受到路灯影响
                logging.debug(f"vehicle_is_at_traffic_light: {vehicle.is_at_traffic_light()}")
                logging.debug(f"Vehicle_Velocity_value: {vehicle.get_velocity().length()}")
                # 获取车辆控制信息
                vehicle_control = vehicle.get_control()
                # 获取方向盘的偏转角度
                steering_angle = vehicle_control.steer
                logging.debug(f"Vehicle_steering_angle: {steering_angle}")
                logging.debug(f"Vehicle_Speed_Limit: {vehicle.get_speed_limit()}")

                logging.debug("-" * 40)
                for key, value in inspect.getmembers(vehicle):
                    if not key.startswith('__'):
                        logging.debug(f"{key}: {value}")

                # 使用 "-" * 60 分隔每一辆车的信息
                logging.debug("-" * 60)

            # 使用 "*" * 70 分隔车辆信息与信号灯信息
            logging.debug("*" * 70)

            # 循环输出交通信号灯信息
            for tls in traffic_lights:
                logging.debug(f"Location: {tls.get_location()}")
                for key, value in inspect.getmembers(tls):
                    if not key.startswith('__'):
                        logging.debug(f"{key}: {value}")
                # 使用 "+" * 40 分隔每一个信号灯信息
                logging.debug("+" * 40)

            # 使用 "+" * 70 分隔信号灯信息
            logging.debug("*" * 70)

            # 循环输出交通标识
            for tls in traffic_signs:
                if tls['type_id'] != "traffic.traffic_light":
                    logging.debug(f"Location: {tls.get_location()}")
                    for key, value in inspect.getmembers(tls):
                        if not key.startswith('__'):
                            logging.debug(f"{key}: {value}")
                    # 使用 "+" * 50 分隔每一个信号灯信息
                    logging.debug("+" * 50)

            # 使用 "+" * 70 分隔交通标识信息
            logging.debug("*" * 70)

            # 循环输出行人
            for pedestrian in pedestrians:
                # 获取行人的位置
                walker_location = pedestrian.get_location()
                logging.debug(f"Location: {walker_location}")
                # 使用行人的位置获取 Waypoint
                waypoint = map_instance.get_waypoint(walker_location)
                # 判断行人是否在道路上
                is_walker_on_road = waypoint is not None
                logging.debug(f"is_walker_on_road: {is_walker_on_road}")
                for key, value in inspect.getmembers(pedestrian):
                    if not key.startswith('__'):
                        logging.debug(f"{key}: {value}")
                # 使用 "+" * 40 分隔每一个行人信息
                logging.debug("+" * 40)

            # 使用 "*" * 80 分隔每一帧
            logging.debug("*" * 80)

            sleep_time = start_time + step_time + pt - time.time()
            print(f"sleep_time: {sleep_time}")
            # 等待0.5秒
            time.sleep(sleep_time)

    finally:
        print('Done.')


if __name__ == '__main__':
    main()
