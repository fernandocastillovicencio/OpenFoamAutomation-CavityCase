#####################################################################
# 1) Geometry Variables (Real)
a=1.0
b=1.0
t=0.1
# # 2) Mesh Variables (Integer)
numSegmFront=20
numSegmSide=1
#####################################################################

# # 3) replacement in python script
perl -i -0pe "s#a = [0-9].[0-9]*\nb = [0-9].[0-9]*\nt = [0-9].[0-9]*#a = $a\nb = $b\nt = $t#" cavityDomain.py
perl -i -0pe "s#numSegmFront = [0-9]*\nnumSegmSide = [0-9]*#numSegmFront = $numSegmFront\nnumSegmSide = $numSegmSide#" cavityDomain.py

# # 4) run Python-Salome script
rm -f cavityDomain.unv
salome -t cavityDomain.py

# 5) run OpenFoam directory
cd $FOAM_RUN
cd cavity
# 6) remove old files 
rm -rf 0.* 
rm -rf constant/polyMesh
rm -rf system/blockMeshDict

# 7) Copy Mesh File from workspace
cp /home/fernando/workspace/engineering/salome/openFoam/cavityMesh.unv .

# 8) Convert mesh from UNV to FOAM
ideasUnvToFoam cavityMesh.unv

# 9) Set Boundary Conditions Type Zones
perl -i -0pe 's#movingWall\n    \{\n        type            patch#movingWall\n    \{\n        type            zeroGradient#' constant/polyMesh/boundary
perl -i -0pe 's#fixedWalls\n    \{\n        type            patch#fixedWalls\n    \{\n        type            zeroGradient#' constant/polyMesh/boundary
perl -i -0pe 's#frontAndBack\n    \{\n        type            patch#frontAndBack\n    \{\n        type            empty#' constant/polyMesh/boundary

# 10) Run OpenFOAM Case
checkMesh
icoFoam
paraFoam -touch
paraFoam -vtk
