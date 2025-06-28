# Import the background scheduler from APScheduler to run jobs in the background
from apscheduler.schedulers.background import BackgroundScheduler

# Import datetime for setting specific times
from datetime import datetime

# Create and start the background scheduler
scheduler = BackgroundScheduler()
scheduler.start()

# Function to simulate alarm notification (could be replaced with sound, popup, etc.)
def notify_user(reason):
    print(f"[{datetime.now()}] ⏰ Alarm: {reason}")

# Main function to schedule alarms based on parsed input
def schedule_alarm(parsed_alarm):
    if parsed_alarm["type"] == "interval":
        # Map parsed units to APScheduler-compatible time keys
        unit_map = {
            "minute": "minutes",
            "minutes": "minutes",
            "hour": "hours",
            "hours": "hours",
            "second": "seconds",
            "seconds": "seconds",
        }

        # Create the trigger argument for interval (e.g., minutes=30)
        trigger_args = {unit_map[parsed_alarm["unit"]]: parsed_alarm["interval"]}

        # Add a recurring job to the scheduler
        scheduler.add_job(
            notify_user,                  # Function to run
            trigger="interval",           # Trigger type: interval-based
            kwargs={"reason": parsed_alarm["reason"]},  # Pass the reason to the function
            **trigger_args                # Pass interval timing (e.g., minutes=30)
        )

    elif parsed_alarm["type"] == "datetime":
        # Convert the parsed ISO format string to datetime object
        dt = datetime.fromisoformat(parsed_alarm["time"])

        # Schedule a one-time job at the specified date and time
        scheduler.add_job(
            notify_user,                  # Function to run
            trigger="date",               # Trigger type: fixed date/time
            run_date=dt,                  # Exact datetime to run
            kwargs={"reason": parsed_alarm["reason"]}  # Pass the reason
        )


# This file handles scheduling alarms using the APScheduler library. 
# It defines schedule_alarm(), which takes the parsed output from user input and either sets a repeating alarm (like “every 30 minutes”) or a one-time alarm (like “tomorrow at 8am”). 
# The notify_user() function simulates an alert by printing a message with the current time and reason. 
# This module is the “clockwork engine” that makes sure alarms go off as intended based on parsed input.