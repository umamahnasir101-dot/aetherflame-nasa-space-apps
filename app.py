import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# ==============================================================================
# PAGE CONFIG & CUSTOM DEEP SPACE GOLD / STARLIGHT THEME
# ==============================================================================
st.set_page_config(
    page_title="AETHERFLAME | Space Habitat Fire Safety Intelligence",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Plus+Jakarta+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    h1, h2, h3 {
        font-family: 'Instrument Serif', serif !important;
        letter-spacing: 0.01em;
    }
    .stApp {
        background: radial-gradient(circle at 85% 10%, rgba(212, 175, 55, 0.10), transparent 35%),
                    radial-gradient(circle at 10% 90%, rgba(56, 189, 248, 0.08), transparent 40%),
                    #070B14;
        color: #F4F1EA;
    }
    section[data-testid="stSidebar"] {
        background-color: #0B1120;
        border-right: 1px solid rgba(212, 175, 55, 0.25);
    }
    .gold-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 999px;
        background: rgba(212, 175, 55, 0.14);
        border: 1px solid rgba(212, 175, 55, 0.45);
        color: #F3D06B;
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        margin-bottom: 8px;
    }
    .metric-card {
        background: rgba(15, 23, 42, 0.78);
        border: 1px solid rgba(212, 175, 55, 0.28);
        border-radius: 14px;
        padding: 18px 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.35);
    }
    .metric-val {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.75rem;
        font-weight: 700;
        color: #F3D06B;
    }
    .metric-lbl {
        font-size: 0.85rem;
        color: #CBD5E1;
        margin-top: 4px;
    }
    .insight-box {
        background: linear-gradient(135deg, rgba(212,175,55,0.12), rgba(15,23,42,0.85));
        border-left: 4px solid #D4AF37;
        border-radius: 10px;
        padding: 16px 20px;
        margin: 12px 0;
        color: #F8FAFC;
    }
    .alert-box {
        background: rgba(239, 68, 68, 0.12);
        border-left: 4px solid #EF4444;
        border-radius: 10px;
        padding: 14px 18px;
        margin: 10px 0;
        color: #FEE2E2;
    }
