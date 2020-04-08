import math

class Point:
	def __init__(self, X, Y):
		self.__X = X
		self.__Y = Y
		self.Coords = (self.X, self.Y)	#returns a tuple of coordinates

	#X
	@property
	def X(self):
		return self.__X
	@X.setter
	def X(self, new_value):
		self.__X = new_value
		self.Coords = (self.__X, self.__Y)
	#Y
	@property
	def Y(self):
		return self.__Y
	@Y.setter
	def Y(self, new_value):
		self.__Y = new_value
		self.Coords = (self.__X, self.__Y)


class Line:
	def __init__(self, StartPoint, EndPoint, SegType=0):
		self.StartPoint = StartPoint
		self.EndPoint = EndPoint
		self.SegmentType = SegType				#0=Line, 1=Arc

	def __eq__(self, other):
		if isinstance(other, Line):
			return ((self.StartPoint == other.StartPoint) and (self.EndPoint == other.EndPoint) and (self.SegmentType==other.SegmentType))
		return False

	def on_segment(self, p, q, r):
		if r.X <= max(p.X, q.X) and r.X >= min(p.X, q.X) and r.Y <= max(p.Y, q.Y) and r.Y >= min(p.Y, q.Y):
			return True
		return False

	def orientation(self, p, q, r):
		val = ((q.Y - p.Y) * (r.X - q.X)) - ((q.X - p.X) * (r.Y - q.Y))
		if val == 0 : return 0
		return 1 if val > 0 else -1

	def intersects(self, seg1):
		p1 = self.StartPoint 
		q1 = self.EndPoint
		p2 = seg1.StartPoint
		q2 = seg1.EndPoint

		o1 = self.orientation(p1, q1, p2)
		o2 = self.orientation(p1, q1, q2)
		o3 = self.orientation(p2, q2, p1)
		o4 = self.orientation(p2, q2, q1)

		if o1 != o2 and o3 != o4 : return True
		if o1 == 0 and self.on_segment(p1, q1, p2) : return True
		if o2 == 0 and self.on_segment(p1, q1, q2) : return True
		if o3 == 0 and self.on_segment(p2, q2, p1) : return True
		if o4 == 0 and self.on_segment(p2, q2, q1) : return True

		return False

class Arc:
	def __init__(self, CenterPoint, Radius, StartAngle, EndAngle):
		self.ArcPoints = []
		self.ArcSegments = []
		self.CenterPoint = CenterPoint
		self.Radius = Radius
		self.StartAngle = StartAngle
		self.EndAngle = EndAngle
		self.DegreeIncrement = 1
		if(self.StartAngle < self.EndAngle):
			self.DegreeIncrement = 1
		else:
			self.DegreeIncrement = -1
		self.getPoints()
		self.makeSegments()
	def getPoints(self):
		for n in range(self.StartAngle,self.EndAngle, self.DegreeIncrement):
			X = self.CenterPoint.X + int(self.Radius*math.cos(n*math.pi/180))
			Y = self.CenterPoint.Y+int(self.Radius*math.sin(n*math.pi/180))
			self.ArcPoints.append(Point(X,Y))
	def makeSegments(self):
		self.ArcSegments.append(Line(self.ArcPoints[0], self.ArcPoints[0+1],0))
		for pointIndeX in range(1, len(self.ArcPoints)-1):
			self.ArcSegments.append(Line(self.ArcPoints[pointIndeX], self.ArcPoints[pointIndeX+1],1))


class TrackBoundry:
	def __init__(self):
		self.Segments = []
	def addLine(self, Line):
		self.Segments.append(Line)
	def addArc(self, Arc):
		for Line in Arc.ArcSegments:
			self.Segments.append(Line)
class Objectives:
	def __init__(self):
		self.Segments = []
		self.Reward = 0
	def Scale(self, scale):
		for Line in self.Segments:
			Line.StartPoint.X = Line.StartPoint.X *scale
			Line.StartPoint.Y = Line.StartPoint.Y *scale
			Line.EndPoint.X = Line.EndPoint.X *scale
			Line.EndPoint.Y = Line.EndPoint.Y *scale
	def Shift(self, Point):
		for Line in self.Segments:
			Line.StartPoint.X += Point.X
			Line.StartPoint.Y += Point.Y
			Line.EndPoint.X += Point.X
			Line.EndPoint.Y += Point.Y
	def addObjective(self, Line):
		self.Segments.append(Line)


