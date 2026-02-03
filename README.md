# Evolutionary Ecosystem Simulator (evo_eco)
An ever-evolving ecosystem of plants and animals, which will grow over time to become a stochastic simulation of Earth (and beyond!)

> "Ever since I've known about computer language, given my background in Biology, I've wanted to create a realistic simulation of the Earth's evolving flora & fauna."

##  The Vision
This project is an exploration of the "Evolutionary Arms Race." It serves as a digital laboratory to process complex ideas about natural systems, from the generation of novel organisms in early Earth to the shifting ecosystem dynamics of the Anthropocene. 

Inspired by the mission of **Silurian** and the **Aurora paper**, this simulation aims to bridge the gap between biological theory and computational infrastructure. While many systems ignore 90% of available environmental data, this project seeks to eventually build "hidden layers" of information that only evolved agents can decode.

## Phase I: Technical Specification (The Seed)
Currently, the simulation is in its foundational phase, focusing on the stochastic stability of a population under metabolic pressure.
* Inheritance Logic: Offspring inherit the metabolism trait from their parent.
* Genetic Drift: A $\pm 10\%$ mutation rate is applied to the metabolism of newborns to ensure trait variance.
* The Malthusian Gate: The "Food Rain" is currently static, creating a resource-limited environment that favors lower-metabolism (energy-efficient) agents.
* Telemetry: The system logs real-time Average Metabolism to observe phenotypic shifts in the population over time.

##  Current Features
* **Bio-Logic Agents:** Organisms with attributes for energy, fatigue, and position.
* **Resource Competition:** A dynamic "World" where agents must hunt for food to survive and reproduce.
* **Lifecycle Mechanics:** Integrated logic for metabolism, movement costs, and starvation.
* **Spatiotemporal Tracking:** Real-time terminal visualization of agent movement and resource depletion.

##  Built With
* **Python 3.x**
* **Human-in-the-loop AI Workflow:** Architected by JT, refined and vibe-coded with assistance from **Google Gemini** and **Claude Code**.

##  The Roadmap
* **Sensory Evolution:** Transitioning from "random-walk" movement to agents with "eyesight" that navigate environmental gradients.
* **Genetic Heredity:** Implementing mutation rates for traits like metabolism speed and defense (e.g., wood and spines).
* **Flora Adaptation:** Co-evolutionary logic allowing plants to develop defense mechanisms in response to predation.
* **The Web Simulacrum:** Moving from terminal output to a tactile, 8-bit interactive experience for the web.

##  Getting Started
1. Clone the repo: `git clone https://github.com/jtgoods/evo_eco.git`
2. Run the simulation: `python evo_eco.py`

##  License
Distributed under the **MIT License**. See `LICENSE` for more information.
