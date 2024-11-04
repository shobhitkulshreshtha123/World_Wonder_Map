from flask import Flask, render_template, request, jsonify
import folium
import json

app = Flask(__name__)

# Load coordinates from wonders_data.json
with open("wonders_data.json") as f:
    wonders_data = json.load(f)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/select_wonder', methods=['POST'])
def select_wonder():
    data = request.get_json()
    selected_wonder = data['wonder']
    
    # Get coordinates for the selected wonder
    coords = wonders_data.get(selected_wonder)
    if coords:
        lat, lon = coords
        wonder_map = folium.Map(location=[lat, lon], zoom_start=6)
        folium.Marker(location=[lat, lon], popup=selected_wonder).add_to(wonder_map)
        map_html = wonder_map._repr_html_()  # Generate HTML representation of the map
        
        return jsonify({'map_html': map_html})
    else:
        return jsonify({'error': 'Wonder not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
