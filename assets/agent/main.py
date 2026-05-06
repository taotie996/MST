from maa import controller
from maa.agent.agent_server import AgentServer
from maa.context import Context
from maa.custom_action import CustomAction

# 注册自定义识别器
# @AgentServer.custom_recognition("MyReco")
# class CustomReco:
#     def analyze(ctx):
#         return (10,10,100,100)  # 返回您自己处理的识别结果

# 注册自定义动作 
@AgentServer.custom_action("my_action_111")
class MyCustomAction(CustomAction):
    def run(
        self,
        ctx: Context,
        argv: CustomAction.RunArg):
        print("12345")
        ctx.tasker.controller.post_click(100, 10).wait()  # 执行点击
        # ctx.override_next(["TaskA", "TaskB"])      # 动态调整任务流

# 启动Agent服务
AgentServer.start_up("114514")
AgentServer.join()
AgentServer.shut_down()