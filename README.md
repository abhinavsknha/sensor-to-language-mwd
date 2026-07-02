# Sensor-to-Language: An NLP Framework for Interpretable Health Monitoring of Military Working Dogs

## Overview
Monitoring the physiological state of Military Working Dogs (MWDs) is critical for mission success and canine welfare. Existing smart collars collect vital signs (heart rate, temperature, GPS) using wearable hardware and trigger threshold-based alarms. However, these systems output raw data that require human interpretation, which can be slow or error-prone in the field. 

This project proposes an NLP-based extension that automatically translates sensor streams into natural language alerts and allows voice-query access. Specifically, the system employs an anomaly detection layer to flag unusual readings and feeds structured sensor events to a transformer-based natural language generation (NLG) model. This model produces concise human-readable status reports (e.g., *"Rex's heart rate is high; possible stress detected"*).

Additionally, a speech interface (using Whisper) lets handlers query dog status hands-free. This multimodal sensor-language framework aims to enhance situational awareness and response time by bridging the gap between raw wearable data and actionable insights for handlers.

## Objectives
1. **Anomaly Detection:** Design a pipeline for MWD sensor data (heart rate, temperature, GPS) to detect events requiring alerts (e.g., tachycardia, hyperthermia).
2. **Natural Language Generation (NLG):** Develop a module that maps structured events (sensor anomalies) into concise, human-readable status reports and warnings.
3. **Voice Interface:** Implement a speech interface using on-device speech-to-text (e.g. Whisper) allowing handlers to ask questions (e.g. *"Is Rex OK?"*) and receive verbal status responses.
4. **End-to-End Integration:** Integrate system components on wearable and mobile/edge devices: sensor collection → data preprocessing → anomaly flagging → NLP model → alert output.
5. **Evaluation:** Evaluate performance by measuring alert accuracy and usability (handler response time with/without NLP alerts).

## Proposed Architecture
The system consists of embedded sensing, data processing, and NLP/communication components:

* **Smart Collar (Wearable Module)**
  * **Sensors:** Heart Rate, Body Temperature, GPS.
  * **Functions:** Raw data acquisition, preliminary noise filtering, packetization.
  * **Transmission:** Send processed sensor packets to base station via WiFi/BLE/LoRa.

* **Base Station / Edge Server**
  * **Preprocessing Layer:** Receives sensor streams; applies smoothing, computes features (e.g., short-term average HR, variance).
  * **Anomaly Detection Module:** Compares features to thresholds or runs a small ML model to flag abnormal vitals.
  * **Event Representation:** Generates a structured JSON event object when an anomaly is detected.

* **NLP Processing Layer**
  * **Input:** Structured event JSON.
  * **Process:** Template-based prompting or fine-tuned transformer (e.g., T5 or BART) for Natural Language Generation (NLG).
  * **Output:** Natural language alert string (e.g., *"Warning: Rex's heart rate is 155 bpm and temperature is 39.8°C. Both are above normal. Possible heat stress. Location: Zone B."*).

* **Voice Interaction Module**
  * **Input:** Handler voice query via ASR model (OpenAI Whisper).
  * **NLP Intent Recognition:** Parse query to identify dog ID and query intent.
  * **Query Response:** Retrieves the latest status and generates a natural language response.

## Tech Stack & Tools
* **HuggingFace Transformers:** Pre-trained transformer models (T5, BART) for natural language generation of alerts.
* **OpenAI Whisper:** Open-source speech-to-text model to enable voice queries.
* **LangChain:** To orchestrate the NLP pipeline (manage prompts, chain sensor inputs to LLM outputs).
* **spaCy:** For NLP preprocessing in the voice query module (entity or intent recognition).
* **FastAPI:** Lightweight Python web framework to host the NLP services (NLG, ASR) as APIs.
* **PyTorch/TensorFlow:** Backend for running transformer models and anomaly detection ML.
* **TensorFlow Lite:** For running lightweight ML models directly on the wearable hardware.
