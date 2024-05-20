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

        # 配置日志级别、格式和文件名
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', filename='myapp1.log')

        # 记录一条日志
        logging.debug('这是一条debug日志')

        # 设置一个持续5分钟的计时器 5 * 60
        duration = 1 * 20
        start_time = time.time()

        while time.time() - start_time < duration:
            # 获取所有车辆、行人和交通信号灯
            vehicles = world.get_actors().filter('vehicle.*')
            pedestrians = world.get_actors().filter('walker.pedestrian.*')
            traffic_lights = world.get_actors().filter('traffic.traffic_light')

            # 输出信息
            pt = time.time() - start_time
            print(f"Time: {pt:.2f}s")
            logging.debug(f"Time: {pt:.2f}s")
            print(f"Vehicles: {len(vehicles)}")
            print(f"Pedestrians: {len(pedestrians)}")
            print(f"Traffic Lights: {len(traffic_lights)}")

            # 循环输出车辆信息
            for vehicle in vehicles:
                # json_string = json.dumps(vehicle)
                # print(f"Vehicle attr: {vars(vehicle)}")
                # print(f"Vehicle : {json_string}")
                # 移除不存在的属性调用
                # print(f"Vehicle Is Invincible: {vehicle.is_invincible}")
                # print(f"Vehicle Is Destroyed: {vehicle.is_destroyed}")
                # print(f"Vehicle Speed Limit: {vehicle.get_speed_limit()}")
                # print("-" * 80)

                logging.debug(f"Vehicle ID: {vehicle.id}")
                logging.debug(f"Vehicle Type: {vehicle.type_id}")
                logging.debug(f"Vehicle Location: {vehicle.get_location()}")
                logging.debug(f"Vehicle Velocity: {vehicle.get_velocity()}")
                logging.debug(f"Vehicle Acceleration: {vehicle.get_acceleration()}")
                logging.debug(f"Vehicle Angular Velocity: {vehicle.get_angular_velocity()}")
                logging.debug(f"Vehicle Angular attributes: {vehicle.attributes}")
                # 移除不存在的属性调用
                # print(f"Vehicle Is Invincible: {vehicle.is_invincible}")
                # print(f"Vehicle Is Destroyed: {vehicle.is_destroyed}")
                logging.debug(f"Vehicle Speed Limit: {vehicle.get_speed_limit()}")

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
                
                for key, value in inspect.getmembers(tls):
                    if not key.startswith('__'):
                        logging.debug(f"{key}: {value}")
                # 使用 "+" * 40 分隔每一个信号灯信息            
                logging.debug("+" * 40)

            # 使用 "+" * 70 分隔信号灯信息

            # 使用 "*" * 80 分隔每一帧
            logging.debug("*" * 80)
            # 等待0.5秒
            time.sleep(0.49)

    finally:
        print('Done.')

if __name__ == '__main__':
    main()
