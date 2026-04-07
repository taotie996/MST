import sys

from maa.controller import AdbController
from maa.resource import Resource
from maa.tasker import Tasker
from maa.toolkit import Toolkit

# 如果你使用的是桌面端/窗口控制，可能需要引入 Win32Controller

if __name__ == "__main__":
    # 初始化 Toolkit
    Toolkit.init_option("./")

    # ==========================================
    # 1. 配置并连接 Controller (以 ADB 连接模拟器为例)
    # ==========================================
    # 请根据你实际使用的模拟器修改 adb_path 和 address（端口号）
    # 比如：雷电默认是 emulator-5554，Mumu12 可能是 127.0.0.1:16384
    controller = AdbController(
        adb_path="I:\\Emulators\\MuMu\\nx_main\\adb.exe", 
        address="127.0.0.1:16384" 
    )
    
    print("正在连接设备...")
    if not controller.post_connection().wait().succeeded:
        print("设备连接失败，请检查 ADB 设置！")
        sys.exit(1)
    print("设备连接成功！")

    # ==========================================
    # 2. 配置并加载 Resource (加载任务 pipeline 和图片资源)
    # ==========================================
    resource = Resource()
    
    print("正在加载资源...")
    # 这里的路径应当指向包含 pipeline.json 和 image 文件夹的资源根目录
    print(resource.loaded)
    if not resource.post_bundle("F:\\Code\\MST\\assets\\resource").wait().succeeded:
        print("资源加载失败，请检查路径！")
        sys.exit(1)
    print("资源加载成功！")

    # ==========================================
    # 3. 创建 Tasker 并绑定
    # ==========================================
    tasker = Tasker()
    # 必须将资源和控制器绑定到 Tasker 上
    tasker.bind(resource, controller)

    if not tasker.inited:
        print("Tasker 初始化失败！")
        sys.exit(1)

    # ==========================================
    # 4. 执行任务
    # ==========================================
    # print("开始执行任务：日常任务_种田")
    # 现在 Tasker 有了眼睛（Resource）和手（Controller），可以开始干活了
    task_result = tasker.post_task("ui_返回主界面").wait()
    
    if task_result.succeeded:
        print("任务执行成功！")
    else:
        print("任务执行失败！")