import pygame
from PIL import Image
import numpy as np
from envs.DIYRobocar_env_dir.geometry import *
GREEN = (54, 119, 45)



class World:
	def __init__(self, ShowWindow, Window_Size, Track, Car):
		self.Track = Track
		self.Scale = self.Track.Scale
		self.Car = Car

		if ShowWindow:
			self.DisplayWindow = GameWindow(Window_Size, Track, Car)
		else:
			self.Car.Scale(self.Scale)
		self.update()

	def update(self):
		carIntersect = self.Car.update(self.Track)
		return carIntersect

	def getReward(self):
		return self.Car.getReward() -.1
	def getState(self):
		return (self.Car.X, self.Car.Y, self.Car.Theta)



def rotate(surface, angle, pivot, offset):
    """Rotate the surface around the pivot point.

    Args:
        surface (pygame.Surface): The surface that is to be rotated.
        angle (float): Rotate by this angle.
        pivot (tuple, list, pygame.math.Vector2): The pivot point.
        offset (pygame.math.Vector2): This vector is added to the pivot.
        scale (float): The zoom factor
    """
    rotated_image = pygame.transform.rotate(surface, -angle)  # Rotate the image.
    rotated_offset = offset.rotate(angle)  # Rotate the offset vector.
    # Add the offset vector to the center/pivot point to shift the rect.
    rect = rotated_image.get_rect(center=pivot+rotated_offset)
    return rotated_image, rect  # Return the rotated image and shifted rect.


class GameWindow:
	def __init__(self, Window_Size, Track, Car):
		pygame.init()
		self.clock = pygame.time.Clock()
		self.screen = pygame.display.set_mode(Window_Size)
		self.Window_Size = Window_Size
		self.Track = Track
		self.Car = Car
		self.Scale = self.Track.Scale
		self.Car.Scale(self.Scale)
		self.Car.Sprite = pygame.transform.scale(pygame.image.load(self.Car.Image).convert_alpha(), Car.size)
		self.Track.MapSprite = pygame.image.load(self.Track.Image).convert()
		pygame.display.flip()
		self.clock.tick(30)

	def  __del__(self):
		pygame.quit()
	def carView(self):
		image, rect = rotate(self.screen, -self.Car.Theta, (self.Window_Size[0]/2, self.Window_Size[1]/2), pygame.math.Vector2(self.Window_Size[0]/2-self.Car.X, self.Window_Size[1]/2-self.Car.Y))
		self.screen.fill(GREEN)
		self.screen.blit(image, rect)
		imgarray = np.array(pygame.surfarray.array3d(self.screen))[300:450,300:450,:]
		imgSurf = pygame.surfarray.make_surface(imgarray)
		imgarray = np.swapaxes(imgarray, 0, 1)
		return imgarray, imgSurf, pygame.Rect(0,0,150, 150)

	def Draw(self, episode):
		self.drawTrack()
		self.drawObjectives()
		self.drawCar()
		self.showEpisode(episode)
		carView_array, carView_Surface, carView_rect = self.carView()
		self.screen.blit(carView_Surface, carView_rect)
		pygame.display.flip()
		
		# return carView_array
		

	def drawTrack(self, Color=(255,255,255), Width=4):
		imageRect = pygame.Rect(self.Track.MinX-7, self.Track.MinY-2, self.Track.MaxX-self.Track.MinX,self.Track.MaxY-self.Track.MinY)
		self.screen.fill(GREEN)
		self.screen.blit(self.Track.MapSprite, imageRect)
		prevPoint = None
		# for LineSegment in self.Track.InnerTrackBoundry.Segments:
		# 	if prevPoint != None:
		# 		pygame.draw.line(self.screen, Color, prevPoint, LineSegment.StartPoint.Coords, Width)
		# 	pygame.draw.line(self.screen, Color, LineSegment.StartPoint.Coords, LineSegment.EndPoint.Coords, Width)
		# 	prevPoint = LineSegment.EndPoint.Coords
		# prevPoint = None
		# for LineSegment in self.Track.OuterTrackBoundry.Segments:
		# 	if prevPoint != None:
		# 		pygame.draw.line(self.screen, Color, prevPoint, LineSegment.StartPoint.Coords, Width)
		# 	pygame.draw.line(self.screen, Color, LineSegment.StartPoint.Coords, LineSegment.EndPoint.Coords, Width)
		# 	prevPoint = LineSegment.EndPoint.Coords
	def showEpisode(self, episode):
		font = pygame.font.Font('freesansbold.ttf', 32)
		text = font.render(str(episode), True, (0,0,0)) 
		textRect = text.get_rect()
		textRect.center = (150,50)
		self.screen.blit(text, textRect)

	def drawObjectives(self):
		pass
		# for Line in self.Track.Objectives.Segments:
		# 	pygame.draw.line(self.screen, (0,180,192), Line.StartPoint.Coords, Line.EndPoint.Coords, 3)


	def drawCar(self, Width=4):
		#draw the front wheels
		leftWheel = pygame.draw.polygon(self.screen, (0,0,0), self.Car.LeftWheel)
		rightWheel = pygame.draw.polygon(self.screen, (0,0,0), self.Car.RightWheel)
		#draw sprite
		left = min(self.Car.NW.X, self.Car.NE.X, self.Car.SW.X, self.Car.SE.X)
		top = min(self.Car.NW.Y, self.Car.NE.Y, self.Car.SW.Y, self.Car.SE.Y)
		width = max(self.Car.NW.X, self.Car.NE.X, self.Car.SW.X, self.Car.SE.X) - left
		height = max(self.Car.NW.Y, self.Car.NE.Y, self.Car.SW.Y, self.Car.SE.Y) - top
		self.Car.Rect = pygame.Rect(left, top, width, height)
		sprite = pygame.transform.rotate(self.Car.Sprite, -self.Car.Theta)
		self.screen.blit(sprite, self.Car.Rect)
		# draw bounding box (for debugging purposes)
		# for L in self.Car.Lines:
		# 	pygame.draw.line(self.screen, self.Car.Color, L.StartPoint.Coords, L.EndPoint.Coords, Width)