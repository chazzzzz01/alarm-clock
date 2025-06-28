# Regular expressions module for pattern matching
import re

# Natural language date/time parser
import dateparser

# Used to work with specific times and durations
from datetime import datetime, timedelta

# Main function to parse natural language alarm text
def parse_alarm_text(text: str):
    text = text.strip().lower()  # Clean and standardize user input

    # Match phrases like "every 30 minutes", "every 2 hours"
    interval_match = re.search(r"every\s+(\d+)\s+(second|seconds|minute|minutes|hour|hours)", text, re.IGNORECASE)
    if interval_match:
        interval = int(interval_match.group(1))  # Get the number (e.g., 30)
        unit = interval_match.group(2).lower()   # Get the time unit (e.g., minutes)

        # Try to extract the reason: e.g., "to drink water every 30 minutes"
        reason_match = re.search(r"(?:to|that says)\s+(.+?)\s+every", text, re.IGNORECASE)
        reason = reason_match.group(1).strip() if reason_match else "Repeating Alarm"

        # Return a dictionary with parsed interval data
        return {
            "type": "interval",
            "interval": interval,
            "unit": unit,
            "reason": reason
        }

    # Match phrases like "in 5 minutes", "in 2 hours"
    delay_match = re.search(r"in\s+(\d+)\s+(second|seconds|minute|minutes|hour|hours)", text, re.IGNORECASE)
    if delay_match:
        amount = int(delay_match.group(1))
        unit = delay_match.group(2).lower()

        # Prepare timedelta parameters (e.g., minutes=5)
        delta_args = {unit.rstrip('s'): amount}  # Convert plural to singular for timedelta
        future_time = datetime.now() + timedelta(**delta_args)  # Calculate future time

        # Try to extract the reason: e.g., "to stretch in 10 minutes"
        reason_match = re.search(r"to\s+(.*?)\s+in", text, re.IGNORECASE)
        reason = reason_match.group(1).strip() if reason_match else "Short-term Alarm"

        # Return parsed data
        return {
            "type": "datetime",
            "time": future_time.isoformat(),
            "reason": reason
        }

    # Fallback: use natural language parsing for things like "tomorrow at 8am"
    parsed = dateparser.parse(text)
    if parsed:
        return {
            "type": "datetime",
            "time": parsed.isoformat(),
            "reason": "Generic Alarm"
        }

    # If all parsing methods fail, raise an error
    raise ValueError(f"Could not parse time from input: '{text}'")



#This parse_alarm_text() function intelligently interprets natural language input using regular expressions and dateparser. 
#It can understand repeating alarms (e.g., “every 30 minutes”), short-term delays (e.g., “in 5 minutes”), or general times (e.g., “tomorrow at 8am”). 
#It returns structured data — including type, time or interval, and reason — which is then used by the backend to schedule the alarm. 
#This AI-like logic enables the alarm clock to understand human-friendly commands.