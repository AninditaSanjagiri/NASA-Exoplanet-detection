import streamlit as st
import streamlit.components.v1 as components
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import os
import warnings
from dotenv import load_dotenv

# Suppress lightkurve warnings
warnings.filterwarnings("ignore", category=UserWarning, module="lightkurve")
load_dotenv()

# Import pipeline modules
from src.pipeline import fetch_and_clean_lightcurve, run_bls, extract_features
from src.model import train_or_load_model, predict_candidate
from src.agent import generate_vetting_report

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="Detector Engine", page_icon="🪐", layout="wide", initial_sidebar_state="collapsed")
# Initialize session state memory for the ledger
if 'history' not in st.session_state:
    st.session_state['history'] = []


# --- 2. GLOBAL UI & SIDEBAR INJECTION ---
components.html("""
<script>
    const win = window.parent;
    const doc = win.document;
    
    /* 1. INJECT CSS STYLES ONCE */
    if (!doc.getElementById('custom-detector-style')) {
        const style = doc.createElement('style');
        style.id = 'custom-detector-style';
        style.innerHTML = `
            body, #root, .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"], main { background: transparent !important; background-color: transparent !important; }
            header { background: transparent !important; box-shadow: none !important; }
            .block-container { padding-top: 4.5rem !important; z-index: 2 !important; position: relative; }
            
            .giant-menu-btn { background: rgba(255, 255, 255, 0.08) !important; border: 1px solid rgba(255, 255, 255, 0.2) !important; border-radius: 50px !important; width: 130px !important; height: 45px !important; display: flex !important; align-items: center !important; justify-content: center !important; margin: 1.5rem !important; backdrop-filter: blur(10px) !important; transition: all 0.3s ease !important; z-index: 999999 !important; position: relative !important;}
            .giant-menu-btn:hover { transform: translateY(-2px) !important; background: rgba(255, 255, 255, 0.15) !important; box-shadow: 0 4px 20px rgba(255, 255, 255, 0.2) !important; }
            .giant-menu-btn svg { display: none !important; }
            .giant-menu-btn::after { content: '☰ MENU' !important; color: #ffffff !important; font-family: 'Inter', sans-serif !important; font-weight: 700 !important; font-size: 1.05rem !important; letter-spacing: 1.5px !important; position: absolute; }
            
            [data-testid="stSidebar"] { position: fixed !important; top: 0 !important; left: 0 !important; min-width: 50vw !important; max-width: 50vw !important; height: 100vh !important; background: linear-gradient(90deg, #0e0e11 40%, #ffffff 40%) !important; border: none !important; box-shadow: 15px 0 50px rgba(0,0,0,0.8) !important; z-index: 999999 !important; transform: translateX(0) !important; transition: transform 0.4s ease-in-out, visibility 0.4s !important; }
            [data-testid="stSidebar"][aria-expanded="false"] { transform: translateX(-50vw) !important; visibility: hidden !important; }
            [data-testid="stSidebar"]::before { content: ''; position: absolute; top: 0; left: 0; bottom: 0; width: 40%; background-image: radial-gradient(rgba(255, 255, 255, 0.12) 1.5px, transparent 1.5px); background-size: 24px 24px; z-index: 1; pointer-events: none; }
            [data-testid="stSidebarNav"] { position: absolute !important; left: 40% !important; top: 12vh !important; width: 60% !important; padding-left: 3rem !important; z-index: 99 !important; background: transparent !important; }
            [data-testid="stSidebarNav"] ul { counter-reset: menu-counter; list-style: none !important; padding: 0 !important; display: flex; flex-direction: column; gap: 1.5rem; }
            
            [data-testid="stSidebarNav"] a { background: transparent !important; text-decoration: none !important; position: relative; display: inline-block; transition: all 0.3s ease !important; padding: 0 !important; width: max-content; }
            [data-testid="stSidebarNav"] a, [data-testid="stSidebarNav"] a * { font-family: 'Inter', sans-serif !important; font-size: 3.5rem !important; font-weight: 800 !important; color: #111111 !important; opacity: 1 !important; text-transform: uppercase !important; letter-spacing: -2px !important; line-height: 1 !important; }
            [data-testid="stSidebarNav"] svg { display: none !important; }
            [data-testid="stSidebarNav"] a:hover { transform: translateX(15px); }
            [data-testid="stSidebarNav"] a:hover, [data-testid="stSidebarNav"] a:hover * { color: #4F46E5 !important; }
            [data-testid="stSidebarNav"] a::after { counter-increment: menu-counter; content: "0" counter(menu-counter); position: absolute; top: 10px; right: -45px; font-size: 1.25rem; color: #4F46E5 !important; font-weight: 600; letter-spacing: 0px; opacity: 1 !important; }
            
            [data-testid="stSidebarHeader"] { position: absolute; top: 1.5rem; right: 2rem; z-index: 100; background: transparent !important; }
            [data-testid="stSidebarHeader"] button svg { display: none !important; }
            [data-testid="stSidebarHeader"] button::before { content: 'Close ✕'; font-family: 'Inter', sans-serif; font-size: 1rem; font-weight: 600; color: #000000; transition: color 0.2s; }
            [data-testid="stSidebarHeader"] button:hover::before { color: #4F46E5; }
        `;
        doc.head.appendChild(style);
    }
    
    /* 2. FIND OR CREATE CANVAS */
    let canvas = doc.getElementById('bg-canvas');
    if (!canvas) {
        const canvasDiv = doc.createElement('div');
        canvasDiv.innerHTML = '<canvas id="bg-canvas" style="position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; z-index: 0; pointer-events: none; background-color: #050505;"></canvas>';
        doc.body.insertBefore(canvasDiv, doc.body.firstChild);
        canvas = doc.getElementById('bg-canvas');
    }
    
    /* 3. REBOOT ANIMATION ENGINE ON EVERY PAGE LOAD */
    const ctx = canvas.getContext('2d');
    let width, height, particles = [];
    let mouse = { x: null, y: null };
    
    win.addEventListener('mousemove', (e) => { mouse.x = e.clientX; mouse.y = e.clientY; });
    
    function init() {
        width = canvas.width = win.innerWidth; 
        height = canvas.height = win.innerHeight; 
        particles = [];
        let numParticles = Math.min(150, Math.floor((width * height) / 12000));
        for (let i = 0; i < numParticles; i++) {
            particles.push({ x: Math.random() * width, y: Math.random() * height, r: Math.random() * 1.5 + 0.5, vx: (Math.random() - 0.5) * 0.5, vy: (Math.random() - 0.5) * 0.5, baseAlpha: Math.random() * 0.5 + 0.1 });
        }
    }
    
    function animate() {
        ctx.clearRect(0, 0, width, height);
        particles.forEach(p => {
            p.x += p.vx; p.y += p.vy;
            if (p.x < 0 || p.x > width) p.vx *= -1;
            if (p.y < 0 || p.y > height) p.vy *= -1;
            let alpha = p.baseAlpha;
            if (mouse.x !== null && mouse.y !== null) {
                let dx = mouse.x - p.x; let dy = mouse.y - p.y;
                let dist = Math.sqrt(dx*dx + dy*dy);
                if (dist < 120) alpha = Math.min(1, alpha + (120-dist)/120);
            }
            ctx.beginPath(); ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2); ctx.fillStyle = `rgba(255, 255, 255, ${alpha})`; ctx.fill();
        });
        win.requestAnimationFrame(animate); 
    }
    init(); 
    win.requestAnimationFrame(animate);
    win.addEventListener('resize', init);
    
    /* 4. CONTINUOUS UI OBSERVER */
    setInterval(() => {
        // A. Maintain Menu Button
        const headerBtns = Array.from(doc.querySelectorAll('header button'));
        const targetBtn = headerBtns.find(b => b.getBoundingClientRect().left < 100);
        if (targetBtn && !targetBtn.classList.contains('giant-menu-btn')) { targetBtn.classList.add('giant-menu-btn'); }
        
        // B. Rename 'App' to 'HOME'
        const navSpans = Array.from(doc.querySelectorAll('[data-testid="stSidebarNav"] a span'));
        navSpans.forEach(span => {
            if (span.textContent.trim().toLowerCase() === 'app') {
                span.textContent = 'HOME';
            }
        });
        
        // C. Clean Menu Retraction (NATIVE CLICK)
        const navLinks = Array.from(doc.querySelectorAll('[data-testid="stSidebarNav"] a'));
        navLinks.forEach(link => {
            if (!link.hasAttribute('data-click-injected')) {
                link.setAttribute('data-click-injected', 'true');
                link.addEventListener('click', () => {
                    const closeBtn = doc.querySelector('[data-testid="stSidebarHeader"] button');
                    if (closeBtn) closeBtn.click(); // Triggers Streamlit's native close sequence
                });
            }
        });
    }, 100);
</script>
""", height=0)

