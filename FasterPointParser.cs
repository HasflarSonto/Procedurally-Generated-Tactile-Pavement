using System;
using System.Collections.Generic;
using Grasshopper;
using Grasshopper.Kernel.Data;
using Grasshopper.Kernel.Types;
using Rhino.Geometry;

List<Polyline> CreatePolylinesFromDataTree(DataTree<string> dataTree)
{
    List<Polyline> polylines = new List<Polyline>();

    if (dataTree == null || dataTree.PathCount == 0)
    {
        throw new ArgumentException("The input data tree is null or empty.");
    }

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
if (x == null)
{
    throw new ArgumentException("Input 'x' is null. Please provide a valid data tree.");
}

// Cast 'x' to DataTree<string> safely
DataTree<string> dataTree = x as DataTree<string>;

if (dataTree == null)
{
    throw new ArgumentException("Failed to cast input 'x' to DataTree<string>. Check the input type.");
}

// Process the data tree and assign the output
curves = CreatePolylinesFromDataTree(dataTree);  // Replace 'curves' with your Grasshopper output name
