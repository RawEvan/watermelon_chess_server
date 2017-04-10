import os
import pylibmc
import sys
import sae
from xiguaqi import wsgi

root = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(root, 'site-packages'))
sys.modules['memcache'] = pylibmc

application = sae.create_wsgi_app(wsgi.application)