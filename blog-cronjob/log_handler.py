import json
import logging

class LambdaLogger:
    def __init__(self, level=logging.INFO):
        self.logger = logging.getLogger()
        self.logger.setLevel(level)

    def log(self, level, message, log_type="application", context=None, event=None):
        log_data = {
            "level": level,
            "message": message,
            "log_type": log_type
        }
        if context:
            log_data.update({
                "function_name": context.function_name,
                "memory_limit_in_mb": context.memory_limit_in_mb,
                "log_stream_name": context.log_stream_name,
                "log_group_name": context.log_group_name,
                "aws_request_id": context.aws_request_id
            })
        if event:
            log_data["event"] = event

        self.logger.log(level, json.dumps(log_data))

    def info(self, message, log_type="application", context=None, event=None):
        self.log(logging.INFO, message, log_type, context, event)

    def error(self, message, log_type="application", context=None, event=None):
        self.log(logging.ERROR, message, log_type, context, event)

    def warning(self, message, log_type="application", context=None, event=None):
        self.log(logging.WARNING, message, log_type, context, event)

    def debug(self, message, log_type="application", context=None, event=None):
        self.log(logging.DEBUG, message, log_type, context, event)