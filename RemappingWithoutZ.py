import rhinoscriptsyntax as rs

def remap(value, old_min, old_max, new_min, new_max):
    """Remaps a value from one range to another, handling zero-division errors."""
    if old_max == old_min:
        # If the range is zero, map all values to the midpoint of the target range
        return (new_min + new_max) / 2
    return ((value - old_min) / (old_max - old_min)) * (new_max - new_min) + new_min

def create_polylines_from_array_with_remap(data_array):
    """
    Parses an array of strings containing coordinate data, remaps x and y, and creates polylines.
    
    Args:
        data_array (list): An array of strings, each containing coordinate data.
    
    Returns:
        list: A list of polyline GUIDs.
    """
    all_points = []  # To store all points for calculating bounds
    polylines = []

    # Step 1: Parse the input data
    for data_string in data_array:
        if not data_string or not data_string.strip():
            continue  # Skip empty strings

        cleaned_string = data_string.strip("[]")  # Remove outer brackets
        coordinate_strings = cleaned_string.split("','")  # Split by delimiter

        points = []
        for coord_string in coordinate_strings:
            try:
                clean_coord = coord_string.strip(" {}'")
                if not clean_coord or ',' not in clean_coord:
                    continue  # Skip malformed entries

                x, y, z = map(float, clean_coord.split(","))
                point = (x, y, z)
                points.append(point)
                all_points.append(point)  # Add to global points list
            except ValueError:
                continue  # Skip malformed entries

        if len(points) > 1:
            points.append(points[0])  # Close the polyline
            polylines.append(points)

    # Step 2: Calculate bounds for x and y
    if not all_points:
        print("No valid points found in the input.")
        return []

    min_x = min(p[0] for p in all_points)
    max_x = max(p[0] for p in all_points)
    min_y = min(p[1] for p in all_points)
    max_y = max(p[1] for p in all_points)

    # Step 3: Remap x and y, keep z unchanged, and create polylines
    remapped_polylines = []
    for points in polylines:
        remapped_points = [
            (
                remap(p[0], min_x, max_x, 0, 100),  # Remap x
                remap(p[1], min_y, max_y, 0, 100),  # Remap y
                0  # Keep z at 0
            )
            for p in points
        ]
        # Create the polyline in Rhino
        polyline = rs.AddPolyline(remapped_points)
        if polyline:
            remapped_polylines.append(polyline)

    return remapped_polylines

# Grasshopper Input
if isinstance(x, list):
    # Process the input array and create polylines
    a = create_polylines_from_array_with_remap(x)
else:
    a = "Input 'x' is not a valid array. Please provide an array of strings."
