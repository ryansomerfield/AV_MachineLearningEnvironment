from envs.DIYRobocar_env_dir.geometry import *
def loadTrack():
	#Start Drawing the Track
	trackIB = TrackBoundry()
	trackOB = TrackBoundry()
	DonkeyObjectives = Objectives()

	trackOB.addLine(Line(Point(1220, 10688), Point(1219, 10688)))
	trackOB.addArc(Arc(Point(1219, 9449), 1219, 90, 180))
	trackOB.addLine(Line(Point(0, 9449), Point(0, 3048)))
	trackOB.addArc(Arc(Point(3048, 3048), 3048, 180, 405))
	trackOB.addLine(Line(Point(5205.286, 5201.235), Point(4733.097, 5674.312)))
	trackOB.addArc(Arc(Point(5380, 6320), 914, 225, 135))
	trackOB.addLine(Line(Point(4733.409, 6966), Point(6353.357, 8587.431)))
	trackOB.addArc(Arc(Point(5491, 9449), 1219, -45, 90))
	trackOB.addLine(Line(Point(5491, 10668), Point(1219, 10688)))



	trackIB.addLine(Line(Point(1219, 9449), Point(1219, 3048)))
	trackIB.addArc(Arc(Point(3048, 3048), 1829, 180, 405))
	trackIB.addLine(Line(Point(4340.57, 4342.026), Point(3871.884, 4810.185)))
	trackIB.addArc(Arc(Point(5380, 6320), 2134, 225, 135))
	trackIB.addLine(Line(Point(3871.002, 7828.934), Point(5491, 9449)))
	trackIB.addLine(Line(Point(5491, 9449), Point(1219, 9449)))


	for i in range(0, 1):
		DonkeyObjectives.addObjective(Line(Point(0, 7312), Point(1219, 7312)))
		DonkeyObjectives.addObjective(Line(Point(0, 5812), Point(1219, 5812)))
		DonkeyObjectives.addObjective(Line(Point(0, 3048), Point(1219, 3048)))
		DonkeyObjectives.addObjective(Line(Point(1447.273, 458), Point(2087.459, 1491.529)))
		DonkeyObjectives.addObjective(Line(Point(4008.541, 1491.529), Point(4648.727, 458)))
		DonkeyObjectives.addObjective(Line(Point(4877, 3048), Point(6096, 3048)))
		DonkeyObjectives.addObjective(Line(Point(4340.57, 4342.026), Point(5205.286, 5201.235)))
		DonkeyObjectives.addObjective(Line(Point(3246, 6320), Point(4466, 6320)))
		DonkeyObjectives.addObjective(Line(Point(4681.001, 8638.967), Point(5543.383, 7776.716)))
		DonkeyObjectives.addObjective(Line(Point(5491, 9449), Point(5491, 10668)))
		DonkeyObjectives.addObjective(Line(Point(3355, 9449), Point(3355, 10668)))
		DonkeyObjectives.addObjective(Line(Point(1219, 9449), Point(1219, 10668)))
		DonkeyObjectives.addObjective(Line(Point(0, 8105), Point(1219, 8105)))

	DonkeyImage = './envs/DIYRobocar_env_dir/Media/bg.png'

	trackMap = Track(trackIB, trackOB, DonkeyObjectives, DonkeyImage)
	return trackMap