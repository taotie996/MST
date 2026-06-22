import json
import uuid

config_list = []
base_config_id = "c_1f266f5d9b23452bb1400a383180895a"

for hour in range(24):
    for minute in [0, 15, 30, 45]:
        # 生成唯一的 entry_id
        entry_id = f"sched_{uuid.uuid4().hex}"
        time_str = f"{hour:02d}:{minute:02d}"
        
        task = {
            "entry_id": entry_id,
            "config_id": base_config_id,
            "name": "自动种田",
            "schedule_type": "daily",
            "params": {
                "interval_days": 1,
                "start_at": f"2026-03-30T{time_str}:00",
                "hour": hour,
                "minute": minute
            },
            "force_start": True,
            "enabled": True,
            "created_at": "2026-03-30T00:00:00.000000",
            "last_run": None,
            "next_run": f"2026-03-30T{time_str}:00"
        }
        config_list.append(task)

# 将生成的96个配置写入文件
with open("daily_tasks.json", "w", encoding="utf-8") as f:
    json.dump(config_list, f, ensure_ascii=False, indent=4)

print("✅ 96个任务配置已成功生成到 daily_tasks.json 中！")