from flask import Flask, request, jsonify
import io
from PIL import Image
import os
from dotenv import load_dotenv
from openai import OpenAI
# import requests
import base64
from google import genai

# Load .env
load_dotenv(r"C:\Users\hasan\Rafi_SAA\python_practices\LLM_Langchain\llm_openai\.env")
API_KEY = os.getenv("gemini_open_router")

client = OpenAI(api_key=API_KEY,base_url="https://openrouter.ai/api/v1")

print(client)
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

        image_bytes = image_file.read()

        # image = Image.open(io.BytesIO(image_bytes))
        # image_b64 = base64.b64encode(image_bytes).decode('utf-8')


        prompt = (
            "You are a professional fashion analyst "
            "Analyze this image and extract outfit attributes such as: "
            "clothing type, color, pattern, sleeve length, and style. "
            "Return a concise JSON output."
            # f"Image (base64): {image_b64}"
        )


        response = client.chat.completions.create(
            model="google/gemini-2.5-flash",
            messages=[
                {"role": "system", "content": ""},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
        )

        # The assistant's response is here:
        assistant_msg = response.choices[0].message.content

        # return jsonify({"attributes": assistant_msg})
        return assistant_msg

    except Exception as e:
        return jsonify({"error": f"Gemini request failed: {str(e)}"}), 500



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
