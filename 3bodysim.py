import pygame
import math
import random
# pygame setup
pygame.init()
width, height = 1280, 720
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Gravity Simulation")
clock = pygame.time.Clock()
running = True
dt = 0
MIDNIGHT_BLUE = (25, 25, 112)
MAX_TRAJ_POINTS = 500

pos1 = (width/2 - 100, height/2)
velocity1 = (15, 20) 
mass1 = 200
radius1 = 15
color1 = (255, 200, 100)
traj_list1 = []

# BODY 2
pos2 = (width/2 + 100, height/2)
velocity2 = (-25, -10)
mass2 = 200
radius2 = 15
color2 = (100, 150, 255)
traj_list2 = []

# BODY 3
pos3 = (width/2, height/2 - 150)
velocity3 = (30, -10) 
mass3 = 150
radius3 = 8
color3 = (200, 255, 150)
traj_list3 = []

def update_pos(pos, velocity):
    posx = pos[0] + velocity[0] * dt
    posy = pos[1] + velocity[1] * dt
    return (posx, posy)

def calculate_Force(pos1, pos2, mass1, mass2):
    r_x = pos2[0] - pos1[0]
    r_y = pos2[1] - pos1[1]
    r = math.sqrt(r_x ** 2 + r_y ** 2)
   
    G = 500
    if r < 1:
        r = 1
   
    F = G * mass1 * mass2 / (r ** 2)
    unit_vector_x = r_x / r
    unit_vector_y = r_y / r
    force_x = F * unit_vector_x
    force_y = F * unit_vector_y
    return force_x, force_y

def calculate_velocity(velocity, mass, forces):
    total_force_x = sum(f[0] for f in forces)
    total_force_y = sum(f[1] for f in forces)
    acceleration_x = total_force_x / mass
    acceleration_y = total_force_y / mass
    velocity = (velocity[0] + acceleration_x * dt, velocity[1] + acceleration_y * dt)
    return velocity

stars = []
for i in range(100):
    x = pygame.math.Vector2(
        pygame.math.Vector2(
            random.randint(0, width),
            random.randint(0, height)
        )
    )
    stars.append(x)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
   
    screen.fill(MIDNIGHT_BLUE)
    
    for star in stars:
        pygame.draw.circle(screen, (255, 255, 255), (int(star.x), int(star.y)), 1)
   
    for pos in traj_list1:
        pygame.draw.circle(screen, color1, pos, 1)
    for pos in traj_list2:
        pygame.draw.circle(screen, color2, pos, 1)
    for pos in traj_list3:
        pygame.draw.circle(screen, color3, pos, 1)
    
    pygame.draw.circle(screen, color1, pos1, radius1)
    pygame.draw.circle(screen, color2, pos2, radius2)
    pygame.draw.circle(screen, color3, pos3, radius3)
   
    traj_list1.append((int(pos1[0]), int(pos1[1])))
    traj_list2.append((int(pos2[0]), int(pos2[1])))
    traj_list3.append((int(pos3[0]), int(pos3[1])))
   
    if len(traj_list1) > MAX_TRAJ_POINTS:
        traj_list1.pop(0)
    if len(traj_list2) > MAX_TRAJ_POINTS:
        traj_list2.pop(0)
    if len(traj_list3) > MAX_TRAJ_POINTS:
        traj_list3.pop(0)
   
    force1_2 = calculate_Force(pos1, pos2, mass1, mass2)
    force1_3 = calculate_Force(pos1, pos3, mass1, mass3)
    force2_3 = calculate_Force(pos2, pos3, mass2, mass3)
    
    forces1 = (force1_2, force1_3)
    forces2 = ((-force1_2[0], -force1_2[1]), force2_3)
    forces3 = ((-force1_3[0], -force1_3[1]), (-force2_3[0], -force2_3[1]))
    
    velocity1 = calculate_velocity(velocity1, mass1, forces1)
    velocity2 = calculate_velocity(velocity2, mass2, forces2)
    velocity3 = calculate_velocity(velocity3, mass3, forces3)
   
    pos1 = update_pos(pos1, velocity1)
    pos2 = update_pos(pos2, velocity2)
    pos3 = update_pos(pos3, velocity3)
   
    fps = int(clock.get_fps())
    font = pygame.font.SysFont('Arial', 18)
    fps_text = font.render(f'FPS: {fps}', True, (255, 255, 255))
    screen.blit(fps_text, (10, 10))
    
    pygame.display.flip()
    dt = min(clock.tick(60) / 1000, 0.1)
pygame.quit()