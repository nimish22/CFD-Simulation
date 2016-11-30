import sys
import os 
import arcpy
from arcpy import env
from arcpy.sa import *


def mosaicCreator(
    _mosaicPath,
    _simulationSteps
):
    try:
        arcpy.CreateMosaicDataset_management(_mosaicPath, "Mosaic", "PROJCS['WGS_1984_Web_Mercator_Auxiliary_Sphere',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Mercator_Auxiliary_Sphere'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',0.0],PARAMETER['Standard_Parallel_1',0.0],PARAMETER['Auxiliary_Sphere_Type',0.0],UNIT['Meter',1.0]]", None, None, "NONE", None)

    except ExceptionI:
        arcpy.AddMessage("Exception")

    arcpy.AddMessage("Before Loop")
    rasters = ''
    for i in range(0,int(_simulationSteps),50):
        file1 = _mosaicPath
        filePath = os.path.join(file1,"Frame"+str(i))
        rasters = rasters + ';' + filePath
        arcpy.AddMessage(filePath)
    
    arcpy.AddMessage("rasters:"+rasters)
    arcpy.management.AddRastersToMosaicDataset(os.path.join(_mosaicPath,'Mosaic'), "Raster Dataset", rasters, "UPDATE_CELL_SIZES", "UPDATE_BOUNDARY", "NO_OVERVIEWS", None, 0, 1500, None, None, "SUBFOLDERS", "ALLOW_DUPLICATES", "NO_PYRAMIDS", "CALCULATE_STATISTICS", "NO_THUMBNAILS", None, "NO_FORCE_SPATIAL_REFERENCE", "ESTIMATE_STATISTICS", None)
        
    # Set local variables
    inFeatures = os.path.join(_mosaicPath,'Mosaic')
    fieldName1 = "Time_Stamp"
    fieldPrecision = 9
    fieldAlias = "time"
 
    # Execute AddField twice for two new fields
    arcpy.AddField_management(inFeatures, fieldName1, "LONG", fieldPrecision,
                             field_alias=fieldAlias, field_is_nullable="NULLABLE")
    arcpy.CalculateField_management(inFeatures, fieldName1, "!OBJECTID!")
    arcpy.AddMessage("After Loop")


if __name__ == '__main__':
    # Arguments are optional
    argv = tuple(arcpy.GetParameterAsText(i)
        for i in range(arcpy.GetArgumentCount()))
    mosaicCreator(*argv)