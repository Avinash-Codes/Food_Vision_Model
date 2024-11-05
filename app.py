from flask import Flask, render_template, request, jsonify
import requests
import base64
import cv2
import numpy as np

app = Flask(__name__)


FOODVISOR_API_URL = "https://vision.foodvisor.io/api/1.0/en/analysis/"
HEADERS = {"Authorization": "Api-Key CfYIA6TX.wTXi765jr1RLDG9CKZV5blIrrjTfaKut"}  




@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    # Get base64 image data
    data = request.json.get('image')
    
    # Log and validate image data
    if not data:
        print("Error: No image data received.")
        return jsonify({"error": "No image data received"}), 400

    # Decode base64 data
    try:
        image_data = base64.b64decode(data.split(",")[1]) 
        image = np.frombuffer(image_data, np.uint8)
        frame = cv2.imdecode(image, cv2.IMREAD_COLOR)
    except Exception as e:
        print(f"Decoding error: {e}")
        return jsonify({"error": "Failed to decode image"}), 400

    # Encode frame for API request
    _, img_encoded = cv2.imencode('.jpg', frame)
    files = {"image": ("image.jpg", img_encoded.tobytes(), "image/jpeg")}

    # Send request to Foodvisor API
    response = requests.post(FOODVISOR_API_URL, headers=HEADERS, files=files)
    
    if response.status_code == 200:
<<<<<<< HEAD
        response_data = response.json()
        # Extract specific data you need to display
        analysis_results = response_data.get("results", [])
        return render_template('results.html', results=analysis_results)
  
    else:
        print(f"Foodvisor API error: {response.text}")
       return jsonify({"error": response.text}), response.status_code
=======
        return jsonify(response.json())

        
    else:
        print(f"Foodvisor API error: {response.text}")
        return jsonify({"error": response.text}), response.status_code
    

>>>>>>> 2e670c93d3a50f7e1fa169675a0bfc210d3d99c1

if __name__ == '__main__':
    app.run(debug=True)


