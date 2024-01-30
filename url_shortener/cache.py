from pymemcache import serde
from pymemcache.client import base

from url_shortener.settings import SETTINGS

cache = base.Client(SETTINGS.cache_dsn, connect_timeout=5, timeout=5, serde=serde.pickle_serde, ignore_exc=True)
