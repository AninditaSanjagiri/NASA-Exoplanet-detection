import streamlit as st
import streamlit.components.v1 as components

# --- 1. PAGE CONFIGURATION & NATIVE UI HIDING ---
st.set_page_config(page_title="TESS Exoplanet AI", layout="wide", initial_sidebar_state="collapsed")

# --- 2. JAVASCRIPT UI INJECTION (THE FOOLPROOF MENU BUTTON) ---
# This script hunts down the >> arrow and forces it to become the MENU pill
components.html("""
<script>
    const doc = window.parent.document;
    
    // Inject custom CSS directly into the parent window
    if (!doc.getElementById('custom-menu-style')) {
        const style = doc.createElement('style');
        style.id = 'custom-menu-style';
        style.innerHTML = `
            .giant-menu-btn {
                background: rgba(255, 255, 255, 0.08) !important;
                border: 1px solid rgba(255, 255, 255, 0.2) !important;
                border-radius: 50px !important;
                width: 130px !important;
                height: 45px !important;
                display: flex !important;
                align-items: center !important;
                justify-content: center !important;
                backdrop-filter: blur(10px) !important;
                transition: all 0.3s ease !important;
                position: relative !important;
                margin-left: 1rem !important;
                margin-top: 0.5rem !important;
                z-index: 999999 !important;
            }
            .giant-menu-btn:hover {
                background: rgba(255, 255, 255, 0.15) !important;
                transform: translateY(-2px) !important;
                box-shadow: 0 4px 15px rgba(255,255,255,0.1) !important;
            }
            .giant-menu-btn svg { display: none !important; }
            .giant-menu-btn::after {
                content: '☰ MENU' !important;
                color: #ffffff !important;
                font-family: 'Inter', sans-serif !important;
                font-weight: 700 !important;
                font-size: 1.05rem !important;
                letter-spacing: 1.5px !important;
            }
        `;
        doc.head.appendChild(style);
    }

    // Loop to continuously ensure the button stays styled, even if Streamlit re-renders
    setInterval(() => {
        // Find all buttons in the header
        const headerBtns = Array.from(doc.querySelectorAll('header button'));
        
        // Find the specific button on the far left of the screen (ignoring the right side)
        const targetBtn = headerBtns.find(b => b.getBoundingClientRect().left < 100);
        
        if (targetBtn && !targetBtn.classList.contains('giant-menu-btn')) {
            targetBtn.classList.add('giant-menu-btn');
        }
    }, 100);
</script>
""", height=0)

# --- CUSTOM LOGO FOR THE SIDEBAR ---
st.sidebar.markdown("""
    <div style="position: absolute; top: 1.5rem; left: 1.5rem; color: white; font-family: 'Inter', sans-serif; font-weight: 700; font-size: 1.2rem; display: flex; align-items: center; gap: 10px; z-index: 99999; letter-spacing: 1px;">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2L2 22h20L12 2z"/></svg>
        EXOPLANET AI
    </div>
""", unsafe_allow_html=True)

