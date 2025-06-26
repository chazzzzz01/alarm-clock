from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.alarm import schedule_alarm
from app.ai_parser import parse_alarm_text

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AlarmRequest(BaseModel):
    text: str

@app.post("/set-alarm")
async def set_alarm(request: AlarmRequest):
    try:
        parsed_alarm = parse_alarm_text(request.text)
        schedule_alarm(parsed_alarm)

        return {
            "status": "success",
            "alarm_time": parsed_alarm.get("time", f"every {parsed_alarm['interval']} {parsed_alarm['unit']}"),
            "reason": parsed_alarm["reason"]
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}
