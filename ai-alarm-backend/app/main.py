# Import FastAPI framework to create the API server
from fastapi import FastAPI

# Import CORS middleware to allow frontend apps (like React) to interact with the backend
from fastapi.middleware.cors import CORSMiddleware

# Pydantic BaseModel is used to validate and structure incoming data
from pydantic import BaseModel

# Import our custom alarm scheduler function that will set up alarms
from .alarm import schedule_alarm

# Import the AI parser that converts natural language input into structured alarm data
from .ai_parser import parse_alarm_text

# Import the os module to access environment variables like PORT
import os

# Initialize a FastAPI application instance
app = FastAPI()

# Set up CORS to allow the frontend (deployed or local) to communicate with this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://alarm-clock-umber.vercel.app",  # ✅ The deployed frontend domain
        "http://localhost:3000"  # Allow localhost during development
    ],
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Define the data model for incoming POST requests to /set-alarm
class AlarmRequest(BaseModel):
    text: str  # The text input from the user like "Set alarm to drink water every 30 minutes"

# Basic root route to test if the API is running
@app.get("/")
def read_root():
    return {"message": "AI Alarm Clock API is running."}

# Endpoint to handle alarm-setting requests
@app.post("/set-alarm")
async def set_alarm(request: AlarmRequest):
    try:
        # Use the AI parser to convert user input into structured data (like time/interval)
        parsed_alarm = parse_alarm_text(request.text)

        # Pass the parsed data to the scheduler to actually create the alarm
        schedule_alarm(parsed_alarm)

        # Return success with details of the alarm set
        return {
            "status": "success",
            "alarm_time": parsed_alarm.get(
                "time", f"every {parsed_alarm['interval']} {parsed_alarm['unit']}"
            ),
            "reason": parsed_alarm["reason"]
        }
    except Exception as e:
        # If something goes wrong, return an error message
        return {"status": "error", "message": str(e)}

# When running this file directly (not importing), start the server
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))  # Get port from environment or default to 8080

    # Launch the Uvicorn server with the FastAPI app
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=False)


#This main.py is the backend controller of the AI Alarm Clock built with FastAPI. 
# It receives natural language input from the frontend, uses parse_alarm_text() to extract time, 
# interval, and reason, then schedules alarms using schedule_alarm() with APScheduler.
# CORS is enabled for frontend connection, and input is validated via AlarmRequest. 
# The /set-alarm route handles alarm creation, returning success or error responses. The app runs with uvicorn