# --- ADVANCED CSS FOR HALF-SCREEN MENU OVERLAY ---
st.markdown("""
    <style>
        /* 1. Base App & Header */
        .stApp { background-color: #050505 !important; }
        .block-container { padding: 0 !important; max-width: 100% !important; margin: 0 !important; }
        header { background: transparent !important; box-shadow: none !important; }

        /* 2. Transform Native Sidebar into 50vw Overlay Drawer */
        [data-testid="stSidebar"] {
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            min-width: 50vw !important;
            max-width: 50vw !important;
            height: 100vh !important;
            background: linear-gradient(90deg, #0e0e11 40%, #ffffff 40%) !important;
            border: none !important;
            box-shadow: 15px 0 50px rgba(0,0,0,0.8) !important;
            z-index: 999999 !important;
            transform: translateX(0) !important;
            transition: transform 0.4s ease-in-out, visibility 0.4s !important;
        }
        
        [data-testid="stSidebar"][aria-expanded="false"] {
            transform: translateX(-50vw) !important;
            visibility: hidden !important;
        }

        [data-testid="stSidebar"]::before {
            content: '';
            position: absolute;
            top: 0; left: 0; bottom: 0; width: 40%;
            background-image: radial-gradient(rgba(255, 255, 255, 0.12) 1.5px, transparent 1.5px);
            background-size: 24px 24px;
            z-index: 1;
            pointer-events: none;
        }

        /* 3. Shift Menu Links to the White Side */
        [data-testid="stSidebarNav"] {
            position: absolute !important;
            left: 40% !important;
            top: 25vh !important;
            width: 60% !important;
            padding-left: 3rem !important;
            z-index: 99 !important;
            background: transparent !important;
        }

        /* 4. Typography Menu Links */
        [data-testid="stSidebarNav"] ul {
            counter-reset: menu-counter;
            list-style: none !important;
            padding: 0 !important;
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
        }

        [data-testid="stSidebarNav"] a {
            font-family: 'Inter', sans-serif !important;
            font-size: 4rem !important;
            font-weight: 800 !important;
            color: #111111 !important;
            background: transparent !important;
            text-transform: uppercase !important;
            letter-spacing: -2px !important;
            line-height: 1 !important;
            text-decoration: none !important;
            position: relative;
            display: inline-block;
            transition: all 0.3s ease !important;
            padding: 0 !important;
            width: max-content;
        }
        
        [data-testid="stSidebarNav"] a span {
            font-family: inherit !important;
            font-size: inherit !important;
            font-weight: inherit !important;
            color: inherit !important;
            text-transform: inherit !important;
            letter-spacing: inherit !important;
        }
        
        [data-testid="stSidebarNav"] svg { display: none !important; }

        [data-testid="stSidebarNav"] a:hover {
            color: #4F46E5 !important;
            transform: translateX(15px);
        }
        
        [data-testid="stSidebarNav"] a[aria-current="page"] {
            background: transparent !important;
            color: #111111 !important;
        }
        
        [data-testid="stSidebarNav"] a::after {
            counter-increment: menu-counter;
            content: "0" counter(menu-counter);
            position: absolute;
            top: 10px;
            right: -45px;
            font-size: 1.25rem;
            color: #4F46E5;
            font-weight: 600;
            letter-spacing: 0px;
        }

        /* 5. Custom "Close ✕" Button */
        [data-testid="stSidebarHeader"] {
            position: absolute;
            top: 1.5rem;
            right: 2rem;
            z-index: 100;
            background: transparent !important;
        }
        [data-testid="stSidebarHeader"] button svg { display: none !important; }
        [data-testid="stSidebarHeader"] button::before {
            content: 'Close ✕';
            font-family: 'Inter', sans-serif;
            font-size: 1rem;
            font-weight: 600;
            color: #000000;
            transition: color 0.2s;
        }
        [data-testid="stSidebarHeader"] button:hover::before { color: #4F46E5; }
        
        /* 6. Massive CTA Button */
        div.stButton > button:first-child {
            background: #ffffff !important;
            border-radius: 50px !important;
            padding: 1.5rem 3rem !important;
            border: none !important;
            box-shadow: 0 4px 20px rgba(255, 255, 255, 0.25) !important;
            transition: all 0.3s ease !important;
            display: block;
            margin: 0 auto;
            margin-top: 1.5rem;
            margin-bottom: 3.5rem;
        }
        div.stButton > button:first-child p {
            color: #000000 !important;
            font-family: 'Orbitron', sans-serif !important;
            font-weight: 900 !important;
            font-size: 1.8rem !important;
            text-transform: uppercase !important;
            letter-spacing: 2px !important;
            margin: 0 !important;
        }
        div.stButton > button:first-child:hover {
            transform: translateY(-4px) !important;
            box-shadow: 0 8px 30px rgba(255, 255, 255, 0.5) !important;
        }
    </style>
""", unsafe_allow_html=True)

