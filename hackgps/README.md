# HackGPS

## Premise

You are helping navigate a self driving car. However, due to a bug, the car randomly disobeyes some of your directions. Can you get to the destination in time?

## Puzzle

The set of roads is represented as a directed graph. The car starts at node `0`, and the goal is to reach node `n-1`, within `T` timesteps. At each timestep, 
the car expects you to direct it to one of the neighboring nodes reachable by an edge. However, with probability `p`, it will ignore your instruction and randomly
move to one of the adjacent nodes. 

Puzzlers can interact with the puzzle through a web interface, but the puzzle is intended to be solved through HTTP requests to our exposed endpoints.

## To Use

Run `build.sh`, and then serve the Flask app in `hackgps/`. `web/` stores source for the front end, and `src/` stores a solver.
