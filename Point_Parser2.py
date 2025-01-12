import rhinoscriptsyntax as rs

def create_polylines_from_array(data_array):
    """
    Parses an array of strings containing coordinate data and creates polylines.
    
    Args:
        data_array (list): An array of strings, each containing coordinate data.
    
    Returns:
        list: A list of polyline GUIDs.
    """
    polylines = []

    for data_string in data_array:
        if not data_string:
            continue  # Skip empty strings

        # Step 1: Clean and split the data string
        cleaned_string = data_string.strip("[]")  # Remove outer brackets
        coordinate_strings = cleaned_string.split("','")  # Split by delimiter

        points = []
        for coord_string in coordinate_strings:
            try:
                # Step 2: Clean each coordinate string and split into x, y, z
                clean_coord = coord_string.strip(" {}'")
                x, y, z = map(float, clean_coord.split(","))
                points.append((x, y, z))
            except ValueError:
                print(f"Skipping malformed entry: {coord_string}")
                continue

        # Step 3: Create a closed polyline if points are available
        if len(points) > 1:
            points.append(points[0])  # Close the polyline
            polyline = rs.AddPolyline(points)
            polylines.append(polyline)

    return polylines

# Grasshopper Input
if isinstance(x, list):
    # Process the input array and create polylines
    a = create_polylines_from_array(x)
else:
    a = "Input 'x' is not a valid array. Please provide an array of strings."
