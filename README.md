# Extract Pixel Values from NetCDF
This toolbox is for extracting pixel values from netCDF (Network Common Data Form) files at the location of a set of points. The toolbox includes a single tool that takes as inputs a folder containing netCDF files, a point shapefile, and an output folder location. The tool outputs a table and a CSV with columns for each point in the shapefile and rows for each date represented in the netCDF files name. The pixel values are extracted for each point using the xarray library in Python.

## Prerequisites
Before using this toolbox, you will need:

- ArcGIS Pro (Tested with ArcGIS Pro 3.0)
- Python 3.7 or later
- [xarray](https://pypi.org/project/xarray/) library

## Installation
1. Clone the repository or download the zip file to your local machine.
2. Open ArcGIS Pro and create a new project or open an existing project.
3. Go to the Project tab and click on the Python tab.
4. Click on the Add Package button and search for xarray. Install the xarray library.
5. Go to the Project tab and click on the Geoprocessing tab.
6. Click on the Tools button and then Add Toolbox.
7. Navigate to the location where you cloned the repository or unzipped the file and select the ExtractNetCDFvalues.pyt file.
8. The Extract Pixel Values from NetCDF toolbox should now be added to your ArcGIS project.

## Usage
1. Go to the Extract Pixel Values from NetCDF toolbox and double-click on the Extract Pixel Values tool.
2. In the NetCDF Folder field, browse to the folder containing the netCDF files.
3. In the Point Shapefile field, select the point shapefile to extract values from the netCDF files.
4. In the Output Folder field, specify the folder to store the output table.
5. In the Output Table field, specify a name for the output table.
6. Click on the Run button to execute the tool.

## Output
The tool will create an output table and a CSV with the following columns:

1. date: date of the netCDF file
2. point1, point2, ..., point_n: pixel values at the points in the shapefile
3. The output table will be stored in the output folder as a dBase file with a .dbf extension and .csv.

## Considerations
1. Tool assumes that your netCDF files have date in their names at specific location.
2. Tool assumes that your shapefile and netCDF have same spatial reference system.
3. Tool assumes that your netCDF files have only single variable along with time, lat, and lng.

You may need to edit the source code to fit your needs.

## Limitations
1. This tool has been tested with netCDF files in the CF convention with lon/lat coordinates. It may not work with other coordinate systems or conventions.
2. The tool assumes that the first variable in the netCDF file is the data variable to extract values from.
3. The tool assumes that the date of the netCDF file can be extracted from the file name.

## Support
If you encounter any issues or have questions about this toolbox, please contact me at [![Linkedin Badge](https://img.shields.io/badge/-Salman-blue?style=flat&logo=Linkedin&logoColor=white)](https://www.linkedin.com/in/salman12haider13/)!