class Track:
	def __init__(self, InnerTrackBoundry, OuterTrackBoundry, Objectives, MapImg):
		self.InnerTrackBoundry = InnerTrackBoundry
		self.OuterTrackBoundry = OuterTrackBoundry
		self.Objectives = Objectives
		self.Image = MapImg
		self.MapSprite = None
		self.Segments = []
		self.Scale = 1
		self.MaxX = None
		self.MaxY = None
		self.MinX = None
		self.MinY = None

		for LineSegment in self.InnerTrackBoundry.Segments:
			self.getWindowBounds(LineSegment)
			self.Segments.append(LineSegment)
		for LineSegment in self.OuterTrackBoundry.Segments:
			self.getWindowBounds(LineSegment)
			self.Segments.append(LineSegment)

	def getWindowBounds(self, LineSegment):
		if(self.MaxX is None):
			self.MaxX =LineSegment.StartPoint.X
		if(self.MaxY is None):
			self.MaxY =LineSegment.StartPoint.Y
		if(self.MinX is None):
			self.MinX =LineSegment.StartPoint.X
		if(self.MinY is None):
			self.MinY =LineSegment.StartPoint.Y

		if(LineSegment.StartPoint.X)>self.MaxX:
			self.MaxX =LineSegment.StartPoint.X
		if(LineSegment.EndPoint.X)>self.MaxX:
			self.MaxX =LineSegment.EndPoint.X
		if(LineSegment.StartPoint.Y)>self.MaxY:
			self.MaxY =LineSegment.StartPoint.Y
		if(LineSegment.EndPoint.Y)>self.MaxY:
			self.MaxY =LineSegment.EndPoint.Y
		if(LineSegment.StartPoint.X)<self.MinX:
			self.MinX =LineSegment.StartPoint.X
		if(LineSegment.EndPoint.X)<self.MinX:
			self.MinX =LineSegment.EndPoint.X
		if(LineSegment.StartPoint.Y)<self.MinY:
			self.MinY =LineSegment.StartPoint.Y
		if(LineSegment.EndPoint.Y)<self.MinY:
			self.MinY =LineSegment.EndPoint.Y

	def shift(self, Point):
		if(self.InnerTrackBoundry.Segments[0].SegmentType == 0):
			self.InnerTrackBoundry.Segments[0].StartPoint.X += Point.X
			self.InnerTrackBoundry.Segments[0].StartPoint.Y += Point.Y
		# if(self.OuterTrackBoundry.Segments[0].SegmentType == 0):
		# 	self.OuterTrackBoundry.Segments[0].StartPoint.X += Point.X
		# 	self.OuterTrackBoundry.Segments[0].StartPoint.Y += Point.Y
		for Seg in self.InnerTrackBoundry.Segments:
			if ((Seg.SegmentType == 0) and (Seg!=self.InnerTrackBoundry.Segments[0])):
				Seg.StartPoint.X += Point.X
				Seg.StartPoint.Y += Point.Y
			Seg.EndPoint.X += Point.X
			Seg.EndPoint.Y += Point.Y
		for Seg in self.OuterTrackBoundry.Segments:
			if ((Seg.SegmentType == 0) and (Seg!=self.InnerTrackBoundry.Segments[0])):
				Seg.StartPoint.X += Point.X
				Seg.StartPoint.Y += Point.Y
			Seg.EndPoint.X += Point.X
			Seg.EndPoint.Y += Point.Y
		self.Objectives.Shift(Point)
		self.MinX += Point.X
		self.MinY += Point.Y
		self.MaxX += Point.X
		self.MaxY += Point.Y


	def scalePercent(self, Percentage):
		raise NotImplementedError
	def scaleToWindowSize(self, WindowSize, padding=10):
		self.shift(Point(-self.MinX+padding, -self.MinY+padding))
		xScale = WindowSize[0]/(self.MaxX - self.MinX + 2*padding)
		yScale = WindowSize[1]/(self.MaxY - self.MinY + 2*padding)
		Scale = min(xScale, yScale)
		self.Scale = Scale
		if(self.InnerTrackBoundry.Segments[0].SegmentType == 0):
			self.InnerTrackBoundry.Segments[0].StartPoint.X = int(Scale*self.InnerTrackBoundry.Segments[0].StartPoint.X)
			self.InnerTrackBoundry.Segments[0].StartPoint.Y = int(Scale*self.InnerTrackBoundry.Segments[0].StartPoint.Y)
		# This is what is broken about having an Arc first. Not really sure what is happening here.
		# if(self.OuterTrackBoundry.Segments[0].SegmentType == 0):
		# 	self.OuterTrackBoundry.Segments[0].StartPoint.X = int(Scale*self.OuterTrackBoundry.Segments[0].StartPoint.X)
		# 	self.OuterTrackBoundry.Segments[0].StartPoint.Y = int(Scale*self.OuterTrackBoundry.Segments[0].StartPoint.Y)

		for Seg in self.InnerTrackBoundry.Segments:
			if ((Seg.SegmentType == 0) and (Seg!=self.InnerTrackBoundry.Segments[0])):
				Seg.StartPoint.X = int(Scale*Seg.StartPoint.X)
				Seg.StartPoint.Y = int(Scale*Seg.StartPoint.Y)
			Seg.EndPoint.X = int(Scale*Seg.EndPoint.X)
			Seg.EndPoint.Y = int(Scale*Seg.EndPoint.Y)
		for Seg in self.OuterTrackBoundry.Segments:
			if ((Seg.SegmentType == 0) and (Seg!=self.InnerTrackBoundry.Segments[0])):
				Seg.StartPoint.X = int(Scale*Seg.StartPoint.X)
				Seg.StartPoint.Y = int(Scale*Seg.StartPoint.Y)
			Seg.EndPoint.X = int(Scale*Seg.EndPoint.X)
			Seg.EndPoint.Y = int(Scale*Seg.EndPoint.Y)
		self.Objectives.Scale(self.Scale)

		#recalculate window bounds
		for Line in (self.InnerTrackBoundry.Segments+self.OuterTrackBoundry.Segments):
			self.getWindowBounds(Line)