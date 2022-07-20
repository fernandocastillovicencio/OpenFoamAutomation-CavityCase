#!/usr/bin/env python

###################################################################################

# 0.1) Import libraries
import sys
import salome

# 0.2) Initialize Salome
salome.salome_init()
import salome_notebook
notebook = salome_notebook.NoteBook()
sys.path.insert(0,r'/home/fernando/workspace/engineering/salome')

###################################################################################
###################################################################################

# 1.0) Open SHAPER Module
# import libraries
from SketchAPI import *
from salome.shaper import model

# start model
model.begin()
# create model
partSet = model.moduleDocument()

###################################################################################

# 1.1) Create Part
Part_1 = model.addPart(partSet)
# change name of Part_1 to cavityDomain
Part_1.setName("cavityDomain")
Part_1.result().setName("Part_1")
# document
Part_1_doc = Part_1.document()

###################################################################################

# 1.2) Create Parameters of Geometry
a = 1.0
b = 1.0
t = 0.1
model.addParameter(Part_1_doc, "a", str(a))
model.addParameter(Part_1_doc, "b", str(b))
model.addParameter(Part_1_doc, "t", str(t))

###################################################################################

# 1.3) Create Sketch in XY-plane
Sketch_1 = model.addSketch(Part_1_doc, model.standardPlane("XOY"))

# 1.3.1) Create Rectangle
#Lines
SketchLine_1 = Sketch_1.addLine(1.8,1.2,-1.0,1.2)
SketchLine_2 = Sketch_1.addLine(-1.0,1.2,-1.0,-2.5)
SketchLine_3 = Sketch_1.addLine(-1.0,-2.5,1.8,-2.5)
SketchLine_4 = Sketch_1.addLine(1.8,-2.5,1.8,1.2)
# Close Lines for rectangle
SketchConstraintCoincidence_1 = Sketch_1.setCoincident(SketchLine_4.endPoint() , SketchLine_1.startPoint())
SketchConstraintCoincidence_2 = Sketch_1.setCoincident(SketchLine_1.endPoint() , SketchLine_2.startPoint())
SketchConstraintCoincidence_3 = Sketch_1.setCoincident(SketchLine_2.endPoint() , SketchLine_3.startPoint())
SketchConstraintCoincidence_4 = Sketch_1.setCoincident(SketchLine_3.endPoint() , SketchLine_4.startPoint())
# Orientation Constraint 
SketchConstraintHorizontal_1 = Sketch_1.setHorizontal(SketchLine_1.result())
SketchConstraintVertical_1 = Sketch_1.setVertical(SketchLine_2.result())
SketchConstraintHorizontal_2 = Sketch_1.setHorizontal(SketchLine_3.result())
SketchConstraintVertical_2 = Sketch_1.setVertical(SketchLine_4.result())

# 1.3.2) Assign dimensions/constraints for rectangle
# set Origin
SketchProjection_1 = Sketch_1.addProjection(model.selection("VERTEX","PartSet/Origin"),False)
SketchPoint_1 = SketchProjection_1.createdFeature()
# Set base and height
SketchConstraintLength_1 = Sketch_1.setLength(SketchLine_1.result() , "b")
SketchConstraintLength_2 = Sketch_1.setLength(SketchLine_2.result() , "a")
# Centralize rectangle
SketchConstraintDistance_1 = Sketch_1.setDistance( SketchLine_1.result() , SketchAPI_Point(SketchPoint_1).coordinates() , "a/2" , True)
SketchConstraintDistance_1 = Sketch_1.setDistance( SketchLine_2.result() , SketchAPI_Point(SketchPoint_1).coordinates() , "b/2" , True)
# exit from sketch
model.do()

# 1.3.3) Extrude the rectangle
Extrusion_1 = model.addExtrusion ( Part_1_doc , [model.selection("COMPOUND", "all-in-Sketch_1")] , model.selection() ,  "t" , 0  )
Extrusion_1.result().setName("cavityDomain")
# part exit
model.do()


