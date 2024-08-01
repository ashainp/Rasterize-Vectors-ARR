# Rasterize-Vectors-ARR
Rasterize shape file vectors(2D zones) from Infoworks ICM to Hazard ARR, Speed and Depth 

Rasterize Vectors Script
This script automates the process of opening a QGIS project, accessing vector 2D zone shapefiles, and rasterizing them based on Hazard, Speed, and Depth attributes. It is particularly useful for data exported from Infoworks ICM. The script also applies the ARR hazard style template to the Hazard layer, if present.

Instructions
1. Open the Script: Enter the paths for your QGIS project file and the 2D zone vector layer. The script will handle the rest.
2. Access 2D Zone Shapefiles: The script automatically locates and accesses the specified vector shapefiles.
3. Rasterization: The script rasterizes the layers according to Hazard, Speed, and Depth attributes. The ARR hazard style template (.qml file) is applied to the Hazard layer. Note: If the Hazard layer is not present, ensure the attributes are correctly set in Infoworks ICM, and the 2D zones are exported with the Hazard ARR layer.
4. ARR Hazard Style: Download and save the ARR hazard style template in .qml format. Make sure to specify the correct path in the script.

User Input
You need to provide three paths:
1. QGIS project file path
2. Vector layer path
3. Hazard style path
Feel free to reach out if you have any questions or need assistance!