# --- 2. THE PARTICLES HERO SECTION ---
# Background set to transparent to blend with Streamlit
particles_hero_html = """
<!DOCTYPE html>
<html>
<head>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;500;700&display=swap" rel="stylesheet">
    <style>
        body { margin: 0; padding: 0; background-color: transparent; color: white; font-family: 'Inter', sans-serif; overflow: hidden; }
        #canvas-container { position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 1; }
        .content { position: relative; z-index: 2; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; text-align: center; pointer-events: none; }
        .pill { background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15); padding: 8px 20px; border-radius: 50px; font-size: 0.9rem; font-weight: 600; letter-spacing: 1.5px; margin-bottom: 1.5rem; backdrop-filter: blur(10px); }
        h1 { font-size: 4.8rem; font-weight: 700; margin: 0 0 1rem 0; letter-spacing: -1.5px; background: linear-gradient(to right, #ffffff, #777777); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        p { font-size: 1.25rem; color: #888; max-width: 650px; line-height: 1.6; margin: 0; font-weight: 300; }
    </style>
</head>
<body>
    <canvas id="canvas-container"></canvas>
    <div class="content">
        <div class="pill"> POWERED BY NASA DATA</div>
        <h1>AI Exoplanet Hunter</h1>
        <p>Ready to hunt for alien worlds? Our AI acts like a smart telescope, analyzing the subtle dips in distant starlight to find hidden planets!<br><br>
        <span style="font-size: 1rem; color: #aaa; background: rgba(255,255,255,0.05); padding: 10px 15px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.1); display: inline-block; margin-top: 10px;">
        <b>🔭 Quick Heads-Up:</b> Tiny, Earth-sized planets are incredibly difficult to detect because they barely block any light when passing in front of their enormous suns. For now, our detector is much better at catching the massive, Jupiter-sized giants!
        </span></p>
    </div>
    <script>
        const canvas = document.getElementById('canvas-container');
        const ctx = canvas.getContext('2d');
        let width, height, particles = [];
        
        let mouse = { x: null, y: null };
        window.addEventListener('mousemove', (e) => { mouse.x = e.x; mouse.y = e.y; });
        
        function init() {
            width = canvas.width = window.innerWidth;
            height = canvas.height = 450; 
            particles = [];
            for (let i = 0; i < 150; i++) {
                particles.push({
                    x: Math.random() * width, y: Math.random() * height,
                    r: Math.random() * 1.5 + 0.5,
                    vx: (Math.random() - 0.5) * 0.5, vy: (Math.random() - 0.5) * 0.5,
                    baseAlpha: Math.random() * 0.5 + 0.1
                });
            }
        }
        
        function animate() {
            ctx.clearRect(0, 0, width, height);
            particles.forEach(p => {
                p.x += p.vx; p.y += p.vy;
                if (p.x < 0 || p.x > width) p.vx *= -1;
                if (p.y < 0 || p.y > height) p.vy *= -1;
                
                let dx = mouse.x - p.x; let dy = mouse.y - p.y;
                let dist = Math.sqrt(dx*dx + dy*dy);
                let alpha = p.baseAlpha;
                if (dist < 100) alpha = Math.min(1, alpha + (100-dist)/100);
                
                ctx.beginPath();
                ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
                ctx.fillStyle = `rgba(255, 255, 255, ${alpha})`;
                ctx.fill();
            });
            requestAnimationFrame(animate);
        }
        init(); animate();
        window.addEventListener('resize', init);
    </script>
</body>
</html>
"""
components.html(particles_hero_html, height=450)

# --- 3. THE NATIVE ROUTING BUTTON ---
col1, col2, col3 = st.columns([1, 1.5, 1])
with col2:
    if st.button("Launch The Detector", use_container_width=True):
        st.switch_page("pages/detector.py")

