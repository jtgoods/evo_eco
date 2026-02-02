import random
import time
import os
import matplotlib.pyplot as plt

class Organism:
    def __init__(self, x, y, metabolism = None):
        self.x, self.y = x, y
        self.energy = 33 # starting energy
        self.is_alive = True

        # If no metabolism is passed (Day 0), pick a random one
        # Otherwise, inherit from parent
        if metabolism is None:
            self.metabolism = random.uniform(0.8, 1.2)
        else:
            # INHERITANCE + MUTATION
            # The child's metabolism is the parent's +/- 10%
            mutation = random.uniform(0.9, 1.1)
            self.metabolism = metabolism * mutation

    def move(self, width, height):
        # Randomly move 1 step, but stay inside the world boundaries
        self.x = max(0, min(width - 1, self.x + random.choice([-1, 0, 1])))
        self.y = max(0, min(height - 1, self.y + random.choice([-1, 0, 1])))
        self.energy -= 1
        if self.energy <= 0:
            self.is_alive = False

    def reproduce(self):
        # Only reproduce if energy is high enough, and two fauna "collide"
        if self.energy > 30:
            self.energy /= 2  # Give half energy to offspring
            # Return a new Organism at the same location
            return Organism(self.x, self.y, self.metabolism)
        return None

class World:
    def __init__(self, size, num_orgs):
        self.size = size
        self.population = [Organism(random.randint(0, size-1), random.randint(0, size-1)) for _ in range(num_orgs)]
        self.food = [(random.randint(0, size-1), random.randint(0, size-1)) for _ in range(5)]

    def update(self):
        # 1. Move everyone
        newborns = []
        for org in self.population:
            if org.is_alive:
                org.move(self.size, self.size)
                
                # 2. Check for food
                if (org.x, org.y) in self.food:
                    org.energy += 10
                    self.food.remove((org.x, org.y))
                    # Spawn new food elsewhere
                    self.food.append((random.randint(0, self.size-1), random.randint(0, self.size-1)))
                # REPRODUCTION CHECK
                child = org.reproduce()
                if child:
                    newborns.append(child)
        
        # Add the newborns to the population
        self.population.extend(newborns)

        # 3. Remove the dead
        self.population = [o for o in self.population if o.is_alive]
        
        # Add a 10% chance of a new plant appearing every day
        if random.random() < 0.10:
            self.food.append((random.randint(0, self.size-1), random.randint(0, self.size-1)))

    def display(self):
        # Create a blank grid
        grid = [["." for _ in range(self.size)] for _ in range(self.size)]
        # Add food
        for f in self.food: grid[f[1]][f[0]] = "f"
        # Add organisms
        for o in self.population: grid[o.y][o.x] = "O"
        
        for row in grid:
            print(" ".join(row))
        print(f"Population: {len(self.population)} | Food: {len(self.food)}")
    
    def get_avg_metabolism(self):
        if not self.population:
            return 0
        total = sum(o.metabolism for o in self.population)
        return total / len(self.population)

history = {
    'days': [],           # [0, 1, 2, 3, ...]
    'population': [],     # [3, 4, 5, 6, 4, ...]
    'food': [],          # [5, 6, 5, 7, ...]
    'avg_metabolism': [] # [1.0, 0.98, 1.02, ...]
}


# --- RUNNING THE SIMULATION ---
my_world = World(size=10, num_orgs=3)

for day in range(50):
    print(f"\n--- DAY {day} ---")
    avg_met = my_world.get_avg_metabolism()
    print(f"Population: {len(my_world.population)} | Avg Metabolism: {avg_met:.3f}")
    
    os.system('cls' if os.name == 'nt' else 'clear') 
    my_world.display()
    
    history['days'].append(day)
    history['population'].append(len(my_world.population))
    history['food'].append(len(my_world.food))
    history['avg_metabolism'].append(avg_met)
    
    my_world.update()
    time.sleep(1) # Slows it down so you can watch

plt.figure(figsize=(12, 5))

# Left graph: Population and Food over time
plt.subplot(1, 2, 1)
plt.plot(history['days'], history['population'], label='Population', color='blue')
plt.plot(history['days'], history['food'], label='Food', color='green')
plt.xlabel('Days')
plt.ylabel('Count')
plt.title('Population Dynamics')
plt.legend()
plt.grid(True, alpha=0.3)

# Right graph: Metabolism evolution over time
plt.subplot(1, 2, 2)
plt.plot(history['days'], history['avg_metabolism'], label='Avg Metabolism', color='red')
plt.xlabel('Days')
plt.ylabel('Metabolism')
plt.title('Metabolic Evolution')
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('evo_eco_results.png', dpi=150)
plt.show()
