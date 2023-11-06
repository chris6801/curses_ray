import curses, math

# Define the colors for the walls and floor/ceiling
WALL_COLOR = curses.COLOR_WHITE
FLOOR_COLOR = curses.COLOR_CYAN

#initialize the screen
screen = curses.initscr()

# Set up the colors
curses.start_color()
curses.init_pair(1, WALL_COLOR, curses.COLOR_BLACK)
curses.init_pair(2, FLOOR_COLOR, curses.COLOR_BLACK)

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
MAX_DEPTH = 10

# the tile map stores the map info as an array of 3 element arrays containing the (y_position, x_position, char)
def draw_map(map):
    for tile in map:
        screen.addch(tile[0], tile[1], tile[2])

def create_tile_map(map):
    tile_locations = []
    for row_index, row in enumerate(map):
        for col_index, char in enumerate(row):
            tile_location = [row_index, col_index, char]
            tile_locations.append(tile_location)
    return tile_locations
def draw_player():
    screen.addch(player_y, player_x, player_char)

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

#second render function
'''def render():
    screen.clear()
    screen_height, screen_width = screen.getmaxyx()

    for x in range(screen_width):
        angle = player_angle + math.atan((x - screen_width / 2) / screen_width / 2)
        distance = cast_ray(angle)
        wall_height = min(int(screen_height / distance), screen_height)

        # Draw the wall
        screen.attron(curses.color_pair(1))
        for y in range(wall_height):
            screen.addstr(y, x, '#')
        screen.attroff(curses.color_pair(1))

        # Draw the floor/ceiling
        screen.attron(curses.color_pair(2))
        for y in range(wall_height, screen_height):
            screen.addstr(y, x, ' ')
        screen.attroff(curses.color_pair(2))
'''

def main():   
    running = True

    tile_map = create_tile_map(MAP_DATA)

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
    
    # prints the coordinates of each wall tile, notated from the top left as a (y, x) pair.
    for row_index, row in enumerate(MAP_DATA):
        for col_index, col in enumerate(row):
            if col == '#':
                print(row_index, col_index)
    
    #print(tile_map)
    #print(list_of_ats)

    for tile in tile_map:
        print(tile[2])

main()