from flask import Flask, request, jsonify
import io
from PIL import Image
import os
from dotenv import load_dotenv
import google.generativeai as genai
import json

# Load .env
load_dotenv(r"C:\Users\hasan\Rafi_SAA\python_practices\LLM_Langchain\llm_openai\.env")
API_KEY = os.getenv("gemini_api_key")  # Use actual Gemini API key

# Configure Gemini
genai.configure(api_key=API_KEY)

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Gemini Outfit API running!"})


@app.route("/api/extract_outfit", methods=["POST"])
def extract_outfit():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    try:
        image_file = request.files['image']
        
        # Read image bytes and convert to PIL Image
        image_bytes = image_file.read()
        image = Image.open(io.BytesIO(image_bytes))
        
        # Initialize Gemini model
        model = genai.GenerativeModel(
            "gemini-2.0-flash-exp",
            generation_config={"response_mime_type": "application/json"}
        )
        
        # Create prompt for outfit analysis
        prompt = """You are a professional fashion analyst. Analyze this image and extract outfit attributes.

Return a JSON object with this exact structure:
{
  "clothing_type": "description of garment type",
  "color": "primary color(s)",
  "pattern": "pattern type or 'solid'",
  "sleeve_length": "sleeveless/short/long/etc",
  "style": "casual/formal/sporty/etc",
  "additional_details": "any notable features"
}"""

        # Generate content with image and prompt
        response = model.generate_content([prompt, image])
        
        # Parse JSON response
        try:
            outfit_data = json.loads(response.text)
            return jsonify({"success": True, "attributes": outfit_data})
        except json.JSONDecodeError:
            # If JSON parsing fails, return raw response
            return jsonify({"success": True, "attributes": {"raw_response": response.text}})

    except Exception as e:
        return jsonify({"error": f"Gemini request failed: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)