# --- 4. THE SPOTLIGHT CARDS ---
# Background set to transparent
spotlight_cards_html = """
<!DOCTYPE html>
<html>
<head>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
    <style>
        body { margin: 0; padding: 20px; background-color: transparent; font-family: 'Inter', sans-serif; display: flex; justify-content: center; gap: 20px; }
        
        .card-spotlight {
            position: relative;
            border-radius: 1.5rem;
            border: 1px solid #222;
            background-color: #0A0A0A; /* Slightly lighter than pitch black for contrast */
            padding: 2rem;
            overflow: hidden;
            --mouse-x: 50%;
            --mouse-y: 50%;
            --spotlight-color: rgba(255, 255, 255, 0.12);
            width: 220px;
            cursor: default;
        }
        .card-spotlight::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background: radial-gradient(circle at var(--mouse-x) var(--mouse-y), var(--spotlight-color), transparent 80%);
            opacity: 0;
            transition: opacity 0.5s ease;
            pointer-events: none;
        }
        .card-spotlight:hover::before { opacity: 1; }
        
        .title { color: #888; font-size: 0.85rem; font-weight: 600; letter-spacing: 0.5px; text-transform: uppercase; margin-bottom: 10px; }
        .value { color: #fff; font-size: 2.2rem; font-weight: 600; margin-bottom: 5px; letter-spacing: -1px; }
        .sub { color: #555; font-size: 0.85rem; }
    </style>
</head>
<body>
    <body>
    <div class="card-spotlight">
        <div class="title">AI Accuracy</div>
        <div class="value">86.8%</div>
        <div class="sub">Trained on Kepler Data</div>
    </div>
    <div class="card-spotlight">
        <div class="title">Known Worlds</div>
        <div class="value">7,016+</div>
        <div class="sub">Confirmed by NASA</div>
    </div>
    <div class="card-spotlight">
        <div class="title">Live Data</div>
        <div class="value">MAST API</div>
        <div class="sub">Real Telescope Telemetry</div>
    </div>
    <div class="card-spotlight">
        <div class="title">AI Assistant</div>
        <div class="value">Gemini</div>
        <div class="sub">Smart Dossier Generation</div>
    </div>

    <script>
        const cards = document.querySelectorAll('.card-spotlight');
        cards.forEach(card => {
            card.addEventListener('mousemove', e => {
                const rect = card.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                card.style.setProperty('--mouse-x', `${x}px`);
                card.style.setProperty('--mouse-y', `${y}px`);
            });
        });
    </script>
</body>
</html>
"""
components.html(spotlight_cards_html, height=220)

# --- INTERACTIVE SIMULATOR (CUSTOM HTML/CANVAS) ---
st.markdown("<br><hr style='border: 1px solid rgba(255,255,255,0.08);'><br>", unsafe_allow_html=True)

st.markdown("""
<div style="text-align: center; margin-bottom: 2rem;">
    <h3 style="font-family: 'Orbitron', sans-serif; font-size: 2rem; margin-bottom: 0.5rem; letter-spacing: 1px;">🎛️ Interactive Light Curve Vetting Dashboard</h3>
    <p style="color: #94A3B8; font-size: 1.1rem; max-width: 800px; margin: 0 auto;">
        Explore how planetary transits differ from stellar eclipsing binaries. Adjust physical parameters below to see the phase-folded light curve update in real-time.
    </p>
</div>
""", unsafe_allow_html=True)