###################################################################################

# 1.4) Create Groups of Boundary Conditions
# 1.4.1) movingWall
Group_1 = model.addGroup ( Part_1_doc ,
                          [model.selection( "FACE" , "cavityDomain/Generated_Face&Sketch_1/SketchLine_1" )] )
Group_1.setName("movingWall")
Group_1.result().setName("movingWall")

# 1.4.2) fixedWalls
Group_2_objects = [ 
                   model.selection("FACE" , "cavityDomain/Generated_Face&Sketch_1/SketchLine_2") , 
                   model.selection("FACE" , "cavityDomain/Generated_Face&Sketch_1/SketchLine_3") , 
                   model.selection("FACE" , "cavityDomain/Generated_Face&Sketch_1/SketchLine_4") 
                   ]
Group_2 = model.addGroup ( Part_1_doc , Group_2_objects )
Group_2.setName("fixedWalls")
Group_2.result().setName("fixedWalls")

# 1.4.3) frontAndBack
Group_3_objects = [ model.selection("FACE" , "cavityDomain/From_Face") , 
                   model.selection("FACE" , "cavityDomain/To_Face") ]
Group_3 = model.addGroup ( Part_1_doc , Group_3_objects )
Group_3.setName("frontAndBack")
Group_3.result().setName("frontAndBack")

###################################################################################

# 1.4) Create Groups of Boundary Conditions
# 1.4.1) frontEdges
Group_4_objects = [ 
                   model.selection("EDGE" , "[cavityDomain/Generated_Face&Sketch_1/SketchLine_1][cavityDomain/From_Face]") , 
                   model.selection("EDGE" , "[cavityDomain/Generated_Face&Sketch_1/SketchLine_1][cavityDomain/To_Face]") , 
                   model.selection("EDGE" , "[cavityDomain/Generated_Face&Sketch_1/SketchLine_2][cavityDomain/From_Face]") , 
                   model.selection("EDGE" , "[cavityDomain/Generated_Face&Sketch_1/SketchLine_2][cavityDomain/To_Face]") , 
                   model.selection("EDGE" , "[cavityDomain/Generated_Face&Sketch_1/SketchLine_3][cavityDomain/From_Face]") , 
                   model.selection("EDGE" , "[cavityDomain/Generated_Face&Sketch_1/SketchLine_3][cavityDomain/To_Face]") , 
                   model.selection("EDGE" , "[cavityDomain/Generated_Face&Sketch_1/SketchLine_4][cavityDomain/From_Face]") , 
                   model.selection("EDGE" , "[cavityDomain/Generated_Face&Sketch_1/SketchLine_4][cavityDomain/To_Face]") 
                   ]
Group_4 = model.addGroup ( Part_1_doc , Group_4_objects )
Group_4.setName("frontEdges")
Group_4.result().setName("frontEdges")

# # 1.4.2) sideEdges
Group_5_objects = [ 
                   model.selection("EDGE" , "[cavityDomain/Generated_Face&Sketch_1/SketchLine_1][cavityDomain/Generated_Face&Sketch_1/SketchLine_2]") , 
                   model.selection("EDGE" , "[cavityDomain/Generated_Face&Sketch_1/SketchLine_2][cavityDomain/Generated_Face&Sketch_1/SketchLine_3]") , 
                   model.selection("EDGE" , "[cavityDomain/Generated_Face&Sketch_1/SketchLine_3][cavityDomain/Generated_Face&Sketch_1/SketchLine_4]") , 
                   model.selection("EDGE" , "[cavityDomain/Generated_Face&Sketch_1/SketchLine_4][cavityDomain/Generated_Face&Sketch_1/SketchLine_1]") 
                   ]
Group_5 = model.addGroup ( Part_1_doc , Group_5_objects )
Group_5.setName("sideEdges")
Group_5.result().setName("sideEdges")

###################################################################################

