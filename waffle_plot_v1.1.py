import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import LinearSegmentedColormap


def waffle_plot(
    categories,
    values,
    width=10,
    height=10,
    cmap=plt.cm.viridis,
    c=None,
    bc="w",
    autoscale=True,
    over_represent=False,
    vertical=True,
    label_v=True,
    label_p=False,
    legend_ncols=1,
    legend_loc=(1.35, 0.685),
    figsize=(6.4, 4.8),
    value_sign="",
    font="DejaVu Sans",
    fontsize=10,
    font_c="black",
    save=None,
):

    """
    Makes a waffle plot, a customized matshow plot that represents
    the proportions of different categories.

    Parameters:
    ----------
    categories: array-like
        A collection of categories.
    values: array-like
        A collection of values corresponding to the categories.
    width : int, default: 10
        The width of the waffle plot in number of tiles.
    height : int, default: 10
        The height of the waffle plot in number of tiles.
    cmap : matplotlib colormap, default: plt.cm.viridis
        The colormap to use for generating colors for the categories.
    c : array-like or list of colors or color, optional
        Possible values:
        - A scalar or sequence of n numbers to be mapped to colors
        - A 2D array in which the rows are RGB or RGBA.
        - A sequence of colors of length n.
        - A single color format string.
        A collection of colors to be used for the tiles of the different
        categories. If not provided, colors will be generated from the cmap.
        If 'c' is shorter then 'categories', the missing colors will be
        taken from cmap.
    bc : str, default: 'white'
        The background color of the plot and the grid.
    autoscale : bool, default: True
        Whether to adjust the width and height of the plot to ensure that
        all categories are represented by at least one tile. If autoscale
        is True, the number of patches will grow until it can accomodate
        the smallest non-zero value from values.
    over_represent : bool, default: False
        Whether to over-represent the proportions by using extra tiles for
        the same category. If the smallest category has one tile and fills
        less than 50% of it, if over_represent is True, the tile will still
        have the category color. If over_represent is False, the tile will
        adopt the color of the background.
    vertical : bool, default: True
        Whether to stack the tiles vertically (True) or horizontally (False).
    label_v : bool, default: True
        Whether to label the tiles with the corresponding values.
        When True, it add value in brackets to the legend.
    label_p : bool, default: False
        Whether to label the tiles with the corresponding proportions.
        When True, the function calculates the percentage of the value and
        adds it in brackets to the legend. When both label_v and label_p
        are True, it will add both, value after colon and percentage
        in brackets.
    legend_ncols : int, default: 1
        The number of columns to use in the legend.
        To make flat horizontal Legend, it should equal the number
        of categories.
    legend_loc : tuple, default: (1.35, 0.695)
        The location of the legend as a tuple of x and y coordinates.
    figsize : tuple, default: (6.4, 4.8)
        The size of the figure as a tuple of width and height in inches.
    value_sign : str, default: ''
        A string to be used as a suffix for the value in the legend.
    font : str, default: 'DejaVu Sans'
        The font to be used for the labels in the legend.
    font_c : str, default: 'black'
        The color of the font to be used for the labels in the legend.
    save : str, optional
        The file name and path to save the plot to. If None, plt.show()
        is used instead.

    Returns:
    -------
    matplotlib.figure.Figure
        The figure object of the waffle plot.

    """

    # Getting sorted categories and values
    categories, values = zip(
        *sorted(zip(categories, values), key=lambda x: x[1], reverse=True)
    )

    # Getting number of categories
    n_categories = len(categories)

    cmap = cmap.resampled(len(categories))

    if c is None:

        c = [cmap(x) for x in range(len(categories))]

    else:
        # If there are fewer colors than categories...
        if len(c) < len(categories):
            # Extend list c with appropriate number of colors from colormap
            c.extend([cmap(x) for x in range(len(categories))][len(c) :])

        if len(c) > len(categories):
            # Cutting colour list in case we have more colours than categories
            c = c[:n_categories]

    proportions_cmap = [(float(v) / sum(values)) for v in values if v > 0]

    # condition variable for 'while' loop for auto-scaling
    condition = False

    while condition is not True:

        total = width * height

        tiles_per_category = [
            round(proportion * total) for proportion in proportions_cmap
        ]

        # Make a dummy matrix for use in plotting.
        waffle = [[0 for col in range(width)] for row in range(height)]

        # Popoulate the dummy matrix with integer values.
        category_index = 0
        tile_index = 0

        if vertical:
            x = width # i is a row
            y = height # j is a col
        else:
            x = height # i is a col
            y = width # j is a row

        # Iterate over each tile.
        for i in range(x):
            for j in range(y):
                tile_index += 1

                # If the number of tiles populated is sufficient for 
                # this category...
                if tile_index > sum(tiles_per_category[0:category_index]):
                    # ...increment to the next category.
                    category_index += 1

                # Set the category value to an integer, which increases 
                # with category.
                if vertical:
                    waffle[j][i] = category_index
                else:
                    waffle[i][j] = category_index

        if len(set([item for sublist in waffle for item in sublist])) < len(
            proportions_cmap
        ):

            if autoscale:
                condition = False
                width += 1
                height += 1
            else:
                condition = True
        else:
            condition = True

    # Getting number of bins. We don't need bins for empty (== 0) categories, 
    # we are only counting non-zero values
    n_bins = len([val for val in values if val != 0])

    if autoscale is False:
        # If number of unique values in waffle is smaller than number of bins,
        # reduce number of bins
        if len(set([i for sublist in waffle for i in sublist])) < n_bins:
            n_bins = len(set([i for sublist in waffle for i in sublist]))

    # Instead of 'c', using special version 'c_for_cmap', that is cut at 
    # the length equal to number of bins
    c_for_cmap = c[:n_bins]

    if not over_represent and len(c_for_cmap) == len(
        [val for val in values if val != 0]
    ):
        for i in proportions_cmap:
            if i < 0.5 * (1 / (height * width)):
                c_for_cmap[-1] = bc

    if any(values) != 0:

        # Constructing colormap
        cmap_name = "the_cmap"
        cmap = LinearSegmentedColormap.from_list(
            cmap_name, c_for_cmap, N=n_bins)

        # Compute the portion of the total assigned to each category.
        proportions = [(value / sum(values)) for value in values]

    else:
        proportions = [1 for v in values] # Just so it does not throw an error

    # Grid line auto-adjustment
    if height < 25 and width < 25:
        linewidth = 1
    else:
        linewidth = 0.5

    # Create a new figure and ax
    fig, ax = plt.subplots(figsize=figsize, facecolor=bc)

    if len(c_for_cmap) > 1:
        # Visualisng the waffle array as waffle plot
        ax.matshow(waffle, cmap=cmap)
    else:
        # Visualisng the waffle array as waffle plot, only transparent
        ax.matshow(waffle, alpha=0)

    # With colours control, to not get an empty plot for only one not empty 
    # category, a facecolor has to be set. Same for the special case of
    # empty waffle.

    if len(c_for_cmap) < 1:
        ax.set_facecolor("lightgrey")
    elif len(c_for_cmap) < 2:
        ax.set_facecolor(c[0])

    # Minor ticks
    ax.set_xticks([x - 0.5 for x in range(width)], minor=True)
    ax.set_yticks([x - 0.5 for x in range(height)], minor=True)

    # Switch the sticking out ticks off (by setting length to 0):
    ax.tick_params(axis="both", which="both", length=0)

    # Gridlines based on minor ticks
    ax.grid(which="minor", color=bc, linestyle="-", linewidth=linewidth)

    # Switch off the numbers associated with ticks
    plt.xticks([])
    plt.yticks([])

    # variables for the legend
    values_cumsum = [sum(values[: i + 1]) for i in range(len(values))]
    total_values = values_cumsum[len(values_cumsum) - 1]

    # Empty list, that will be filled with legend handles
    legend_handles = []

    # Constructing the legend. Depending on the controls, it can have:

    for i, (category, colour) in enumerate(zip(categories, c)):
        if label_v and not label_p: # Values only, with the sign or without it
            if value_sign == "%":
                label_str = f"{category} ({values[i]}{value_sign})"
            else:
                label_str = f"{category} ({value_sign}{values[i]})"

        elif label_v and label_p: #Values and percentages calculated automatically
            if value_sign == "%":
                label_str = (
                    f"{category}: {values[i]}{value_sign} ({proportions[i] * 100:.2f}%)"
                )
            else:
                label_str = (
                    f"{category}: {value_sign}{values[i]} ({proportions[i] * 100:.2f}%)"
                )

        elif not label_v and label_p: # only percentages calculated automatically
            label_str = f"{category} ({proportions[i] * 100:.2f}%)"

        if not label_v and not label_p: # The name of the category only
            label_str = f"{category}"
            
        legend_handles.append(mpatches.Patch(color=c[i], label=label_str))

    # Add the legend
    l = ax.legend(
        handles=legend_handles,
        loc="lower center",
        ncol=legend_ncols,
        labelcolor=font_c,
        bbox_to_anchor=legend_loc,
    )

    # Font controls for the legend
    plt.setp(l.texts, family=font, fontsize=fontsize)

    # Option to save an image
    if save is not None:
        plt.savefig(save, bbox_inches="tight", dpi=300)

    else:
        plt.show()
