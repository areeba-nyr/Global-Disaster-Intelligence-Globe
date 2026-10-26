"""
Global Disaster Intelligence Globe
Real-time 3D visualization of global disaster activity
Live data: USGS Earthquakes + OpenAQ Air Quality + Open-Meteo Weather + Flood zones
"""

from flask import Flask, render_template, jsonify
import urllib.request, urllib.error
import json, random, math
from datetime import datetime, timedelta

app = Flask(__name__)

# ── GLOBAL CITIES ────────────────────────────────────────────────────────────
CITIES = {
    "lahore":       {"name":"Lahore",       "lat":31.5497,"lng":74.3436,"pop":"14M"},
    "karachi":      {"name":"Karachi",      "lat":24.8607,"lng":67.0011,"pop":"16M"},
    "tokyo":        {"name":"Tokyo",        "lat":35.6762,"lng":139.6503,"pop":"37M"},
    "jakarta":      {"name":"Jakarta",      "lat":-6.2088,"lng":106.8456,"pop":"34M"},
    "manila":       {"name":"Manila",       "lat":14.5995,"lng":120.9842,"pop":"14M"},
    "mexico_city":  {"name":"Mexico City",  "lat":19.4326,"lng":-99.1332,"pop":"22M"},
    "los_angeles":  {"name":"Los Angeles",  "lat":34.0522,"lng":-118.2437,"pop":"13M"},
    "istanbul":     {"name":"Istanbul",     "lat":41.0082,"lng":28.9784,"pop":"15M"},
    "kathmandu":    {"name":"Kathmandu",    "lat":27.7172,"lng":85.3240,"pop":"1.5M"},
    "santiago":     {"name":"Santiago",     "lat":-33.4489,"lng":-70.6693,"pop":"6.8M"},
    "wellington":   {"name":"Wellington",   "lat":-41.2865,"lng":174.7762,"pop":"0.4M"},
    "san_francisco":{"name":"San Francisco","lat":37.7749,"lng":-122.4194,"pop":"0.9M"},
}

# ── MAJOR GLOBAL FAULT LINES ───────────────────────────────────────────────────
FAULT_LINES = [
    {"name":"San Andreas Fault","coords":[[32.7,-115.5],[34.0,-117.3],[36.0,-120.5],[38.8,-123.0]],"type":"strike-slip","risk":"critical"},
    {"name":"Chaman Fault","coords":[[30.9,66.4],[31.9,67.0],[32.9,67.6],[33.9,68.2],[34.9,68.8]],"type":"strike-slip","risk":"critical"},
    {"name":"North Anatolian Fault","coords":[[40.7,29.0],[40.8,33.0],[40.5,37.0],[39.5,40.0]],"type":"strike-slip","risk":"critical"},
    {"name":"Japan Median Tectonic Line","coords":[[35.0,135.5],[34.5,137.5],[34.0,139.5]],"type":"strike-slip","risk":"high"},
    {"name":"Main Karakoram Thrust","coords":[[35.5,74.0],[35.8,75.5],[36.1,76.8],[36.3,77.9]],"type":"thrust","risk":"high"},
    {"name":"Sunda Megathrust","coords":[[-6.0,105.0],[-4.0,101.0],[2.0,96.0],[6.0,94.0]],"type":"subduction","risk":"critical"},
    {"name":"Makran Subduction Zone","coords":[[25.0,61.0],[25.2,62.5],[25.3,64.0],[25.2,65.5],[25.0,67.0]],"type":"subduction","risk":"high"},
]

