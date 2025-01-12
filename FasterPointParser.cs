using System;
using System.Collections.Generic;
using Rhino.Geometry;

private List<Polyline> CreatePolylinesFromDataTree(List<List<string>> dataTree)
{
    List<Polyline> polylines = new List<Polyline>();

    foreach (var branch in dataTree)
    {
        List<Point3d> points = new List<Point3d>();

        foreach (var item in branch)
        {
            try
            {
                // Clean and parse the coordinate string
                string cleanItem = item.Trim(new char[] { '{', '}', '[', ']', ' ' });
                string[] coords = cleanItem.Split(',');

                if (coords.Length == 3)
                {
                    double x = double.Parse(coords[0]);
                    double y = double.Parse(coords[1]);
                    double z = double.Parse(coords[2]);

                    points.Add(new Point3d(x, y, z));
                }
            }
            catch
            {
                // Skip malformed items
                continue;
            }
        }

        if (points.Count > 1)
        {
            // Close the polyline by adding the first point to the end
            points.Add(points[0]);
            polylines.Add(new Polyline(points));
        }
    }

    return polylines;
}

// Grasshopper Inputs
// 'x' is a DataTree<string> containing coordinate strings

// Convert the input DataTree into a C# List<List<string>>
List<List<string>> dataTree = new List<List<string>>();

foreach (var path in x.Paths)
{
    List<string> branch = new List<string>(x.Branch(path));
    dataTree.Add(branch);
}

// Process the data tree and create polylines
A = CreatePolylinesFromDataTree(dataTree);  // Output polylines to 'A'
