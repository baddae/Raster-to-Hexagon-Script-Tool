# Raster-to-Hexagon-Script-Tool
ArcGIS Pro scripting tool for converting raster datasets to DGGS hexagons

# Hexagon Sampling Script Tool for ArcGIS Pro

This script tool generates hexagonal polygons that cover the extent of one or more input raster layers. The raster values are sampled into the hexagon polygons to represent their attribute values. The hexagonal cells are generated using the H3 (h3-py) Python library, and the user specifies the resolution at which the hexagons will be generated.

## Description

This tool is designed to:

- Generate hexagonal polygons over the extent of the input raster layers.
- Sample raster values into the generated hexagon polygons, storing these values as attributes.
- Allow users to specify the field names for the sampled raster values.
- Work with multiple raster layers as input, each having its sampled values stored in separate fields.

## Inputs

The script tool requires four parameters:

1. **Input Rasters**: Label: Input Rasters
Name: input_rasters
Data Type: Raster Layer
Type: Required
Multivalue: Yes
2. **Field Names**: Label: Field Names
Name: field_names
Data Type: String
Type: Required
Multivalue: Yes
3. **Output Feature Class**: Label: Output Feature Class
Name: output_fc
Data Type: Feature Class
Type: Required
4. **Resolution**: Label: Resolution
Name: resolution
Data Type: Long
Type: Required

## Important Notes

- Ensure that the total number of field names matches the number of input rasters.
- The script assumes that all input rasters have the same extent and spatial reference.
- The output feature class will have a field for each raster layer's sampled values using the user-defined field names and an additional field for the H3 index.
- H3 expects coordinates in Latitude, Longitude pairs (WGS 84, EPSG:4326), so the script includes coordinate transformation.

## Dependencies

Ensure you have the necessary libraries installed:  The `h3` library is a third-party Python library, so you may have to clone your ArcGIS Pro Python environment in order to properly install the library and get it working in ArcGIS Pro.
- `arcpy`
- `h3`
- `numpy`



