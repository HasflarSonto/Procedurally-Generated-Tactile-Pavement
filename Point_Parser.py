import rhinoscriptsyntax as rs

def parse_coordinate_string(coord_string):
    """
    Converts a coordinate string '{x,y,z}' to a tuple (x, y, z).
    Handles malformed strings gracefully.
    """
    try:
        # Clean and parse the coordinate string
        coord_string = coord_string.strip("{}").strip("[]").strip()
        coords = map(float, coord_string.split(","))
        return tuple(coords)
    except ValueError:
        # Return None for malformed strings
        print(f"Skipping malformed coordinate: {coord_string}")
        return None

def process_data_tree(data_tree):
    """
    Processes a data tree from Grasshopper, parses coordinates, and creates polycurves.
    """
    polycurves = []
    for branch in data_tree:
        # Parse all coordinates in the branch
        points = [parse_coordinate_string(item) for item in branch]
        # Filter out None (malformed) points
        points = [pt for pt in points if pt is not None]
        if len(points) > 1:
            # Create a closed polyline from the points
            polycurve = rs.AddPolyline(points + [points[0]])
            polycurves.append(polycurve)
    return polycurves

# Grasshopper Inputs:
# 'x' is the data tree containing coordinate strings
data_tree = x  # Connect your data tree from Grasshopper

# Process the data tree and create polycurves
a = process_data_tree(data_tree)  # Output polycurves to 'a'
