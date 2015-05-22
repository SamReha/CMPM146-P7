import subprocess
import json
import collections
import random
import sys

# Helper Functions
def parse_json_result(out):
    """Parse the provided JSON text and extract a dict
    representing the predicates described in the first solver result."""

    result = json.loads(out)
    
    assert len(result['Call']) > 0
    assert len(result['Call'][0]['Witnesses']) > 0
    
    witness = result['Call'][0]['Witnesses'][0]['Value']
    
    class identitydefaultdict(collections.defaultdict):
        def __missing__(self, key):
            return key
    
    preds = collections.defaultdict(set)
    env = identitydefaultdict()
    
    for atom in witness:
        if '(' in atom:
            left = atom.index('(')
            functor = atom[:left]
            arg_string = atom[left:]
            try:
                preds[functor].add( eval(arg_string, env) )
            except TypeError:
                pass # at least we tried...
            
        else:
            preds[atom] = True
    
    return dict(preds) 
    
def solve():
    """Run clingo with the provided argument list and return the parsed JSON result."""
    print "About to Gringo!"
    gringo = subprocess.Popen(['clingo\gringo', 'level-core.lp', 'level-style.lp', 'level-sim.lp', 'level-shortcuts.lp'], stdout=subprocess.PIPE, shell=True)
    #gringo = subprocess.Popen(['clingo\gringo', 'meta.lp', 'metaD.lp', 'metaO.lp', 'metaS.lp'], stdout=subprocess.PIPE, shell=True)
    print "About to Reify!"
    reify = subprocess.Popen(['clingo\\reify'], stdin=gringo.stdout, stdout=subprocess.PIPE, shell=True)
    print "About to Clingo!"
    #clingo = subprocess.Popen(['clingo\clingo', 'meta.lp', 'metaD.lp', 'metaO.lp', 'metaS.lp', '--outf=2'], stdin=reify.stdout, stdout=subprocess.PIPE, shell=True)
    clingo = subprocess.Popen(['clingo\clingo', 'level-core.lp', 'level-style.lp', 'level-sim.lp', '--outf=2'], stdin=reify.stdout, stdout=subprocess.PIPE, shell=True)
    out, err = clingo.communicate()
    if err:
        print "ERR: " + err
        
    #print "OUT: " + out
        
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
design = solve()
print render_ascii_dungeon(design)