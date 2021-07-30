import seaborn as sns
import matplotlib
from bokeh.plotting import figure
from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource, HoverTool, Panel, Tabs
from bokeh.layouts import gridplot
import tempfile
from pathlib import Path
from tqdm import tqdm

DEFAULT_WIDTH = 800#1200
DEFAULT_HEIGHT = 400#600


def plot_multi_data(dfs, title='', out_put_path=None, add_tools=True, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT):
    panels = []
    x_range, y_range = None, None
    for header, df in tqdm(dfs.items()):
        p = _get_data_figure(df, add_tools, height, width, title=header,
                             x_range=x_range, y_range=y_range)

        x_range = x_range or p.x_range
        y_range = y_range or p.y_range

        panels.append((p, header))

    _ = _set_output_file(title, out_put_path)

    # tabs = Tabs(tabs=[Panel(tabs=p, title=header) for p, header in panels])
    # show(tabs)

    grid = gridplot([[p] for p, header in panels], )
    show(grid)


def plot_data(df, title='', out_put_path=None, add_tools=True, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT):
    p = _get_data_figure( df, add_tools, height, width, title=title)
    _ = _set_output_file(title, out_put_path)
    show(p)



    # median_path = _path.parent / 'median.jpg'
    # if median_path.exists():
    #     fig, ax = plt.subplots(figsize=(20, 10))
    #     img = mpimg.imread(str(median_path))
    #     imgplot = plt.imshow(img, 'gray')
    #     plt.show()

    # plt.figure()
    # ax = sns.lineplot('x', 'y', hue='id',data=df)
    # ax.set_title(title)
    # ax.figure.show()


def _set_output_file(title, out_put_path=None):
    if not out_put_path:
        tmp_dir = Path(tempfile.gettempdir())
        # noinspection PyProtectedMember
        out_put_path = str(tmp_dir / f'plot_{title}_{next(tempfile._get_candidate_names())}.html')
    output_file(out_put_path, title=title)
    return out_put_path


def _get_data_figure(df, add_tools,  plot_height, plot_width, title='', x_range=None, y_range=None):
    left, right = 0, df.x.max()
    bottom, top = 0, df.y.max()

    _x_range = x_range or (left, right)
    _y_range = y_range or (top, bottom)

    p = figure(plot_width=plot_width, plot_height=plot_height, x_axis_location="above",
               x_range=_x_range, y_range=_y_range, title=title)
    ids = df.id.drop_duplicates()
    palette = sns.color_palette("hls", len(ids))
    # noinspection PyUnresolvedReferences
    hex_platte = [matplotlib.colors.to_hex(rgb) for rgb in palette]
    colors = dict(zip(ids, hex_platte))
    for curr_id, curr_df in df.groupby('id'):
        source = ColumnDataSource(curr_df)
        color = colors[curr_id]

        legend = curr_df.label.values[0]  # str(curr_id)
        p.circle(x='x', y='y', source=source, legend=legend, color=color, muted_color=color, muted_alpha=0.1, alpha=0.5,
                 muted=True)
    if add_tools:
        # tooltips=[(clm, f'@{clm}') for clm in df.columns]
        tooltips = [('id', '@id'), ('Frame', '@frame'), ('(X, Y)', '(@x, @y)'), ('(W, H)', '(@w, @h)'),
                    ('angle', '@angle'),
                    ('distance', '@distance'), ('Label', '@label')]
        hover_tool = HoverTool(tooltips=tooltips, )

        p.add_tools(hover_tool)
    p.legend.click_policy = "mute"
    return p
