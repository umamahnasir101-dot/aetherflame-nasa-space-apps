import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# ==============================================================================
# PAGE CONFIG & LIVE SPACE VISUALS / IONIZED CYAN & DEEP VACUUM THEME
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
        color: #F8FAFC !important;
    }

    /* Deep Vacuum Black (#080B10) Background */
    .stApp {
        background:
            radial-gradient(circle at 80% 18%, rgba(0, 229, 255, 0.11), transparent 38%),
            radial-gradient(circle at 18% 82%, rgba(255, 77, 77, 0.07), transparent 42%),
            #080B10;
        color: #F8FAFC;
        overflow-x: hidden;
    }

    /* Hide default Streamlit chrome for clean product look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Animated Live Space Scene Banner (Stars + Orbiting Rocket + 0g Cyan Flame Orb) */
    .space-stage {
        position: relative;
        width: 100%;
        min-height: 310px;
        border-radius: 22px;
        background: radial-gradient(ellipse at 50% 115%, rgba(0, 229, 255, 0.16) 0%, #0F151E 60%, #080B10 100%);
        border: 1px solid #1E293B;
        box-shadow: 0 24px 60px rgba(0, 0, 0, 0.72), inset 0 0 48px rgba(0, 229, 255, 0.06);
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
            radial-gradient(2px 2px at 12% 22%, #F8FAFC, transparent),
            radial-gradient(1.5px 1.5px at 28% 68%, #00E5FF, transparent),
            radial-gradient(2px 2px at 45% 15%, #00E5FF, transparent),
            radial-gradient(1.5px 1.5px at 67% 32%, #F8FAFC, transparent),
            radial-gradient(2px 2px at 84% 72%, #00E5FF, transparent),
            radial-gradient(1.5px 1.5px at 91% 24%, #F8FAFC, transparent),
            radial-gradient(1.5px 1.5px at 18% 84%, #00E5FF, transparent),
            radial-gradient(2px 2px at 56% 78%, #F8FAFC, transparent),
            radial-gradient(1.5px 1.5px at 74% 12%, #00E5FF, transparent);
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
        filter: drop-shadow(0 0 12px rgba(0, 229, 255, 0.85));
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

    /* Pulsing Zero-G Spherical Ionized Cyan Flame Visual */
    .zero-g-orb {
        width: 68px;
        height: 68px;
        margin: 0 auto 12px auto;
        border-radius: 50%;
        background: radial-gradient(circle at 50% 50%, #F8FAFC 10%, #7DF9FF 34%, #00E5FF 64%, rgba(0, 229, 255, 0.06) 100%);
        box-shadow: 0 0 28px rgba(0, 229, 255, 0.8), 0 0 54px rgba(0, 229, 255, 0.35);
        animation: pulseFlame 2.8s ease-in-out infinite;
    }

    @keyframes pulseFlame {
        0%, 100% { transform: scale(0.95); box-shadow: 0 0 24px rgba(0, 229, 255, 0.65), 0 0 42px rgba(0, 229, 255, 0.28); }
        50%      { transform: scale(1.06); box-shadow: 0 0 40px rgba(0, 229, 255, 0.98), 0 0 68px rgba(0, 229, 255, 0.5); }
    }

    .hero-title {
        font-family: 'Cinzel', serif;
        font-size: clamp(2.4rem, 5vw, 4.1rem);
        font-weight: 800;
        background: linear-gradient(90deg, #F8FAFC 0%, #80F2FF 48%, #00E5FF 100%);
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

    .cyan-pill {
        display: inline-block;
        padding: 5px 14px;
        border-radius: 999px;
        background: rgba(0, 229, 255, 0.12);
        border: 1px solid rgba(0, 229, 255, 0.45);
        color: #00E5FF;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 10px;
    }

    /* Interactive Front-Page Module Cards (#0F151E with #1E293B hairline borders) */
    .nav-card {
        background: #0F151E;
        border: 1px solid #1E293B;
        border-radius: 16px;
        padding: 20px;
        min-height: 175px;
        transition: transform 0.25s ease, border-color 0.25s ease, box-shadow 0.25s ease;
        box-shadow: 0 12px 28px rgba(0, 0, 0, 0.5);
        margin-bottom: 10px;
    }
    .nav-card:hover {
        transform: translateY(-4px);
        border-color: #00E5FF;
        box-shadow: 0 14px 32px rgba(0, 229, 255, 0.14);
    }
    .nav-card-icon {
        font-size: 1.85rem;
        margin-bottom: 8px;
    }
    .nav-card-title {
        font-family: 'Cinzel', serif;
        font-size: 1.15rem;
        font-weight: 700;
        color: #00E5FF;
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
        border: 1px solid rgba(0, 229, 255, 0.45);
        background: linear-gradient(135deg, rgba(0, 229, 255, 0.14), #0F151E);
        color: #F8FAFC;
        font-weight: 600;
        padding: 0.6rem 1rem;
        transition: all 0.2s ease;
    }
    div.stButton > button:hover {
        border-color: #00E5FF;
        background: #00E5FF;
        color: #080B10;
        box-shadow: 0 0 20px rgba(0, 229, 255, 0.45);
    }

    .metric-card {
        background: #0F151E;
        border: 1px solid #1E293B;
        border-radius: 14px;
        padding: 16px 18px;
        text-align: center;
    }
    .metric-val {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.65rem;
        font-weight: 700;
        color: #00E5FF;
    }
    .metric-lbl {
        font-size: 0.82rem;
        color: #CBD5E1;
        margin-top: 4px;
    }
    .insight-box {
        background: linear-gradient(135deg, rgba(0, 229, 255, 0.10), #0F151E);
        border: 1px solid #1E293B;
        border-left: 4px solid #00E5FF;
        border-radius: 10px;
        padding: 16px 20px;
        margin: 12px 0;
        color: #F8FAFC;
    }
    .alert-box {
        background: linear-gradient(135deg, rgba(255, 77, 77, 0.13), #0F151E);
        border: 1px solid #1E293B;
        border-left: 4px solid #FF4D4D;
        border-radius: 10px;
        padding: 14px 18px;
        margin: 10px 0;
        color: #F8FAFC;
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
        "fuels": "Ethylene & Methane in Normal and Inverse Oxygen-Enriched Spheres (up to 50% O2)",
        "o2_min": 15.0, "o2_max": 50.0, "p_min": 0.5, "p_max": 2.0,
        "flow_min": 0.0, "flow_max": 5.0,
        "sensors": "Two-Color Pyrometry, LLLUV Camera, Radiometers, Photomultipliers",
        "plain_summary": "Demonstrated how tailoring oxygen-to-fuel mixing ratios eliminates soot completely in oxygen-enriched atmospheres (15–50% O2), informing cleaner engines and habitat safety.",
        "habitats": ["Moon Base", "ISS", "Mars Transit"]
    },
    {
        "id": "PSI-39", "name": "Cool Flames Investigation (CFI)",
        "type": "Microgravity Flight (ISS)", "pillar": "Detection & Suppression",
        "hardware": "CIR (MDCA)", "fuel_cat": "Liquid Droplet",
        "fuels": "Heavy Hydrocarbon Surrogates: n-Dodecane, iso-Dodecane, n-Decane (0.25–5 atm)",
        "o2_min": 15.0, "o2_max": 30.0, "p_min": 0.25, "p_max": 5.0,
        "flow_min": 0.0, "flow_max": 0.0,
        "sensors": "HiBMs Backlit Camera, 350 nm Formaldehyde (HCHO*) UV Camera, Radiometers",
        "plain_summary": "Revealed that heavy jet/diesel fuel droplets transition into long-lived invisible cool flames across sub-atmospheric to high pressures (0.25–5 atm), emitting toxic CO and formaldehyde.",
        "habitats": ["Moon Base", "ISS", "Mars Transit"]
    },
    {
        "id": "DAFT", "name": "Dust and Aerosol Measurement Feasibility Test (DAFT / DAFT-2)",
        "type": "Microgravity Flight (ISS)", "pillar": "Detection",
        "hardware": "ISS Cabin (Modified P-Trak & DustTrak)", "fuel_cat": "Cabin Dust / Aerosol",
        "fuels": "Ambient ISS Cabin Dust, Lint, and Ultrafine Background Particulates",
        "o2_min": 21.0, "o2_max": 21.0, "p_min": 1.0, "p_max": 1.0,
        "flow_min": 5.0, "flow_max": 20.0,
        "sensors": "Modified Alcohol-Wick P-Trak CNC (0.02–1 µm), DustTrak Photometer",
        "plain_summary": "Measured floating cabin dust across ISS modules, proving HEPA filters keep ultrafine counts low while coarse lint floats indefinitely—explaining why detectors must separate dust from smoke.",
        "habitats": ["ISS", "Moon Base", "Mars Transit"]
    },
    {
        "id": "PSI-21", "name": "ACME Coflow Laminar Diffusion Flame (CLD Flame)",
        "type": "Microgravity Flight (ISS)", "pillar": "Prevention",
        "hardware": "CIR (ACME Coflow Burner)", "fuel_cat": "Gaseous",
        "fuels": "Nitrogen-Diluted Methane & Ethylene Lifted Jet Flames",
        "o2_min": 15.0, "o2_max": 30.0, "p_min": 1.0, "p_max": 1.0,
        "flow_min": 5.0, "flow_max": 50.0,
        "sensors": "Two-Color Pyrometry, Thermocouples, LLLUV & HiBMs Cameras",
        "plain_summary": "Validated soot and extinction sub-models at extreme fuel dilution and heavy sooting limits without burner heat-loss distortion.",
        "habitats": ["ISS", "Moon Base"]
    },
    {
        "id": "PSI-23", "name": "ACME Structure & Response of Spherical Diffusion Flames (s-Flame)",
        "type": "Microgravity Flight (ISS)", "pillar": "Prevention",
        "hardware": "CIR (ACME Spherical Burner)", "fuel_cat": "Gaseous",
        "fuels": "Hydrogen, Methane, Propane, Ethylene diluted with Ar, He, N2",
        "o2_min": 15.0, "o2_max": 40.0, "p_min": 0.5, "p_max": 2.0,
        "flow_min": 0.0, "flow_max": 0.0,
        "sensors": "Radiometers, LLLUV Camera, HiBMs Cameras, Photomultipliers",
        "plain_summary": "Mapped radiative vs. diffusive extinction boundaries and Lewis-number pulsating instabilities in pure 1D spherical flames.",
        "habitats": ["Moon Base", "ISS", "Spacesuit EVA"]
    },
    {
        "id": "PSI-107", "name": "Smoke Point In Co-flow Experiment (SPICE)",
        "type": "Microgravity Flight (ISS)", "pillar": "Detection & Prevention",
        "hardware": "MSG (SPICE Flow Duct)", "fuel_cat": "Gaseous",
        "fuels": "Methane, Ethylene, Propane, Propylene, n-Butane, 1-Butene",
        "o2_min": 21.0, "o2_max": 21.0, "p_min": 1.0, "p_max": 1.0,
        "flow_min": 2.0, "flow_max": 40.0,
        "sensors": "Nikon DSLR, Color Video, Radiometer, Hot-Wire Anemometer",
        "plain_summary": "Established 0g smoke-point thresholds for gaseous fuels and introduced the modular MSG flow duct later used for SLICE, BASS, and BASS-II.",
        "habitats": ["ISS", "Moon Base"]
    },
    {
        "id": "PSI-106", "name": "Structure and Liftoff In Combustion Experiment (SLICE)",
        "type": "Microgravity Flight (ISS)", "pillar": "Prevention",
        "hardware": "MSG (SPICE Flow Duct)", "fuel_cat": "Gaseous",
        "fuels": "Methane, Ethylene, n-Butane diluted with Nitrogen",
        "o2_min": 21.0, "o2_max": 21.0, "p_min": 1.0, "p_max": 1.0,
        "flow_min": 5.0, "flow_max": 50.0,
        "sensors": "Digital Still & Video Cameras, Thermocouples, Flow Sensors",
        "plain_summary": "Quantified how increasing ventilation co-flow causes microgravity flames to detach from a burner, flatten into a cap, and blow out.",
        "habitats": ["ISS", "Moon Base"]
    },
    {
        "id": "PSI-62", "name": "Concurrent Flame Spread Modeling (FGM) vs. BASS",
        "type": "Ground / CFD Modeling", "pillar": "Prevention",
        "hardware": "Computational CFD + Two-Color Tomography", "fuel_cat": "Solid Model",
        "fuels": "Digital Twin of BASS/BASS-II SIBAL Fabric & PMMA",
        "o2_min": 15.0, "o2_max": 21.0, "p_min": 1.0, "p_max": 1.0,
        "flow_min": 1.0, "flow_max": 30.0,
        "sensors": "3D Flamelet Generated Manifold CFD + Two-Color Tomography",
        "plain_summary": "Validated 3D predictive fire-spread models directly against ISS BASS experimental data.",
        "habitats": ["ISS", "Moon Base", "Mars Transit"]
    },
    {
        "id": "PSI-60", "name": "Computational & Experimental Analysis of SPICE Data",
        "type": "Ground / CFD Analysis", "pillar": "Detection & Prevention",
        "hardware": "Color-Ratio Pyrometry & Soot CFD", "fuel_cat": "Gaseous Model",
        "fuels": "SPICE Ethylene & Hydrocarbon Jet Flames",
        "o2_min": 21.0, "o2_max": 21.0, "p_min": 1.0, "p_max": 1.0,
        "flow_min": 2.0, "flow_max": 40.0,
        "sensors": "3-Channel RGB Color-Ratio Pyrometry from Raw Nikon NEF Images",
        "plain_summary": "Decoded raw ISS SPICE images into full-field temperature and soot maps to explain why 0g flames produce larger soot aggregates than 1g flames.",
        "habitats": ["ISS", "Moon Base"]
    },
    {
        "id": "PSI-117", "name": "Thermo-Convective Perturbation on Cool Flame Dynamics (CFD)",
        "type": "Ground / CFD Modeling", "pillar": "Suppression",
        "hardware": "OpenFOAM 3D Multi-Physics CFD", "fuel_cat": "Liquid Model",
        "fuels": "n-Alkane Droplet Cool Flames from FLEX",
        "o2_min": 15.0, "o2_max": 30.0, "p_min": 0.5, "p_max": 2.0,
        "flow_min": 0.0, "flow_max": 10.0,
        "sensors": "3D Variable-Density Navier-Stokes + Low-Temp Chemistry Solver",
        "plain_summary": "Simulated how gentle spacecraft air currents perturb invisible cool flames and trigger either extinction or sudden re-ignition.",
        "habitats": ["ISS", "Moon Base"]
    },
    {
        "id": "PSI-142", "name": "Cool Flame Transitions at Radiation/Stretch Extinction",
        "type": "Ground / Numerical Study", "pillar": "Suppression",
        "hardware": "Counterflow Kinetic Modeling", "fuel_cat": "Liquid Model",
        "fuels": "FLEX Heptane & Alkane Surrogates",
        "o2_min": 15.0, "o2_max": 30.0, "p_min": 0.5, "p_max": 2.0,
        "flow_min": 0.0, "flow_max": 5.0,
        "sensors": "3 Detailed Chemical Kinetic Counterflow Solvers",
        "plain_summary": "Mapped the exact oxygen thresholds separating hot radiative flameout from persistent low-temperature cool flames.",
        "habitats": ["ISS", "Moon Base"]
    },
    {
        "id": "PSI-115", "name": "Advanced Modeling of SAME Microgravity Smoke Generation",
        "type": "Ground / DNS Modeling", "pillar": "Detection",
        "hardware": "Navier-Stokes Nodal Aerosol DNS", "fuel_cat": "Aerosol Model",
        "fuels": "Dibutyl-Phthalate (DBP) & Polymer Pyrolysis Smoke",
        "o2_min": 21.0, "o2_max": 21.0, "p_min": 1.0, "p_max": 1.0,
        "flow_min": 2.0, "flow_max": 10.0,
        "sensors": "Direct Numerical Simulation (DNS) Nodal Coagulation Code",
        "plain_summary": "Simulated particle nucleation and coagulation in 0g vs 1g, enabling digital design of multi-wavelength spacecraft smoke sensors.",
        "habitats": ["ISS", "Moon Base", "Mars Transit"]
    },
    {
        "id": "PSI-108", "name": "Surface Tension Driven Convection Experiment-1 (STDCE-1)",
        "type": "Microgravity Flight (Spacelab)", "pillar": "Prevention",
        "hardware": "Spacelab USML-1 Fluid Module", "fuel_cat": "Liquid Pool Dynamics",
        "fuels": "Heated Silicone Oil Pools (10-cm Chamber)",
        "o2_min": 21.0, "o2_max": 21.0, "p_min": 1.0, "p_max": 1.0,
        "flow_min": 0.0, "flow_max": 5.0,
        "sensors": "Infrared Thermography, Laser Sheet Velocimetry",
        "plain_summary": "Quantified surface-tension (Marangoni) convection in heated liquids—the exact mechanism pulling flame fronts across liquid fuel spills in microgravity.",
        "habitats": ["ISS", "Moon Base"]
    },
    {
        "id": "PSI-181", "name": "Pb-Sn and Pb-free Solders in Microgravity vs. Terrestrial",
        "type": "Ground / Materials Science", "pillar": "Prevention (Ignition Control)",
        "hardware": "ISS Isothermal Furnace / Microscopy", "fuel_cat": "Avionics Wiring",
        "fuels": "40Pb-60Sn, 50Pb-50Sn, and 95.5Sn-3.8Ag-0.7Cu Solder Alloys",
        "o2_min": 21.0, "o2_max": 21.0, "p_min": 1.0, "p_max": 1.0,
        "flow_min": 0.0, "flow_max": 0.0,
        "sensors": "Microstructural Void & Porosity Tomography",
        "plain_summary": "Found that 0g solder joints trap gas voids that increase electrical resistance and overheating—addressing electrical arc ignition, the root cause of Apollo 1 and Apollo 13.",
        "habitats": ["ISS", "Moon Base", "Spacesuit EVA", "Mars Transit"]
    },
    {
        "id": "FM2 / SoFIE / FLARE", "name": "Active Lunar & ISS Campaigns (FM2, SoFIE, FLARE)",
        "type": "Active ISS & Lunar Flight", "pillar": "Prevention (Partial-g)",
        "hardware": "CIR (SoFIE Insert) & Lunar Surface (1/6g)", "fuel_cat": "Solid",
        "fuels": "SIBAL Fabric, PMMA, Delrin, Spacecraft Polymers (10–40% O2, 0.2–1.5 atm)",
        "o2_min": 10.0, "o2_max": 40.0, "p_min": 0.2, "p_max": 1.5,
        "flow_min": 0.0, "flow_max": 30.0,
        "sensors": "Two-Color Cameras, UV Camera, Radiometers, Gas Chromatograph",
        "plain_summary": "FM2 is the first-ever combustion experiment on the Moon (1/6g), while ISS SoFIE and FLARE directly close the partial-gravity flammability gap for Artemis habitats.",
        "habitats": ["Moon Base", "Mars Transit", "ISS"]
    }
]

df = pd.DataFrame(PSI_DATA)

# ==============================================================================
# PERSISTENT TOP NAVIGATION BAR (WHEN INSIDE ANY MODULE)
# ==============================================================================
if st.session_state.active_page != "Home":
    top_col1, top_col2, top_col3 = st.columns([1.4, 3.6, 1.5])
    with top_col1:
        if st.button("← Back to Home", key="nav_back_home"):
            go_to("Home")
            st.rerun()
    with top_col2:
        st.markdown(
            f"<div style='text-align:center; padding-top:6px; font-family:Cinzel,serif; color:#00E5FF; font-size:1.15rem; font-weight:700;'>"
            f"🔥 AETHERFLAME &nbsp;•&nbsp; {st.session_state.active_page.upper()}"
            f"</div>",
            unsafe_allow_html=True
        )
    with top_col3:
        quick_jump = st.selectbox(
            "Switch Module",
            ["Home", "Flame Physics Lab", "Habitat SI Ranker", "Flammability & Partial-g", "PSI Explorer", "Forensics & Spinoffs"],
            index=["Home", "Flame Physics Lab", "Habitat SI Ranker", "Flammability & Partial-g", "PSI Explorer", "Forensics & Spinoffs"].index(st.session_state.active_page),
            label_visibility="collapsed"
        )
        if quick_jump != st.session_state.active_page:
            go_to(quick_jump)
            st.rerun()
    st.divider()

# ==============================================================================
# FRONT PAGE (HOME LANDING STAGE WITH ANIMATED ROCKET, 0G ORB & MODULE BUTTONS)
# ==============================================================================
if st.session_state.active_page == "Home":
    st.markdown("""
    <div class="space-stage">
        <div class="stars-layer"></div>
        <div class="rocket-flight">🚀</div>
        <div class="zero-g-orb"></div>
        <div class="cyan-pill">Super-Intelligent Microgravity Fire Safety Platform</div>
        <div class="hero-title">AETHERFLAME</div>
        <div class="hero-sub">
            Turning decades of <strong>NASA Physical Sciences Informatics (PSI)</strong> microgravity combustion research
            into clear, actionable fire prevention, detection, and suppression intelligence for the <strong>ISS, Artemis Moon Base, and Mars</strong>.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Key Mission KPIs Strip
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown('<div class="metric-card"><div class="metric-val">26+</div><div class="metric-lbl">NASA PSI Investigations</div></div>', unsafe_allow_html=True)
    with k2:
        st.markdown('<div class="metric-card"><div class="metric-val">10 cm/s</div><div class="metric-lbl">Low-g Ventilation Trap</div></div>', unsafe_allow_html=True)
    with k3:
        st.markdown('<div class="metric-card"><div class="metric-val">≥30% O₂</div><div class="metric-lbl">Lunar Habitat Atmosphere</div></div>', unsafe_allow_html=True)
    with k4:
        st.markdown('<div class="metric-card"><div class="metric-val" style="color:#FF4D4D;">500–800 K</div><div class="metric-lbl">Invisible Cool Flame Zone</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### Launch an Interactive Intelligence Module")

    # Row 1 of Front-Page Module Cards & Launch Buttons
    r1c1, r1c2, r1c3 = st.columns(3)
    with r1c1:
        st.markdown("""
        <div class="nav-card">
            <div class="nav-card-icon">🛸</div>
            <div class="nav-card-title">1. Microgravity Flame Lab</div>
            <div class="nav-card-desc">Compare Earth (1g), Orbital (0g), and Lunar (1/6g) flames interactively as you adjust spacecraft HVAC ventilation airflow and cabin oxygen %.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open Flame Lab →", key="btn_lab"):
            go_to("Flame Physics Lab")
            st.rerun()

    with r1c2:
        st.markdown("""
        <div class="nav-card">
            <div class="nav-card-icon">🧠</div>
            <div class="nav-card-title">2. Habitat Risk & SI Ranker</div>
            <div class="nav-card-desc">Select Moon Base, ISS, Spacesuit EVA, or Mars Transit to dynamically rank the top PSI experiments for Prevention, Detection, and Suppression.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open Habitat Ranker →", key="btn_ranker"):
            go_to("Habitat SI Ranker")
            st.rerun()

    with r1c3:
        st.markdown("""
        <div class="nav-card">
            <div class="nav-card-icon">📈</div>
            <div class="nav-card-title">3. Flammability & Partial-g</div>
            <div class="nav-card-desc">Explore the Negative Oxygen Margin of Safety (ISS Guide Fig. 8), upstream flame spread, N₂ extinguisher air-entrainment, and 10 kV partial-g proxies.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open Flammability Map →", key="btn_flam"):
            go_to("Flammability & Partial-g")
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Row 2 of Front-Page Module Cards & Launch Buttons
    r2c1, r2c2 = st.columns(2)
    with r2c1:
        st.markdown("""
        <div class="nav-card">
            <div class="nav-card-icon">🔬</div>
            <div class="nav-card-title">4. PSI Repository Explorer & Comparator</div>
            <div class="nav-card-desc">Search, filter by ISS rack hardware (CIR-ACME, CIR-MDCA, MSG, Cygnus), and compare any PSI investigations side-by-side.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open PSI Explorer →", key="btn_exp"):
            go_to("PSI Explorer")
            st.rerun()

    with r2c2:
        st.markdown("""
        <div class="nav-card">
            <div class="nav-card-icon">🚒</div>
            <div class="nav-card-title">5. Space Forensics & Earth Spinoffs</div>
            <div class="nav-card-desc">Inspect root causes of Apollo 1, Apollo 13, and Mir (1997) alongside life-saving Earth firefighter tanks, mine smoke sensors, and PBI turnout gear.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open Forensics & Spinoffs →", key="btn_spinoff"):
            go_to("Forensics & Spinoffs")
            st.rerun()

# ==============================================================================
# MODULE 1: MICROGRAVITY FLAME PHYSICS LAB
# ==============================================================================
elif st.session_state.active_page == "Flame Physics Lab":
    st.title("Interactive Gravity & Cabin Ventilation Flame Simulator")
    st.markdown(
        "Adjust gravity level, cabin HVAC ventilation airflow, and oxygen concentration to see how flame geometry and fire risk transform between Earth (**1g**), Orbit (**0g**), and the Moon (**1/6g**)."
    )

    col_ctrl, col_viz = st.columns([1, 2])
    with col_ctrl:
        grav_mode = st.selectbox(
            "Gravitational Environment",
            ["Orbital Microgravity (0g — ISS)", "Lunar Partial Gravity (1/6g — Artemis Base)", "Earth Normal Gravity (1g — Reference)"]
        )
        vent_speed = st.slider("Cabin HVAC Ventilation Airflow (cm/s)", 0, 30, 10)
        o2_level = st.slider("Cabin Oxygen Concentration (% O₂)", 14, 40, 32 if "Lunar" in grav_mode else 21)

        if "0g" in grav_mode:
            if vent_speed == 0:
                status = "DIM DIFFUSION SPHERE — Weak ~1W ionized blue flame; radiative heat loss can transition liquid/gas fuels into invisible Cool Flames (PSI-69 / PSI-159)."
                box_cls = "insight-box"
            elif 1 <= vent_speed <= 15:
                status = "⚠️ CRITICAL VENTILATION TRAP — Low-speed HVAC airflow (1–15 cm/s) strips CO₂ blankets and feeds fresh O₂, letting solids burn FASTER and at LOWER O₂% than on Earth (PSI-26 BASS)."
                box_cls = "alert-box"
            else:
                status = "HIGH CONVECTIVE STRETCH — Flame elongates downstream; spread rate scales proportionally with airflow (PSI-100 SAFFIRE-III at 30 cm/s)."
                box_cls = "insight-box"
        elif "Lunar" in grav_mode:
            status = "🌙 LUNAR SEA REGIME (1/6g, ≥30% O₂, ≤10.2 psi) — >40% higher oxygen concentration than Earth dramatically lowers ignition energy; bounded via PSI-22 E-FIELD and FM2."
            box_cls = "alert-box"
        else:
            status = "🌍 EARTH 1g BUOYANCY — Hot gases rise at ~100 cm/s, creating a tall soot-luminous teardrop flame (NASA-STD-6001 Test 1 baseline)."
            box_cls = "insight-box"

        st.markdown(f'<div class="{box_cls}"><strong>Live Physics Interpretation:</strong><br>{status}</div>', unsafe_allow_html=True)

    with col_viz:
        theta = np.linspace(0, 2 * np.pi, 300)
        if "0g" in grav_mode:
            stretch = 1.0 + (vent_speed / 25.0) * 1.4
            shift_x = (vent_speed / 30.0) * 1.2
            r_outer = 1.6 + (o2_level - 21) * 0.03
            x_outer = r_outer * np.cos(theta) * stretch + shift_x
            y_outer = r_outer * np.sin(theta)
            flame_color = "rgba(0, 229, 255, 0.32)" if o2_level <= 26 else "rgba(255, 77, 77, 0.35)"
            line_color = "#00E5FF" if o2_level <= 26 else "#FF4D4D"
            title_txt = f"0g Diffusion Flame Envelope ({o2_level}% O₂, {vent_speed} cm/s Airflow)"
        elif "Lunar" in grav_mode:
            stretch = 1.35 + (vent_speed / 30.0) * 0.9
            x_outer = (1.5 + (o2_level - 21) * 0.03) * np.cos(theta)
            y_outer = (1.5 + (o2_level - 21) * 0.03) * np.sin(theta) * stretch + 0.5
            flame_color = "rgba(0, 229, 255, 0.36)"
            line_color = "#00E5FF"
            title_txt = f"1/6g Lunar Partial-Gravity Flame ({o2_level}% O₂, {vent_speed} cm/s Airflow)"
        else:
            x_outer = 1.1 * np.cos(theta) * (1 - 0.35 * np.sin(theta))
            y_outer = 2.6 * np.sin(theta) + 1.6
            flame_color = "rgba(255, 77, 77, 0.42)"
            line_color = "#FF4D4D"
            title_txt = f"1g Buoyant Teardrop Flame ({o2_level}% O₂, ~100 cm/s Buoyant Plume)"

        fig_flame = go.Figure()
        fig_flame.add_trace(go.Scatter(
            x=x_outer, y=y_outer, fill="toself",
            fillcolor=flame_color, line=dict(color=line_color, width=3),
            name="Reaction Zone"
        ))
        fig_flame.add_trace(go.Scatter(
            x=0.35 * np.cos(theta), y=0.35 * np.sin(theta), fill="toself",
            fillcolor="#F8FAFC", line=dict(color="#00E5FF", width=1.5),
            name="Fuel Sample / Burner (2 cm)"
        ))
        fig_flame.update_layout(
            title=title_txt,
            template="plotly_dark",
            paper_bgcolor="#0F151E",
            plot_bgcolor="#080B10",
            xaxis=dict(range=[-4.5, 5.5], title="Axial / Ventilation Direction (cm)", zeroline=False, gridcolor="#1E293B"),
            yaxis=dict(range=[-3.5, 5.0], title="Vertical / Radial Axis (cm)", scaleanchor="x", scaleratio=1, zeroline=False, gridcolor="#1E293B"),
            height=400,
            margin=dict(l=20, r=20, t=45, b=20)
        )
        st.plotly_chart(fig_flame, use_container_width=True)

# ==============================================================================
# MODULE 2: HABITAT RISK & SI RANKER
# ==============================================================================
elif st.session_state.active_page == "Habitat SI Ranker":
    st.title("Mission Habitat Relevance & SI Priority Ranker")
    st.markdown("Select a human spaceflight habitat and fire safety pillar to rank the most relevant NASA PSI investigations.")

    c1, c2 = st.columns(2)
    with c1:
        habitat = st.selectbox(
            "Target Crew Environment",
            ["Moon Base", "ISS", "Spacesuit EVA", "Mars Transit", "Cargo Transit"]
        )
    with c2:
        pillar_filter = st.selectbox(
            "Fire Safety Engineering Focus",
            ["All Pillars", "Prevention", "Detection", "Suppression"]
        )

    scores = []
    for _, row in df.iterrows():
        score = 55
        if habitat in row["habitats"]:
            score += 25
        if pillar_filter != "All Pillars" and pillar_filter.lower() in row["pillar"].lower():
            score += 15
        if habitat in ["Moon Base", "Spacesuit EVA"] and row["o2_max"] >= 30:
            score += 5
        if "Microgravity Flight" in row["type"]:
            score += 3
        scores.append(min(score, 99))

    ranked_df = df.copy()
    ranked_df["SI Relevance Score"] = scores
    ranked_df = ranked_df.sort_values(by="SI Relevance Score", ascending=False)

    col_chart1, col_chart2 = st.columns(2)
    with col_chart1:
        top10 = ranked_df.head(10)
        fig_rank = px.bar(
            top10[::-1], x="SI Relevance Score", y="id", orientation="h",
            color="SI Relevance Score", color_continuous_scale=["#1E293B", "#00E5FF"],
            hover_data=["name", "pillar", "hardware"],
            title=f"Top 10 Ranked PSI Investigations for {habitat}"
        )
        fig_rank.update_layout(
            template="plotly_dark", paper_bgcolor="#0F151E",
            plot_bgcolor="#080B10", height=370, showlegend=False,
            xaxis=dict(gridcolor="#1E293B"), yaxis=dict(gridcolor="#1E293B")
        )
        st.plotly_chart(fig_rank, use_container_width=True)

    with col_chart2:
        env_df = pd.DataFrame([
            {"Environment": "Earth Sea Level (1g)", "O2_pct": 21, "Pressure_psi": 14.7},
            {"Environment": "ISS Cabin (0g)", "O2_pct": 21, "Pressure_psi": 14.7},
            {"Environment": "Artemis Moon Base (1/6g)", "O2_pct": 34, "Pressure_psi": 8.2},
            {"Environment": "Pressurized Lunar Rover", "O2_pct": 32, "Pressure_psi": 10.2},
            {"Environment": "EVA Spacesuit (100% O₂)", "O2_pct": 100, "Pressure_psi": 4.3},
            {"Environment": "Apollo 1 Cabin (1967)", "O2_pct": 100, "Pressure_psi": 16.7}
        ])
        fig_env = px.scatter(
            env_df, x="Pressure_psi", y="O2_pct", text="Environment",
            size=[22, 26, 34, 30, 36, 38], color="O2_pct",
            color_continuous_scale=["#00E5FF", "#80F2FF", "#FF4D4D"],
            title="Spacecraft & Planetary Atmosphere Flammability Envelopes"
        )
        fig_env.update_traces(textposition="top center")
        fig_env.update_layout(
            template="plotly_dark", paper_bgcolor="#0F151E",
            plot_bgcolor="#080B10", height=370,
            xaxis_title="Cabin Pressure (psi)", yaxis_title="Oxygen Concentration (% O₂)",
            yaxis=dict(range=[10, 115], gridcolor="#1E293B"),
            xaxis=dict(range=[2, 19], gridcolor="#1E293B")
        )
        st.plotly_chart(fig_env, use_container_width=True)

    st.subheader(f"Prioritized Investigation Briefings for {habitat}")
    for _, r in ranked_df.head(6).iterrows():
        with st.expander(f"💠 {r['SI Relevance Score']}% Match | {r['id']}: {r['name']} ({r['hardware']})"):
            st.markdown(f"**Plain-English Insight:** {r['plain_summary']}")
            st.markdown(f"- **Test Envelope:** `{r['o2_min']}–{r['o2_max']}% O₂` | `{r['p_min']}–{r['p_max']} atm` | Airflow: `{r['flow_min']}–{r['flow_max']} cm/s`")
            st.markdown(f"- **Fuels / Materials:** {r['fuels']}")
            st.markdown(f"- **Diagnostics & Sensors:** {r['sensors']}")

# ==============================================================================
# MODULE 3: FLAMMABILITY & PARTIAL-G PREDICTIVE LAB
# ==============================================================================
elif st.session_state.active_page == "Flammability & Partial-g":
    st.title("Microgravity Flammability Map & Partial-Gravity Bounding")
    st.markdown(
        "NASA's **NASA-STD-6001 Test 1** screens spacecraft materials in upward 1g flow on Earth. "
        "However, **BASS (`PSI-26`)** and **BASS-II (`PSI-25`)** proved that slow cabin ventilation flows (**1–15 cm/s**) "
        "create a **Negative Oxygen Margin of Safety** where materials burn at lower oxygen concentrations in space than on Earth."
    )

    col_left, col_right = st.columns([2, 1])
    with col_left:
        v_flow = np.linspace(0.5, 45, 200)
        loi_0g = 14.5 + 0.032 * (v_flow - 10.0) ** 2 / (1 + 0.04 * v_flow)
        loi_0g = np.clip(loi_0g, 14.2, 28.0)
        nasa_test1_limit = np.full_like(v_flow, 18.5)

        fig_map = go.Figure()
        fig_map.add_trace(go.Scatter(
            x=v_flow, y=nasa_test1_limit, mode="lines",
            name="NASA-STD-6001 Test 1 Limit (1g Earth Standard ~18.5% O₂)",
            line=dict(color="#94A3B8", width=2.5, dash="dash")
        ))
        fig_map.add_trace(go.Scatter(
            x=v_flow, y=loi_0g, mode="lines",
            name="Actual 0g Microgravity Flammability Limit (BASS / BASS-II)",
            line=dict(color="#00E5FF", width=3.5),
            fill="tonexty", fillcolor="rgba(255, 77, 77, 0.22)"
        ))
        fig_map.add_annotation(
            x=10, y=14.6, text="0g Minimum LOI (~10 cm/s)<br>Negative Oxygen Margin of Safety",
            showarrow=True, arrowhead=2, ax=40, ay=35, font=dict(color="#FF4D4D")
        )
        fig_map.add_hrect(y0=30, y1=36, fillcolor="rgba(0, 229, 255, 0.12)", line_width=0,
                          annotation_text="Artemis Lunar Base Target Atmosphere (30–34% O₂)")

        fig_map.update_layout(
            title="Flammability Map: Limiting Oxygen Concentration vs. Ventilation Velocity",
            template="plotly_dark", paper_bgcolor="#0F151E",
            plot_bgcolor="#080B10",
            xaxis_title="Forced or Buoyant Airflow Velocity (cm/s)",
            yaxis_title="Ambient Oxygen Concentration (% O₂)",
            yaxis=dict(range=[12, 37], gridcolor="#1E293B"),
            xaxis=dict(gridcolor="#1E293B"), height=420
        )
        st.plotly_chart(fig_map, use_container_width=True)

    with col_right:
        st.subheader("3 Critical Spacecraft Fire Traps")
        st.markdown("""
        <div class="alert-box">
        <strong>1. Upstream Flame Spread (PSI-26):</strong><br>
        In slow airflows (&lt;15 cm/s), flames spread <em>upstream</em> into oncoming ventilation air—opposite to Earth fires.
        </div>
        <div class="alert-box">
        <strong>2. Nitrogen Extinguisher Paradox (PSI-26):</strong><br>
        Aiming a local N₂ extinguisher jet at a wake-stabilized flame in 0g can <em>strengthen</em> the fire by entraining cabin oxygen.
        </div>
        <div class="insight-box">
        <strong>3. Partial-Gravity Bounding (PSI-22 & FM2):</strong><br>
        PSI currently lacks 1/6g Lunar data. <strong>ACME E-FIELD (PSI-22)</strong> uses up to <strong>10 kV</strong> electric fields on flame ions to simulate intermediate buoyant convection until Lunar <strong>FM2</strong> & <strong>LUCI</strong> data arrive.
        </div>
        """, unsafe_allow_html=True)

# ==============================================================================
# MODULE 4: PSI REPOSITORY EXPLORER & COMPARATOR
# ==============================================================================
elif st.session_state.active_page == "PSI Explorer":
    st.title("PSI Combustion Repository Explorer & Comparator")

    f1, f2, f3 = st.columns(3)
    with f1:
        hw_filter = st.multiselect(
            "Filter by ISS / Flight Hardware",
            options=sorted(df["hardware"].unique()),
            default=[]
        )
    with f2:
        fuel_filter = st.multiselect(
            "Filter by Fuel Category",
            options=sorted(df["fuel_cat"].unique()),
            default=[]
        )
    with f3:
        search_txt = st.text_input("Search Keyword (e.g., PMMA, Cool Flame, SIBAL, Soot)")

    filtered = df.copy()
    if hw_filter:
        filtered = filtered[filtered["hardware"].isin(hw_filter)]
    if fuel_filter:
        filtered = filtered[filtered["fuel_cat"].isin(fuel_filter)]
    if search_txt:
        mask = filtered.apply(lambda r: search_txt.lower() in str(r.values).lower(), axis=1)
        filtered = filtered[mask]

    st.dataframe(
        filtered[["id", "name", "type", "hardware", "fuel_cat", "o2_min", "o2_max", "flow_min", "flow_max", "pillar"]],
        use_container_width=True,
        hide_index=True
    )

    st.markdown("### Side-by-Side Investigation Comparator")
    comp_ids = st.multiselect(
        "Select 2 or 3 PSI Investigations to Compare",
        options=df["id"].tolist(),
        default=["PSI-26", "PSI-98", "PSI-69"]
    )
    if comp_ids:
        comp_df = df[df["id"].isin(comp_ids)].set_index("id").T
        st.dataframe(comp_df, use_container_width=True)

# ==============================================================================
# MODULE 5: SPACE FORENSICS & EARTH SPINOFFS
# ==============================================================================
elif st.session_state.active_page == "Forensics & Spinoffs":
    st.title("Spaceflight Fire Forensics & Earth Firefighter Spinoffs")

    st.subheader("1. Historical Spaceflight Fire Incidents Driving NASA Safety")
    h1, h2, h3 = st.columns(3)
    with h1:
        st.markdown("""
        <div class="alert-box">
        <h4>Apollo 1 (Jan 27, 1967)</h4>
        <strong>Condition:</strong> 100% O₂ at 16.7 psi on Launch Pad 34.<br>
        <strong>Cause:</strong> Wire arcing near ECS ignited Velcro & nylon; inward hatch pinned shut.<br>
        <strong>Legacy:</strong> Outward 3-sec hatch, strict NASA-STD-6001 material limits, and fireproof PBI/Beta cloth suits.
        </div>
        """, unsafe_allow_html=True)
    with h2:
        st.markdown("""
        <div class="alert-box">
        <h4>Apollo 13 (Apr 13, 1970)</h4>
        <strong>Condition:</strong> Cryogenic O₂ Tank No. 2 in transit to Moon.<br>
        <strong>Cause:</strong> 65V heater cycle degraded Teflon wire insulation at ~1,000°F, sparking an O₂ tank explosion.<br>
        <strong>Legacy:</strong> Stainless-steel sheathed tank wiring, upgraded thermostats, and isolated 3rd O₂ tank.
        </div>
        """, unsafe_allow_html=True)
    with h3:
        st.markdown("""
        <div class="alert-box">
        <h4>Space Station Mir (Feb 24, 1997)</h4>
        <strong>Condition:</strong> Kvant-1 module during 6-crew handover.<br>
        <strong>Cause:</strong> Latex glove fragment contaminated a lithium perchlorate (Vika) O₂ canister, shooting a 3-ft molten flame.<br>
        <strong>Legacy:</strong> Dissimilar redundant ISS O₂ generation (Elektron + OGS) and respirator protocols.
        </div>
        """, unsafe_allow_html=True)

    st.subheader("2. NASA Fire Safety Spinoffs Saving Lives on Earth")
    s1, s2, s3, s4 = st.columns(4)
    with s1:
        st.markdown("""
        <div class="metric-card">
        <div class="metric-val">20 lbs</div>
        <div class="metric-lbl"><strong>Scott Air-Pak 4.5 Tanks</strong><br>Composite 4,500 psi tanks cut firefighter SCBA weight by 13 lbs (from 33 lbs).</div>
        </div>
        """, unsafe_allow_html=True)
    with s2:
        st.markdown("""
        <div class="metric-card">
        <div class="metric-val">U508</div>
        <div class="metric-lbl"><strong>Dust-Immune Smoke Sensor</strong><br>Shuttle/SAME/DAFT aerosol sizing discriminates smoke from mining dust.</div>
        </div>
        """, unsafe_allow_html=True)
    with s3:
        st.markdown("""
        <div class="metric-card">
        <div class="metric-val">12.5 lbs</div>
        <div class="metric-lbl"><strong>Project FIRES Turnout Gear</strong><br>Apollo PBI & GORE-TEX vapor barrier cut gear weight 40% & heat stress.</div>
        </div>
        """, unsafe_allow_html=True)
    with s4:
        st.markdown("""
        <div class="metric-card">
        <div class="metric-val" style="color:#FF4D4D;">ISS Mist</div>
        <div class="metric-lbl"><strong>Fine-Water-Mist Extinguishers</strong><br>Non-toxic micro-droplet suppression replacing Halon & CO₂ units.</div>
        </div>
        """, unsafe_allow_html=True)
