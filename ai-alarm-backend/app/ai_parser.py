import re
import dateparser
from datetime import datetime, timedelta

def parse_alarm_text(text: str):
    text = text.strip().lower()

    # Match repeating alarms: "every 30 minutes", "every 2 hours"
    interval_match = re.search(r"every\s+(\d+)\s+(second|seconds|minute|minutes|hour|hours)", text, re.IGNORECASE)
    if interval_match:
        interval = int(interval_match.group(1))
        unit = interval_match.group(2).lower()
        reason_match = re.search(r"(?:to|that says)\s+(.+?)\s+every", text, re.IGNORECASE)
        reason = reason_match.group(1).strip() if reason_match else "Repeating Alarm"
        return {
            "type": "interval",
            "interval": interval,
            "unit": unit,
            "reason": reason
        }

    # Match short-term delay: "in 2 seconds", "in 5 minutes", etc.
    delay_match = re.search(r"in\s+(\d+)\s+(second|seconds|minute|minutes|hour|hours)", text, re.IGNORECASE)
    if delay_match:
        amount = int(delay_match.group(1))
        unit = delay_match.group(2).lower()

        delta_args = {unit.rstrip('s'): amount}  # remove 's' if plural
        future_time = datetime.now() + timedelta(**delta_args)

        reason_match = re.search(r"to\s+(.*?)\s+in", text, re.IGNORECASE)
        reason = reason_match.group(1).strip() if reason_match else "Short-term Alarm"

        return {
            "type": "datetime",
            "time": future_time.isoformat(),
            "reason": reason
        }

    # Fallback to natural language parser (e.g., "tomorrow at 8am")
    parsed = dateparser.parse(text)
    if parsed:
        return {
            "type": "datetime",
            "time": parsed.isoformat(),
            "reason": "Generic Alarm"
        }

    raise ValueError(f"Could not parse time from input: '{text}'")
