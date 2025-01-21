import rhinoscriptsyntax as rs

def remap(value, old_min, old_max, new_min, new_max):
    """Remaps a value from one range to another, handling zero-division errors."""
    if old_max == old_min:
        return (new_min + new_max) / 2
    return ((value - old_min) / (old_max - old_min)) * (new_max - new_min) + new_min

def clean_and_split(data_string):
    """Cleans and splits the input data string into individual coordinate strings."""
    cleaned_string = data_string.strip("[]")  # Remove outer brackets
    return [coord.strip(" {}'") for coord in cleaned_string.split("', '")]

def split_into_curves(points):
    """Splits points into multiple curves based on repeated points."""
    curves = []
    current_curve = []

    for i, point in enumerate(points):
        current_curve.append(point)
        # Check if the current point is repeated
        if i < len(points) - 1 and points[i + 1] == point:
            # Add the current curve as a closed loop
            curves.append(current_curve)
            current_curve = []  # Start a new curve after the repeated point
            continue  # Move to the next point after the repeated point

    # Add the last curve if it's not empty
    if current_curve:
        curves.append(current_curve)

    return curves

def create_polylines_by_sidewalk(data_array):
    """
    Parses an array of strings containing coordinate data, splits rows into multiple curves, remaps x and y, 
    and returns a list of lists of polyline GUIDs.
    
    Args:
        data_array (list): An array of strings, each containing coordinate data.
    
    Returns:
        list: A nested list of polyline GUIDs grouped by row.
    """
    all_points = []  # To store all points for calculating bounds
    sidewalks = []  # To store all sidewalks with their curves

    # Step 1: Parse the input data
    for row_index, data_string in enumerate(data_array):
        if not data_string or not data_string.strip():
            print(f"Skipping empty or null entry at row {row_index}")
            continue

        print(f"Processing data string at row {row_index}: {data_string[:100]}...")  # Log processing
        coordinate_strings = clean_and_split(data_string)  # Clean and split the data string

        points = []
        for coord_string in coordinate_strings:
            try:
                if not coord_string or ',' not in coord_string:
                    print(f"Skipping malformed entry: {coord_string}")
                    continue

                x, y, z = map(float, coord_string.split(","))
                points.append((x, y, z))
                all_points.append((x, y, z))
            except ValueError:
                print(f"Skipping malformed entry: {coord_string}")
                continue

        if points:
            # Step 2: Split into curves
            curves = split_into_curves(points)

            # Step 3: Remap and create polylines for each curve
            row_polylines = []
            for curve_points in curves:
                remapped_points = [
                    (
                        remap(p[0], min(p[0] for p in all_points), max(p[0] for p in all_points), 0, 100),  # Remap x
                        remap(p[1], min(p[1] for p in all_points), max(p[1] for p in all_points), 0, 100),  # Remap y
                        0  # Keep z at 0
                    )
                    for p in curve_points
                ]
                polyline = rs.AddPolyline(remapped_points)
                if polyline:
                    row_polylines.append(polyline)

            # Add all polylines for this row to the sidewalks list
            sidewalks.append(row_polylines)

    return sidewalks

# Grasshopper Input
if isinstance(x, list):
    # Process the input array and create a nested list of polyline GUIDs
    a = create_polylines_by_sidewalk(x)
else:
    a = "Input 'x' is not a valid array. Please provide an array of strings."
