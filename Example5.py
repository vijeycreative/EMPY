from EMPY.Magnetostatics import Wire

wire = Wire.Wire(0.5, [1,1])
wire.plotBField2D([-4,4],[-4,4])

wire.plotBField3D([-4,4],[-4,4], [-4,4])