# ── HISTORIC DISASTERS (GLOBAL) ────────────────────────────────────────────────
HISTORIC = [
    {"name":"2005 Kashmir Earthquake","lat":34.493,"lng":73.629,"magnitude":7.6,"deaths":87350,"year":2005,"type":"earthquake"},
    {"name":"2004 Indian Ocean Earthquake & Tsunami","lat":3.3,"lng":95.9,"magnitude":9.1,"deaths":227898,"year":2004,"type":"earthquake"},
    {"name":"2011 Tohoku Earthquake & Tsunami","lat":38.3,"lng":142.4,"magnitude":9.1,"deaths":19759,"year":2011,"type":"earthquake"},
    {"name":"2010 Haiti Earthquake","lat":18.457,"lng":-72.533,"magnitude":7.0,"deaths":316000,"year":2010,"type":"earthquake"},
    {"name":"2022 Pakistan Mega Floods","lat":27.0,"lng":68.0,"magnitude":None,"deaths":1739,"year":2022,"type":"flood","area":"33M hectares"},
    {"name":"2023 Turkey-Syria Earthquake","lat":37.17,"lng":37.03,"magnitude":7.8,"deaths":59259,"year":2023,"type":"earthquake"},
    {"name":"2023 Harnai Earthquake","lat":30.1,"lng":67.9,"magnitude":5.9,"deaths":20,"year":2023,"type":"earthquake"},
]

