class SizeFormatter:
    
    def format_size(self, size):
        if size is None:
            return "Unknown"

        units = ["B", "KB", "MB", "GB", "TB"]

        size = float(size)

        for unit in units:
            if size < 1024:
                return f"{size:.2f} {unit}"

            size /= 1024

        return f"{size:.2f} PB"