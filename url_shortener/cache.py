from pymemcache import serde
from pymemcache.client import base


from url_shortener.settings import SETTINGS

cache = base.Client(SETTINGS.cache_dsn, timeout=5, serde=serde.pickle_serde)