def fetch_usgs_earthquakes():
    """Fetch real earthquakes from USGS API - affected region"""
    url = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&minmagnitude=3.5&orderby=time&limit=50"
    try:
        req = urllib.request.Request(url, headers={"User-Agent":"GlobalDisasterWatch/1.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
            quakes = []
            for f in data.get("features", []):
                p = f["properties"]
                c = f["geometry"]["coordinates"]
                quakes.append({
                    "id": f["id"],
                    "lat": c[1], "lng": c[0], "depth": c[2],
                    "magnitude": p["mag"],
                    "place": p["place"] or "affected region",
                    "time": datetime.fromtimestamp(p["time"]/1000).strftime("%d %b %H:%M"),
                    "url": p["url"],
                    "type": "earthquake",
                    "source": "USGS Live"
                })
            return quakes, "live"
    except Exception as e:
        return generate_fake_quakes(), "simulated"

def generate_fake_quakes():
    """Realistic Pakistan earthquake simulation"""
    hotspots = [
        (34.5, 73.6, "Kashmir"),
        (30.9, 66.4, "Balochistan"),
        (30.2, 67.0, "Quetta region"),
        (35.5, 74.0, "Karakoram"),
        (25.2, 63.5, "Makran Coast"),
        (33.7, 73.1, "Islamabad region"),
        (34.0, 71.5, "KPK"),
    ]
    quakes = []
    for i in range(random.randint(8, 18)):
        base = random.choice(hotspots)
        mag = round(random.uniform(2.1, 6.2), 1)
        hrs_ago = random.randint(0, 72)
        t = datetime.now() - timedelta(hours=hrs_ago)
        quakes.append({
            "id": f"sim_{i}",
            "lat": base[0] + random.uniform(-1.5, 1.5),
            "lng": base[1] + random.uniform(-1.5, 1.5),
            "depth": round(random.uniform(5, 80), 1),
            "magnitude": mag,
            "place": f"{round(random.uniform(5,80))}km from {base[2]}",
            "time": t.strftime("%d %b %H:%M"),
            "type": "earthquake",
            "source": "Simulated"
        })
    return quakes

def fetch_aqi():
    """Fetch AQI for Pakistani cities from OpenAQ"""
    results = {}
    for key, city in CITIES.items():
        url = f"https://api.openaq.org/v3/locations?coordinates={city['lat']},{city['lng']}&radius=20000&parameters_id=2&limit=3"
        try:
            req = urllib.request.Request(url, headers={"Accept":"application/json","User-Agent":"GlobalDisasterWatch/1.0"})
            with urllib.request.urlopen(req, timeout=6) as resp:
                data = json.loads(resp.read())
                for r in data.get("results", []):
                    for s in r.get("sensors", []):
                        if s.get("parameter", {}).get("name") == "pm25":
                            val = s.get("summary", {}).get("lastValue", 0)
                            if val and val > 0:
                                pm25 = round(val, 1)
                                aqi = pm25_to_aqi(pm25)
                                results[key] = {"aqi": aqi, "pm25": pm25, "source": "live"}
                                break
        except:
            pass
        if key not in results:
            results[key] = get_simulated_aqi(key)
    return results

def pm25_to_aqi(pm25):
    breakpoints = [(0,12,0,50),(12.1,35.4,51,100),(35.5,55.4,101,150),(55.5,150.4,151,200),(150.5,250.4,201,300),(250.5,500,301,500)]
    for lo,hi,alo,ahi in breakpoints:
        if lo<=pm25<=hi:
            return round(((ahi-alo)/(hi-lo))*(pm25-lo)+alo)
    return 500

def get_simulated_aqi(key):
    base = {"lahore":185,"karachi":115,"faisalabad":160,"islamabad":90,"peshawar":140,"multan":145,"quetta":95,"rawalpindi":110}
    m = datetime.now().month
    b = base.get(key, 120)
    if m in [11,12,1,2]: b = int(b*1.4)
    elif m in [6,7,8]: b = int(b*0.65)
    aqi = max(20, b + random.randint(-20,25))
    return {"aqi": aqi, "pm25": round((aqi/100)*35.4,1), "source": "simulated"}

def aqi_color(aqi):
    if aqi<=50: return "#22c55e"
    if aqi<=100: return "#eab308"
    if aqi<=150: return "#f97316"
    if aqi<=200: return "#ef4444"
    if aqi<=300: return "#a855f7"
    return "#dc2626"

def aqi_label(aqi):
    if aqi<=50: return "Good"
    if aqi<=100: return "Moderate"
    if aqi<=150: return "Unhealthy for Sensitive"
    if aqi<=200: return "Unhealthy"
    if aqi<=300: return "Very Unhealthy"
    return "Hazardous"

def fetch_weather():
    """Fetch weather for major cities from Open-Meteo (free, no key)"""
    results = {}
    for key, city in list(CITIES.items())[:4]:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={city['lat']}&longitude={city['lng']}&current=temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code&timezone=auto"
        try:
            req = urllib.request.Request(url, headers={"User-Agent":"GlobalDisasterWatch/1.0"})
            with urllib.request.urlopen(req, timeout=6) as resp:
                data = json.loads(resp.read())
                cur = data.get("current", {})
                results[key] = {
                    "temp": cur.get("temperature_2m", 0),
                    "humidity": cur.get("relative_humidity_2m", 0),
                    "wind": cur.get("wind_speed_10m", 0),
                    "code": cur.get("weather_code", 0),
                    "source": "live"
                }
        except:
            results[key] = {
                "temp": round(random.uniform(15,38), 1),
                "humidity": random.randint(30,80),
                "wind": round(random.uniform(5,25), 1),
                "code": 0,
                "source": "simulated"
            }
    return results

def get_flood_risk_zones():
    """Major global flood risk zones based on historical data"""
    return [
        {"name":"Indus River Basin","lat":27.5,"lng":68.5,"risk":"critical","description":"Pakistan's main flood corridor. 2022 floods submerged 1/3 of country.","area":"500,000 km²"},
        {"name":"Ganges-Brahmaputra Delta","lat":23.5,"lng":90.0,"risk":"critical","description":"Bangladesh's low-lying delta. Among the most flood-prone regions on Earth.","area":"150,000 km²"},
        {"name":"Mekong Delta","lat":9.5,"lng":106.0,"risk":"high","description":"Vietnam's rice-growing delta, increasingly affected by sea-level rise and monsoon flooding.","area":"40,000 km²"},
        {"name":"Mississippi River Basin","lat":32.0,"lng":-91.0,"risk":"high","description":"Major US river system with recurring seasonal flood events.","area":"3,200,000 km²"},
        {"name":"Rhine River Basin","lat":51.0,"lng":6.5,"risk":"medium","description":"Central European river system, periodic severe flooding in Germany and the Netherlands.","area":"190,000 km²"},
        {"name":"Gilgit-Baltistan Glaciers","lat":36.0,"lng":74.5,"risk":"medium","description":"Among the highest glacier concentrations outside the poles. GLOF risk rising with climate change.","area":"30,000 km²"},
    ]

# ── ROUTES ─────────────────────────────────────────────────────────────────────

def haversine_km(lat1, lng1, lat2, lng2):
    """Straight-line distance in km between two points on Earth."""
    R = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lng2 - lng1)
    a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dlambda / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))


