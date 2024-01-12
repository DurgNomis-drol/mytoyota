"""Module with filter log filter classes."""
import logging


class RedactingFilter(logging.Filter):
    """Helper class to filter logs by given pattern via 'logging.Filter'."""

    def __init__(self, patterns):
        """Initialise RedactingFilter class."""
        super(RedactingFilter, self).__init__()
        self._patterns = patterns

    def filter(self, record):
        """Modify the log record to mask sensitive data."""
        record.msg = self.redact(record.msg)
        if isinstance(record.args, dict):
            for k in record.args.keys():
                record.args[k] = self.redact(record.args[k])
        else:
            record.args = tuple(self.redact(arg) for arg in record.args)
        return True

    def redact(self, msg):
        """Redact logs by given patterns."""
        msg = isinstance(msg, str) and msg or str(msg)
        for pattern in self._patterns:
            msg = msg.replace(pattern, "<<***>>")
        return msg
