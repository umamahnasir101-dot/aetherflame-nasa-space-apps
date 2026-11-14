# AETHERFLAME — Microgravity Combustion & Habitat Fire Safety Intelligence

**NASA Space Apps Challenge 2026 | Flame in Freefall**

AETHERFLAME is an interactive, intelligence-driven fire safety analytics platform built on **NASA's Physical Sciences Informatics (PSI) Combustion Science Repository** (`psi.nasa.gov/physci/repo`), the *ISS Researcher's Guide to Combustion Science* (`NP-2015-10-034-JSC`), and historical NASA spaceflight fire forensics.

## Core Capabilities
1. **Interactive Microgravity Flame Physics Simulator:** Compare Earth ($1g$ buoyant teardrop), ISS ($0g$ diffusion blue sphere), and Lunar ($1/6g$) flames across cabin ventilation velocities ($0\text{–}30\text{ cm/s}$).
2. **Habitat Relevance & SI Priority Ranker:** Ranks all 26 PSI combustion investigations for the **Artemis Lunar Base ($\ge 30\%\ O_2, \le 10.2\text{ psi}$)**, **ISS ($21\%\ O_2, 14.7\text{ psi}$)**, **Spacesuit EVA ($100\%\ O_2, 4.3\text{ psi}$)**, and **Mars Transit** across Prevention, Detection, and Suppression.
3. **Flammability & Partial-Gravity Predictive Lab:** Models the **Negative Oxygen Margin of Safety** ($1\text{–}15\text{ cm/s}$ ventilation danger zone vs. NASA-STD-6001 Test 1), Cool Flame invisible re-ignition ($500\text{–}800\text{ K}$), and `PSI-22` E-FIELD ($10\text{ kV}$) partial-gravity bounding.
4. **PSI Repository Explorer & Comparator:** Search, filter, and compare all 26 PSI experiments (`PSI-10` to `PSI-181`, `DAFT`, `FM2`, `SoFIE`, `FLARE`).
5. **Spaceflight Forensics & Earth Spinoffs:** Connects lessons from **Apollo 1**, **Apollo 13**, and **Space Station Mir (1997)** to terrestrial spinoffs (**Scott Air-Pak 4.5** 20-lb tanks, **Brunswick U508** mine smoke detectors, **Project FIRES** 12.5-lb PBI/GORE-TEX gear, and ISS water-mist extinguishers).

## Open-Source & AI Disclosure
- Built with Python, Streamlit, Pandas, NumPy, and Plotly.
- AI assistance was utilized for code structuring and data formatting; all scientific parameters, test envelopes, and investigation records are verified directly against official NASA PSI documentation.