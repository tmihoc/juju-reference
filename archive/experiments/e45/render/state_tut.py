"""Render a state view to SVG (the ggarch CLI has no state command): state.py "View name" out.svg [dark]"""
import sys
from ggarch.parser import parse
from ggarch.state_renderer import render_state
f = parse(open("/home/dora/git/misc/juju-tutorial-diagrams/docs/juju.ggarch").read())
st = next(s for s in f.states if s.name == sys.argv[1])
open(sys.argv[2], "w").write(render_state(st, f.get_model(st.model_name), dark=len(sys.argv) > 3))
