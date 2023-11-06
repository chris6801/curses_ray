import curses, math

#initialize the screen
screen = curses.initscr()

MAP_WIDTH = 20
MAP_HEIGHT = 20
MAP_SIZE = MAP_HEIGHT * MAP_WIDTH
TILE_SIZE = 32

SCREEN_HEIGHT, SCREEN_WIDTH = screen.getmaxyx()

MAP_DATA = ['####################', 
            '#                  #',
            '#                  #',
            '#                  #',
            '#                  #',
            '#                  #',
            '#                  #',
            '#                  #',
            '#                  #',
            '#                  #',
            '#                  #',
            '#                  #',
            '#                  #',
            '#                  #',
            '#           ###    #',
            '#                  #',
            '#                  #',
            '#                  #',
            '#                  #',
            '####################']

#reverse map
MAP_DATA = list(reversed(MAP_DATA))

#define player starting point


#player global variables
player_char = '@'
player_x = 7.0
player_y = 7.0 
player_angle = 1.55

#Field of View, expressed in radians
FOV = 3.1415 / 4

#raycasting constants
STEP_ANGLE = FOV/SCREEN_WIDTH

#raycasting algorithm
def cast_ray(angle):
    step_size = 1
    x, y = player_x, player_y
    dx, dy = math.cos(angle), math.sin(angle)
    distance = 0.01
    while True:
        x += dx * step_size
        y += dy * step_size
        distance += step_size
        if MAP_DATA[int(x)][int(y)] == '#':
            return distance * math.cos(player_angle - angle)
#render
def render():
    start_angle = player_angle - FOV/2
    angle = start_angle
    for i in range(SCREEN_WIDTH):
        distance = cast_ray(angle)
        line_height = min(int(MAP_HEIGHT / distance), SCREEN_HEIGHT)
        screen.vline(int((SCREEN_HEIGHT / 2) - line_height / 2), i, 'x', line_height) 
        angle += STEP_ANGLE        

def main():   
    running = True

    while(running):
        
        #get player input 
        global player_x
        global player_y
        global player_angle
    
        screen.nodelay(1)
        input = screen.getch()

        #movement
        if input == ord('4'):
            player_x += math.cos(player_angle - math.pi/4)
        elif input == ord('6'):
            player_x += math.cos(player_angle + math.pi/4)
        elif input == ord('8'):
            player_x += math.cos(player_angle)
            player_y += math.sin(player_angle)
        elif input == ord('2'):
            player_x -= math.cos(player_angle)
            player_y -= math.sin(player_angle)
            
        #rotate FOV
        elif input == ord ('a'):
            player_angle -= math.pi/20
        elif input == ord('d'):
            player_angle += math.pi/20
            
        #quit
        elif input == ord('q'):
            running = False

        #check collisions with wall
        if player_x < 0:
            player_x = 0
        if player_x > MAP_WIDTH:
            player_x = MAP_WIDTH
        if player_y < 0:
            player_y = 0
        if player_y > MAP_HEIGHT:
            player_y = MAP_HEIGHT

        screen.clear()

        render()
        
        screen.refresh()
        curses.napms(20)
    
    #curses.endwin()

main()