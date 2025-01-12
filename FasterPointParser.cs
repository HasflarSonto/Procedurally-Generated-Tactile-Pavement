using System;
using System.Collections.Generic;
using Rhino.Geometry;

List<Polyline> CreatePolylinesFromArray(string[] inputArray)
{
    List<Polyline> polylines = new List<Polyline>();

    foreach (string inputData in inputArray)
    {
        if (string.IsNullOrWhiteSpace(inputData)) continue;

        // Clean and prepare the input string
        string cleanedData = inputData.Trim(new char[] { '[', ']' }); // Remove outer brackets
        string[] coordinateGroups = cleanedData.Split(new string[] { "','" }, StringSplitOptions.RemoveEmptyEntries);

        List<Point3d> points = new List<Point3d>();

        foreach (string coordString in coordinateGroups)
        {
            try
            {
                // Parse each coordinate string
                string cleanCoord = coordString.Trim(new char[] { '{', '}', ' ', '\'' });
                string[] parts = cleanCoord.Split(',');

                if (parts.Length == 3)
                {
                    // Convert to numeric values
                    double x = double.Parse(parts[0]);
                    double y = double.Parse(parts[1]);
                    double z = double.Parse(parts[2]);

                    // Add the point to the list
                    points.Add(new Point3d(x, y, z));
                }
            }
            catch
            {
                // Skip malformed entries
                Rhino.RhinoApp.WriteLine($"Skipping malformed entry: {coordString}");
                continue;
            }
        }

        // Create a polyline if points are available
        if (points.Count > 1)
        {
            // Close the polyline by adding the first point to the end
            points.Add(points[0]);
            polylines.Add(new Polyline(points));
        }
    }

    return polylines;
}

// Grasshopper Input
if (x is string[] inputArray)
{
    // If the input is an array, process it
    curves = CreatePolylinesFromArray(inputArray); // Replace 'curves' with the output name in your Grasshopper script
}
else
{
    throw new ArgumentException("Input 'x' is not a valid string array. Please check the input format.");
}
