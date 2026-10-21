"""
Minimal Flask backend for the grievance classification demo.

Loads a saved scikit-learn Pipeline (TF-IDF + Logistic Regression, matching
Section IV/V of the paper), serves the built React frontend, and exposes a
JSON /predict endpoint.

By default it loads `grievance_classifier_demo.pkl` (the small illustrative
model produced by train_demo_model.py). To serve the real model described in
the paper, place the actual `grievance_classifier.pkl` produced by the
notebook pipeline in this folder and set:

    export GRIEVANCE_MODEL_PATH=grievance_classifier.pkl

Build the frontend in `frontend/` with `npm install` and `npm run build`, then:
    pip install -r requirements.txt
    python app.py
Then open http://127.0.0.1:5000
"""

import os
from pathlib import Path

import joblib
from deep_translator import GoogleTranslator
from deep_translator.exceptions import TooManyRequests
from flask import Flask, jsonify, request, send_from_directory

MODEL_PATH = os.environ.get("GRIEVANCE_MODEL_PATH", "grievance_classifier_demo.pkl")

FRONTEND_DIST = Path(__file__).parent / "frontend" / "dist"
app = Flask(__name__)
pipeline = joblib.load(MODEL_PATH)
translator = GoogleTranslator(source="auto", target="en")


def contains_devanagari(text):
    """The demo classifier was trained on English; detect Hindi/Marathi script."""
    return any("\u0900" <= char <= "\u097f" for char in text)


def local_civic_translation(text):
    """Map common Hindi/Marathi civic phrases to English classifier examples."""
    value = text.casefold()

    def has_any(*terms):
        return any(term in value for term in terms)

    water_words = ("पाणी", "पाण्याचा", "पाण्याची", "पानी", "जलापूर्ति")
    if has_any(*water_words):
        if has_any("दूषित", "घाण", "दुर्गंध", "गंदा"):
            return "The tap water in our building smells foul and is unsafe to drink."
        if has_any("गळती", "गळत", "लीक", "रिसाव"):
            return "A major pipeline leak near our street is wasting water daily."
        if has_any("नाही", "नही", "नसत", "आलेले नाही", "येत नाही", "बंद", "नहीं", "नहीं आ", "नही आ"):
            return "There has been no water supply in our locality for the past four days."
        return "Water supply timing has been irregular in our locality."

    if has_any("कचरा", "कचऱ्या", "कचरे"):
        if has_any("नाही", "नही", "नसत", "उचल", "जमा", "नहीं"):
            return "Garbage has not been collected from our street for over a week."
        return "Garbage collection in our locality needs attention."
    if has_any("खड्ड", "गड्ढ", " pothole"):
        return "The main road in our area has several large potholes causing accidents."
    if has_any("सांडपाणी", "गटार", "नाली", "सीवेज", "ओव्हरफ्लो"):
        return "Sewage water is overflowing onto the main road."
    if has_any("वीज", "विजे", "बिजली", "बत्ती"):
        if has_any("खांब", "तार", "वायर", "तुट", "लटक"):
            return "A live wire is hanging dangerously low near the road."
        if has_any("दिवा", "लाईट", "लाइट", "स्ट्रीट लाइट"):
            return "The streetlight outside our house has not worked for over a month."
        return "There have been frequent power cuts in our area."
    if has_any("बस", "बससेवा", "बस सेवा"):
        return "The local bus on our route has been consistently delayed."
    if has_any("रुग्णालय", "दवाखाना", "औषध", "अस्पताल", "डॉक्टर"):
        return "The local government hospital has been out of essential medicines."
    if has_any("पोलीस", "पोलिस", "पुलिस", "एफआयआर", "एफआईआर"):
        return "The local police station has not responded to our complaint."
    if has_any("लाच", "भ्रष्टाचार", "लाचखोरी", "रिश्वत", "घूस"):
        return "A government official is demanding a bribe to process our complaint."
    if has_any("रस्ता", "रस्त्यावर", "सड़क", "सड़क"):
        return "The main road in our area has damage that needs repair."
    return None


@app.route("/")
def index():
    if not (FRONTEND_DIST / "index.html").exists():
        return jsonify({"error": "React frontend is not built. Run npm install and npm run build in frontend/."}), 503
    return send_from_directory(FRONTEND_DIST, "index.html")


@app.route("/<path:path>")
def frontend_assets(path):
    return send_from_directory(FRONTEND_DIST, path)


@app.route("/predict", methods=["POST"])
def predict():
    payload = request.get_json(force=True)
    text = (payload or {}).get("text", "").strip()
    if not text:
        return jsonify({"error": "text is required"}), 400

    translated = contains_devanagari(text)
    classifier_text = text
    translation_method = "none"
    if translated:
        classifier_text = local_civic_translation(text)
        if classifier_text:
            translation_method = "local"
        else:
            try:
                classifier_text = translator.translate(text)
                translation_method = "google"
            except TooManyRequests:
                app.logger.warning("Online complaint translation was rate-limited")
                return jsonify({"error": "Online translation is temporarily rate-limited. Try a shorter complaint or rephrase it using a common civic issue term, such as water, garbage, road, electricity, bus, hospital, or police."}), 503
            except Exception as error:
                app.logger.warning("Complaint translation failed (%s)", type(error).__name__)
                return jsonify({"error": "Online translation is unavailable right now. Please try again."}), 502
        if not classifier_text or not classifier_text.strip():
            return jsonify({"error": "We could not translate this complaint. Please try rephrasing it."}), 502

    prediction = pipeline.predict([classifier_text])[0]
    return jsonify({"category": prediction, "translated": translated, "translation_method": translation_method})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
