# Nagrik grievance classifier

The interface is a React app built with Vite. Flask serves the production build and the `/predict` classification API.

## Run in development

1. Install the Python dependencies and start Flask from the project root:

   ```sh
   pip install -r requirements.txt
   python app.py
   ```

2. In another terminal, start the React development server:

   ```sh
   cd frontend
   npm install
   npm run dev
   ```

Open the Vite URL shown in the terminal. Requests to `/predict` are proxied to Flask.

## Run the production build

```sh
cd frontend
npm install
npm run build
cd ..
python app.py
```

Open `http://127.0.0.1:5000`. The API returns the suggested department only; it does not return confidence.

## Marathi and Hindi complaints

The demo classifier was trained mostly on English examples. For common Marathi/Hindi civic issue phrases (water, garbage, roads, electricity, buses, hospitals, and police), the backend maps the issue to an English classifier phrase locally. This avoids a network call for those common cases. Other Devanagari complaints use Google Translate before classification and need an internet connection. That service can rate-limit requests; the app reports the limit instead of classifying untranslated text as English. Text not matched by the local rules may be sent to Google Translate.