# --- 3. PAGE STYLING ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;900&family=JetBrains+Mono:wght@400;600;700&family=Orbitron:wght@600;800;900&display=swap');
        h1, h2, h3 { font-family: 'Inter', sans-serif !important; }
        p, label { font-family: 'Inter', sans-serif !important; color: #94A3B8; }
        
        .metric-card { background: rgba(10, 10, 10, 0.7); border: 1px solid rgba(255,255,255,0.1); border-radius: 1rem; padding: 1.5rem; text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.5); backdrop-filter: blur(10px); }
        .metric-title { font-size: 0.85rem; color: #64748B; text-transform: uppercase; letter-spacing: 1px; font-weight: 600; margin-bottom: 0.5rem; }
        .metric-val { font-size: 2rem; color: #fff; font-family: 'JetBrains Mono', monospace; font-weight: 700; }
        .pred-exo { text-shadow: 0 0 20px rgba(0, 229, 255, 0.8); color: #00E5FF; }
        .pred-false { text-shadow: 0 0 20px rgba(255, 51, 102, 0.8); color: #FF3366; }
        
        /* Guide HUD Box */
        .guide-box {
            background: rgba(15, 23, 42, 0.5);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            padding: 1.25rem 1.5rem;
            backdrop-filter: blur(8px);
            margin-bottom: 2rem;
        }
        .guide-title {
            font-family: 'Orbitron', sans-serif;
            font-size: 0.95rem;
            font-weight: 700;
            color: #ffffff;
            letter-spacing: 1.2px;
            text-transform: uppercase;
            margin-bottom: 0.5rem;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .guide-text {
            font-size: 0.88rem;
            line-height: 1.5;
            color: #94A3B8;
            margin-bottom: 0.75rem;
        }
        .guide-tag {
            display: inline-block;
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.15);
            padding: 3px 10px;
            border-radius: 6px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.82rem;
            color: #E2E8F0;
            margin-right: 6px;
            margin-bottom: 4px;
        }
        .db-link {
            color: #00E5FF !important;
            text-decoration: none !important;
            font-weight: 600;
            transition: all 0.2s ease;
        }
        .db-link:hover {
            text-decoration: underline !important;
            color: #ffffff !important;
        }
        
        /* Input Styling */
        div[data-testid="stTextInput"] label p, div[data-testid="stNumberInput"] label p { font-family: 'Orbitron', sans-serif !important; color: #ffffff !important; letter-spacing: 1.5px; font-size: 0.85rem; text-transform: uppercase; }
        div[data-baseweb="input"] { background-color: rgba(10, 15, 29, 0.6) !important; border: 1px solid rgba(255, 255, 255, 0.2) !important; border-radius: 8px !important; backdrop-filter: blur(5px); }
        div[data-baseweb="input"] input { color: #ffffff !important; font-family: 'JetBrains Mono', monospace !important; font-size: 1.1rem !important; }
        div[data-baseweb="input"]:focus-within { border-color: #ffffff !important; box-shadow: 0 0 15px rgba(255,255,255,0.2) !important; }
        
        /* Run Analysis Button */
        div.stButton > button { background: #ffffff !important; color: #000000 !important; border: none !important; font-family: 'Orbitron', sans-serif !important; font-weight: 900 !important; font-size: 1.2rem !important; padding: 1.2rem !important; border-radius: 8px !important; box-shadow: 0 4px 20px rgba(255, 255, 255, 0.25) !important; text-transform: uppercase !important; letter-spacing: 2px !important; transition: all 0.3s ease !important; margin-top: 1rem; }
        div.stButton > button:hover { background: #f0f0f0 !important; color: #000000 !important; box-shadow: 0 8px 30px rgba(255, 255, 255, 0.5) !important; transform: translateY(-4px) !important; }
        div.stButton > button p { color: #000000 !important; }
        
        /* Agent Dossier Box */
        .agent-box { background: rgba(10, 15, 29, 0.8); border-left: 4px solid #ffffff; padding: 2rem; border-radius: 0 1rem 1rem 0; color: #E2E8F0; margin-top: 1.5rem; backdrop-filter: blur(10px); line-height: 1.6; }
        .agent-header { color: #fff; font-family: 'Orbitron', sans-serif; font-size: 1.2rem; margin-bottom: 1.2rem; display: flex; align-items: center; gap: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- 4. API CONFIGURATION (TOP LEFT HUD) ---
col_key, col_spacer = st.columns([1.6, 3.4])
with col_key:
    user_api_key = st.text_input(
        "GEMINI API KEY (OPTIONAL)", 
        type="password", 
        placeholder="Enter personal key...",
        help="If left blank, the server will securely use its internal key or standard fallback."
    )

# --- 5. MODEL CACHING ---
@st.cache_resource
def load_cached_model():
    return train_or_load_model()

try:
    model = load_cached_model()
except Exception as e:
    st.error(f"🚨 Model Error: {e}")
    st.stop()

# --- 6. HEADER & GUIDANCE CONSOLE ---
st.markdown("""
<div style="text-align: center; margin-bottom: 2rem;">
    <h1 style="font-family: 'Inter', sans-serif; font-weight: 700; font-size: 3.8rem; background: linear-gradient(to right, #ffffff, #777777); -webkit-background-clip: text; -webkit-text-fill-color: transparent; letter-spacing: -1.5px; margin-bottom: 0;">AI TELEMETRY PIPELINE</h1>
    <p style="color: #94A3B8; font-size: 1.05rem; margin-top: 0.5rem; max-width: 650px; margin-left: auto; margin-right: auto;">Autonomous NASA MAST telemetry pipeline with Box Least Squares signal extraction, XGBoost classification, and Gemini 3.6 vetting intelligence.</p>
</div>
""", unsafe_allow_html=True)

# --- GUIDE & DATABASE ACCESS SECTION ---
col_guide1, col_guide2 = st.columns(2)

with col_guide1:
    st.markdown("""
    <div class="guide-box">
        <div class="guide-title">📡 What is an Observation Sector?</div>
        <div class="guide-text">
            TESS divides the celestial sky into 24° × 96° swaths called <b>Sectors</b>, imaging each for ~27.4 days.<br>
            • <b>Sector 0 (Recommended)</b>: Queries the database to retrieve all available observation windows for the target.<br>
            • <b>Specific Sector (e.g. 1 to 80+)</b>: Targets a specific 27-day observation campaign.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_guide2:
    st.markdown("""
    <div class="guide-box">
        <div class="guide-title">🌌 NASA Star Catalog Access</div>
        <div class="guide-text">
            Find target IDs via official public repositories:<br>
            • <a href="https://exoplanetarchive.ipac.caltech.edu/" target="_blank" class="db-link">NASA Exoplanet Archive ↗</a> (Confirmed exoplanets & candidates)<br>
            • <a href="https://mast.stsci.edu/search/ui/#/" target="_blank" class="db-link">Mikulski Archive (MAST) Portal ↗</a> (Kepler & TESS raw targets)<br>
            • <a href="https://exofop.ipac.caltech.edu/tess/" target="_blank" class="db-link">ExoFOP-TESS Portal ↗</a> (Community exoplanet follow-up)
        </div>
    </div>
    """, unsafe_allow_html=True)

# Quick sample chips
st.markdown("""
<div style="text-align: center; margin-bottom: 1.5rem;">
    <span style="font-family: 'Orbitron', sans-serif; font-size: 0.8rem; color: #64748B; letter-spacing: 1px; text-transform: uppercase; margin-right: 8px;">Try sample targets:</span>
    <span class="guide-tag">Pi Mensae</span>
    <span class="guide-tag">Kepler-10</span>
    <span class="guide-tag">TOI-700</span>
    <span class="guide-tag">WASP-12</span>
    <span class="guide-tag">KIC 10030943 (Binary)</span>
</div>
""", unsafe_allow_html=True)

# --- 7. TARGET INPUT HUD ---
col_space1, col_target, col_sector, col_space2 = st.columns([1, 2, 1, 1])

with col_target:
    target_name = st.text_input("STAR TARGET ID", value="Pi Mensae", placeholder="e.g. Pi Mensae, Kepler-10, KIC 10030943")

with col_sector:
    sector = st.number_input("SECTOR (0 = ALL)", min_value=0, max_value=100, value=1)

col_b1, col_btn, col_b2 = st.columns([1, 3, 1])
with col_btn:
    run_analysis_btn = st.button("RUN ANALYSIS", use_container_width=True)

st.markdown("<br><hr style='border: 1px solid rgba(255,255,255,0.05);'><br>", unsafe_allow_html=True)

# --- 8. MAIN ANALYSIS EXECUTION ---
if run_analysis_btn and target_name:
    analysis_success = False
    
    with st.status(f"📡 Initializing deep-space query for {target_name}...", expanded=True) as status:
        st.write("📥 Querying NASA MAST servers and downloading pixel telemetry...")
        sec = sector if sector > 0 else None
        raw_lc, clean_lc = fetch_and_clean_lightcurve(target_name, sector=sec)
        
        if clean_lc is None:
            status.update(label="Query Failed", state="error", expanded=True)
            st.error(f"Could not find valid telemetry for '{target_name}'. Try Sector 0 to search all available observation windows.")
        else:
            st.write("🧮 Executing Box Least Squares (BLS) transit periodogram...")
            bls, best_period, best_t0 = run_bls(clean_lc)
            
            st.write("🤖 Extracting photometric morphology features...")
            features = extract_features(clean_lc, period=best_period, t0=best_t0)
            
            st.write("🧠 Consulting XGBoost Classification Engine...")
            prediction, confidence = predict_candidate(model, features)
            
            st.write("📝 Synthesizing observation dossier with Gemini 3.6...")
            dossier_content = generate_vetting_report(
                target_name=target_name,
                features=features,
                prediction=prediction,
                confidence=confidence,
                api_key=user_api_key
            )
            
            status.update(label="Analysis Complete", state="complete", expanded=False)
            analysis_success = True

            status.update(label="Analysis Complete", state="complete", expanded=False)
            analysis_success = True

            # --- NEW: SAVE TO MEMORY ---
            st.session_state['history'].append({
                "Target": target_name.upper(),
                "Sector": sector,
                "Period (d)": round(features.get('period_days', best_period), 3),
                "SNR": round(features.get('snr', 0), 1),
                "Confidence": f"{confidence:.1f}%",
                "Classification": "CONFIRMED PLANET" if (prediction == 1) else "FALSE POSITIVE",
                "Dossier": dossier_content
            })

    # --- 9. RESULTS DISPLAY ---
    if analysis_success:
        is_planet = (prediction == 1)
        
        # Metric Cards
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.markdown(f"<div class='metric-card'><div class='metric-title'>Orbital Period</div><div class='metric-val'>{features.get('period_days', best_period):.3f} d</div></div>", unsafe_allow_html=True)
        with m2:
            st.markdown(f"<div class='metric-card'><div class='metric-title'>Transit Depth</div><div class='metric-val'>{features.get('signal_depth', 0):.4f}</div></div>", unsafe_allow_html=True)
        with m3:
            st.markdown(f"<div class='metric-card'><div class='metric-title'>Model SNR</div><div class='metric-val'>{features.get('snr', 0):.1f}</div></div>", unsafe_allow_html=True)
        with m4:
            cls_text = "CONFIRMED PLANET" if is_planet else "FALSE POSITIVE"
            glow_class = "pred-exo" if is_planet else "pred-false"
            st.markdown(f"<div class='metric-card'><div class='metric-title'>AI Classification ({confidence:.1f}%)</div><div class='metric-val {glow_class}'>{cls_text}</div></div>", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)

        # Plotly Visuals
        folded_lc = clean_lc.fold(period=best_period, epoch_time=best_t0)
        binned_lc = folded_lc.bin(time_bin_size=0.01)

        tab1, tab2, tab3 = st.tabs(["📈 Phase-Folded Transit Signal", "📊 Raw Photometry Flux", "📋 Extracted Parameters"])

        with tab1:
            fig_fold = go.Figure()
            # Raw Scatter
            fig_fold.add_trace(go.Scatter(
                x=np.array(folded_lc.time.value, dtype=float),
                y=np.array(folded_lc.flux.value, dtype=float),
                mode='markers',
                marker=dict(size=2.5, color='rgba(148, 163, 184, 0.4)'),
                name='Raw Phase Data'
            ))
            # Binned Signal
            if len(binned_lc) > 0:
                fig_fold.add_trace(go.Scatter(
                    x=np.array(binned_lc.time.value, dtype=float),
                    y=np.array(binned_lc.flux.value, dtype=float),
                    mode='markers+lines',
                    marker=dict(size=6, color='#00E5FF'),
                    line=dict(color='#00E5FF', width=1.5),
                    name='Binned Signal'
                ))
            fig_fold.update_layout(
                template="plotly_dark",
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                title=f"Phase-Folded Transit (Period: {best_period:.4f} days)",
                xaxis_title="Phase Offset (Days)",
                yaxis_title="Normalized Flux",
                height=450
            )
            st.plotly_chart(fig_fold, use_container_width=True)

        with tab2:
            fig_raw = go.Figure()
            fig_raw.add_trace(go.Scatter(
                x=np.array(clean_lc.time.value, dtype=float),
                y=np.array(clean_lc.flux.value, dtype=float),
                mode='markers',
                marker=dict(size=2, color='#94A3B8'),
                name='Cleaned Flux'
            ))
            fig_raw.update_layout(
                template="plotly_dark",
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                title="Continuous Light Curve Photometry",
                xaxis_title="Time (BTJD / Days)",
                yaxis_title="Normalized Flux",
                height=450
            )
            st.plotly_chart(fig_raw, use_container_width=True)

        with tab3:
            feature_display_df = pd.DataFrame([features]).T.reset_index()
            feature_display_df.columns = ["Astrometric Feature Parameter", "Extracted Value"]
            st.dataframe(feature_display_df, use_container_width=True)

        # Gemini 3.6 Observation Memo
        st.markdown(f"""
        <div class="agent-box">
            <div class="agent-header">
                <span>🧠</span> GEMINI 3.6 ASTROPHYSICS DOSSIER
            </div>
            {dossier_content.replace(chr(10), '<br>')}
        </div>
        """, unsafe_allow_html=True)

        