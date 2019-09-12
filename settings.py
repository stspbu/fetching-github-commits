import json
import threading

__all__ = ('get', 'set')


def get(name, default=None):
    val = settings.get(name)
    if val is None:
        val = default

    return val


def set(key, value):
    settings[key] = value

    with _lock:
        with open('settings.json', 'w+') as f:
            f.write(json.dumps(settings, indent=4))


def _load():
    with open('settings.json', 'a+') as f:
        f.seek(0)
        data = f.read()
        loaded_settings = json.loads(data) if data else {}

    return loaded_settings


_lock = threading.Lock()
settings = _load()
