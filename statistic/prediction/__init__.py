import os
import sys

current_dir = os.path.dirname(__file__)
sys.path.append(current_dir)
from script.model import train_models
from script.draw import draw_feature_importance, draw_heatmap, draw_model_accuracy

train_models()
draw_heatmap()
draw_feature_importance()
draw_model_accuracy()
