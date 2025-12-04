from json import loads
import os
from subprocess import PIPE, run

CONFIG = loads(run(["nix", "eval", "--json", "--file", os.path.dirname(__file__)+"/../../config/zedless-config.nix"], stdout=PIPE).stdout.decode())
