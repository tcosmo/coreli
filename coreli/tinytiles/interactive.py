import copy
import ipywidgets as widgets
from IPython.display import display

from coreli.tinytiles.model import Tiling
from coreli.tinytiles.svg_view import draw_tiling

def interactive(tiling: Tiling):

    first_world = copy.deepcopy(tiling.tiling)
    
    button_step = widgets.Button(description="Step")
    button_steps = widgets.Button(description="All steps")
    button_reset = widgets.Button(description="Reset")
    output = widgets.Output()

    with output:
        output.clear_output(wait=True)
        display(draw_tiling(tiling))

    display(output, widgets.HBox([button_step, button_steps, button_reset]))
    
    def callback_step(b):
        with output:
            output.clear_output(wait=True)
            tiling.step()
            display(draw_tiling(tiling))

    def callback_steps(b):
        with output:
            output.clear_output(wait=True)
            tiling.all_steps()
            display(draw_tiling(tiling))
            
    def callback_reset(b):
        with output:
            output.clear_output(wait=True)
            for p in list(tiling.tiling.keys())[:]:
                del tiling.tiling[p]
            for p in first_world:
                tiling.tiling[p] = first_world[p]
            display(draw_tiling(tiling))
            
    button_step.on_click(callback_step)
    button_steps.on_click(callback_steps)
    button_reset.on_click(callback_reset)