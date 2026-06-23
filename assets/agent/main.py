import re
from _sitebuiltins import _Printer
from maa import controller
from maa.agent.agent_server import AgentServer
from maa.context import Context
from maa.custom_action import CustomAction
from maa.custom_recognition import CustomRecognition
# from maa.pipeline import JOCR
# 注册自定义识别器
# @AgentServer.custom_recognition("MyReco")
# class CustomReco:
#     def analyze(ctx):
#         return (10,10,100,100)  # 返回您自己处理的识别结果

# 注册自定义动作


# context is a reference, will override the pipeline for whole task
# context.override_pipeline({"MyCustomOCR": {"roi": [1, 1, 114, 514]}})
# # context.run_recognition ...

# # make a new context to override the pipeline, only for itself
# new_context = context.clone()
# new_context.override_pipeline({"MyCustomOCR": {"roi": [100, 200, 300, 400]}})
# reco_detail = new_context.run_recognition("MyCustomOCR", argv.image)

# click_job = context.tasker.controller.post_click(10, 20)
# click_job.wait()

# context.override_next(argv.node_name, ["TaskA", "TaskB"])


# return CustomRecognition.AnalyzeResult(
#     box=(0, 0, 100, 100), detail="Hello World!"
# )
@AgentServer.custom_action("分配事务")
class InitTransactionState(CustomAction):
    def run(self, context: Context, argv: CustomAction.RunArg) -> bool:
        # 1. 获取当前画面的缓存截图
        image = context.tasker.controller.cached_image
        if image is None:
            # 如果没有缓存，主动请求一张新截图
            image = context.tasker.controller.post_screencap().wait().get()

        # 2. 调用第一个 OCR 节点
        reco_1 = context.run_recognition("get刷新次数", image)
        text_1 = reco_1.best_result.text if reco_1 and reco_1.best_result else ""

        # 正则提取数字
        pattern1 = r"(\d+)"
        match1 = re.search(pattern1, text_1)
        if match1:
            free_refresh_count = int(match1.group(1))

        else:
            free_refresh_count = 0

        # 3. 调用第二个 OCR 节点
        reco_2 = context.run_recognition("get事务次数", image)
        text_2 = reco_2.best_result.text if reco_2 and reco_2.best_result else ""

        pattern2 = r"(\d+)/(\d+)"
        match2 = re.search(pattern2, text_2)
        if match2:
            transaction_count = int(match2.group(2))
        else:
            transaction_count = 0

        # context.set_variable("free_refresh_count", free_refresh_count)
        # context.set_variable("transaction_count", transaction_count)

        print("刷新次数：", free_refresh_count)
        print("事务次数：", transaction_count)

        return True


# @AgentServer.custom_action("Update_Refresh_Count")
# class UpdateRefreshCount(CustomAction):
#     def run(self, ctx: Context, argv: CustomAction.RunArg):
#         global remaining_refreshes
#         rec_detail = argv.rec_detail
#         if rec_detail and rec_detail.text:
#             import re

#             match = re.search(r"\d+", rec_detail.text)
#             if match:
#                 remaining_refreshes = int(match.group())
#                 print(f"OCR读取刷新次数成功: {remaining_refreshes}")
#         else:
#             remaining_refreshes -= 1
#             if remaining_refreshes < 0:
#                 remaining_refreshes = 0
#             print(f"未通过OCR读取，默认刷新次数减1: {remaining_refreshes}")
#         return True


# @AgentServer.custom_action("Record_Task_Accepted")
# class RecordTaskAccepted(CustomAction):
#     def run(self, ctx: Context, argv: CustomAction.RunArg):
#         global tasks_remaining
#         tasks_remaining -= 1
#         if tasks_remaining < 0:
#             tasks_remaining = 0
#         print(f"接取任务成功，剩余任务: {tasks_remaining}")
#         return True


# def evaluate_3_star_logic(slot_num: int, ctx: Context):
#     global remaining_refreshes, tasks_remaining
#     print(
#         f"槽位{slot_num} 遇到3星任务。当前剩余刷新: {remaining_refreshes}, 剩余任务: {tasks_remaining}"
#     )
#     # 保守策略: 剩余刷新 > 剩余任务 * 2 时才刷新3星
#     if remaining_refreshes > tasks_remaining * 2:
#         print("策略判定: 次数充裕，点击刷新争取4星！")
#         ctx.override_next([f"槽位{slot_num}_刷新"])
#     else:
#         print("策略判定: 次数紧张，收手接取3星！")
#         ctx.override_next([f"槽位{slot_num}_接取"])
#     return True


# @AgentServer.custom_action("Evaluate_3_Star_Slot1")
# class Evaluate3StarSlot1(CustomAction):
#     def run(self, ctx: Context, argv: CustomAction.RunArg):
#         return evaluate_3_star_logic(1, ctx)


# @AgentServer.custom_action("Evaluate_3_Star_Slot2")
# class Evaluate3StarSlot2(CustomAction):
#     def run(self, ctx: Context, argv: CustomAction.RunArg):
#         return evaluate_3_star_logic(2, ctx)


# @AgentServer.custom_action("Evaluate_3_Star_Slot3")
# class Evaluate3StarSlot3(CustomAction):
#     def run(self, ctx: Context, argv: CustomAction.RunArg):
#         return evaluate_3_star_logic(3, ctx)


# @AgentServer.custom_action("Evaluate_3_Star_Slot4")
# class Evaluate3StarSlot4(CustomAction):
#     def run(self, ctx: Context, argv: CustomAction.RunArg):
#         return evaluate_3_star_logic(4, ctx)


# @AgentServer.custom_action("Evaluate_3_Star_Slot5")
# class Evaluate3StarSlot5(CustomAction):
#     def run(self, ctx: Context, argv: CustomAction.RunArg):
#         return evaluate_3_star_logic(5, ctx)


# 启动Agent服务


def main():
    print("启动")
    AgentServer.start_up("114514")
    AgentServer.join()
    AgentServer.shut_down()


if __name__ == "__main__":
    main()
