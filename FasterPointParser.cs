using System;
using System.Collections.Generic;
using Grasshopper;
using Grasshopper.Kernel.Data;
using Grasshopper.Kernel.Types;
using Rhino.Geometry;

List<Polyline> CreatePolylinesFromDataTree(DataTree<string> dataTree)
{
    List<Polyline> polylines = new List<Polyline>();

    foreach (GH_Path path in dataTree.Paths)
    {
        List<Point3d> points = new List<Point3d>();

        foreach (string item in dataTree.Branch(path))
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
// Cast 'x' to DataTree<string>
DataTree<string> dataTree = x as DataTree<string>;

// Process the data tree and create polylines
A = CreatePolylinesFromDataTree(dataTree);  // Assign result to output 'A'
