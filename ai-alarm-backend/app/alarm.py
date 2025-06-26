from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

scheduler = BackgroundScheduler()
scheduler.start()

def notify_user(reason):
    print(f"[{datetime.now()}] ⏰ Alarm: {reason}")

def schedule_alarm(parsed_alarm):
    if parsed_alarm["type"] == "interval":
        unit_map = {
            "minute": "minutes",
            "minutes": "minutes",
            "hour": "hours",
            "hours": "hours",
            "second": "seconds",
            "seconds": "seconds",
        }

        trigger_args = {unit_map[parsed_alarm["unit"]]: parsed_alarm["interval"]}

        scheduler.add_job(
            notify_user,
            trigger="interval",
            kwargs={"reason": parsed_alarm["reason"]},
            **trigger_args
        )

    elif parsed_alarm["type"] == "datetime":
        dt = datetime.fromisoformat(parsed_alarm["time"])
        scheduler.add_job(
            notify_user,
            trigger="date",
            run_date=dt,
            kwargs={"reason": parsed_alarm["reason"]}
        )
