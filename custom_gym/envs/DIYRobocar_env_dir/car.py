from envs.DIYRobocar_env_dir.geometry import Point, Line
from math import cos, sin, radians

class Car:
	def __init__(self):
		self.size = (381, 824)
		# self.size = (190.5, 412.0)
		self.Color = (0,0,0)
		self.Rect = None
		self.Image = './envs/DIYRobocar_env_dir/Media/car_sprite.png'
		self.Sprite = None
		self.X = 200
		self.Y = 550
		self.Theta = 0
		self.Steer = 0
		self.Throttle = 0
		self.LeftWheel = None		#NW, SW, NE, SE
		self.RightWheel = None
		self.Reward = 0


		self.min_throttle = -8.0
		self.max_throttle = 8.0
		self.min_steer = -8.0
		self.max_steer = 8.0

	def Scale(self, scale):
		self.size = (int(self.size[0]*scale), int(self.size[1]*scale))

	def drive(self, throttle_change, steer_change):
		self.Steer += steer_change
		self.Throttle += throttle_change

		if self.Steer > self.max_steer:
			self.Steer = self.max_steer
		elif self.Steer < self.min_steer:
			self.Steer = self.min_steer

		if self.Throttle > self.max_throttle:
			self.Throttle = self.max_throttle
		elif self.Throttle < self.min_throttle:
			self.Throttle = self.min_throttle

		if(self.Throttle !=0):
			self.Theta += self.Steer
			self.X -= -self.Throttle*sin(radians(self.Theta))
			self.Y += -self.Throttle*cos(radians(self.Theta))
			if(self.Theta>360):
				self.Theta -=360
			if(self.Theta<0):
				self.Theta+=360

	def checkIntersect(self, Line):
		for L in self.Lines:
			if (L.intersects(Line)==True):
				return True
		return False
	def getTransform(self, ptX, ptY, centerX, centerY, angle):
		#APPLY ROTATION
		x1 = ptX * cos(radians(angle))-ptY * sin(radians(angle))
		y1 = ptX * sin(radians(angle))+ptY * cos(radians(angle))

		x = x1+centerX
		y = y1+centerY
		return Point(x,y)

	def update(self, Track):
		#fix these given the orientation.
		LwheelCenter = self.getTransform((-self.size[0]/4),(-self.size[1]/4), self.X, self.Y, self.Theta)
		RwheelCenter = self.getTransform((self.size[0]/4),(-self.size[1]/4), self.X, self.Y, self.Theta)
		self.LeftWheel = [self.getTransform((-self.size[0]/7),(self.size[1]/7), LwheelCenter.X, LwheelCenter.Y, self.Theta+self.Steer).Coords, self.getTransform((-self.size[0]/7),(-self.size[1]/7), LwheelCenter.X, LwheelCenter.Y, self.Theta+self.Steer).Coords, self.getTransform((self.size[0]/7),(-self.size[1]/7), LwheelCenter.X, LwheelCenter.Y, self.Theta+self.Steer).Coords, self.getTransform((self.size[0]/7),(self.size[1]/7), LwheelCenter.X, LwheelCenter.Y, self.Theta+self.Steer).Coords]
		self.RightWheel = [self.getTransform((-self.size[0]/7),(self.size[1]/7), RwheelCenter.X, RwheelCenter.Y, self.Theta+self.Steer).Coords, self.getTransform((-self.size[0]/7),(-self.size[1]/7), RwheelCenter.X, RwheelCenter.Y, self.Theta+self.Steer).Coords, self.getTransform((self.size[0]/7),(-self.size[1]/7), RwheelCenter.X, RwheelCenter.Y, self.Theta+self.Steer).Coords, self.getTransform((self.size[0]/7),(self.size[1]/7), RwheelCenter.X, RwheelCenter.Y, self.Theta+self.Steer).Coords]



		self.NW = self.getTransform((-self.size[0]/2),(self.size[1]/2), self.X, self.Y, self.Theta)
		self.SW = self.getTransform((-self.size[0]/2),(-self.size[1]/2), self.X, self.Y, self.Theta)
		self.NE = self.getTransform((self.size[0]/2),(-self.size[1]/2), self.X, self.Y, self.Theta)
		self.SE = self.getTransform((self.size[0]/2),(self.size[1]/2), self.X, self.Y, self.Theta)
		self.Left = Line(self.NW, self.SW)
		self.Front = Line(self.SW, self.NE)
		self.Right = Line(self.SE, self.NE)
		self.Back = Line(self.SE, self.NW)

	
		self.Lines = [self.Left, self.Front, self.Right, self.Back]

		#Check intersect with a wall
		for T in Track.Segments:
			if self.checkIntersect(T):
				#intersected with Wall
				self.Reward = -200
				return True
		if len(Track.Objectives.Segments)>0:
			if self.checkIntersect(Track.Objectives.Segments[0]):
				self.Reward = 200
				Track.Objectives.Segments.pop(0)
			else:
				self.Reward = 0
		else:
			return True
		return False
	def getReward(self):
		return self.Reward