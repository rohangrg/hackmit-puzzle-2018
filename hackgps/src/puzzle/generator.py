'''

Generates an imperfect, directed maze.

'''

import random
import json
import os

from . import lib

class Generator:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        # Set up graph folder
        if not os.path.exists(lib.DIR):
            os.makedirs(lib.DIR)
        self.filenum = len(next(os.walk(lib.DIR))[2])

    def run(self, num):
        '''Generates num random mazes.'''
        files = []
        for _ in range(num):
            files.append(self._generate())
        return files

    def _generate(self):
        '''Generates a random maze and writes it to file.'''
        adjLists = [[] for _ in range(self.width * self.height)]

        # Use Prim's to create MST
        added = set([0])
        boundary = self._borders(0)
        while len(added) < self.width * self.height:
            # Choose edge to add to MST
            toAdd = random.choice(boundary)
            while toAdd[1] in added:
                boundary.remove(toAdd)
                toAdd = random.choice(boundary)

            # Update
            adjLists[toAdd[0]].append(toAdd[1])
            added.add(toAdd[1])
            boundary.extend(self._borders(toAdd[1]))
            boundary.remove(toAdd)

        # Make the graph more connected
        # self._connect(adjLists)

        # Randomly add edges
        factor = 2.4
        for _ in range(round(factor * self.height * self.width)):
            node = random.randint(0, self.height * self.width - 1)
            nnode = random.choice(self._borders(node))[1]
            if nnode not in adjLists[node]:
                adjLists[node].append(nnode)

        
        # Write to file
        file_name = lib.filename(self.filenum)
        with open(os.path.join(lib.DIR, file_name), 'w') as output:
            toWrite = {
                'graph': adjLists,
                'mistake': random.uniform(0.3, 0.32),
                'time': int(round(2 * (self.width + self.height)))
            }
            json.dump(toWrite, output)
            self.filenum += 1
        
        return file_name

    def _connect(self, adjLists):
        visited = [False for _ in range(len(adjLists))]
        level = [0 for _ in range(len(adjLists))]
        reach = [0 for _ in range(len(adjLists))]
        parent = [-1 for _ in range(len(adjLists))]
        def dfs(node):
            if visited[node]:
                return
            visited[node] = True
            for n in adjLists[node]:
                level[n] = level[node] + 1
                parent[n] = node
                reach[n] = level[n]
                dfs(n)
                reach[node] = min(reach[node], reach[n])
            if node > 0 and reach[node] == level[node]:
                neighbors = [b[1] for b in self._borders(node) if level[b[1]] < level[node]]
                if len(neighbors) > 0:
                    n = min(neighbors, key = lambda v: level[v])
                    adjLists[node].append(n)
                    reach[node] = level[n]
        dfs(0)

    def _borders(self, node):
        '''Finds the edges coming from a node'''
        row = node // self.width
        col = node % self.width
        dr = [-1, 0, 1, 0]
        dc = [0, -1, 0, 1]
        ret = []
        for r,c in zip(dr, dc):
            if self._valid(row+r, col+c):
                nnode = (row+r)*self.width + (col+c)
                ret.append((node, nnode))
        return ret

    def _valid(self, row, col):
        '''Checks that node is valid.'''
        return (0 <= row < self.height) and (0 <= col < self.width)
