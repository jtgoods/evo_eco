"""
Ocean-to-Land Evolution Simulator

An immersive evolutionary simulation recreating life's journey from primordial
oceans to terrestrial ecosystems. Watch organisms evolve air breathing, land
mobility, desiccation resistance, and photosynthesis as they transition from
sea to land over hundreds of generations.

Original Creator: JT Goodman
Ocean-to-Land Evolution Enhancement: Gh0st-La6z-exe
With AI assistance from Claude Sonnet
"""

import random
import time
import os

# Simulation Configuration
WORLD_WIDTH = 15           # Width of the evolutionary world
WORLD_HEIGHT = 10          # Height of the evolutionary world  
MAX_OCEAN_DEPTH = 4        # Maximum depth in ocean zones
INITIAL_POPULATION = 8     # Starting number of organisms
SIMULATION_DAYS = 300      # Total days to run simulation
UPDATE_SPEED = 1.2         # Seconds between updates (lower = faster)

# Evolution Parameters
MUTATION_RATE = 0.02       # Chance for major trait mutations (2%)
LAND_MUTATION_BIAS = 0.1   # Bias toward developing land traits
REPRODUCTION_AGE = 5       # Minimum age before reproduction
ENERGY_REPRODUCTION_COST = 0.6  # Fraction of energy lost when reproducing

