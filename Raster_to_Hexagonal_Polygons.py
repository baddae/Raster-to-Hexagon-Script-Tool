"""
Hexagon Sampling Script for ArcGIS Pro

This script tool generates hexagonal polygons that cover the extent of one or more input raster layers. The raster values 
are sampled into the hexagon polygons to represent their attribute values. The hexagonal cells are generated using the 
H3 (h3-py) Python library, and the user specifies the resolution at which the hexagons will be generated.

Author: Bright Addae
License: MIT License

Copyright (c) 2024 Bright Addae

"""
import arcpy
import h3
import numpy as np
import os

def raster_to_hexagons(input_rasters, field_names, output_fc, resolution):
    # Load the rasters
    rasters = [arcpy.Raster(raster) for raster in input_rasters]
    raster_desc = arcpy.Describe(rasters[0])
    
    # Get raster properties (assuming all rasters have the same extent and spatial reference)
    extent = raster_desc.extent
    spatial_ref = raster_desc.spatialReference
    
    # Extract workspace and feature class name
    workspace = os.path.dirname(output_fc)
    out_name = os.path.basename(output_fc)

    # Set the workspace to the directory of the output feature class
    arcpy.env.workspace = workspace

    # Create an empty feature class for the hexagons
    arcpy.management.CreateFeatureclass(
        out_path=workspace,
        out_name=out_name,
        geometry_type="POLYGON",
        spatial_reference=spatial_ref
    )

    # Add fields for the raster values and H3 ID
    for field_name in field_names:
        arcpy.management.AddField(output_fc, field_name, "DOUBLE")
    arcpy.management.AddField(output_fc, "H3_ID", "TEXT")

    # Calculate the extent in lat/lon
    ll_corner = arcpy.PointGeometry(extent.lowerLeft, spatial_ref).projectAs(arcpy.SpatialReference(4326))
    ur_corner = arcpy.PointGeometry(extent.upperRight, spatial_ref).projectAs(arcpy.SpatialReference(4326))
    min_lat, min_lon = ll_corner.centroid.Y, ll_corner.centroid.X
    max_lat, max_lon = ur_corner.centroid.Y, ur_corner.centroid.X

    # Generate H3 hexagons over the extent
    hexagons = set()
    for lat in np.arange(min_lat, max_lat, 0.01):
        for lon in np.arange(min_lon, max_lon, 0.01):
            hexagons.add(h3.geo_to_h3(lat, lon, resolution))

    # Create an insert cursor for the output feature class
    cursor_fields = ["SHAPE@", "H3_ID"] + field_names
    with arcpy.da.InsertCursor(output_fc, cursor_fields) as cursor:
        for hex in hexagons:
            # Get the hexagon boundary as a list of lat/lon pairs
            boundary = h3.h3_to_geo_boundary(hex, geo_json=True)
            
            # Create a polygon from the boundary
            points = [arcpy.Point(lon, lat) for lon, lat in boundary]
            polygon = arcpy.Polygon(arcpy.Array(points), arcpy.SpatialReference(4326)).projectAs(spatial_ref)
            
            # Sample the raster values at the hexagon center
            center_lat, center_lon = h3.h3_to_geo(hex)
            center_point = arcpy.PointGeometry(arcpy.Point(center_lon, center_lat), arcpy.SpatialReference(4326)).projectAs(spatial_ref)
            
            # Convert the center point to the raster's coordinate system
            center_x, center_y = center_point.centroid.X, center_point.centroid.Y
            lower_left_corner = arcpy.Point(center_x - 0.005, center_y - 0.005)  # Adjust for hexagon size
            
            # Sample the raster values at the hexagon center
            raster_vals = [arcpy.RasterToNumPyArray(raster, lower_left_corner, 1, 1)[0, 0] for raster in rasters]
            
            # Insert the polygon, the H3 ID, and the sampled raster values into the feature class
            cursor.insertRow([polygon, hex] + raster_vals)

    arcpy.AddMessage(f"Hexagonal sampling completed. Output saved to {output_fc}")

if __name__ == "__main__":
    # Get parameters from the script tool
    input_rasters = arcpy.GetParameterAsText(0).split(';')
    field_names = arcpy.GetParameterAsText(1).split(';')
    output_fc = arcpy.GetParameterAsText(2)
    resolution = int(arcpy.GetParameterAsText(3))
    
    # Run the hexagon generation function
    raster_to_hexagons(input_rasters, field_names, output_fc, resolution)
