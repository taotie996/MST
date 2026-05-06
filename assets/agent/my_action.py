
from maa import controller
from maa.agent.agent_server import AgentServer
from maa.context import Context
from maa.custom_action import CustomAction


@AgentServer.custom_action("my_action_111")
class MyCustomAction(CustomAction):

    def run(
        self,
        context: Context,
        argv: CustomAction.RunArg,
    ) -> bool:

        controller.post_click(100, 10).wait()  # 执行点击
        context.override_next(["TaskA", "TaskB"])      # 动态调整任务流
        return True
