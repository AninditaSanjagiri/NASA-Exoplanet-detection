import streamlit as st
import streamlit.components.v1 as components
import pandas as pd

# --- 1. PAGE CONFIGURATION ---

st.set_page_config(page_title="Discovery Ledger", page_icon="📜", layout="wide", initial_sidebar_state="collapsed")

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

# --- 3. HEADER ---
st.markdown("""
<div style="text-align: center; margin-bottom: 3rem; padding-top: 2rem;">
    <h1 style="font-family: 'Inter', sans-serif; font-weight: 700; font-size: 3.5rem; background: linear-gradient(to right, #ffffff, #777777); -webkit-background-clip: text; -webkit-text-fill-color: transparent; letter-spacing: -1.5px; margin-bottom: 0;">MISSION LEDGER</h1>
    <p style="color: #94A3B8; font-size: 1.1rem; margin-top: 0.5rem;">Historical database of all analyzed space telemetry and AI verdicts from your current session.</p>
</div>
""", unsafe_allow_html=True)

# --- 4. DATA RENDERING ---
if 'history' not in st.session_state or len(st.session_state['history']) == 0:
    st.info("🛰️ No telemetry logs found in current session. Run an analysis on the Detector page to populate the ledger.")
else:
    # Convert history to DataFrame
    df = pd.DataFrame(st.session_state['history'])
    
    # Display the table (excluding the massive dossier text for cleanliness)
    display_df = df.drop(columns=["Dossier"])
    st.dataframe(display_df, use_container_width=True, hide_index=True)
    
    st.markdown("<br><hr style='border: 1px solid rgba(255,255,255,0.1);'><br>", unsafe_allow_html=True)
    st.subheader("Archived AI Dossiers")
    
    # Loop through history and create an expandable drop-down for each Gemini report
    for idx, row in df.iterrows():
        icon = "🟢" if row['Classification'] == "CONFIRMED PLANET" else "🔴"
        with st.expander(f"{icon} {row['Target']} (Sector {row['Sector']}) — {row['Confidence']}"):
            st.markdown(f"""
            <div class="agent-box">
                {row['Dossier']}
            </div>
            """, unsafe_allow_html=True)