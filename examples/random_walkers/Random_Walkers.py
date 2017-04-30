import random
import math

from mesa import Agent, Model
from mesa.space import ContinuousSpace
from mesa.time import RandomActivation


class Walker(Agent):

	def __init__(self, unique_id, model, pos, speed=5, heading=None):
		super().__init__(unique_id, model)
		if heading is None:
			heading = random.random() * 2 * math.pi
		self.heading = heading
		self.speed = speed

	def step(self):
		if random.random() < self.model.p_reorient:
			self.heading = random.random() * 2 * math.pi
		dx = self.speed * math.cos(self.heading)
		dy = self.speed * math.sin(self.heading)
		new_x = self.pos[0] + dx
		new_y = self.pos[1] + dy
		self.model.space.move_agent(self, (new_x, new_y))

class SpaceTest(Model):

	def __init__(self, N, width, height, p_reorient=0.25):
		self.N = N
		self.width = width
		self.height = height
		self.p_reorient = 0.25
		self.schedule = RandomActivation(self)
		self.space = ContinuousSpace(width, height, True, grid_width=10, grid_height=10)
		self.make_agents()
		self.running = True

	def make_agents(self):
		for i in range(self.N):
			x = random.random() * self.width
			y = random.random() * self.height
			pos = (x,y)
			agent = Walker(i, self, pos)
			self.space.place_agent(agent, pos)
			self.schedule.add(agent)

	def step(self):
		self.schedule.step()