class EvolvingOrganism:
    def __init__(self, x, y, depth, parent=None):
        self.x, self.y, self.depth = x, y, depth
        self.energy = 15
        self.is_alive = True
        self.age = 0
        
        # Core evolutionary traits
        if parent is None:  # First generation - primordial soup
            self.metabolism_rate = random.uniform(0.5, 1.5)
            self.size = random.uniform(0.1, 0.3)
            self.chemical_affinity = random.choice(['methane', 'sulfur', 'ammonia'])
            self.heat_tolerance = random.uniform(0.3, 0.8)
            self.depth_preference = random.uniform(0.0, 1.0)
            
            # NEW: Land evolution traits (start at 0)
            self.air_breathing = 0.0      # 0=water only, 1=can breathe air
            self.land_mobility = 0.0      # 0=water only, 1=can move on land  
            self.desiccation_resistance = 0.0  # 0=dies on land, 1=survives drying
            self.photosynthesis = 0.0     # 0=chemotroph, 1=can photosynthesize
        else:  # Inherited with evolutionary pressure
            # Existing traits with mutation
            self.metabolism_rate = max(0.1, parent.metabolism_rate * random.uniform(0.9, 1.1))
            self.size = max(0.05, parent.size * random.uniform(0.95, 1.05))
            self.heat_tolerance = max(0.0, min(1.0, parent.heat_tolerance + random.uniform(-0.1, 0.1)))
            self.depth_preference = max(0.0, min(1.0, parent.depth_preference + random.uniform(-0.1, 0.1)))
            
            # LAND ADAPTATION EVOLUTION - gradual mutations toward land capability
            self.air_breathing = max(0.0, min(1.0, parent.air_breathing + random.uniform(-0.05, LAND_MUTATION_BIAS)))
            self.land_mobility = max(0.0, min(1.0, parent.land_mobility + random.uniform(-0.05, LAND_MUTATION_BIAS)))
            self.desiccation_resistance = max(0.0, min(1.0, parent.desiccation_resistance + random.uniform(-0.05, LAND_MUTATION_BIAS)))
            self.photosynthesis = max(0.0, min(1.0, parent.photosynthesis + random.uniform(-0.02, 0.08)))
            
            # Chemical affinity can evolve
            if random.random() < MUTATION_RATE:
                self.chemical_affinity = random.choice(['methane', 'sulfur', 'ammonia', 'organic_matter'])
            else:
                self.chemical_affinity = parent.chemical_affinity
    def get_evolutionary_stage(self):
        """Determine what evolutionary stage this organism represents"""
        land_traits = self.air_breathing + self.land_mobility + self.desiccation_resistance
        
        if land_traits < 0.3:
            return "Primordial"
        elif land_traits < 0.8:
            return "Tidal"
        elif land_traits < 1.5:
            return "Amphibious"
        else:
            return "Terrestrial"
    
    def can_survive_on_land(self):
        """Check if organism can survive on land"""
        return (self.air_breathing > 0.3 and 
                self.desiccation_resistance > 0.2 and 
                self.land_mobility > 0.1)

    def move(self, world):
        """Movement through ocean and onto land as evolution progresses"""
        # Attempt to move to land if capable
        current_tile = world.get_tile_type(self.x, self.y)
        
        # Random movement
        new_x = max(0, min(world.width - 1, self.x + random.choice([-1, 0, 1])))
        new_y = max(0, min(world.height - 1, self.y + random.choice([-1, 0, 1])))
        target_tile = world.get_tile_type(new_x, new_y)
        
        # Check if movement is possible
        can_move = True
        if target_tile == 'land' and not self.can_survive_on_land():
            can_move = False  # Can't go on land yet
        elif target_tile == 'tidal' and self.air_breathing < 0.1:
            can_move = False  # Need some air breathing for tidal zones
            
        if can_move:
            self.x, self.y = new_x, new_y
            # Reset depth if moving to land
            if target_tile == 'land':
                self.depth = 0
        
        # Vertical movement in water
        if target_tile in ['ocean', 'tidal'] and random.random() < 0.3:
            if self.depth_preference > 0.6:
                self.depth = min(world.max_depth - 1, self.depth + random.choice([0, 1]))
            elif self.depth_preference < 0.4:
                self.depth = max(0, self.depth + random.choice([-1, 0]))
            else:
                self.depth = max(0, min(world.max_depth - 1, self.depth + random.choice([-1, 0, 1])))
        
        # Energy costs
        self.age += 1
        energy_cost = self.metabolism_rate
        
        # Land movement costs more energy initially
        if world.get_tile_type(self.x, self.y) == 'land':
            energy_cost *= (2.0 - self.land_mobility)  # Less cost as land mobility improves
            
        self.energy -= energy_cost
        
        # Death conditions
        if self.energy <= 0:
            self.is_alive = False
        # Die on land without proper adaptations
        elif world.get_tile_type(self.x, self.y) == 'land' and not self.can_survive_on_land():
            self.is_alive = False
    
    def feed(self, world):
        """Consume resources from environment - ocean chemicals or land organics"""
        tile_type = world.get_tile_type(self.x, self.y)
        
        if tile_type == 'land':
            # Land feeding: organic matter and photosynthesis
            if self.photosynthesis > 0.1:  # Can photosynthesize
                light_energy = 3 * self.photosynthesis  # Abundant energy from sun
                self.energy += light_energy
            
            if self.chemical_affinity == 'organic_matter':
                # Feed on dead organic material on land
                self.energy += random.uniform(1, 3)
                
        else:  # Ocean or tidal feeding
            current_cell = None
            if tile_type == 'ocean':
                current_cell = world.get_ocean_cell(self.x, self.y, self.depth)
            elif tile_type == 'tidal':  # tidal
                current_cell = world.get_ocean_cell(self.x, self.y, 0)  # Shallow tidal water
            
            if current_cell and current_cell['chemicals']:
                chemical_level = current_cell['chemicals'].get(self.chemical_affinity, 0)
                
                if chemical_level > 0:
                    consumption = min(chemical_level, self.size * 3)
                    self.energy += consumption * 2
                    world.consume_chemical(self.x, self.y, self.depth, self.chemical_affinity, consumption)
    
    def can_reproduce(self):
        """Check if organism has enough energy to reproduce"""
        reproduction_threshold = 20 + (self.size * 30)  # Larger organisms need more energy
        return self.energy > reproduction_threshold and self.age > REPRODUCTION_AGE
    
    def reproduce(self):
        """Create offspring with inherited traits + land evolution pressure"""
        if self.can_reproduce():
            self.energy *= ENERGY_REPRODUCTION_COST
            return EvolvingOrganism(self.x, self.y, self.depth, parent=self)
        return None

