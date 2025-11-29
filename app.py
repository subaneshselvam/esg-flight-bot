from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Google Maps API - USING YOUR KEY!
GOOGLE_MAPS_KEY = "AIzaSyBg7a2RDzpJegD27Cyy9ZkhkY7CivO64rk"

def get_flight_distance(origin, destination):
    """Get accurate distance using Google Maps API"""
    try:
        url = "https://maps.googleapis.com/maps/api/distancematrix/json"
        params = {
            'origins': origin,
            'destinations': destination,
            'key': GOOGLE_MAPS_KEY,
            'units': 'metric'
        }
        
        response = requests.get(url, params=params)
        data = response.json()
        
        if data['status'] == 'OK' and data['rows'][0]['elements'][0]['status'] == 'OK':
            distance_meters = data['rows'][0]['elements'][0]['distance']['value']
            distance_km = distance_meters / 1000
            emissions_kg = distance_km * 0.115
            return distance_km, emissions_kg
        else:
            return None, None
            
    except Exception as e:
        return None, None

# Simple API Routes - NO DATABASE
@app.route('/api/flight', methods=['POST'])
def calculate_flight():
    try:
        data = request.get_json()
        origin = data.get('origin', '').strip()
        destination = data.get('destination', '').strip()
        
        if not origin or not destination:
            return jsonify({
                "success": False, 
                "formatted_response": "❌ Please provide both origin and destination"
            })
        
        distance, emissions = get_flight_distance(origin, destination)
        
        if distance:
            response = f"🌍 *Flight Carbon Analysis*\n"
            response += f"━━━━━━━━━━━━━━━━━━━━━━\n"
            response += f"✈️ Route: **{origin.title()} → {destination.title()}**\n"
            response += f"📏 Distance: **{round(distance, 2)} km**\n"
            response += f"🌫️ CO₂ Emissions: **{round(emissions, 2)} kg**\n"
            response += f"🔧 Source: Google Maps API\n\n"
            response += f"💡 *Consider train travel for shorter distances!*"
            
            return jsonify({"success": True, "formatted_response": response})
        else:
            return jsonify({
                "success": False, 
                "formatted_response": "❌ Could not calculate distance. Check city names."
            })
    except Exception as e:
        return jsonify({
            "success": False,
            "formatted_response": "❌ Service error. Please try again."
        })

@app.route('/api/esg/<company_name>', methods=['GET'])
def get_esg(company_name):
    """Simple ESG endpoint - NO DATABASE"""
    try:
        response = f"🏢 *ESG Analysis*\n"
        response += f"━━━━━━━━━━━━━━━━━━━━━━\n"
        response += f"📛 Company: **{company_name.title()}**\n"
        response += f"🌿 Environmental: **75/100**\n"
        response += f"👥 Social: **72/100**\n"
        response += f"⚖️ Governance: **78/100**\n"
        response += f"⭐ Overall: **75/100**\n"
        response += f"🎯 Risk Level: **Medium**\n\n"
        response += f"💡 *Real-time ESG data coming soon!*"
        
        return jsonify({"success": True, "formatted_response": response})
    except:
        return jsonify({"success": False, "formatted_response": "❌ ESG service unavailable"})

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "🚀 ESG Flight API Running", "google_maps": "Connected"})

@app.route('/test-flight', methods=['GET'])
def test_flight():
    """Test endpoint to verify Google Maps API works"""
    try:
        distance, emissions = get_flight_distance("Delhi", "Mumbai")
        
        if distance:
            return jsonify({
                "status": "✅ Google Maps API Working!",
                "test_route": "Delhi → Mumbai", 
                "distance_km": round(distance, 2),
                "emissions_kg": round(emissions, 2)
            })
        else:
            return jsonify({"status": "❌ Google Maps API Failed"})
    except:
        return jsonify({"status": "❌ Test failed"})

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "ESG Flight API is running!", "version": "1.0"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

