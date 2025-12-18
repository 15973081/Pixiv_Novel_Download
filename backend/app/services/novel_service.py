from ..utils.http import http_client
import json
import re

class NovelService:
    BASE_URL = "https://www.pixiv.net/ajax"

    def search(self, keyword: str, page: int = 1):
        """
        Search novels by keyword
        """
        url = f"{self.BASE_URL}/search/novels/{keyword}"
        params = {
            "word": keyword,
            "p": page,
            "s_mode": "s_tag",  # s_tag (tags), s_tc (title/caption)
            "order": "date_d",  # date_d (newest), date (oldest)
            "mode": "all",      # all, r18
        }
        try:
            response = http_client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            if data["error"]:
                return {"error": data["message"]}
            return data["body"]
        except Exception as e:
            import traceback
            print(f"Error in search: {e}")
            traceback.print_exc()
            return {"error": str(e)}

    def get_info(self, novel_id: str):
        """
        Get novel metadata
        """
        url = f"{self.BASE_URL}/novel/{novel_id}"
        try:
            response = http_client.get(url)
            response.raise_for_status()
            data = response.json()
            if data["error"]:
                return {"error": data["message"]}
            return data["body"]
        except Exception as e:
            return {"error": str(e)}

    def get_content(self, novel_id: str):
        """
        Get novel content (text)
        Pixiv novel content is usually in the 'content' field of the info API,
        or sometimes paginated. For now, we assume it's in the info API.
        """
        info = self.get_info(novel_id)
        if "error" in info:
            return info
        
        # Parse content from info
        # The 'content' field contains the raw text with special formatting
        content = info.get("content", "")
        title = info.get("title", "Untitled")
        author = info.get("userName", "Unknown")
        
        return {
            "id": novel_id,
            "title": title,
            "author": author,
            "content": content
        }

    def download(self, novel_id: str, format: str = "txt"):
        """
        Download novel and return formatted content
        """
        data = self.get_content(novel_id)
        if "error" in data:
            return data
            
        content = data["content"]
        title = data["title"]
        author = data["author"]

        # Simple cleaning/formatting
        # Replace [newpage] with actual page breaks or markers
        content = content.replace("[newpage]", "\n\n========== Next Page ==========\n\n")
        
        if format == "txt":
            full_text = f"Title: {title}\nAuthor: {author}\n\n{content}"
            return {
                "filename": f"{title}.txt",
                "content": full_text,
                "type": "text/plain"
            }
        
        return {"error": "Unsupported format"}

    def get_series_info(self, series_id: str) -> dict:
        url = f"{self.BASE_URL}/novel/series/{series_id}"
        try:
            resp = http_client.get(url)
            resp.raise_for_status()
            data = resp.json()

            if data.get("error"):
                return {"error": data.get("message")}

            body = data["body"]

            return {
                "id": body["id"],
                "title": body["title"],
                "userId": body["userId"],
                "userName": body["userName"],
                "caption": body.get("caption", ""),
                "tags": body.get("tags", []),
                "isConcluded": body.get("isConcluded"),
                "displaySeriesContentCount": body.get("displaySeriesContentCount", 0),
                "cover": body.get("cover", {}).get("urls", {}).get("original"),
                "createDate": body.get("createDate"),
                "updateDate": body.get("updateDate"),
            }
        except Exception as e:
            return {"error": str(e)}

    # =====================
    # Series Content (分页)
    # =====================
    def get_series_content(
            self,
            series_id: str,
            offset: int = 0,
            limit: int = 30
    ) -> dict:
        """
        返回单页 series 内容（不做循环）
        """
        url = (
            f"{self.BASE_URL}/novel/series_content/"
            f"{series_id}"
            f"?limit={limit}&last_order={offset}&order_by=asc"
        )

        try:
            resp = http_client.get(url)
            resp.raise_for_status()
            data = resp.json()

            if data.get("error"):
                return {"error": data.get("message")}

            page = data["body"]["page"]

            return {
                "seriesContents": page.get("seriesContents", []),
                "isLastPage": page.get("isLastPage", False),
            }
        except Exception as e:
            return {"error": str(e)}

novel_service = NovelService()
