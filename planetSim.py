import pygame
import math
pygame.init()

#Window width and height coord
WIDTH, HEIGHT = 800, 800
#Surface
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
#Title of the Window
pygame.display.set_caption("Planet Simulation")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
DARK_GREY = (80, 78, 81)

FONT = pygame.font.SysFont("arial", 16)

class Planet:
    #Astronomical Units: aprox calculation of the distance between the planet and the sun
    #kilometers multiplied by 1000 because i want it in meters
    AU = 149.6e9
    G = 6.67428e-11
    SCALE = 200 / AU # 1AU = 100 pixels
    TIMESTEP = 3600 * 24 #3600 Number of seconds in an hour; 1 day

    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.orbit = []

        self.sun = False
        self.distance_to_sun = 0

        self.x_vel = 0
        self.y_vel = 0
        
    def draw(self, win):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2
        
        if len(self.orbit) >= 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x, y))

            pygame.draw.lines(win, self.color, False, updated_points, 2)

        if not self.sun:
            distance_text = FONT.render(f"{round(self.distance_to_sun/1000, 1)}km", 1, WHITE)
            win.blit(distance_text, (x - distance_text.get_width()/2, y - distance_text.get_width()/2))

        pygame.draw.circle(win, self.color, (x, y), self.radius)

    #Distance between two objects
    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

    #Determine if the object is a sun, if it is we store the distance
        if other.sun:
            self.distance_to_sun = distance

    #Calculate force of attraction: F = m/r^2 * g
        force = self.G * self.mass * other.mass / distance ** 2
        
        #We want to calculate the forces of the two axes so first we find the angle
        theta = math.atan2(distance_y, distance_x)

        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y

    #Loop through all the planets, calculate the force of attraction between the current planet and all the other planets
    #We then calculate what the velocity would be for these planets and then we move them 
    def update_position(self, planets):
        total_fx = total_fy = 0
        
        for planet in planets:
            if self == planet:
                continue

            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        # F = m * a
        # a = f / m

        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))

       
#pygame event loop
def main():
    run = True
    clock = pygame.time.Clock() #Clock so the framerate does not go past a certain number, syncs game

    sun = Planet(0, 0, 30, YELLOW, 1.98892 * 10**30)
    sun.sun = True

    earth = Planet(-1 * Planet.AU, 0, 16, BLUE, 5.9742 * 10**24)
    earth.y_vel = 29.783 * 1000

    mars = Planet(-1.524 * Planet.AU, 0, 12, RED, 6.39 * 10**23)
    mars.y_vel = 24.077 * 1000

    mercury = Planet(0.387 * Planet.AU, 0, 8, DARK_GREY, 0.330 * 10**23)
    mercury.y_vel = -47.4 * 1000

    venus = Planet(0.723 * Planet.AU, 0, 14, WHITE, 4.8685 * 10**24)
    venus.y_vel = -35.02 * 1000

#List of planets
    planets = [sun, earth, mars, mercury, venus]

    while run:
        #Going to run this loop a maximum of 60 times per second
        clock.tick(60)
        WIN.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
    
        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)
        
        pygame.display.update()

    pygame.quit()

main()
