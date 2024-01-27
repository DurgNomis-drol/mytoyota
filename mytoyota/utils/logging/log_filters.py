"""Module with filter log filter classes."""
import logging
import re


class RedactingFilter(logging.Filter):
    """Helper class to filter logs by given pattern via 'logging.Filter'."""

    def __init__(self, patterns):
        """Initialise RedactingFilter class."""
        super(RedactingFilter, self).__init__()
        self._patterns = patterns

    def filter(self, record):
        """Modify the log record to mask sensitive data."""
        record.msg = self.mask_sensitive_data(record.msg)
        return True

    def mask_sensitive_data(self, msg):
        """Mask sensitive data in logs by given patterns."""
        for pattern in self._patterns:
            compiled_pattern = re.compile(pattern)
            msg = compiled_pattern.sub("****", str(msg))
        return msg