simulator_html = """
<!DOCTYPE html>
<html>
<head>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=Orbitron:wght@600&family=JetBrains+Mono&display=swap" rel="stylesheet">
    <style>
        body { margin: 0; padding: 0; background: transparent; color: white; font-family: 'Inter', sans-serif; display: flex; gap: 20px; }
        
        /* Layout */
        .simulator-box { display: flex; width: 100%; background: #0A0A0A; border: 1px solid #222; border-radius: 1.5rem; padding: 25px; box-sizing: border-box; box-shadow: 0 10px 40px rgba(0,0,0,0.5); gap: 25px;}
        .controls { flex: 1; display: flex; flex-direction: column; gap: 20px; }
        .display { flex: 2; position: relative; background: #050505; border: 1px solid #1A1A1A; border-radius: 1rem; overflow: hidden; }
        
        /* Typography */
        h4 { font-family: 'Orbitron', sans-serif; margin: 0 0 15px 0; font-size: 1.2rem; color: #fff; letter-spacing: 1px; }
        label { font-size: 0.85rem; color: #94A3B8; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; display: flex; justify-content: space-between; margin-bottom: 8px;}
        span.val { font-family: 'JetBrains Mono', monospace; color: #fff; }
        
        /* Toggles */
        .toggle-group { display: flex; gap: 10px; background: #111; padding: 5px; border-radius: 8px; border: 1px solid #222;}
        .btn { flex: 1; text-align: center; padding: 10px; font-size: 0.8rem; font-weight: 600; cursor: pointer; border-radius: 5px; transition: all 0.3s; color: #666; text-transform: uppercase;}
        .btn.active.exo { background: rgba(0, 229, 255, 0.15); color: #00E5FF; box-shadow: 0 0 15px rgba(0, 229, 255, 0.2); }
        .btn.active.bin { background: rgba(255, 51, 102, 0.15); color: #FF3366; box-shadow: 0 0 15px rgba(255, 51, 102, 0.2); }
        
        /* Custom Sliders */
        input[type=range] { -webkit-appearance: none; width: 100%; background: transparent; }
        input[type=range]:focus { outline: none; }
        input[type=range]::-webkit-slider-runnable-track { width: 100%; height: 6px; cursor: pointer; background: #222; border-radius: 5px; }
        input[type=range]::-webkit-slider-thumb { height: 16px; width: 16px; border-radius: 50%; background: #fff; cursor: pointer; -webkit-appearance: none; margin-top: -5px; box-shadow: 0 0 10px rgba(255,255,255,0.5);}
        .exo-theme input[type=range]::-webkit-slider-thumb { background: #00E5FF; box-shadow: 0 0 15px #00E5FF; }
        .exo-theme input[type=range]::-webkit-slider-runnable-track { background: linear-gradient(90deg, rgba(0,229,255,0.3) 0%, #222 100%); }
        .bin-theme input[type=range]::-webkit-slider-thumb { background: #FF3366; box-shadow: 0 0 15px #FF3366; }
        .bin-theme input[type=range]::-webkit-slider-runnable-track { background: linear-gradient(90deg, rgba(255,51,102,0.3) 0%, #222 100%); }

        canvas { width: 100%; height: 100%; display: block; }
    </style>
</head>
<body>

<div class="simulator-box" id="sim-box">
    <div class="controls">
        <h4>Signal Source</h4>
        <div class="toggle-group">
            <div class="btn active exo" id="btn-exo" onclick="setType('exo')">Exoplanet</div>
            <div class="btn" id="btn-bin" onclick="setType('bin')">Eclipsing Binary</div>
        </div>
        
        <div style="margin-top: 10px;" id="theme-wrapper" class="exo-theme">
            <div>
                <label>Transit Depth <span class="val" id="val-depth">1.2%</span></label>
                <input type="range" id="slider-depth" min="0.001" max="0.040" step="0.001" value="0.012">
            </div>
            <div style="margin-top: 20px;">
                <label>Duration (Phase) <span class="val" id="val-dur">0.10</span></label>
                <input type="range" id="slider-dur" min="0.04" max="0.20" step="0.01" value="0.10">
            </div>
            <div style="margin-top: 20px;">
                <label>Photometric Noise <span class="val" id="val-noise">0.0015</span></label>
                <input type="range" id="slider-noise" min="0.0" max="0.006" step="0.0005" value="0.0015">
            </div>
            <div style="margin-top: 20px; transition: opacity 0.3s;" id="sec-ratio-container" style="opacity: 0.3; pointer-events: none;">
                <label>Secondary Eclipse Ratio <span class="val" id="val-sec">45%</span></label>
                <input type="range" id="slider-sec" min="0.1" max="0.9" step="0.05" value="0.45">
            </div>
        </div>
    </div>
    <div class="display">
        <canvas id="plot"></canvas>
    </div>
</div>

<script>
    let type = 'exo';
    let depth = 0.012;
    let dur = 0.10;
    let noise = 0.0015;
    let sec = 0.45;
    
    const canvas = document.getElementById('plot');
    const ctx = canvas.getContext('2d');
    
    // Sliders
    const sDepth = document.getElementById('slider-depth');
    const sDur = document.getElementById('slider-dur');
    const sNoise = document.getElementById('slider-noise');
    const sSec = document.getElementById('slider-sec');
    const themeWrapper = document.getElementById('theme-wrapper');
    const secContainer = document.getElementById('sec-ratio-container');
    
    function setType(t) {
        type = t;
        document.getElementById('btn-exo').className = 'btn ' + (t==='exo'?'active exo':'');
        document.getElementById('btn-bin').className = 'btn ' + (t==='bin'?'active bin':'');
        themeWrapper.className = t==='exo' ? 'exo-theme' : 'bin-theme';
        secContainer.style.opacity = t==='exo' ? '0.2' : '1';
        secContainer.style.pointerEvents = t==='exo' ? 'none' : 'auto';
        draw();
    }
    
    function updateVals() {
        depth = parseFloat(sDepth.value);
        dur = parseFloat(sDur.value);
        noise = parseFloat(sNoise.value);
        sec = parseFloat(sSec.value);
        
        document.getElementById('val-depth').innerText = (depth*100).toFixed(1) + '%';
        document.getElementById('val-dur').innerText = dur.toFixed(2);
        document.getElementById('val-noise').innerText = noise.toFixed(4);
        document.getElementById('val-sec').innerText = (sec*100).toFixed(0) + '%';
        draw();
    }
    
    sDepth.oninput = updateVals; sDur.oninput = updateVals;
    sNoise.oninput = updateVals; sSec.oninput = updateVals;
    
    // Pre-generate random Gaussian multipliers for noise
    const noiseArr = Array.from({length: 800}, () => (Math.random() + Math.random() + Math.random() + Math.random() - 2) * 0.866);

    function getFlux(p) {
        let f = 1.0;
        if (type === 'exo') {
            if (Math.abs(p) < dur/2) {
                f -= depth * (1.0 - Math.pow(Math.abs(p)/(dur/2), 6));
            }
        } else {
            if (Math.abs(p) < dur/2) {
                f -= depth * (1.0 - Math.abs(p)/(dur/2));
            }
            let p2 = Math.abs(Math.abs(p) - 0.5);
            if (p2 < dur/2) {
                f -= (depth * sec) * (1.0 - p2/(dur/2));
            }
            f += 0.0025 * Math.cos(4.0 * Math.PI * p);
        }
        return f;
    }

    function draw() {
        const W = canvas.offsetWidth * window.devicePixelRatio;
        const H = canvas.offsetHeight * window.devicePixelRatio;
        canvas.width = W; canvas.height = H;
        
        ctx.clearRect(0, 0, W, H);
        
        // Grid
        ctx.strokeStyle = '#1A1A1A'; ctx.lineWidth = 1;
        for(let i=1; i<5; i++) {
            ctx.beginPath(); ctx.moveTo(0, H*i/5); ctx.lineTo(W, H*i/5); ctx.stroke();
            ctx.beginPath(); ctx.moveTo(W*i/5, 0); ctx.lineTo(W*i/5, H); ctx.stroke();
        }
        
        const yMin = 0.94; const yMax = 1.01;
        const mapY = (val) => H - ((val - yMin) / (yMax - yMin)) * H;
        const mapX = (val) => ((val + 0.5) / 1.0) * W;
        
        // Draw Scatter (Noise)
        ctx.fillStyle = 'rgba(148, 163, 184, 0.4)';
        for(let i=0; i<800; i++) {
            let p = (i/799) - 0.5;
            let f = getFlux(p) + (noiseArr[i] * noise);
            ctx.beginPath();
            ctx.arc(mapX(p), mapY(f), 2 * window.devicePixelRatio, 0, Math.PI*2);
            ctx.fill();
        }
        
        // Draw Theoretical Line
        ctx.beginPath();
        for(let i=0; i<800; i++) {
            let p = (i/799) - 0.5;
            let f = getFlux(p);
            if (i===0) ctx.moveTo(mapX(p), mapY(f));
            else ctx.lineTo(mapX(p), mapY(f));
        }
        
        ctx.strokeStyle = type === 'exo' ? '#00E5FF' : '#FF3366';
        ctx.lineWidth = 3 * window.devicePixelRatio;
        ctx.shadowBlur = 15 * window.devicePixelRatio;
        ctx.shadowColor = type === 'exo' ? '#00E5FF' : '#FF3366';
        ctx.stroke();
        
        // Stroke again without shadow for solid core
        ctx.shadowBlur = 0;
        ctx.lineWidth = 1.5 * window.devicePixelRatio;
        ctx.strokeStyle = '#FFFFFF';
        ctx.stroke();
    }
    
    window.addEventListener('resize', draw);
    setType('exo');
</script>
</body>
</html>
"""
components.html(simulator_html, height=500)

