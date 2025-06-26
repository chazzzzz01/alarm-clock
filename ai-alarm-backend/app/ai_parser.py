import re
import dateparser

def parse_alarm_text(text: str):
    # Match repeating alarms: "every 30 minutes", "every 2 hours"
    interval_match = re.search(r"every\s+(\d+)\s+(minute|minutes|hour|hours|second|seconds)", text, re.IGNORECASE)
    if interval_match:
        interval = int(interval_match.group(1))
        unit = interval_match.group(2).lower()
        reason_match = re.search(r"to (.+?) every", text, re.IGNORECASE)
        reason = reason_match.group(1).strip() if reason_match else "Repeating Alarm"
        return {"type": "interval", "interval": interval, "unit": unit, "reason": reason}

    # Otherwise, parse as datetime
    parsed = dateparser.parse(text)
    if not parsed:
        raise ValueError("Could not parse time")
    return {"type": "datetime", "time": parsed.isoformat(), "reason": "Generic Alarm"}
