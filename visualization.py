from typing import List, Optional
import pygal
from datetime import date
import cairosvg  # for converting SVG to PNG


def plot_time_series(
    x: List,
    y: List,
    output_file: str,
    title: str = "Time Series Plot",
    x_label: str = "Date",
    y_label: str = "Value",
    line_color: Optional[str] = None,
    show_dots: bool = True,
    width: int = 800,
    height: int = 400,
):
    """
    Generic time-series plotting utility using Pygal (PNG output).

    Args:
        x: List of x-axis values (dates or numbers)
        y: List of y-axis values (numeric)
        output_file: File path to save PNG (must end with .png)
        title: Graph title
        x_label: X-axis label
        y_label: Y-axis label
        line_color: Hex or color name for the line
        show_dots: Whether to show markers for each point
        width: Width of chart in pixels
        height: Height of chart in pixels
    """

    if not output_file.endswith(".png"):
        raise ValueError("output_file must end with .png")

    # Convert dates to strings if needed
    x_labels = [
        xi.strftime("%Y-%m-%d") if isinstance(xi, date) else str(xi) for xi in x
    ]

    line_chart = pygal.Line(
        x_label_rotation=45,
        show_dots=show_dots,
        width=width,
        height=height,
        title=title,
        show_legend=False,
    )
    line_chart.x_labels = x_labels
    line_chart.add(
        y_label, y, stroke_style={"color": line_color} if line_color else None
    )

    # Render to SVG in memory
    svg_data = line_chart.render()

    # Convert SVG to PNG using cairosvg
    cairosvg.svg2png(bytestring=svg_data, write_to=output_file)
