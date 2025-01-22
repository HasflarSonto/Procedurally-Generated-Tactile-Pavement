import rhinoscriptsyntax as rs
import clr
clr.AddReference("Grasshopper")
from Grasshopper import DataTree
from Grasshopper.Kernel.Data import GH_Path

def remap(value, old_min, old_max, new_min, new_max):
    """Remaps a value from one range to another, handling zero-division errors."""
    if old_max == old_min:
        return (new_min + new_max) / 2
    return ((value - old_min) / (old_max - old_min)) * (new_max - new_min) + new_min

def clean_and_split(data_string):
    """Cleans and splits the input data string into individual coordinate strings."""
    cleaned_string = data_string.strip("[]")  # Remove outer brackets
    return [coord.strip(" {}'") for coord in cleaned_string.split("', '")]

def process_row(points):
    """
    Splits a row of points into multiple closed curves based on repeated points.
    Whenever a repeated point is detected, a closed curve is created.
    """
    curves = []
    current_curve = []
    seen_points = set()

    i = 0
    while i < len(points):
        if points[i] in seen_points:
            # Repeated point found: finalize the current curve
            current_curve.append(points[i])  # Close the curve with the repeated point
            curves.append(current_curve)  # Save the current curve
            current_curve = []  # Start a new curve
            seen_points.clear()  # Reset the seen points
        else:
            current_curve.append(points[i])
            seen_points.add(points[i])
        i += 1

    # Add the remaining points as a curve if not empty
    if current_curve:
        curves.append(current_curve)

    return curves

def create_datatree_from_curves(data_array):
    """
    Parses an array of strings containing coordinate data, splits into curves, remaps x and y, 
    and returns a Grasshopper DataTree of polyline GUIDs.
    
    Args:
        data_array (list): An array of strings, each containing coordinate data.
    
    Returns:
        DataTree: A Grasshopper DataTree containing polyline GUIDs.
    """
    all_points = []  # To store all points for calculating global bounds
    data_tree = DataTree[object]()  # Initialize a DataTree

    # Step 1: Parse all rows to gather global bounds
    for data_string in data_array:
        if not data_string or not data_string.strip():
            continue

        coordinate_strings = clean_and_split(data_string)  # Clean and split the data string

        for coord_string in coordinate_strings:
            try:
                if not coord_string or ',' not in coord_string:
                    continue
                x, y, z = map(float, coord_string.split(","))
                all_points.append((x, y, z))
            except ValueError:
                continue

    # Global bounds for remapping
    if not all_points:
        print("No valid points found in the input.")
        return data_tree

    global_min_x = min(p[0] for p in all_points)
    global_max_x = max(p[0] for p in all_points)
    global_min_y = min(p[1] for p in all_points)
    global_max_y = max(p[1] for p in all_points)

    # Step 2: Process each row for curve splitting and remapping
    for row_index, data_string in enumerate(data_array):
        if not data_string or not data_string.strip():
            continue

        coordinate_strings = clean_and_split(data_string)  # Clean and split the data string
        points = []
        for coord_string in coordinate_strings:
            try:
                if not coord_string or ',' not in coord_string:
                    continue
                x, y, z = map(float, coord_string.split(","))
                points.append((x, y, z))
            except ValueError:
                continue

        if points:
            # Split into curves
            curves = process_row(points)

            # Remap and add curves to the DataTree
            for curve_index, curve_points in enumerate(curves):
                remapped_points = [
                    (
                        remap(p[0], global_min_x, global_max_x, 0, 100),  # Remap x globally
                        remap(p[1], global_min_y, global_max_y, 0, 100),  # Remap y globally
                        0  # Keep z at 0
                    )
                    for p in curve_points
                ]
                polyline = rs.AddPolyline(remapped_points)
                if polyline:
                    path = GH_Path(row_index)  # Create a path for the current row
                    data_tree.Add(polyline, path)

    return data_tree

# Grasshopper Input
if isinstance(x, list):
    # Process the input array and create a DataTree of polylines
    a = create_datatree_from_curves(x)
else:
    a = "Input 'x' is not a valid array. Please provide an array of strings."
