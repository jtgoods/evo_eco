import random
import time
import os

class Organism:
    def __init__(self, x, y, metabolism = None):
        self.x, self.y = x, y
        self.energy = 19 # starting energy
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
    
# --- RUNNING THE SIMULATION ---
my_world = World(size=10, num_orgs=3)

for day in range(50):
    print(f"\n--- DAY {day} ---")
    # In your display method or run loop:
    avg_met = my_world.get_avg_metabolism()
    print(f"Population: {len(my_world.population)} | Avg Metabolism: {avg_met:.3f}")
    os.system('cls' if os.name == 'nt' else 'clear') 
    my_world.display()
    my_world.update()
    time.sleep(1) # Slows it down so you can watch