def calculate_risk_alerts(quakes):
    """
    Rule-based 'elevated activity' flag — NOT a machine-learning prediction.
    For each known fault line, counts how many live earthquakes from the
    last USGS fetch occurred within 300km of any point on that fault line.
    If that count crosses a threshold, the fault line is flagged as having
    elevated current activity. This is a transparent, explainable alert,
    not a forecast of future events.
    """
    alerts = []
    threshold_by_risk = {"critical": 2, "high": 3, "complex": 3, "subduction": 3, "strike-slip": 3, "thrust": 3}

    for fault in FAULT_LINES:
        nearby_count = 0
        for q in quakes:
            for (flat, flng) in fault["coords"]:
                if haversine_km(q["lat"], q["lng"], flat, flng) <= 300:
                    nearby_count += 1
                    break
        threshold = threshold_by_risk.get(fault["risk"], 3)
        if nearby_count >= threshold:
            alerts.append({
                "fault_name": fault["name"],
                "risk_level": fault["risk"],
                "nearby_quake_count": nearby_count,
                "message": f"{nearby_count} recent earthquakes detected within 300km of {fault['name']} — elevated activity based on live data."
            })

    return alerts


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/globe-data')
def api_globe_data():
    quakes, quake_source = fetch_usgs_earthquakes()
    aqi_data = fetch_aqi()
    weather = fetch_weather()
    flood_zones = get_flood_risk_zones()

    # Build city objects
    cities_out = []
    for key, city in CITIES.items():
        aqi_info = aqi_data.get(key, {"aqi": 100, "pm25": 35, "source": "unknown"})
        w = weather.get(key, {})
        cities_out.append({
            "key": key,
            "name": city["name"],
            "lat": city["lat"],
            "lng": city["lng"],
            "pop": city["pop"],
            "aqi": aqi_info["aqi"],
            "pm25": aqi_info["pm25"],
            "aqi_color": aqi_color(aqi_info["aqi"]),
            "aqi_label": aqi_label(aqi_info["aqi"]),
            "temp": w.get("temp", "—"),
            "humidity": w.get("humidity", "—"),
            "wind": w.get("wind", "—"),
            "aqi_source": aqi_info["source"],
            "weather_source": w.get("source", "unknown"),
        })

    # Stats
    total_quakes = len(quakes)
    big_quakes = [q for q in quakes if q["magnitude"] >= 4.0]
    worst_aqi_city = max(cities_out, key=lambda x: x["aqi"])
    risk_alerts = calculate_risk_alerts(quakes)

    return jsonify({
        "earthquakes": quakes,
        "cities": cities_out,
        "fault_lines": FAULT_LINES,
        "flood_zones": flood_zones,
        "historic": HISTORIC,
        "risk_alerts": risk_alerts,
        "stats": {
            "total_quakes_72h": total_quakes,
            "big_quakes": len(big_quakes),
            "worst_aqi": worst_aqi_city["name"],
            "worst_aqi_val": worst_aqi_city["aqi"],
            "quake_source": quake_source,
            "updated": datetime.now().strftime("%d %b %Y %H:%M UTC")
        }
    })

if __name__ == '__main__':
    print("\n" + "="*52)
    print("  GLOBAL DISASTER INTELLIGENCE GLOBE")
    print("  http://localhost:5000")
    print("="*52 + "\n")
    app.run(debug=True, port=5000)
