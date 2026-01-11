import random
import time

class Organism:
def init(self, x, y):
self.x, self.y = x, y
self.energy = 10
self.is_alive = True

text
def move(self, width, height):
    # Randomly move 1 step, but stay inside the world boundaries
    self.x = max(0, min(width - 1, self.x + random.choice([-1, 0, 1])))
    self.y = max(0, min(height - 1, self.y + random.choice([-1, 0, 1])))
    self.energy -= 1
    if self.energy <= 0:
        self.is_alive = False
class World:
def init(self, size, num_orgs):
self.size = size
self.population = [Organism(random.randint(0, size-1), random.randint(0, size-1)) for _ in range(num_orgs)]
self.food = [(random.randint(0, size-1), random.randint(0, size-1)) for _ in range(5)]

text
def update(self):
    # 1. Move everyone
    for org in self.population:
        if org.is_alive:
            org.move(self.size, self.size)
            
            # 2. Check for food
            if (org.x, org.y) in self.food:
                org.energy += 5
                self.food.remove((org.x, org.y))
                # Spawn new food elsewhere
                self.food.append((random.randint(0, self.size-1), random.randint(0, self.size-1)))
    
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
# --- RUNNING THE SIMULATION ---
my_world = World(size=10, num_orgs=3)

for day in range(10):
print(f"\n--- DAY {day} ---")
my_world.display()
my_world.update()
time.sleep(1) # Slows it down so you can watch
