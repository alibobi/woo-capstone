from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


limiter = Limiter(key_func=get_remote_address, default_limits=["300 per hour", "50 per minute", "5 per second"])
