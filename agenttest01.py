import carla

# 连接到CARLA服务器
client = carla.Client('localhost', 2000)

# 设置超时时间，单位为秒
client.set_timeout(2.0)

# 获取当前场景的世界对象
world = client.get_world()

# 获取所有车辆
vehicles = world.get_actors().filter('vehicle.*')

# 遍历所有车辆以找到当前控制的车辆
controlled_vehicle = None
for vehicle in vehicles:
    # 这里需要根据你的代理和车辆控制逻辑来确定哪个车辆是被控制的
    # 例如，你的代理可能有唯一的标识符或者特定的属性
    # 以下是一个简单的示例，我们假设控制的车辆有一个特定的标签
    if 'controlled' in vehicle.attributes:
        if vehicle.attributes['controlled'] == 'true':
            controlled_vehicle = vehicle
            break

# 如果找到了被控制的车辆，获取其信息
if controlled_vehicle:
    # 获取车辆的位置
    location = controlled_vehicle.get_location()
    print(f"Controlled Vehicle Location: {location}")

    # 获取车辆的速度
    speed = controlled_vehicle.get_velocity()
    print(f"Controlled Vehicle Speed: {speed}")

    # 获取车辆的旋转
    rotation = controlled_vehicle.get_rotation()
    print(f"Controlled Vehicle Rotation: {rotation}")

    # 获取车辆的传感器数据（如果有）
    sensors = controlled_vehicle.get_ensors()
    for sensor in sensors:
        print(f"Sensor Type: {sensor.type_id}")
        # 根据传感器类型获取数据
        # 注意：这里需要根据传感器的具体类型来调用相应的方法获取数据
else:
    print("No controlled vehicle found.")

# 断开与CARLA服务器的连接
# client.close()