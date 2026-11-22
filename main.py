import os
import shutil

here = os.path.dirname(os.path.abspath(__file__))
out = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
os.makedirs(out, exist_ok=True)
shutil.copy(os.path.join(here, "entry.png"), os.path.join(out, "entry.png"))
print("copied entry.png to", out)

