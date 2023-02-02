import arcpy
import xarray as xr
from datetime import datetime

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the .pyt file)."""
        self.label = "Extract Pixel Values from NetCDF"
        self.alias = "extract_pixel_values"

        # List of tool classes associated with this toolbox
        self.tools = [ExtractPixelValues]

class ExtractPixelValues(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Extract Pixel Values"
        self.description = "Extracts pixel values from netCDF files for a given point shapefile"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        params = [
            arcpy.Parameter(
                displayName="NetCDF Folder",
                name="netcdf_folder",
                datatype="DEFolder",
                parameterType="Required",
                direction="Input"
            ),
            arcpy.Parameter(
                displayName="Point Shapefile",
                name="point_shapefile",
                datatype="DEShapefile",
                parameterType="Required",
                direction="Input"
            ),
            arcpy.Parameter(
                displayName="Output Folder",
                name="output_folder",
                datatype="DEFolder",
                parameterType="Required",
                direction="Input"
            ),
            arcpy.Parameter(
                displayName="Output Table",
                name="output_table",
                datatype="GPString",
                parameterType="Required",
                direction="Output"
            ),
        ]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal validation is performed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool parameter."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        netcdf_folder = parameters[0].valueAsText
        point_shapefile = parameters[1].valueAsText
        output_folder = parameters[2].valueAsText
        output_table = parameters[3].valueAsText

        arcpy.env.workspace = netcdf_folder

        # Count the number of points in the shapefile
        num_points = int(arcpy.GetCount_management(point_shapefile).getOutput(0))

        # Create empty table with columns: date, point1, point2, ..., point_n
        arcpy.management.CreateTable(output_folder, output_table + ".dbf")
        table_path = os.path.join(output_folder, output_table + ".dbf")
        arcpy.management.AddField(table_path, "date", "DATE")

        # Add a field for each point
        for i in range(1, num_points + 1):
            arcpy.management.AddField(table_path, f"point{i}", "DOUBLE")

        # Loop through each netCDF file in the folder
        for netcdf_file in arcpy.ListFiles("*.nc"):
            # Extract date from file name
            date_str = netcdf_file.split("_")[4][:8]
            date = datetime.strptime(date_str, "%Y%m%d").date()

            # Open the netCDF file using xarray
            ds = xr.open_dataset(f"{netcdf_folder}/{netcdf_file}")
            
            #Read variable name from NetCDF file
            variable_name = list(ds.data_vars.keys())[1]

            # Get the pixel values at the points in the shapefile
            point_list = []
            with arcpy.da.SearchCursor(point_shapefile, ["SHAPE@XY"]) as cursor:
                for row in cursor:
                    x, y = row[0]
                    point_list.append((x, y))

            values = []
            for pts in range(len(point_list)):
                value = ds[variable_name].interp(x=point_list[pts][0], y=point_list[pts][1]).values
                values.append(value)

            # Insert the date and pixel values into the table
            fields = ["date"] + [f"point{i}" for i in range(1, num_points + 1)]
            with arcpy.da.InsertCursor(table_path, fields) as cursor:
                cursor.insertRow([date] + [value.item() for value in values])

        # Export the table to a CSV file
        #csv_file = os.path.join(output_folder, output_table + ".csv")
        arcpy.TableToTable_conversion(table_path, output_folder, output_table+".csv")

        return


