import carla
import time
import logging

try:
    client = carla.Client('localhost', 2000)
    client.set_timeout(2.0)

    world = client.get_world()
    blueprint_library = world.get_blueprint_library()

    client.start_recorder('recording01.log')

    # 配置日志级别、格式和文件名
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', filename='myapp.log')

    # 记录一条日志
    logging.debug('这是一条debug日志')

    # 设置循环次数为100
    for _ in range(100):
        vehicles = world.get_actors().filter('vehicle.*')

        pedestrian = world.get_actors().filter('*pedestrian*')

        for vehicle in vehicles:
            print(f"Vehicle ID: {vehicle.id}")
            print(f"Vehicle Type: {vehicle.type_id}")
            print(f"Vehicle Location: {vehicle.get_location()}")
            print(f"Vehicle Velocity: {vehicle.get_velocity()}")
            print(f"Vehicle Acceleration: {vehicle.get_acceleration()}")
            print(f"Vehicle Angular Velocity: {vehicle.get_angular_velocity()}")
            # 移除不存在的属性调用
            # print(f"Vehicle Is Invincible: {vehicle.is_invincible}")
            # print(f"Vehicle Is Destroyed: {vehicle.is_destroyed}")
            print(f"Vehicle Speed Limit: {vehicle.get_speed_limit()}")
            print("-" * 80)

            logging.debug(f"Vehicle ID: {vehicle.id}")
            logging.debug(f"Vehicle Type: {vehicle.type_id}")
            logging.debug(f"Vehicle Location: {vehicle.get_location()}")
            logging.debug(f"Vehicle Velocity: {vehicle.get_velocity()}")
            logging.debug(f"Vehicle Acceleration: {vehicle.get_acceleration()}")
            logging.debug(f"Vehicle Angular Velocity: {vehicle.get_angular_velocity()}")
            # 移除不存在的属性调用
            # print(f"Vehicle Is Invincible: {vehicle.is_invincible}")
            # print(f"Vehicle Is Destroyed: {vehicle.is_destroyed}")
            logging.debug(f"Vehicle Speed Limit: {vehicle.get_speed_limit()}")
            logging.debug("-" * 80)

            
        time.sleep(0.05)

except KeyboardInterrupt:
    print('Cancelled by user.')
except Exception as e:
    print(f'An exception occurred: {e}')
finally:
    print('Cleaning up...')
    client.stop_recorder()
    # 移除不存在的disconnect方法调用
    # client.disconnect()
