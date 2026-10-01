import requests
from urllib.parse import urlparse, unquote
import re


class FileResolver:

    def resolve(self, url: str) -> dict:

        headers = {
            "User-Agent": "Nexora/1.0"
        }

        response = None

        try:

            # -------------------------
            # 1. Try HEAD
            # -------------------------
            response = requests.head(
                url,
                headers=headers,
                allow_redirects=True,
                timeout=20
            )

            # -------------------------
            # 2. HEAD မရရင် GET
            # -------------------------
            if (
                response.status_code >= 400
                or not response.headers.get("Content-Length")
            ):

                response.close()

                response = requests.get(
                    url,
                    headers=headers,
                    allow_redirects=True,
                    stream=True,
                    timeout=20
                )

            # -------------------------
            # 3. HTTP status
            # -------------------------

            if response.status_code != 200:

                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}",
                    "status": response.status_code
                }

            # -------------------------
            # 4. Headers
            # -------------------------

            content_length = response.headers.get(
                "Content-Length"
            )

            content_type = response.headers.get(
                "Content-Type"
            )

            content_disposition = response.headers.get(
                "Content-Disposition"
            )

            # -------------------------
            # 5. Filename
            # -------------------------

            filename = self._get_filename(
                response.headers,
                response.url
            )

            # -------------------------
            # 6. Range support
            # -------------------------

            accept_ranges = response.headers.get(
                "Accept-Ranges"
            )

            supports_range = (
                accept_ranges.lower() == "bytes"
                if accept_ranges
                else False
            )

            # -------------------------
            # 7. Result
            # -------------------------

            return {
                "success": True,
                "status": response.status_code,
                "original_url": url,
                "final_url": response.url,
                "filename": filename,
                "size": (
                    int(content_length)
                    if content_length
                    else None
                ),
                "content_type": content_type,
                "supports_range": supports_range
            }

        except requests.RequestException as e:

            return {
                "success": False,
                "error": str(e)
            }

        finally:

            if response:
                response.close()

    def _get_filename(self, headers, url):

        # Content-Disposition
        content_disposition = headers.get(
            "Content-Disposition",
            ""
        )

        if content_disposition:

            match = re.search(
                r'filename\*?=(?:UTF-8\'\')?["\']?([^;"\']+)',
                content_disposition,
                re.IGNORECASE
            )

            if match:

                return unquote(
                    match.group(1).strip('"\' ')
                )

        # URL fallback
        path = urlparse(url).path

        filename = path.rstrip("/").split("/")[-1]

        if filename:

            return unquote(filename)

        return None