class EvolutionaryWorld:
    def __init__(self, width=WORLD_WIDTH, height=WORLD_HEIGHT, max_depth=MAX_OCEAN_DEPTH, num_orgs=INITIAL_POPULATION):
        self.width, self.height, self.max_depth = width, height, max_depth
        self.day = 0
        
        # Create world geography: ocean -> tidal -> land
        self.terrain = []
        for x in range(width):
            column = []
            for y in range(height):
                # Create realistic coastline: left=ocean, middle=tidal, right=land
                if x < width * 0.4:  # 40% ocean
                    terrain_type = 'ocean'
                elif x < width * 0.6:  # 20% tidal zones  
                    terrain_type = 'tidal'
                else:  # 40% land
                    terrain_type = 'land'
                column.append(terrain_type)
            self.terrain.append(column)
        
        # Create ocean chemistry grid (only for water areas)
        self.ocean_grid = []
        for x in range(width):
            column = []
            for y in range(height):
                if self.terrain[x][y] in ['ocean', 'tidal']:
                    depth_layers = []
                    for d in range(max_depth if self.terrain[x][y] == 'ocean' else 1):
                        cell = {
                            'temperature': self.get_base_temperature(d),
                            'chemicals': {
                                'methane': random.uniform(2, 8),
                                'sulfur': random.uniform(1, 6), 
                                'ammonia': random.uniform(1, 5),
                                'organic_matter': random.uniform(0, 2)
                            }
                        }
                        depth_layers.append(cell)
                    column.append(depth_layers)
                else:  # Land - no ocean chemistry
                    column.append([])
            self.ocean_grid.append(column)
        
        # Create initial population in ocean
        self.population = []
        for _ in range(num_orgs):
            # Start all organisms in ocean
            x = random.randint(0, int(width * 0.4) - 1)
            y = random.randint(0, height - 1) 
            depth = random.randint(0, max_depth - 1)
            self.population.append(EvolvingOrganism(x, y, depth))
    
    def get_base_temperature(self, depth):
        return 20 + (depth * 15)
    
    def get_tile_type(self, x, y):
        return self.terrain[x][y]
    
    def get_ocean_cell(self, x, y, depth):
        if self.terrain[x][y] in ['ocean', 'tidal'] and self.ocean_grid[x][y]:
            depth = min(depth, len(self.ocean_grid[x][y]) - 1)
            return self.ocean_grid[x][y][depth]
        return None

    def consume_chemical(self, x, y, depth, chemical_type, amount):
        """Organism consumes chemicals from ocean environment"""
        if self.terrain[x][y] in ['ocean', 'tidal'] and self.ocean_grid[x][y]:
            depth = min(depth, len(self.ocean_grid[x][y]) - 1)
            cell = self.ocean_grid[x][y][depth]
            current = cell['chemicals'].get(chemical_type, 0)
            cell['chemicals'][chemical_type] = max(0, current - amount)
    
    def regenerate_environment(self):
        """Environmental processes: ocean chemistry + land organics"""
        # Ocean chemical regeneration
        for x in range(self.width):
            for y in range(self.height):
                if self.terrain[x][y] in ['ocean', 'tidal'] and self.ocean_grid[x][y]:
                    for depth_layer in self.ocean_grid[x][y]:
                        depth = self.ocean_grid[x][y].index(depth_layer)
                        
                        # Thermal vents produce chemicals
                        if depth >= 2:
                            depth_layer['chemicals']['sulfur'] += random.uniform(0.5, 2.0)
                            depth_layer['chemicals']['methane'] += random.uniform(0.3, 1.5)
                        
                        # Surface gets atmospheric input  
                        if depth == 0:
                            depth_layer['chemicals']['ammonia'] += random.uniform(0.2, 1.0)
                            depth_layer['chemicals']['methane'] += random.uniform(0.1, 0.8)
                        
                        # Organic matter background production and from dead organisms
                        # Always have a small baseline so early organic_matter feeders aren't starved
                        depth_layer['chemicals']['organic_matter'] += random.uniform(0.02, 0.1)
                        if len(self.population) > 5:  # Additional input when life is established
                            depth_layer['chemicals']['organic_matter'] += random.uniform(0.1, 0.5)
                        
                        # Cap concentrations
                        for chem in depth_layer['chemicals']:
                            depth_layer['chemicals'][chem] = min(12, depth_layer['chemicals'][chem])
    
    def update(self):
        """Advance one day in evolutionary world"""
        self.day += 1
        newborns = []
        
        # Organism life cycle
        for org in self.population:
            if org.is_alive:
                org.move(self)
                org.feed(self)
                
                # Reproduction
                child = org.reproduce()
                if child:
                    newborns.append(child)
        
        # Add offspring
        self.population.extend(newborns)
        
        # Remove dead organisms
        self.population = [org for org in self.population if org.is_alive]
        
        # Environmental regeneration
        if self.day % 3 == 0:
            self.regenerate_environment()
    
    def get_evolution_stats(self):
        """Get current evolutionary progress statistics"""
        if not self.population:
            return {}
        
        # Count organisms by evolutionary stage
        stages = {'Primordial': 0, 'Tidal': 0, 'Amphibious': 0, 'Terrestrial': 0}
        land_count = 0
        
        total_air = total_land_mob = total_photo = 0
        
        for org in self.population:
            stages[org.get_evolutionary_stage()] += 1
            if self.get_tile_type(org.x, org.y) == 'land':
                land_count += 1
            
            total_air += org.air_breathing
            total_land_mob += org.land_mobility  
            total_photo += org.photosynthesis
        
        pop_size = len(self.population)
        return {
            'population': pop_size,
            'land_population': land_count,
            'stages': stages,
            'avg_air_breathing': total_air / pop_size,
            'avg_land_mobility': total_land_mob / pop_size,
            'avg_photosynthesis': total_photo / pop_size
        }

    def display(self):
        """Display evolutionary world with ocean to land progression"""
        stats = self.get_evolution_stats()
        
        print(f"\n🌍 EVOLUTIONARY WORLD - Day {self.day} 🌍")
        if stats:
            print(f"Population: {stats['population']} | On Land: {stats['land_population']}")
            print(f"Evolutionary Stages - Primordial: {stats['stages']['Primordial']}, Tidal: {stats['stages']['Tidal']}, Amphibious: {stats['stages']['Amphibious']}, Terrestrial: {stats['stages']['Terrestrial']}")
            print(f"Air Breathing: {stats['avg_air_breathing']:.3f} | Land Mobility: {stats['avg_land_mobility']:.3f} | Photosynthesis: {stats['avg_photosynthesis']:.3f}")
        else:
            print("Population: 0 - EXTINCTION!")
        
        # Create world display
        print("\n🗺️  WORLD MAP:")
        display_grid = []
        
        for y in range(self.height):
            row = []
            for x in range(self.width):
                # Base terrain
                if self.terrain[x][y] == 'ocean':
                    cell = "~"  # Ocean
                elif self.terrain[x][y] == 'tidal':
                    cell = "≈"  # Tidal zone
                else:
                    cell = "▓"  # Land
                
                # Add organisms
                for org in self.population:
                    if org.x == x and org.y == y:
                        stage = org.get_evolutionary_stage()
                        if stage == "Primordial":
                            cell = "○"  # Basic life
                        elif stage == "Tidal":
                            cell = "◐"  # Tidal adapted
                        elif stage == "Amphibious":
                            cell = "●"  # Amphibious
                        else:  # Terrestrial
                            cell = "◆"  # Land life
                        break
                
                row.append(cell)
            display_grid.append(row)
        
        for row in display_grid:
            print(" ".join(row))
        
        print("\nLegend: ~ Ocean | ≈ Tidal | ▓ Land | ○ Primordial | ◐ Tidal-Adapted | ● Amphibious | ◆ Terrestrial")
    
