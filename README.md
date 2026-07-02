# Sensor-to-Language: MWD Health Monitoring

This repository contains the codebase for the **Sensor-to-Language alerts and voice queries** project for Military Working Dogs (MWDs). The system is designed to translate raw physiological sensor data (like heart rate) into interpretable natural language alerts, and provides a voice interface for handlers to query the dog's status in real time.

## Project Structure

* **`app.py`**: The main application script (FastAPI/Flask or similar) that handles the NLP pipeline and API endpoints.
* **`mwd_nlp.ipynb`**: Jupyter Notebook containing the data exploration, model training, and experimentation for the anomaly detection and NLP tasks.
* **`data/`**: Contains the datasets (like `dataset.csv`), processed sensor features, and JSON event files representing detected anomalies.
* **`audio/`**: Stores audio queries (e.g., `query.wav`) used by the speech-to-text module (Whisper) for voice interaction.
* **`outputs/`**: Generated outputs such as JSON alerts and audio responses.

## Key Technologies Used
* **NLP & Text Generation:** HuggingFace Transformers (T5/BART), LangChain, spaCy.
* **Voice Interface:** OpenAI Whisper for Speech-to-Text.
* **Data Processing:** Python, Pandas, Scikit-Learn.
