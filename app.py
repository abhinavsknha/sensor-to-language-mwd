from fastapi import FastAPI
import json
import re
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

with open("outputs/generated_alerts.json", "r") as f:
    alerts = json.load(f)

alert_map = {a["dog_id"]: a for a in alerts if "dog_id" in a}


@app.get("/")
def root():
    return {
        "message": "MWD NLP Health Monitoring API is running",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/dog/{dog_id}")
def get_dog(dog_id: str):
    dog_id = dog_id.upper()

    data = alert_map.get(dog_id)

    if not data:
        return {
            "error": "Dog not found",
            "timestamp": datetime.now().isoformat()
        }

    severity = data.get("severity", "UNKNOWN")
    message = data.get("alert") or data.get("message") or "No details available"

    return {
        "dog_id": dog_id,
        "response": f"{dog_id} is currently in {severity} condition. {message}",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/critical")
def get_critical():
    results = [a for a in alerts if a.get("severity") == "CRITICAL"]

    return {
        "count": len(results),
        "response": f"There are {len(results)} critical alerts requiring immediate attention.",
        "data": results,
        "timestamp": datetime.now().isoformat()
    }


@app.get("/warning")
def get_warning():
    results = [a for a in alerts if a.get("severity") == "WARNING"]

    return {
        "count": len(results),
        "response": f"There are {len(results)} warning alerts to monitor.",
        "data": results,
        "timestamp": datetime.now().isoformat()
    }


@app.get("/query")
def query(q: str):
    try:
        q_lower = q.lower()

        if "critical" in q_lower:
            results = [a for a in alerts if a.get("severity") == "CRITICAL"]
            return {
                "response": f"There are {len(results)} critical alerts.",
                "data": results,
                "timestamp": datetime.now().isoformat()
            }

        if "warning" in q_lower:
            results = [a for a in alerts if a.get("severity") == "WARNING"]
            return {
                "response": f"There are {len(results)} warning alerts.",
                "data": results,
                "timestamp": datetime.now().isoformat()
            }

        match = re.search(r"([A-Z]{2,3})[_\s-]?(\d{3})", q.upper())

        if match:
            dog_id = f"{match.group(1)}_{match.group(2)}"
            data = alert_map.get(dog_id)

            if data:
                severity = data.get("severity", "UNKNOWN")
                message = data.get("alert") or data.get("message") or "No details available"

                return {
                    "response": f"{dog_id} status: {message} (Severity: {severity})",
                    "timestamp": datetime.now().isoformat()
                }

            return {
                "response": "Dog not found",
                "timestamp": datetime.now().isoformat()
            }

        return {
            "response": "Invalid query",
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        return {"error": str(e)}


@app.get("/demo")
def demo():
    if not alerts:
        return {"error": "No data available"}

    sample = alerts[0]

    severity = sample.get("severity", "UNKNOWN")
    message = sample.get("alert") or sample.get("message") or "No details available"

    return {
        "input": sample,
        "output": f"{sample.get('dog_id')} is in {severity} condition. {message}",
        "timestamp": datetime.now().isoformat()
    }
    
    
@app.post("/ingest")
def ingest_data(payload: dict):
    try:
        dog_id = payload.get("dog_id", "MWD_001")

        temp = payload.get("temp")
        bpm = payload.get("bpm")
        lat = payload.get("lat")
        lon = payload.get("lon")

        # ===== SIMPLE LOGIC (replace with your NLP later) =====
        severity = "NORMAL"
        message = "All vitals are stable."

        if ((temp is not None and temp > 38) or
                (bpm is not None and bpm > 110)):
            severity = "WARNING"
            message = "Elevated vitals detected."

        if ((temp is not None and temp > 39) or
                (bpm is not None and bpm > 130)):
            severity = "CRITICAL"
            message = "Severe condition detected. Immediate attention required."

        new_entry = {
            "dog_id": dog_id,
            "temp": temp,
            "bpm": bpm,
            "lat": lat,
            "lon": lon,
            "severity": severity,
            "alert": message,
            "timestamp": datetime.now().isoformat()
        }

        # Update memory
        alert_map[dog_id] = new_entry
        alerts.append(new_entry)

        return {
            "status": "success",
            "generated_alert": f"{dog_id} is {severity}. {message}"
        }

    except Exception as e:
        return {"error": str(e)}