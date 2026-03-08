import logging

class CustomLogger(logging.Logger):
    def __init__(self, name, level=logging.NOTSET):
        super().__init__(name, level)
        self.logs = []  # Variable for osdag-web
    
    def _store(self, level_name: str, msg: str, *args, **kwargs):
        """Helper to store log messages in the list"""
        # Handle both % formatting and .format() style
        try:
            formatted_msg = str(msg) % args if args else str(msg)
        except (TypeError, ValueError):
            # Fallback if formatting fails
            formatted_msg = str(msg)
        
        self.logs.append({
            "message": formatted_msg,
            "type": level_name.lower(),
            "timestamp": self.getCurrentTime()
        })
    
    def getCurrentTime(self):
        """Get current timestamp for logging"""
        import datetime
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

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
    
    def get_logs(self):
        """Method to retrieve stored logs"""
        return self.logs
    
    def clear_logs(self):
        """Method to clear stored logs"""
        self.logs.clear()