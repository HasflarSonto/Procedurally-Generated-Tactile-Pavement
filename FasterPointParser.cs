using System;
using System.Collections.Generic;
using Rhino.Geometry;

List<Polyline> CreatePolylinesFromArray(string[] inputArray)
{
    List<Polyline> polylines = new List<Polyline>();

    foreach (string item in inputArray)
    {
        if (string.IsNullOrWhiteSpace(item)) continue;

        try
        {
            // Split the string into coordinate groups if needed
            string[] groups = item.Split(new[] { "}, {" }, StringSplitOptions.RemoveEmptyEntries);

            List<Point3d> points = new List<Point3d>();

            foreach (string group in groups)
            {
                // Clean and parse each coordinate group
                string cleanGroup = group.Trim(new char[] { '{', '}', '[', ']', ' ' });
                string[] coords = cleanGroup.Split(',');

                if (coords.Length == 3)
                {
                    double x = double.Parse(coords[0]);
                    double y = double.Parse(coords[1]);
                    double z = double.Parse(coords[2]);

                    points.Add(new Point3d(x, y, z));
                }
            }

            if (points.Count > 1)
            {
                // Close the polyline by adding the first point to the end
                points.Add(points[0]);
                polylines.Add(new Polyline(points));
            }
        }
        catch
        {
            // Skip malformed items and log the issue
            Rhino.RhinoApp.WriteLine($"Skipped malformed entry: {item}");
            continue;
        }
    }

    return polylines;
}

// Grasshopper Input
Rhino.RhinoApp.WriteLine($"Input 'x' type: {x?.GetType()}");  // Inspect the type of the input

if (x is string[] inputArray)
{
    // If the input is an array, process it directly
    curves = CreatePolylinesFromArray(inputArray);
}
else
{
    throw new ArgumentException("Input 'x' is not a valid string array. Please check the input format.");
}
