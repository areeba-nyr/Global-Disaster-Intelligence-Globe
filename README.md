# 🌍 Global Disaster Intelligence Globe

**A live, interactive 3D globe visualizing real-time global disaster activity — earthquakes, flood risk zones, fault lines, and historic events — in one place.**

![Status](https://img.shields.io/badge/status-working-brightgreen)
![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?logo=flask&logoColor=white)

---

## 🧭 The Problem

Most people don't have one easy, visual place to see real-time global disaster activity. News coverage is scattered, and there's no simple way to see current earthquakes, flood-risk zones, and historic disaster patterns together, in context.

## 💡 The Solution

A live 3D globe that pulls **real, free public data** and displays it as interactive layers:

- 🔴 **Live Earthquakes** — real-time data from the USGS (US Geological Survey)
- 🟣 **Fault Lines** — major known fault lines worldwide (San Andreas, North Anatolian, etc.)
- 🔵 **Flood Risk Zones** — major flood-prone river basins and deltas globally
- 🟡 **Historic Disasters** — major past events for context (2004 Indian Ocean Tsunami, 2011 Tohoku, 2023 Turkey-Syria earthquake, and more)
- ⚠️ **Elevated Activity Alerts** — a transparent, rule-based system that flags fault lines with multiple recent live earthquakes nearby. **This is not a machine-learning prediction** — it's an honest, explainable rule based on real current data.

## 👤 Who This Helps

Anyone wanting quick situational awareness of global disaster activity — students, researchers, journalists, or anyone curious about what's happening on Earth right now, with historical context.

## 🛠️ How It Was Built

- **Backend:** Python, Flask
- **3D Rendering:** Three.js (WebGL)
- **Data Sources:** USGS Earthquake API (free, live), Open-Meteo Weather API (free, live) — no paid APIs or keys required
- **AI Assistance:** Built and reworked with help from Claude (Anthropic). This project builds on an earlier, Pakistan-focused version, significantly expanded and reworked to be global, with the Elevated Activity Alert feature added, for this submission.

## 🧩 Challenges & What I Learned

Working with live public APIs reliably was the biggest challenge — making sure the app stays functional even if a data source doesn't respond (handled with a clearly-labeled simulated-data fallback). I also learned to keep the "alert" feature honest and explainable rather than overstating it as prediction.

## 🚀 How to Run It

```bash
python -m venv myenv
myenv\Scripts\activate       # Windows
pip install -r requirements.txt
python app.py
```

Then open `http://localhost:5000` in your browser.

## 📦 Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| 3D Visualization | Three.js |
| Earthquake Data | USGS (live, free) |
| Weather Data | Open-Meteo (live, free) |
| AI Assistance | Claude (Anthropic) |

## ⚠️ Note on Environment Variables

This project currently uses no API keys — all data sources are free and public. If extended in the future to use a key-requiring service, it should be stored in a `.env` file (excluded via `.gitignore`) and loaded with `python-dotenv`, never hardcoded directly in the source code.