</style>
""", unsafe_allow_html=True)

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
        "habitats": ["ISS", "Moon Base", "Mars Transit"],
        "related": "PSI-25, PSI-62, PSI-98, PSI-107"
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
        "habitats": ["ISS", "Moon Base", "Mars Transit"],
        "related": "PSI-26, PSI-62, PSI-98"
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
        "habitats": ["ISS", "Cargo Transit", "Moon Base"],
        "related": "PSI-99, PSI-100, PSI-26"
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
        "habitats": ["ISS", "Cargo Transit", "Moon Base"],
        "related": "PSI-98, PSI-100, PSI-26"
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
        "habitats": ["ISS", "Cargo Transit", "Moon Base"],
        "related": "PSI-98, PSI-99, PSI-26"
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
        "habitats": ["ISS", "Moon Base", "Mars Transit"],
        "related": "PSI-68, PSI-39, PSI-117, PSI-142"
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
        "habitats": ["ISS", "Moon Base", "Mars Transit"],
        "related": "PSI-69, PSI-39, PSI-117"
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
        "habitats": ["ISS", "Moon Base", "Mars Transit", "Cargo Transit"],
        "related": "PSI-101, PSI-115, DAFT"
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
        "habitats": ["ISS", "Moon Base", "Mars Transit"],
        "related": "PSI-102, PSI-115, DAFT"
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
        "habitats": ["Moon Base", "Spacesuit EVA", "Mars Transit"],
        "related": "PSI-39, PSI-69, PSI-10"
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
        "habitats": ["Moon Base", "Mars Transit"],
        "related": "PSI-21, PSI-23, FM2"
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
        "habitats": ["Moon Base", "ISS", "Spacesuit EVA"],
        "related": "PSI-10, PSI-21, PSI-22, PSI-23"
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
        "habitats": ["Moon Base", "ISS", "Mars Transit"],
        "related": "PSI-20, PSI-23, PSI-159"
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
        "habitats": ["Moon Base", "ISS", "Mars Transit"],
        "related": "PSI-69, PSI-68, PSI-159"
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
        "habitats": ["ISS", "Moon Base", "Mars Transit"],
        "related": "PSI-102, PSI-101, PSI-115"
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
        "habitats": ["ISS", "Moon Base"],
        "related": "PSI-106, PSI-22, PSI-10"
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
        "habitats": ["Moon Base", "ISS", "Spacesuit EVA"],
        "related": "PSI-10, PSI-20, PSI-159"
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
        "habitats": ["ISS", "Moon Base"],
        "related": "PSI-60, PSI-106, PSI-26"
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
        "habitats": ["ISS", "Moon Base"],
        "related": "PSI-107, PSI-21"
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
        "habitats": ["ISS", "Moon Base", "Mars Transit"],
        "related": "PSI-25, PSI-26"
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
        "habitats": ["ISS", "Moon Base"],
        "related": "PSI-107"
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
        "habitats": ["ISS", "Moon Base"],
        "related": "PSI-69, PSI-142"
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
        "habitats": ["ISS", "Moon Base"],
        "related": "PSI-69, PSI-117"
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
        "habitats": ["ISS", "Moon Base", "Mars Transit"],
        "related": "PSI-102, PSI-101"
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
        "habitats": ["ISS", "Moon Base"],
        "related": "PSI-69"
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
        "habitats": ["ISS", "Moon Base", "Spacesuit EVA", "Mars Transit"],
        "related": "PSI-77"
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
        "habitats": ["Moon Base", "Mars Transit", "ISS"],
        "related": "PSI-25, PSI-26, PSI-22"
    }
]

df = pd.DataFrame(PSI_DATA)

# ==============================================================================
# SIDEBAR NAVIGATION & MISSION PROFILE
# ==============================================================================
with st.sidebar:
    st.markdown('<div class="gold-badge">NASA PSI Intelligence MVP</div>', unsafe_allow_html=True)
    st.title("🔥 AETHERFLAME")
    st.caption("Super-Intelligent Fire Safety Insights from Microgravity Combustion Data")
    st.divider()

    page = st.radio(
        "Navigation",
        [
            "1. Microgravity Flame Lab",
            "2. Habitat Risk & SI Ranker",
            "3. Flammability & Partial-g Lab",
            "4. PSI Explorer & Comparator",
            "5. Space Forensics & Earth Spinoffs"
        ]
    )

    st.divider()
    st.markdown("**Mission Atmosphere Reference**")
    st.markdown("""
    - **ISS Cabin:** `21% O₂` | `14.7 psi` (`1.0 atm`)
    - **Artemis Moon Base:** `≥30–34% O₂` | `≤10.2 psi`
    - **EVA Spacesuit:** `100% O₂` | `4.3 psi`
    - **Ventilation Danger Zone:** `1–15 cm/s`
    """)
    st.divider()
    st.caption("Data Source: NASA Physical Sciences Informatics (PSI) Combustion Repository & ISS Researcher's Guide (NP-2015-10-034-JSC).")

# ==============================================================================
# PAGE 1: MICROGRAVITY FLAME LAB (HOME & PHYSICS VISUALIZER)
# ==============================================================================
if page == "1. Microgravity Flame Lab":
    st.markdown('<div class="gold-badge">Flame in Freefall • Space Habitat Fire Intelligence</div>', unsafe_allow_html=True)
    st.title("Why Fire Behaves Differently in Space")
    st.markdown(
        "On Earth, hot combustion gases rise due to gravity-driven buoyancy, pulling fresh oxygen into a flickering teardrop flame. "
        "In orbital microgravity (**0g**) and lunar partial gravity (**1/6g**), buoyancy vanishes or weakens—creating spherical diffusion flames, "
        "invisible **cool flames**, and a counter-intuitive **ventilation flammability trap**."
    )

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown('<div class="metric-card"><div class="metric-val">26+</div><div class="metric-lbl">NASA PSI Investigations Indexed</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="metric-card"><div class="metric-val">10 cm/s</div><div class="metric-lbl">Peak Low-g Ventilation Hazard</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="metric-card"><div class="metric-val">≥30% O₂</div><div class="metric-lbl">Lunar Base Exploration Atmosphere</div></div>', unsafe_allow_html=True)
    with c4:
        st.markdown('<div class="metric-card"><div class="metric-val">500–800 K</div><div class="metric-lbl">Invisible Cool Flame Regime</div></div>', unsafe_allow_html=True)

    st.markdown("### Interactive Gravity & Cabin Ventilation Flame Simulator")
    col_ctrl, col_viz = st.columns([1, 2])

    with col_ctrl:
        grav_mode = st.selectbox(
            "Select Gravitational Environment",
            ["Orbital Microgravity (0g — ISS)", "Lunar Partial Gravity (1/6g — Artemis Base)", "Earth Normal Gravity (1g — Reference)"]
        )
        vent_speed = st.slider("Spacecraft HVAC Ventilation Airflow (cm/s)", 0, 30, 10)
        o2_level = st.slider("Cabin Oxygen Concentration (% O₂)", 14, 40, 32 if "Lunar" in grav_mode else 21)

        if "0g" in grav_mode:
            if vent_speed == 0:
                status = "DIM DIFFUSION SPHERE — Weak ~1W blue flame; radiative heat loss can transition liquid/gas fuels into invisible Cool Flames (PSI-69 / PSI-159)."
            elif 1 <= vent_speed <= 15:
                status = "⚠️ CRITICAL VENTILATION TRAP — Low-speed HVAC airflow (1–15 cm/s) strips CO₂ blankets and feeds fresh O₂, letting solids burn FASTER and at LOWER O₂% than on Earth (PSI-26 BASS)."
            else:
                status = "HIGH CONVECTIVE STRETCH — Flame elongates downstream; spread rate scales proportionally with airflow (PSI-100 SAFFIRE-III at 30 cm/s)."
        elif "Lunar" in grav_mode:
            status = "🌙 LUNAR SEA REGIME (1/6g, ≥30% O₂, ≤10.2 psi) — >40% higher oxygen concentration than Earth dramatically lowers ignition energy; bounded via PSI-22 E-FIELD and FM2."
        else:
            status = "🌍 EARTH 1g BUOYANCY — Hot gases rise at ~100 cm/s, creating a tall yellow soot-luminous teardrop flame (NASA-STD-6001 Test 1 baseline)."

        st.markdown(f'<div class="insight-box"><strong>Live Physics Interpretation:</strong><br>{status}</div>', unsafe_allow_html=True)

    with col_viz:
        # Plotly parametric flame shape & temperature field visualization
        theta = np.linspace(0, 2 * np.pi, 300)
        if "0g" in grav_mode:
            stretch = 1.0 + (vent_speed / 25.0) * 1.4
            shift_x = (vent_speed / 30.0) * 1.2
            r_outer = 1.6 + (o2_level - 21) * 0.03
            x_outer = r_outer * np.cos(theta) * stretch + shift_x
            y_outer = r_outer * np.sin(theta)
            flame_color = "rgba(56, 189, 248, 0.35)" if o2_level <= 24 else "rgba(243, 208, 107, 0.42)"
            line_color = "#38BDF8" if o2_level <= 24 else "#F3D06B"
            title_txt = f"0g Diffusion Flame Envelope ({o2_level}% O₂, {vent_speed} cm/s Airflow)"
        elif "Lunar" in grav_mode:
            stretch = 1.35 + (vent_speed / 30.0) * 0.9
            x_outer = (1.5 + (o2_level - 21) * 0.03) * np.cos(theta)
            y_outer = (1.5 + (o2_level - 21) * 0.03) * np.sin(theta) * stretch + 0.5
            flame_color = "rgba(245, 158, 11, 0.40)"
            line_color = "#F59E0B"
            title_txt = f"1/6g Lunar Partial-Gravity Flame ({o2_level}% O₂, {vent_speed} cm/s Airflow)"
        else:
            x_outer = 1.1 * np.cos(theta) * (1 - 0.35 * np.sin(theta))
            y_outer = 2.6 * np.sin(theta) + 1.6
            flame_color = "rgba(249, 115, 22, 0.45)"
            line_color = "#F97316"
            title_txt = f"1g Buoyant Teardrop Flame ({o2_level}% O₂, ~100 cm/s Buoyant Plume)"

        fig_flame = go.Figure()
        fig_flame.add_trace(go.Scatter(
            x=x_outer, y=y_outer, fill="toself",
            fillcolor=flame_color, line=dict(color=line_color, width=3),
            name="Reaction Zone"
        ))
        # Fuel core
        fig_flame.add_trace(go.Scatter(
            x=0.35 * np.cos(theta), y=0.35 * np.sin(theta), fill="toself",
            fillcolor="#F3D06B", line=dict(color="#FFFFFF", width=1.5),
            name="Fuel Sample / Burner (2 cm)"
        ))
        fig_flame.update_layout(
            title=title_txt,
            template="plotly_dark",
            paper_bgcolor="rgba(15,23,42,0.6)",
            plot_bgcolor="rgba(7,11,20,0.9)",
            xaxis=dict(range=[-4.5, 5.5], title="Axial / Ventilation Direction (cm)", zeroline=False),
            yaxis=dict(range=[-3.5, 5.0], title="Vertical / Radial Axis (cm)", scaleanchor="x", scaleratio=1, zeroline=False),
            height=380,
            margin=dict(l=20, r=20, t=45, b=20)
        )
        st.plotly_chart(fig_flame, use_container_width=True)

# ==============================================================================
# PAGE 2: HABITAT RISK & SI RANKER
# ==============================================================================
elif page == "2. Habitat Risk & SI Ranker":
    st.markdown('<div class="gold-badge">Super-Intelligent Decision Engine</div>', unsafe_allow_html=True)
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

    # Compute SI Relevance Score dynamically
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
            color="SI Relevance Score", color_continuous_scale=["#38BDF8", "#D4AF37"],
            hover_data=["name", "pillar", "hardware"],
            title=f"Top 10 Ranked PSI Investigations for {habitat}"
        )
        fig_rank.update_layout(
            template="plotly_dark", paper_bgcolor="rgba(15,23,42,0.6)",
            plot_bgcolor="rgba(7,11,20,0.85)", height=360, showlegend=False
        )
        st.plotly_chart(fig_rank, use_container_width=True)

    with col_chart2:
        # Habitat Atmosphere Envelope Chart (O2% vs Pressure psi)
        env_df = pd.DataFrame([
            {"Environment": "Earth Sea Level (1g)", "O2_pct": 21, "Pressure_psi": 14.7, "Risk": "Baseline"},
            {"Environment": "ISS Cabin (0g)", "O2_pct": 21, "Pressure_psi": 14.7, "Risk": "Low-Flow Ventilation Trap"},
            {"Environment": "Artemis Moon Base (1/6g)", "O2_pct": 34, "Pressure_psi": 8.2, "Risk": "Elevated O₂ (>40% jump)"},
            {"Environment": "Pressurized Lunar Rover", "O2_pct": 32, "Pressure_psi": 10.2, "Risk": "Elevated O₂ SEA"},
            {"Environment": "EVA Spacesuit (100% O₂)", "O2_pct": 100, "Pressure_psi": 4.3, "Risk": "Pure Oxygen Ignition"},
            {"Environment": "Apollo 1 Cabin (1967)", "O2_pct": 100, "Pressure_psi": 16.7, "Risk": "Catastrophic Flash Fire"}
        ])
        fig_env = px.scatter(
            env_df, x="Pressure_psi", y="O2_pct", text="Environment",
            size=[22, 26, 34, 30, 36, 38], color="O2_pct",
            color_continuous_scale=["#38BDF8", "#F3D06B", "#EF4444"],
            title="Spacecraft & Planetary Atmosphere Flammability Envelopes"
        )
        fig_env.update_traces(textposition="top center")
        fig_env.update_layout(
            template="plotly_dark", paper_bgcolor="rgba(15,23,42,0.6)",
            plot_bgcolor="rgba(7,11,20,0.85)", height=360,
            xaxis_title="Cabin Pressure (psi)", yaxis_title="Oxygen Concentration (% O₂)",
            yaxis=dict(range=[10, 115]), xaxis=dict(range=[2, 19])
        )
        st.plotly_chart(fig_env, use_container_width=True)

    st.subheader(f"Prioritized Investigation Briefings for {habitat}")
    for _, r in ranked_df.head(6).iterrows():
        with st.expander(f"⭐ {r['SI Relevance Score']}% Match | {r['id']}: {r['name']} ({r['hardware']})"):
            st.markdown(f"**Plain-English Insight:** {r['plain_summary']}")
            st.markdown(f"- **Test Envelope:** `{r['o2_min']}–{r['o2_max']}% O₂` | `{r['p_min']}–{r['p_max']} atm` | Airflow: `{r['flow_min']}–{r['flow_max']} cm/s`")
            st.markdown(f"- **Fuels / Materials:** {r['fuels']}")
            st.markdown(f"- **Diagnostics & Sensors:** {r['sensors']}")

# ==============================================================================
# PAGE 3: FLAMMABILITY & PARTIAL-G PREDICTIVE LAB
# ==============================================================================
elif page == "3. Flammability & Partial-g Lab":
    st.markdown('<div class="gold-badge">ISS Researcher\'s Guide Fig. 8 • Negative Margin of Safety</div>', unsafe_allow_html=True)
    st.title("Microgravity Flammability Map & Partial-Gravity Bounding")
    st.markdown(
        "NASA's **NASA-STD-6001 Test 1** screens spacecraft materials in upward 1g flow on Earth. "
        "However, **BASS (`PSI-26`)** and **BASS-II (`PSI-25`)** proved that slow cabin ventilation flows (**1–15 cm/s**) "
        "create a **Negative Oxygen Margin of Safety** where materials burn at lower oxygen concentrations in space than on Earth."
    )

    col_left, col_right = st.columns([2, 1])
    with col_left:
        # Reproduce Figure 8 Flammability Curve from ISS Researcher's Guide
        v_flow = np.linspace(0.5, 45, 200)
        # U-shaped 0g limiting oxygen index curve (minimum around 10 cm/s at ~14.5% O2)
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
            line=dict(color="#F3D06B", width=3.5),
            fill="tonexty", fillcolor="rgba(239, 68, 68, 0.18)"
        ))
        fig_map.add_annotation(
            x=10, y=14.6, text="0g Minimum LOI (~10 cm/s)<br>Negative Oxygen Margin of Safety",
            showarrow=True, arrowhead=2, ax=40, ay=35, font=dict(color="#FCA5A5")
        )
        fig_map.add_hrect(y0=30, y1=36, fillcolor="rgba(212,175,55,0.15)", line_width=0,
                          annotation_text="Artemis Lunar Base Target Atmosphere (30–34% O₂)")

        fig_map.update_layout(
            title="Flammability Map: Limiting Oxygen Concentration vs. Ventilation Velocity",
            template="plotly_dark", paper_bgcolor="rgba(15,23,42,0.6)",
            plot_bgcolor="rgba(7,11,20,0.9)",
            xaxis_title="Forced or Buoyant Airflow Velocity (cm/s)",
            yaxis_title="Ambient Oxygen Concentration (% O₂)",
            yaxis=dict(range=[12, 37]), height=420
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
# PAGE 4: PSI REPOSITORY EXPLORER & COMPARATOR
# ==============================================================================
elif page == "4. PSI Explorer & Comparator":
    st.markdown('<div class="gold-badge">26 Indexed NASA PSI Investigations</div>', unsafe_allow_html=True)
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
# PAGE 5: SPACE FORENSICS & EARTH SPINOFFS
# ==============================================================================
elif page == "5. Space Forensics & Earth Spinoffs":
    st.markdown('<div class="gold-badge">Historical Lessons & Terrestrial Impact</div>', unsafe_allow_html=True)
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
        <div class="metric-val">ISS Mist</div>
        <div class="metric-lbl"><strong>Fine-Water-Mist Extinguishers</strong><br>Non-toxic micro-droplet suppression replacing Halon & CO₂ units.</div>
        </div>
        """, unsafe_allow_html=True)