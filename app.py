from flask import Flask, render_template, request, jsonify
import folium
import json

app = Flask(__name__)

# Load the wonders data from the JSON file
with open("wonders_data.json") as f:
    wonders_data = json.load(f)

@app.route('/')
def home():
    # Generate the initial map without markers
    wonder_map = folium.Map(location=[20, 0], zoom_start=2, tiles="Stamen Terrain", attr="Map tiles by Stamen Design, under CC BY 3.0. Data by OpenStreetMap, under ODbL.")
    wonder_map = wonder_map._repr_html_()  # Render HTML
    return render_template('index.html', map=wonder_map, wonders=wonders_data.keys())

@app.route('/select_wonder', methods=['POST'])
def select_wonder():
    selected_wonder = request.form.get("wonder")
    lat, lon = wonders_data[selected_wonder]

    # Create map centered on the selected wonder
    wonder_map = folium.Map(location=[lat, lon], zoom_start=6, tiles="Stamen Terrain")
    folium.Marker(location=[lat, lon], popup=selected_wonder, tooltip=selected_wonder).add_to(wonder_map)
    wonder_map = wonder_map._repr_html_()  # Render HTML

    return jsonify({"map": wonder_map})

if __name__ == '__main__':
    app.run(debug=True)
