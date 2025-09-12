import logging

class CustomLogger(logging.Logger):
    logs = []
    def _store(self, level_name: str, msg: str, *args, **kwargs):
        """Helper to store log messages in the list"""
        self.logs.append({
            "message": str(msg) % args if args else str(msg),
            "type": level_name.lower()
        })

    def info(self, msg, *args, **kwargs):
        self._store("INFO", msg, *args, **kwargs)
        super().info(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self._store("ERROR", msg, *args, **kwargs)
        super().error(msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        self._store("DEBUG", msg, *args, **kwargs)
        super().debug(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self._store("WARNING", msg, *args, **kwargs)
        super().warning(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        self._store("CRITICAL", msg, *args, **kwargs)
        super().critical(msg, *args, **kwargs)
