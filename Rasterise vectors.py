import os
import sys
import subprocess
from qgis.core import QgsProject, QgsVectorLayer, QgsRasterLayer

# User input for project file path and vector layer directory
project_file = r'C:\Users\enoks\Desktop\test qgis\24000_HOME\08 - Model Files\QGIS\home.qgz'
vector_layer_dir = r'C:\Users\enoks\Desktop\test qgis\24000_HOME\08 - Model Files\Infoworks ICM\Results\231107 NEW POST\PRE NEW NEW_post new dw2 SST_1pct_4_5hr_5'

# Path to the style file for the Hazard layer
hazard_style_path = r'E:\Sync\05_QGIS RESOURCES\CLR\Hazard color ramp\Hazard ARR.qml'

# Automatically select the "2D zones.shp" file in the specified directory
vector_layer_path = os.path.join(vector_layer_dir, "2D zones.shp")
if not os.path.isfile(vector_layer_path):
    print(f"The file '2D zones.shp' does not exist in the directory {vector_layer_dir}!")
    sys.exit(1)

# Open the project
print("Opening project...")
project = QgsProject.instance()
result = project.read(project_file)

# Debugging information
print(f"Project read result: {result}")
print(f"Project file name after read: {project.fileName()}")

# Check if the project is loaded
if project.fileName() == project_file:
    print("Project opened successfully.")
else:
    print("Failed to open project.")

# Load the vector layer
print(f"Loading vector layer from {vector_layer_path}...")
vector_layer = QgsVectorLayer(vector_layer_path, "2D zones", "ogr")

# Check if the layer is valid
if not vector_layer.isValid():
    print(f"Layer {vector_layer_path} failed to load!")
    sys.exit(1)
else:
    print(f"Vector layer {vector_layer_path} loaded successfully.")
    project.addMapLayer(vector_layer)
    print("Vector layer added to the project.")

# Create output directory
output_dir = r'C:\Users\enoks\Desktop\test qgis\24000_HOME\08 - Model Files\QGIS\Raster'
os.makedirs(output_dir, exist_ok=True)
print(f"Output directory created at {output_dir}.")

# Extract the first four characters of the folder name
folder_name = os.path.basename(vector_layer_dir)[:4]

# Function to rasterize the field and load it into the project
def rasterize_and_load_field(vector_layer, field, output_dir, folder_name, style_path=None):
    print(f"Rasterizing field {field}...")
    raster_output_path = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(vector_layer.source()))[0]}_{field}_{folder_name}.tif")
    extent = vector_layer.extent()
    xmin, ymin, xmax, ymax = extent.xMinimum(), extent.yMinimum(), extent.xMaximum(), extent.yMaximum()
    gdal_command = [
        'gdal_rasterize',
        '-a', field,
        '-tr', '0.5', '0.5',
        '-te', str(xmin), str(ymin), str(xmax), str(ymax),
        '-a_nodata', '-9999',
        '-ot', 'Float32',
        '-of', 'GTiff',
        vector_layer.source(),
        raster_output_path
    ]
    print(f"Running GDAL command: {' '.join(gdal_command)}")
    try:
        result = subprocess.run(gdal_command, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"GDAL command failed with error: {result.stderr}")
        else:
            print(f"Rasterization of field {field} completed successfully.")
    except Exception as e:
        print(f"Error during rasterization of {field}: {e}")
        sys.exit(1)
    
    # Check if the raster file was created
    if not os.path.isfile(raster_output_path):
        print(f"Raster file {raster_output_path} was not created.")
    else:
        print(f"Raster file {raster_output_path} was created successfully.")
        
        # Load the raster layer into the project
        print(f"Loading raster layer from {raster_output_path}...")
        raster_layer = QgsRasterLayer(raster_output_path, f"{field} Raster")
        if not raster_layer.isValid():
            print(f"Raster layer {raster_output_path} failed to load!")
        else:
            project.addMapLayer(raster_layer)
            print(f"Raster layer {raster_output_path} loaded and added to the project.")
            
            # Apply the style if provided
            if style_path and field == 'Hazard_ARR':
                print(f"Applying style from {style_path} to {field} Raster layer...")
                raster_layer.loadNamedStyle(style_path)
                raster_layer.triggerRepaint()
                print(f"Style applied to {field} Raster layer.")

# Rasterize and load each field
rasterize_and_load_field(vector_layer, 'Hazard_ARR', output_dir, folder_name, hazard_style_path)  # Function to rasterize and load the field Hazard
rasterize_and_load_field(vector_layer, 'SPEED2D', output_dir, folder_name)  # Function to rasterize and load the field SPEED2D
rasterize_and_load_field(vector_layer, 'DEPTH2D', output_dir, folder_name)  # Function to rasterize and load the field DEPTH2D
