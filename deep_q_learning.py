import numpy


population_d = 70


#Rewards
def take_step(boat, action, environment_grid, avg_population):
    if action == 0:
        if boat.move_up():
            return -5
        return -100
    elif action == 1:
        if boat.move_down():
            return -1
        return -100
    elif action == 2:
        if boat.move_left():
            return -1.5
        return -100
    elif action == 3:
        if boat.move_right():
            return -1.5
        return -100
    elif action == 4:
        fish_population = environment_grid[boat.pos[1]][boat.pos[0]].fish_population
        if fish_population < avg_population:
            return -1*fish_population/population_d
        return fish_population/population_d