# --- 5. RESOURCE DIRECTORY & CITATIONS ---
st.markdown("""
<style>
    .resource-container {
        display: flex;
        gap: 20px;
        justify-content: center;
        flex-wrap: wrap;
        margin-top: 1rem;
        margin-bottom: 3rem;
        font-family: 'Inter', sans-serif;
    }
    .resource-card {
        background: #0A0A0A;
        border: 1px solid #222;
        border-radius: 1rem;
        padding: 1.5rem;
        flex: 1;
        min-width: 250px;
        transition: all 0.3s ease;
    }
    .resource-card:hover {
        border-color: #00E5FF;
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(0, 229, 255, 0.1);
    }
    .resource-card h4 {
        color: #fff;
        margin-top: 0;
        font-family: 'Orbitron', sans-serif;
        font-size: 1.1rem;
        letter-spacing: 0.5px;
        margin-bottom: 10px;
    }
    .resource-card p {
        color: #888;
        font-size: 0.9rem;
        line-height: 1.5;
        margin-bottom: 15px;
    }
    .resource-card ul {
        padding-left: 20px;
        margin: 0;
    }
    .resource-card li {
        margin-bottom: 8px;
        color: #888;
    }
    .resource-card a {
        color: #00E5FF;
        text-decoration: none;
        font-size: 0.9rem;
        font-weight: 600;
        transition: color 0.2s;
    }
    .resource-card a:hover {
        color: #fff;
    }
</style>

<div class="resource-container">
    <div class="resource-card">
        <h4>📡 NASA Archives</h4>
        <p>Official space telescope telemetry and confirmed exoplanet tables.</p>
        <ul>
            <li><a href="https://archive.stsci.edu/" target="_blank">MAST Data Archive</a></li>
            <li><a href="https://exoplanetarchive.ipac.caltech.edu/" target="_blank">NASA Exoplanet Archive</a></li>
            <li><a href="https://tess.mit.edu/" target="_blank">MIT TESS Overview</a></li>
        </ul>
    </div>
    <div class="resource-card">
        <h4>🧮 Signal Processing</h4>
        <p>Core scientific computing and transit periodogram libraries.</p>
        <ul>
            <li><a href="https://docs.lightkurve.org/" target="_blank">Lightkurve Documentation</a></li>
            <li><a href="https://docs.lightkurve.org/reference/api/lightkurve.periodogram.BoxLeastSquaresPeriodogram.html" target="_blank">Box Least Squares (BLS)</a></li>
            <li><a href="https://www.astropy.org/" target="_blank">Astropy Project</a></li>
        </ul>
    </div>
    <div class="resource-card">
        <h4>💻 Architecture & ML</h4>
        <p>Project repository, model documentation, and pipeline blueprints.</p>
        <ul>
            <li><a href="https://xgboost.readthedocs.io/" target="_blank">XGBoost ML API</a></li>
            <li><a href="https://streamlit.io/" target="_blank">Streamlit Framework</a></li>
            <li><a href="https://github.com/" target="_blank">GitHub Source Code</a></li>
        </ul>
    </div>
</div>
""", unsafe_allow_html=True)