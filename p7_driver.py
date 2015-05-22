import subprocess
import json
import collections
import random
import sys

# Helper Functions
def solve(*args):
    """Run clingo with the provided argument list and return the parsed JSON result."""
    
    CLINGO = "./clingo-4.5.0-macos-10.9/clingo"
    
    clingo = subprocess.Popen(
        [CLINGO, "--outf=2"] + list(args),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    out, err = clingo.communicate()
    if err:
        print err
        
    return parse_json_result(out)
    
def render_ascii_dungeon(design):
    """Given a dict of predicates, return an ASCII-art depiction of the a dungeon."""
    
    sprite = dict(design['sprite'])
    param = dict(design['param'])
    width = param['width']
    glyph = dict(space='.', wall='W', altar='a', gem='g', trap='_')
    block = ''.join([''.join([glyph[sprite.get((r,c),'space')]+' ' for c in range(width)])+'\n' for r in range(width)])
    return block
    
# Generate the dungeon and draw it to the console
with open(sys.argv[1]) as myfile:
    data = myfile.read().replace('\n', '')

design = solve(sys.argv)
print render_ascii_dungeon(design)