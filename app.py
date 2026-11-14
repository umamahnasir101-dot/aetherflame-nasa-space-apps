import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# ==============================================================================
# PAGE CONFIG & LIVE SPACE VISUALS / FRONT PAGE STYLING
# ==============================================================================
st.set_page_config(
    page_title="AETHERFLAME | Space Habitat Fire Safety Intelligence",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    h1, h2, h3 {
        font-family: 'Cinzel', serif !important;
        letter-spacing: 0.03em;
    }

    /* Deep Space Obsidian + Starlight + Solar Gold Background */
    .stApp {
        background:
            radial-gradient(circle at 80% 18%, rgba(212, 175, 55, 0.16), transparent 36%),
            radial-gradient(circle at 18% 82%, rgba(56, 189, 248, 0.12), transparent 42%),
            linear-gradient(180deg, #040711 0%, #091022 55%, #050814 100%);
        color: #F8F5EE;
        overflow-x: hidden;
    }

    /* Hide default Streamlit chrome for clean product look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Animated Live Space Scene Banner (Stars + Orbiting Rocket + 0g Blue Flame Sphere) */
    .space-stage {
        position: relative;
        width: 100%;
        min-height: 310px;
        border-radius: 22px;
        background: radial-gradient(ellipse at 50% 115%, rgba(212, 175, 55, 0.22) 0%, rgba(11, 18, 36, 0.92) 58%, #040711 100%);
        border: 1px solid rgba(212, 175, 55, 0.42);
        box-shadow: 0 24px 60px rgba(0, 0, 0, 0.65), inset 0 0 50px rgba(212, 175, 55, 0.08);
        padding: 36px 28px 28px 28px;
        text-align: center;
        overflow: hidden;
        margin-bottom: 22px;
    }

    /* Twinkling Starfield Layer */
    .stars-layer {
        position: absolute;
        inset: 0;
        background-image:
            radial-gradient(2px 2px at 12% 22%, #FFFFFF, transparent),
            radial-gradient(1.5px 1.5px at 28% 68%, #F3D06B, transparent),
            radial-gradient(2px 2px at 45% 15%, #38BDF8, transparent),
            radial-gradient(1.5px 1.5px at 67% 32%, #FFFFFF, transparent),
            radial-gradient(2px 2px at 84% 72%, #F3D06B, transparent),
            radial-gradient(1.5px 1.5px at 91% 24%, #FFFFFF, transparent),
            radial-gradient(1.5px 1.5px at 18% 84%, #38BDF8, transparent),
            radial-gradient(2px 2px at 56% 78%, #FFFFFF, transparent),
            radial-gradient(1.5px 1.5px at 74% 12%, #F3D06B, transparent);
        animation: twinkle 4s ease-in-out infinite alternate;
        pointer-events: none;
    }

    @keyframes twinkle {
        0% { opacity: 0.45; transform: scale(1); }
        100% { opacity: 1.0; transform: scale(1.02); }
    }

    /* Animated Rocket Flying Across Orbital Arc */
    .rocket-flight {
        position: absolute;
        top: 26px;
        left: -10%;
        font-size: 2rem;
        filter: drop-shadow(0 0 12px rgba(243, 208, 107, 0.85));
        animation: flyOrbit 14s linear infinite;
        pointer-events: none;
    }

    @keyframes flyOrbit {
        0%   { left: -8%;  top: 68px; transform: rotate(18deg) scale(0.9); opacity: 0; }
        10%  { opacity: 1; }
        50%  { left: 50%;  top: 18px; transform: rotate(32deg) scale(1.1); }
        90%  { opacity: 1; }
        100% { left: 108%; top: 64px; transform: rotate(45deg) scale(0.9); opacity: 0; }
    }

    /* Pulsing Zero-G Spherical Blue Flame Visual */
    .zero-g-orb {
        width: 68px;
        height: 68px;
        margin: 0 auto 12px auto;
        border-radius: 50%;
        background: radial-gradient(circle at 50% 50%, #FFFBEB 8%, #F3D06B 28%, #38BDF8 62%, rgba(14, 165, 233, 0.08) 100%);
        box-shadow: 0 0 28px rgba(56, 189, 248, 0.75), 0 0 52px rgba(212, 175, 55, 0.35);
        animation: pulseFlame 2.8s ease-in-out infinite;
    }

    @keyframes pulseFlame {
        0%, 100% { transform: scale(0.95); box-shadow: 0 0 24px rgba(56, 189, 248, 0.65), 0 0 42px rgba(212, 175, 55, 0.3); }
        50%      { transform: scale(1.06); box-shadow: 0 0 38px rgba(56, 189, 248, 0.95), 0 0 65px rgba(212, 175, 55, 0.55); }
    }

    .hero-title {
        font-family: 'Cinzel', serif;
        font-size: clamp(2.4rem, 5vw, 4.1rem);
        font-weight: 800;
        background: linear-gradient(90deg, #FFFDF7 0%, #F3D06B 48%, #D4AF37 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 4px 0 6px 0;
        letter-spacing: 0.08em;
    }

    .hero-sub {
        font-size: 1.08rem;
        color: #E2E8F0;
        max-width: 760px;
        margin: 0 auto 14px auto;
        line-height: 1.55;
    }

    .gold-pill {
        display: inline-block;
        padding: 5px 14px;
        border-radius: 999px;
        background: rgba(212, 175, 55, 0.16);
        border: 1px solid rgba(212, 175, 55, 0.5);
        color: #F3D06B;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 10px;
    }

    /* Interactive Front-Page Module Cards */
    .nav-card {
        background: linear-gradient(160deg, rgba(15, 23, 42, 0.88), rgba(9, 14, 28, 0.95));
        border: 1px solid rgba(212, 175, 55, 0.32);
        border-radius: 16px;
        padding: 20px;
        min-height: 175px;
        transition: transform 0.25s ease, border-color 0.25s ease;
        box-shadow: 0 12px 28px rgba(0, 0, 0, 0.45);
        margin-bottom: 10px;
    }
    .nav-card:hover {
        transform: translateY(-4px);
        border-color: #F3D06B;
    }
    .nav-card-icon {
        font-size: 1.85rem;
        margin-bottom: 8px;
    }
    .nav-card-title {
        font-family: 'Cinzel', serif;
        font-size: 1.15rem;
        font-weight: 700;
        color: #F3D06B;
        margin-bottom: 6px;
    }
    .nav-card-desc {
        font-size: 0.88rem;
        color: #CBD5E1;
        line-height: 1.45;
    }

    /* Styled Streamlit Buttons */
    div.stButton > button {
        width: 100%;
        border-radius: 12px;
        border: 1px solid rgba(212, 175, 55, 0.55);
        background: linear-gradient(135deg, rgba(212, 175, 55, 0.22), rgba(15, 23, 42, 0.92));
        color: #FFFDF7;
        font-weight: 600;
        padding: 0.6rem 1rem;
        transition: all 0.2s ease;
    }
    div.stButton > button:hover {
        border-color: #F3D06B;
        background: linear-gradient(135deg, #D4AF37, #B48A1E);
        color: #040711;
        box-shadow: 0 0 20px rgba(212, 175, 55, 0.45);
    }

    .metric-card {
        background: rgba(15, 23, 42, 0.82);
        border: 1px solid rgba(212, 175, 55, 0.3);
        border-radius: 14px;
        padding: 16px 18px;
        text-align: center;
    }
    .metric-val {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.65rem;
        font-weight: 700;
        color: #F3D06B;
    }
    .metric-lbl {
        font-size: 0.82rem;
        color: #CBD5E1;
        margin-top: 4px;
    }
    .insight-box {
        background: linear-gradient(135deg, rgba(212,175,55,0.14), rgba(15,23,42,0.88));
        border-left: 4px solid #D4AF37;
        border-radius: 10px;
        padding: 16px 20px;
        margin: 12px 0;
        color: #F8FAFC;
    }
    .alert-box {
        background: rgba(239, 68, 68, 0.14);
        border-left: 4px solid #EF4444;
        border-radius: 10px;
        padding: 14px 18px;
        margin: 10px 0;
        color: #FEE2E2;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# NAVIGATION STATE (FRONT PAGE HOME + 5 DEDICATED INTERACTIVE TABS)
# ==============================================================================
if "active_page" not in st.session_state:
    st.session_state.active_page = "Home"

def go_to(page_name):
    st.session_state.active_page = page_name

# ==============================================================================
# COMPLETE NASA PSI COMBUSTION DATASET (26 INVESTIGATIONS + PLANETARY MISSIONS)
# ==============================================================================
PSI_DATA = [
    {
        "id": "PSI-26", "name": "Burning and Suppression of Solids (BASS)",
        "type": "Microgravity Flight (ISS)", "pillar": "Prevention & Suppression",
        "hardware": "MSG (SPICE Flow Duct)", "fuel_cat": "Solid",
        "fuels": "SIBAL (75% Cotton / 25% Fiberglass), PMMA Acrylic Spheres & Sheets, Wax",
        "o2_min": 17.0, "o2_max": 21.0, "p_min": 1.0, "p_max": 1.0,
        "flow_min": 0.0, "flow_max": 30.0,
        "sensors": "Nikon DSLR (1.5s), Video, Radiometer, Hot-Wire Anemometer",
        "plain_summary": "Proved spacecraft ventilation airflow (1–15 cm/s) lets plastics and fabrics burn at LOWER oxygen levels in 0g than NASA's Earth test predicts—and showed nitrogen extinguisher jets can accidentally feed wake flames by entraining cabin air.",
        "habitats": ["ISS", "Moon Base", "Mars Transit"]
    },
    {
        "id": "PSI-25", "name": "Burning and Suppression of Solids - II (BASS-II)",
        "type": "Microgravity Flight (ISS)", "pillar": "Prevention & Suppression",
        "hardware": "MSG (SPICE Flow Duct)", "fuel_cat": "Solid",
        "fuels": "Cast PMMA Rods & Slabs, Cellulose, SIBAL, Nomex, Silicone, Ultem",
        "o2_min": 13.5, "o2_max": 21.0, "p_min": 1.0, "p_max": 1.0,
        "flow_min": 0.0, "flow_max": 40.0,
        "sensors": "High-Res DSLR, Two-Color Pyrometry, Thermocouples, Radiometer, O2 Analyzer",
        "plain_summary": "Mapped exact flammability boundaries for thick solid cylinders and slabs in slow airflows, establishing baseline limits for ISS SoFIE hardware and habitat material screening.",
        "habitats": ["ISS", "Moon Base", "Mars Transit"]
    },
    {
        "id": "PSI-98", "name": "Spacecraft Fire Safety Experiment-I (SAFFIRE-I)",
        "type": "Microgravity Flight (Cygnus)", "pillar": "Prevention",
        "hardware": "Cygnus Cargo Spacecraft", "fuel_cat": "Solid",
        "fuels": "Large-scale SIBAL Cotton-Fiberglass Sheet (0.94 m x 0.40 m)",
        "o2_min": 21.0, "o2_max": 21.0, "p_min": 1.0, "p_max": 1.0,
        "flow_min": 20.0, "flow_max": 20.0,
        "sensors": "2 HD Cameras (Green LED), Thermocouple Array, Radiometers, O2/CO2/Pressure Sensors",
        "plain_summary": "First meter-scale fire burned inside an uncrewed Cygnus cargo ship; proved concurrent flame spread in 20 cm/s ventilation reaches a steady speed (~1.5 mm/s) rather than accelerating infinitely.",
        "habitats": ["ISS", "Cargo Transit", "Moon Base"]
    },
    {
        "id": "PSI-99", "name": "Spacecraft Fire Experiment-II (SAFFIRE-II)",
        "type": "Microgravity Flight (Cygnus)", "pillar": "Prevention",
        "hardware": "Cygnus Cargo Spacecraft", "fuel_cat": "Solid",
        "fuels": "9 Spacecraft Materials: SIBAL, Cotton, Nomex, Silicone (0.25–2 mm), Grooved PMMA",
        "o2_min": 21.0, "o2_max": 21.0, "p_min": 1.0, "p_max": 1.0,
        "flow_min": 13.0, "flow_max": 20.0,
        "sensors": "2 HD Video Cameras, Thermocouples, Radiometers, O2/CO2 Sensors, Anemometers",
        "plain_summary": "Tested 9 spacecraft cabin materials of varying thicknesses on a motorized card frame to compare real large-scale 0g burn limits directly against NASA-STD-6001 Test 1.",
        "habitats": ["ISS", "Cargo Transit", "Moon Base"]
    },
    {
        "id": "PSI-100", "name": "Spacecraft Fire Experiment-III (SAFFIRE-III)",
        "type": "Microgravity Flight (Cygnus)", "pillar": "Prevention",
        "hardware": "Cygnus Cargo Spacecraft", "fuel_cat": "Solid",
        "fuels": "Large-scale SIBAL Cotton-Fiberglass Sheet (0.94 m x 0.40 m)",
        "o2_min": 21.0, "o2_max": 21.0, "p_min": 1.0, "p_max": 1.0,
        "flow_min": 30.0, "flow_max": 30.0,
        "sensors": "2 HD Cameras, Thermocouple Rake, Radiometers, O2/CO2 Sensors",
        "plain_summary": "Increased cabin airflow to 30 cm/s on a meter-sized fabric sheet, proving fire spread speed scales nearly proportionally (~50% faster) with ventilation airflow rate.",
        "habitats": ["ISS", "Cargo Transit", "Moon Base"]
    },
    {
        "id": "PSI-69", "name": "Flame Extinguishment Experiment (FLEX)",
        "type": "Microgravity Flight (ISS)", "pillar": "Suppression",
        "hardware": "CIR (MDCA)", "fuel_cat": "Liquid Droplet",
        "fuels": "Liquid n-Heptane and Methanol Droplets (1–5 mm) in CO2, He, N2, Xe",
        "o2_min": 11.0, "o2_max": 40.0, "p_min": 0.5, "p_max": 3.0,
        "flow_min": 0.0, "flow_max": 5.0,
        "sensors": "HiBMs Multispectral Camera, Low-Light UV Camera (OH*), Radiometers",
        "plain_summary": "Discovered 'Cool Flames'—droplets whose visible flame goes out yet continue burning invisibly at 500–800 K and can spontaneously reignite—while proving 0g requires higher suppressant concentrations than Earth.",
        "habitats": ["ISS", "Moon Base", "Mars Transit"]
    },
    {
        "id": "PSI-68", "name": "Flame Extinguishment Experiment - 2 (FLEX-2)",
        "type": "Microgravity Flight (ISS)", "pillar": "Suppression",
        "hardware": "CIR (MDCA)", "fuel_cat": "Liquid Droplet",
        "fuels": "n-Heptane, Octane, Decane, Ethanol, Methyl Butanoate, Binary Fuel Mixtures",
        "o2_min": 10.0, "o2_max": 40.0, "p_min": 0.5, "p_max": 3.0,
        "flow_min": 0.0, "flow_max": 4.0,
        "sensors": "Dual HiBMs Cameras, Low-Light UV Camera, Narrowband Radiometers",
        "plain_summary": "Extended droplet suppression and two-stage hot-to-cool flame extinction testing across multi-component fuels, droplet arrays, and elevated pressures up to 3.0 atm.",
        "habitats": ["ISS", "Moon Base", "Mars Transit"]
    },
    {
        "id": "PSI-102", "name": "Smoke and Aerosol Measurement Experiment (SAME)",
        "type": "Microgravity Flight (ISS)", "pillar": "Detection",
        "hardware": "MSG (SAME Near/Far Field)", "fuel_cat": "Pyrolysis Aerosol",
        "fuels": "Overheated Kapton, Teflon (PTFE), Silicone Rubber, Cellulose, Lamp Wick",
        "o2_min": 21.0, "o2_max": 21.0, "p_min": 1.0, "p_max": 1.0,
        "flow_min": 2.0, "flow_max": 10.0,
        "sensors": "P-Trak CNC, DustTrak Photometer, Ionization Chamber, TEM Grid Samplers",
        "plain_summary": "Proved smoke particles grow much larger (0.3 to >1.0 micron) in microgravity than on Earth because lack of buoyancy gives droplets time to coagulate—requiring recalibrated spacecraft smoke detectors.",
        "habitats": ["ISS", "Moon Base", "Mars Transit", "Cargo Transit"]
    },
    {
        "id": "PSI-101", "name": "Smoke Aerosol Measurement Experiment - Reflight (SAME-R)",
        "type": "Microgravity Flight (ISS)", "pillar": "Detection",
        "hardware": "MSG (SAME-R Hardware)", "fuel_cat": "Pyrolysis Aerosol",
        "fuels": "Pyrell® Fire-Retardant Foam, Kapton, Teflon, Silicone, Cellulose, Lamp Wick",
        "o2_min": 21.0, "o2_max": 21.0, "p_min": 1.0, "p_max": 1.0,
        "flow_min": 2.0, "flow_max": 10.0,
        "sensors": "P-Trak, DustTrak, Shuttle & ISS Smoke Detectors, Thermophoretic TEM Probes",
        "plain_summary": "Added Pyrell acoustic foam across 106 test runs to build NASA's definitive aerosol signature database for early fire detection with minimal nuisance alarms.",
        "habitats": ["ISS", "Moon Base", "Mars Transit"]
    },
    {
        "id": "PSI-159", "name": "ACME Cool Flames Investigation with Gases (CFI-G)",
        "type": "Microgravity Flight (ISS)", "pillar": "Prevention & Detection",
        "hardware": "CIR (ACME Spherical Burner)", "fuel_cat": "Gaseous",
        "fuels": "Propane, n-Butane, n-Pentane with up to 85% O2 / N2 Spherical Burner Flow",
        "o2_min": 21.0, "o2_max": 85.0, "p_min": 0.5, "p_max": 3.0,
        "flow_min": 0.0, "flow_max": 2.0,
        "sensors": "Low-Light UV Camera (OH*/HCHO*), HiBMs Cameras, Radiometers, Thermocouples",
        "plain_summary": "Tested the HIGHEST oxygen concentrations in PSI (up to 85% O2) using inside-out spherical flames, directly bounding fire reactivity for high-oxygen Moon Bases (>=30% O2) and Spacesuits (100% O2).",
        "habitats": ["Moon Base", "Spacesuit EVA", "Mars Transit"]
    },
    {
        "id": "PSI-22", "name": "ACME Electric-Field Effects on Laminar Diffusion Flames (E-FIELD)",
        "type": "Microgravity Flight (ISS)", "pillar": "Prevention & Partial-g Proxy",
        "hardware": "CIR (ACME Coflow + 10 kV Mesh)", "fuel_cat": "Gaseous",
        "fuels": "Methane and Ethylene Flames under 0 to 10,000 Volt Electric Fields",
        "o2_min": 18.0, "o2_max": 30.0, "p_min": 1.0, "p_max": 1.0,
        "flow_min": 0.0, "flow_max": 20.0,
        "sensors": "Ion-Current Ammeter, HiBMs/Color Cameras, LLLUV Camera, Radiometers",
        "plain_summary": "Uses up to 10 kV electric fields acting on natural flame ions to mimic buoyant convection in 0g—serving as PSI's key experimental proxy for 1/6g Lunar and 3/8g Martian partial gravity.",
        "habitats": ["Moon Base", "Mars Transit"]
    },
    {
        "id": "PSI-20", "name": "ACME Burning Rate Emulator (ACME BRE)",
        "type": "Microgravity Flight (ISS)", "pillar": "Prevention",
        "hardware": "CIR (ACME Porous Flat Burner)", "fuel_cat": "Gaseous (Solid Emulator)",
        "fuels": "Ethylene, Methane, Propane metered to emulate Solid PMMA, Paper & Alcohols",
        "o2_min": 14.0, "o2_max": 40.0, "p_min": 0.5, "p_max": 1.5,
        "flow_min": 0.0, "flow_max": 0.0,
        "sensors": "Embedded Burner Heat-Flux Sensor, Thermocouples, Pyrometry, Gas Chromatograph",
        "plain_summary": "Uses feedback-controlled gas burners to mimic how solid plastics and fabrics burn in still 0g atmospheres, rapidly mapping material flammability limits across 14–40% O2.",
        "habitats": ["Moon Base", "ISS", "Spacesuit EVA"]
    },
    {
        "id": "PSI-10", "name": "ACME Flame Design",
        "type": "Microgravity Flight (ISS)", "pillar": "Prevention",
        "hardware": "CIR (ACME Spherical Burner)", "fuel_cat": "Gaseous",
        "fuels": "Ethylene & Methane in Normal and Inverse Oxygen-Enriched Spheres (up to 5
