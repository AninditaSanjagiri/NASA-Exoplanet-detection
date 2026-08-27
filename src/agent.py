import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()


def generate_vetting_report(target_name, features, prediction, confidence, api_key=None):
    """
    Synthesizes extracted features and ML predictions into a scientific memo using Gemini 3.6.
    """
    is_planet = (prediction == 1)
    status_text = "Confirmed Candidate" if is_planet else "False Positive (Stellar Binary / Noise)"
    
    system_prompt = (
        "You are an expert astrophysicist and exoplanet vetting specialist working on NASA's TESS mission. "
        "Your task is to analyze photometric light curve features and an ML model verdict to produce a "
        "structured, concise, and professional scientific observation memo."
    )
    
    user_prompt = f"""
Target Star: {target_name}
Automated Classifier Verdict: {status_text} (Model Confidence: {confidence:.2f}%)

Extracted Photometric Parameters:
- Orbital Period: {features.get('period_days')} days
- Observed Transits: {features.get('transit_count')}
- Primary Signal Depth: {features.get('signal_depth')}
- Signal-to-Noise Ratio (SNR): {features.get('snr')}
- Odd/Even Transit Depth Difference: {features.get('odd_even_diff')}
- Out-of-Transit Baseline Variance: {features.get('out_of_transit_variance')}
- Secondary Eclipse Dip Ratio: {features.get('secondary_dip_ratio')}

Please write a 3-part scientific summary:
1. Signal Assessment: Discuss the depth, SNR, and transit periodicity.
2. Binary Contamination Analysis: Interpret the odd/even difference, out-of-transit variance, and secondary dip ratio.
3. Final Recommendation: State whether follow-up spectroscopic radial velocity observations are warranted.
"""

    # User-entered key takes priority; falls back to server .env
    cleaned_key = api_key.strip() if (api_key and api_key.strip()) else os.getenv("GEMINI_API_KEY")
    
    if cleaned_key:
        try:
            client = genai.Client(api_key=cleaned_key)
            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=user_prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    temperature=0.2
                )
            )
            return response.text
        except Exception as e:
            return f"*(Gemini API Notice: {e}. Displaying deterministic report)*\n\n" + _offline_report(target_name, features, is_planet, confidence)

    return _offline_report(target_name, features, is_planet, confidence)


def _offline_report(target_name, features, is_planet, confidence):
    """
    Deterministic fallback generator for scientific reports.
    """
    period = features.get("period_days", 0)
    snr = float(features.get("snr") or 0.0)
    oot_var = float(features.get("out_of_transit_variance") or 0.0)
    sec_ratio = float(features.get("secondary_dip_ratio") or 0.0)
    odd_even = float(features.get("odd_even_diff") or 0.0)
    
    if is_planet:
        recommendation = (
            "High-priority candidate for ground-based radial velocity (RV) follow-up "
            "and high-resolution spectroscopy to confirm planetary mass."
        )
        binary_notes = (
            f"Minimal odd/even transit asymmetry ({odd_even:.6f}) and low secondary eclipse ratio ({sec_ratio:.4f}) "
            "indicate that the photometric dip is consistent with a planetary occultation rather than an eclipsing binary."
        )
    else:
        recommendation = (
            "Flagged as a false positive. Follow-up observations are not recommended at this time."
        )
        binary_notes = (
            f"Elevated out-of-transit variance ({oot_var:.6f}) and/or secondary dip ratio ({sec_ratio:.4f}) "
            "indicate potential stellar variability or alternating eclipses characteristic of a binary system."
        )

    return f"""### 📝 Automated Scientific Observation Memo
**Target:** `{target_name}` | **Classification:** `{'Planetary Candidate' if is_planet else 'False Positive'}` | **Confidence:** `{confidence:.2f}%`

---

#### 1. Signal Assessment
* **Orbital Period:** {period} days with {features.get('transit_count', 0)} observed transits in window.
* **Signal-to-Noise Ratio (SNR):** {snr:.2f} (Detection threshold > 7.0).
* **Transit Depth:** {features.get('signal_depth', 0)} relative flux drop.

#### 2. Binary Contamination & Morphological Analysis
* {binary_notes}
* **Baseline Stability:** Out-of-transit flux dispersion measured at {oot_var:.6f}.

#### 3. Strategic Recommendation
* {recommendation}
"""