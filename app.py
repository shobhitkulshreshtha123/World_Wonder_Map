import json
import folium
from flask import Flask, request, render_template

app = Flask(__name__)

# Load coordinates from wonders_data.json
with open("wonders_data.json") as f:
    wonders_data = json.load(f)

@app.route('/')
def home():
    return render_template('index.html', wonders=wonders_data.keys())

@app.route('/select_wonder', methods=['POST'])
def select_wonder():
    selected_wonder = request.form.get("wonder")
    if selected_wonder in wonders_data:
        lat, lon = wonders_data[selected_wonder]
        # Create map centered on selected wonder
        wonder_map = folium.Map(location=[lat, lon], zoom_start=6, tiles="OpenStreetMap")
        # Add marker for the selected wonder
        folium.Marker([lat, lon], popup=selected_wonder, tooltip=selected_wonder).add_to(wonder_map)
        # Save map to HTML file
        wonder_map.save("templates/wonder_map.html")
    return render_template('wonder_map.html')

if __name__ == '__main__':
    app.run(debug=True)