# --- OCEAN TO LAND EVOLUTION SIMULATION ---
my_world = EvolutionaryWorld()

print("🧬 Welcome to the Ocean-to-Land Evolution Simulator! 🧬")
print("Watch life evolve from primordial oceans to terrestrial ecosystems!\n")
print("Organisms will gradually develop land adaptations:")
print("• Air breathing capability")
print("• Land mobility")
print("• Desiccation resistance")
print("• Photosynthesis")
print("\nPress Ctrl+C to stop the simulation.\n")
time.sleep(4)

try:
    for day in range(SIMULATION_DAYS):
        os.system('cls' if os.name == 'nt' else 'clear')
        my_world.display()
        
        # Check for extinction
        if len(my_world.population) == 0:
            print("\n💀 MASS EXTINCTION - All life has perished!")
            break
        
        # Evolutionary milestone announcements
        stats = my_world.get_evolution_stats()
        if stats:
            if day == 50 and stats['avg_air_breathing'] > 0.1:
                print("\n🫁 BREAKTHROUGH: First organisms developing air breathing!")
            elif day == 100 and stats['land_population'] > 0:
                print("\n🌿 HISTORIC MOMENT: First life colonizes land!")
            elif stats['avg_photosynthesis'] > 0.3:
                print("\n☀️ PHOTOSYNTHESIS EVOLUTION: Solar-powered life emerges!")
            elif stats['stages']['Terrestrial'] > 5:
                print("\n🦕 TERRESTRIAL DOMINANCE: Complex land ecosystems forming!")
        
        my_world.update()
        time.sleep(UPDATE_SPEED)  # Use configuration constant
        
except KeyboardInterrupt:
    print("\n\n🔬 Evolution simulation concluded!")
    if my_world.population:
        final_stats = my_world.get_evolution_stats()
        print(f"Final population: {final_stats['population']} organisms")
        print(f"Land colonizers: {final_stats['land_population']}")
        print("The journey from ocean to land continues...")
    else:
        print("Evolution ended in extinction.")
