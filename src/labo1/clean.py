import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backend_bases import MouseButton


class Remover:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.indices_to_remove = []
        self.init_plot()
        self.connect()

    def connect(self):
        self.fig.canvas.mpl_connect("button_press_event", self.on_click)
        self.fig.canvas.mpl_connect("motion_notify_event", self.on_motion)

    def on_motion(self, event):
        if event.button is MouseButton.LEFT:
            self.append_closest(event.xdata, event.ydata)
        elif event.button is MouseButton.RIGHT:
            self.remove_closest(event.xdata, event.ydata)
        self.update_plot()

    def on_click(self, event):
        if event.button is MouseButton.LEFT:
            self.append_closest(event.xdata, event.ydata)
        elif event.button is MouseButton.RIGHT:
            self.remove_closest(event.xdata, event.ydata)
        self.update_plot()

    def append_closest(self, xmouse, ymouse):
        idx = self.find_index_closest(xmouse, ymouse)
        if idx not in self.indices_to_remove:
            self.indices_to_remove.append(idx)

    def remove_closest(self, xmouse, ymouse):
        idx = self.find_index_closest(xmouse, ymouse)
        if idx in self.indices_to_remove:
            self.indices_to_remove.pop(self.indices_to_remove.index(idx))

    def init_plot(self):
        self.fig, self.ax = plt.subplots()
        self.ax.plot(self.x, self.y, ".-", zorder=1)
        self.sc = self.ax.scatter([], [], color="C1", zorder=2, label="Outliers")
        plt.legend()

    def update_plot(self):
        if self.indices_to_remove:
            self.sc.set_offsets(
                list(
                    zip(
                        self.x[self.indices_to_remove],
                        self.y[self.indices_to_remove],
                    )
                )
            )
        else:
            self.sc.set_offsets(np.empty((0, 2)))
        self.fig.canvas.draw()

    def find_index_closest(self, xmouse, ymouse):
        distances = (self.x - xmouse) ** 2 + (self.y - ymouse) ** 2
        return np.where(distances == np.min(distances))[0][0]

    def get_cleaned_data(self):
        plt.show()
        xidx = np.arange(len(self.x))
        idx = np.in1d(xidx, self.indices_to_remove, invert=True)
        return self.x[idx], self.y[idx]


def remove_outliers(x: np.ndarray, y: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """An easy to use GUI to remove outliers from data. 
    Left click to mark outliers, right click to unmark.

    Parameters:
        x: A numpy 1d array with the x axis data.
        y: a numpy 1d array with the y axis data.

    Returns:
        Two numpy 1d arrays with the x and y data without the marked outliers.
    """
    remover = Remover(x, y)
    x, y = remover.get_cleaned_data()
    return x, y
