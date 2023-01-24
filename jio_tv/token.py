import json
import hashlib
import base64
import time
from .settings import BASE_DIR

with open(BASE_DIR / "jio_tv/creds.json", "r") as f:
    creds = json.load(f)

ssoToken = creds["ssoToken"]



def magic(str):
    str = base64.b64encode(hashlib.md5(str.encode()).digest()).decode()
    return str.replace("\n", "").replace("\r", "").replace("/", "_").replace("+", "-").replace("=", "")

def generateToken():
    st = magic(ssoToken)
    pxe = int(time.time() + 6000000)
    jct = magic("cutibeau2ic" + st + str(pxe)).strip()
    return "?jct=" + jct + "&pxe=" + str(pxe) + "&st=" + st

token = generateToken()