# 1.6) Export Shaper to Geom
Export_1 = model.exportToXAO ( Part_1_doc , '/tmp/shaper1.xao' , model.selection("SOLID","cavityDomain") , "XAO" )
# End model
model.end()
###################################################################################
###################################################################################

# 2.0) Open GEOMETRY Module
# import libraries
import GEOM
from salome.geom import geomBuilder
import math
import SALOMEDS
# create module
geompy = geomBuilder.New()

###################################################################################
# 2.1) Import Geometry
( imported , cavityDomain , [] , [movingWall, fixedWalls, frontAndBack, frontEdges, sideEdges] , [] )  = geompy.ImportXAO("/tmp/shaper1.xao")
# import domain and boundary conditions
geompy.addToStudy(cavityDomain,'cavityDomain')
geompy.addToStudyInFather(cavityDomain, movingWall, 'movingWall')
geompy.addToStudyInFather(cavityDomain,fixedWalls,'fixedWalls')
geompy.addToStudyInFather(cavityDomain,frontAndBack,'frontAndBack')
geompy.addToStudyInFather(cavityDomain,frontEdges,'frontEdges')
geompy.addToStudyInFather(cavityDomain,sideEdges,'sideEdges')

###################################################################################
###################################################################################

# 3.0) Open MESH Module
import SMESH, SALOMEDS
from salome.smesh import smeshBuilder
# load module
smesh = smeshBuilder.New()

###################################################################################

# 3.1) Create Parameters of Geometry
numSegmFront = 20
numSegmSide = 1

###################################################################################
# 3.2) Create Mesh
cavityMesh = smesh.Mesh(cavityDomain)
smesh.SetName(cavityMesh.GetMesh() , 'cavityMesh')

###################################################################################
# 3.3) Configure Mesh Method
meshHexa3D = cavityMesh.Hexahedron(algo=smeshBuilder.Hexa)
smesh.SetName(meshHexa3D.GetAlgorithm(), 'meshHexa3D')
meshMapping2D = cavityMesh.Quadrangle(algo=smeshBuilder.QUADRANGLE)
smesh.SetName(meshMapping2D.GetAlgorithm(),'meshMapping2D')
meshWire1D = cavityMesh.Segment()
smesh.SetName(meshWire1D.GetAlgorithm(),'meshWire1D')

###################################################################################
# 3.4) Mesh Front Edges
meshFrontEdges1D = cavityMesh.Segment(geom=frontEdges)
numberOfSegments1 = meshFrontEdges1D.NumberOfSegments(numSegmFront)
smesh.SetName(numberOfSegments1,'numberOfSegments1')
subMesh_frontEdges = meshFrontEdges1D.GetSubMesh()
smesh.SetName(subMesh_frontEdges,'subMesh_frontEdges')

###################################################################################
# 3.5) Mesh Side Edges
meshSideEdges1D = cavityMesh.Segment(geom=sideEdges)
numberOfSegments2 = meshSideEdges1D.NumberOfSegments(numSegmSide)
smesh.SetName(numberOfSegments2,'numberOfSegments2')
subMesh_sideEdges = meshSideEdges1D.GetSubMesh()
smesh.SetName(subMesh_sideEdges,'subMesh_sideEdges')

###################################################################################
# 3.6) Compute Mesh
isDone = cavityMesh.Compute()

###################################################################################
# 3.7) Create Groups
movingWallBC = cavityMesh.GroupOnGeom(movingWall,'movingWall',SMESH.FACE)
fixedWallsBC = cavityMesh.GroupOnGeom(fixedWalls,'fixedWalls',SMESH.FACE)
frontAndBackBC = cavityMesh.GroupOnGeom(frontAndBack,'frontAndBack',SMESH.FACE)

###################################################################################
# 3.8) Export Mesh to UNV
cavityMesh.ExportUNV(r'/home/fernando/workspace/engineering/salome/openFoam/cavityMesh.unv')

###################################################################################
###################################################################################

# Update Salome
if salome.sg.hasDesktop():
    salome.sg.updateObjBrowser()