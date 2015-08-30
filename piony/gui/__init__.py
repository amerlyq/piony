import re
import logging
logger = logging.getLogger(__name__)


def fmt(obj):
    return re.compile('^.*\.(\w+\(.*\))').sub(r'\1', str(obj))
