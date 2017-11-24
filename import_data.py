import json
from pages.models import *

with open('db.json') as f:
    data = json.load(f)

import_data(data)
