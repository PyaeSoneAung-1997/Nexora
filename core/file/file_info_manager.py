from core.file.file_resolver import FileResolver

class FileInfoManager:

    def __init__(self):
        self.resolver = FileResolver()

    def get_info(self,url: str) -> dict:
        result = self.resolver.resolve(url)

        if not result["success"]:
            return result

        return {
            "success": True,
            "filename": result.get("filename"),
            "size": result.get("size"),
            "content_type": result.get("content_type"),
            "supports_range": result.get("supports_range"),
            "original_url": result.get("original_url"),
            "final_url": result.get("final_url")
        }