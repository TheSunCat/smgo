Convert a Wavefront OBJ files to a KCL and PA file that can be used for
collision in SMG1/2. 

Requires Python 3 with PyQt4 installed to run.
 
To use it
first prepare the OBJ file. In a 3D modelling program (such as Blender,
SketchUp or 3DStudioMax) choose all the faces you want to have a specific
set of properties, assign a material to these faces and give that material
a descriptive name so you are able to find it later. Repeat for all the
different surface types you want. 

Now open up collision_creator and open
the OBJ file. This should give a list of the names of all the materials
used by the OBJ file. Select a name and edit the surface properties.
When all the surface properties are set save the collision. This can
take some time for large models.