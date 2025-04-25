from Traversals import bfs_path
import heapq
from collections import deque
from Simulator import Simulator
import sys
class Solution:

    def __init__(self, problem, isp, graph, info):
        self.problem = problem
        self.isp = isp
        self.graph = graph
        self.info = info

    def output_paths(self):
        """
        This method must be filled in by you. You may add other methods and subclasses as you see fit,
        but they must remain within the Solution class.
        """
        paths, bandwidths, priorities = {}, {}, {}

        # Compute shortest paths and paths from neighbors
        shortestPaths = bfs_path(self.graph, self.isp, self.info["list_clients"])
        tableForPaths = {neighbor: self.output_pathBFS(neighbor) for neighbor in self.graph[self.isp]}
        nodeCapacity = {node: 0 for node in self.graph[self.isp]}

        # Sort neighbors by bandwidth
        sortedNeighbors = sorted(
            self.graph[self.isp], key=lambda n: self.info["bandwidths"][n], reverse=True
        )

        # Assign paths to clients
        for client in self.info["list_clients"]:
            for neighbor in sortedNeighbors:
                if nodeCapacity[neighbor] < self.info["bandwidths"][neighbor] and client in tableForPaths[neighbor]:
                    paths[client] = tableForPaths[neighbor][client]
                    nodeCapacity[neighbor] += 1
                    break
            else:
                paths[client] = shortestPaths[client]  # Fallback to shortest path

        # Adjust bandwidths for specific nodes
        bandwidths = {node: self.info["bandwidths"][node] for node in self.graph}
        for fln in self.graph[self.isp]:
            bandwidths[fln] *= 5  # Scale bandwidth by 5 for ISP neighbors

        # Assign priorities based on client processing order
        priorities = {client: idx for idx, client in enumerate(self.info["list_clients"], start=1)}
        
        #DO NOT MODIFY THE LINE BELOW, OR BAD THINGS WILL HAPPEN
        return (paths, bandwidths, priorities)
    
    def output_pathBFS(self, start):
        visited = {}
        paths = {}
        queue = deque([start])
        for node in self.graph:
            visited[node] = False
        for neighbor in self.graph[self.isp]:
            visited[neighbor] = True
        visited[self.isp] = True
        paths[start] = [self.isp, start]
        while queue:
            curr = queue.popleft()
            for neighbor in self.graph[curr]:
                if not visited[neighbor]:
                    queue.append(neighbor)
                    visited[neighbor] = True
                    paths[neighbor] = paths[curr] + [neighbor]
        return paths