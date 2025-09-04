# environment.py
from listenerclass import CustomListener

def before_all(context):
    context.listener = CustomListener()
    if hasattr(context.listener, "before_all"):
        context.listener.before_all(context)

def after_all(context):
    if hasattr(context, "listener") and hasattr(context.listener, "after_all"):
        context.listener.after_all(context)

def before_feature(context, feature):
    if hasattr(context.listener, "before_feature"):
        context.listener.before_feature(context, feature)

def after_feature(context, feature):
    if hasattr(context.listener, "after_feature"):
        context.listener.after_feature(context, feature)

def before_scenario(context, scenario):
    if hasattr(context.listener, "before_scenario"):
        context.listener.before_scenario(context, scenario)

def after_scenario(context, scenario):
    if hasattr(context.listener, "after_scenario"):
        context.listener.after_scenario(context, scenario)

def before_step(context, step):
    if hasattr(context.listener, "before_step"):
        context.listener.before_step(context, step)

def after_step(context, step):
    if hasattr(context.listener, "after_step"):
        context.listener.after_step(context, step)
