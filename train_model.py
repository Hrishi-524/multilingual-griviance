"""
Trains a small illustrative TF-IDF + Logistic Regression classifier, matching
the architecture described in the paper (Section IV), so the demo app has
something real to load.

IMPORTANT: this is a small illustrative dataset for demoing the app's wiring,
NOT the actual 240-record trilingual corpus described in the paper. To use
the real trained model, drop the actual `grievance_classifier.pkl` (produced
by the notebook pipeline) into this folder instead of running this script.
"""

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

EXAMPLES = {
    "Water Supply": [
        "There has been no water supply in our locality for the past four days.",
        "The water pressure from the municipal pipeline has been extremely low all week.",
        "Our area's water tank has not been refilled since last Monday.",
        "The tap water in our building smells foul and is unsafe to drink.",
        "Water supply timing has been irregular for over two weeks now.",
        "A major pipeline leak near our street is wasting thousands of litres of water daily.",
    ],
    "Electricity": [
        "There have been frequent power cuts in our area for the last three days.",
        "The streetlight outside our house has not worked for over a month.",
        "Our electricity meter is showing incorrect readings every month.",
        "A live wire has been hanging dangerously low near the bus stop.",
        "Voltage fluctuations have damaged several appliances in our home.",
        "The transformer near our society keeps tripping every evening.",
    ],
    "Roads & Public Works": [
        "The main road in our area has several large potholes causing accidents.",
        "Construction debris has been left on the roadside for weeks.",
        "The footpath near the school has collapsed and is unsafe for pedestrians.",
        "Streetlights along the highway have been non-functional for months.",
        "The newly laid road has already started cracking after one monsoon.",
        "A broken manhole cover on our street is a serious safety hazard.",
    ],
    "Sanitation & Waste Management": [
        "Garbage has not been collected from our street for over a week.",
        "The public toilet near the market is in an extremely unhygienic condition.",
        "Overflowing dustbins are attracting stray animals and pests.",
        "Sewage water is regularly overflowing onto the main road.",
        "Waste segregation is not being followed by the collection truck.",
        "A dead animal has been lying uncollected near our colony for two days.",
    ],
    "Public Transport": [
        "The local bus on our route has been consistently delayed by over 30 minutes.",
        "Buses on this route are overcrowded during peak hours every single day.",
        "The bus stop shelter has been damaged and offers no protection from rain.",
        "Auto-rickshaw drivers on this route are refusing to use the meter.",
        "The last bus timing displayed at the stop does not match actual service.",
        "Train announcements at this station are inaudible and unclear.",
    ],
    "Health Services": [
        "The local government hospital has been out of essential medicines for weeks.",
        "There is no doctor available at the primary health centre after 2 PM.",
        "The ambulance service took over an hour to respond to an emergency call.",
        "The public health centre is severely understaffed during evening hours.",
        "Vaccination camps announced for our area have been repeatedly postponed.",
        "The maternity ward at the municipal hospital lacks basic equipment.",
    ],
    "Law & Order / Police": [
        "Repeated complaints about noise and rowdy behaviour at night have been ignored.",
        "The local police station has not responded to our complaint for two weeks.",
        "There has been a rise in chain-snatching incidents in our neighbourhood.",
        "Traffic police are not present at a dangerous intersection during school hours.",
        "An FIR filed last month has still not been registered properly.",
        "Illegal parking outside the police chowky itself is causing daily traffic jams.",
    ],
    "Corruption / Administrative Misconduct": [
        "A municipal clerk is demanding an unofficial fee to process a routine certificate.",
        "An official asked for a bribe to approve a building completion certificate.",
        "Funds allocated for road repair in our ward appear to have been misused.",
        "An inspector demanded payment to overlook a licensing violation.",
        "Ration shop owner is demanding extra money for supplies that should be free.",
        "A government contractor submitted fake bills for work never carried out.",
    ],
}


def main():
    texts, labels = [], []
    for category, sentences in EXAMPLES.items():
        for s in sentences:
            texts.append(s)
            labels.append(category)

    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True)),
        ("classifier", LogisticRegression(max_iter=2000, random_state=42)),
    ])
    pipeline.fit(texts, labels)

    joblib.dump(pipeline, "grievance_classifier_demo.pkl")
    print(f"Trained demo pipeline on {len(texts)} examples across {len(EXAMPLES)} categories.")
    print("Saved to grievance_classifier_demo.pkl")


if __name__ == "__main__":
    main()