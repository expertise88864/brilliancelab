import re, sys

# --- Auto-locate the repo root so this script can be run from anywhere ---
import os as _os, pathlib as _pl
_os.chdir(_pl.Path(__file__).resolve().parents[2])  # → BrillianceLab/
# -------------------------------------------------------------------------

src = open('blog/blog-shared.js', encoding='utf-8').read()
# Strip block comments, line comments, then strings
clean = re.sub(r'/\*[\s\S]*?\*/', '', src)
clean = re.sub(r'(?m)//[^\n]*', '', clean)
clean = re.sub(r"'(?:[^'\\\n]|\\.)*'", "''", clean)
clean = re.sub(r'"(?:[^"\\\n]|\\.)*"', '""', clean)
clean = re.sub(r'`(?:[^`\\]|\\.)*`', '``', clean)
print('{:>6} open {:>6} close'.format(clean.count('{'), clean.count('}')))
print('{:>6} (    {:>6} )'.format(clean.count('('), clean.count(')')))
print('{:>6} [    {:>6} ]'.format(clean.count('['), clean.count(']')))
