# TESS Exoplanet AI 

<img align="right" src="https://upload.wikimedia.org/wikipedia/commons/e/e5/NASA_logo.svg" alt="NASA Logo" width="120">

An autonomous, deep-space pipeline that acts as a smart telescope. It fetches live astrophysical telemetry from NASA's Kepler and TESS missions, processes the light curves to detect planetary transits, and uses machine learning paired with generative AI to classify and analyze potential exoplanets.

---

## 🚀 Why I Built This

I have been fascinated by space, the stars, and the possibility of other worlds since I was a kid. As a Computer Science major, I realized I finally had the technical toolkit to stop just reading about space exploration and start actively participating in it. This project is the ultimate intersection of my childhood passion for astronomy and my professional focus on software engineering, data science, and AI. What better way to apply machine learning than hunting for alien worlds?

---

## 🛠️ How I Built It

Building this pipeline was a journey from understanding basic astrophysics to deploying a full-stack automated AI application. 

### 1. Learning the Fundamentals
I started completely from scratch by studying how exoplanet transits actually work. I followed this excellent [YouTube Tutorial - INSERT LINK HERE] to understand the math behind dips in starlight and how to interact with NASA's archive. 

![Placeholder: Image of you watching the tutorial or a screenshot of the video](INSERT_IMAGE_LINK_HERE)

### 2. Manual Data Analysis
Before automating anything, I had to get my hands dirty with the data. Using the `lightkurve` library, I manually queried the MAST (Mikulski Archive for Space Telescopes) API. I learned how to download raw flux data, clean out stellar noise, flatten the light curves, and manually fold the data to find periodic transit signals.

![Placeholder: Image of a raw, messy light curve vs a clean, folded light curve](INSERT_IMAGE_LINK_HERE)

### 3. Pipeline Automation & AI Integration
Once I understood the manual process, I engineered an automated pipeline. 
* I implemented the **Box Least Squares (BLS)** algorithm to automatically hunt for the best transit periods.
* I trained an **XGBoost** machine learning model on historical Kepler data to classify whether a signal was a true planet or a false positive.
* I integrated the **Gemini 3.6 API** to act as an automated astrophysicist, generating a comprehensive, human-readable dossier based on the telemetry and model confidence.
* Finally, I wrapped it all in a responsive **Streamlit** web application.

![Placeholder: Screenshot of the final working Streamlit dashboard](INSERT_IMAGE_LINK_HERE)

---

## 🧠 System Architecture

![Placeholder: Architecture Diagram - Create a quick flowchart in Canva or draw.io showing: User Input -> MAST API -> Data Cleaning -> BLS Algorithm -> XGBoost Model -> Gemini API -> Streamlit Output](INSERT_IMAGE_LINK_HERE)

**Workflow Summary:**
1. **Target Query:** User inputs a target star (e.g., `TOI-700`).
2. **Telemetry Fetch:** Python backend queries the MAST API for TESS/Kepler sectors.
3. **Signal Processing:** Light curves are stitched, flattened, and cleaned of outliers.
4. **Periodogram Analysis:** BLS algorithm calculates the orbital period and transit depth.
5. **AI Classification:** XGBoost evaluates the signal signature against known planetary parameters.
6. **Dossier Generation:** Telemetry metrics are passed to Gemini to synthesize an astrophysical report.

---

## 💻 Tech Stack

* **Frontend/UI:** Streamlit, HTML/CSS
* **Backend Pipeline:** Python, Pandas, NumPy
* **Astrophysics Library:** Lightkurve (MAST API)
* **Machine Learning:** XGBoost, Scikit-learn
* **Generative AI:** Google Gemini API
* **Data Visualization:** Plotly

---

## 📊 Results & Performance

* **Model Accuracy:** 86.89% classification accuracy achieved against the NASA Kepler baseline testing data.
* **Live Telemetry:** Successfully handles live API calls for both modern TESS targets and historical Kepler targets.
* **Contextual Processing:** The pipeline successfully detects significant transit dips (like Jupiter-sized gas giants and clear terrestrial signals), though ultra-small Earth-sized planets still remain a challenge for the current signal-to-noise ratio configuration.

---

## 🌍 Why This Matters

Finding exoplanets used to require a massive team of institutional astronomers manually reviewing data for years. This project demonstrates how modern data science and open-source APIs can democratize space exploration. By automating the heavy lifting of signal processing and initial vetting, tools like this can help citizen scientists and researchers filter through the millions of stars TESS observes, accelerating the discovery of new worlds.

---

**Author:**
Anindita Sanjagiri 
*[Insert Link to your LinkedIn/Portfolio]*
