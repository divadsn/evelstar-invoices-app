from httpx import AsyncClient

from invoices_app.api.firebase import FirebaseAuthClient


class EvelstarAPIClient:
    def __init__(self, auth_client: FirebaseAuthClient, base_url: str = "https://api.evelstar.com/api"):
        self._auth_client = auth_client
        self._client = AsyncClient(base_url=base_url)

    async def fetch(self, method: str, endpoint_url: str, headers: dict|None = None, auth: bool = True, **kwargs) -> dict:
        headers = headers or {}

        if auth:
            headers["Authorization"] = self._auth_client.access_token

        response = await self._client.request(method, endpoint_url, headers=headers, **kwargs)
        response.raise_for_status()

        if response.content:
            return response.json()

    async def get_me(self) -> dict:
        return await self.fetch("GET", "/v1/users/me")

    async def get_invoices(self, limit: int = 10, page = 1, query: str|None = None) -> dict:
        return await self.fetch("GET", "/v1/invoices/user", params={"limit": limit, "page": page, "query": query})

    async def get_invoice(self, invoice_id: str) -> dict:
        return await self.fetch("GET", f"/v1/invoices/{invoice_id}")

    async def upload_invoice(self, file_path: str) -> dict:
        pass

    async def close(self):
        await self._client.aclose()
