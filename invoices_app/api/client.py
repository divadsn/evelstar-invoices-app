from io import BytesIO

from httpx import AsyncClient

from invoices_app.api.firebase import FirebaseAuthClient
from invoices_app.api.models import Invoice


class EvelstarAPIClient:
    def __init__(self, auth_client: FirebaseAuthClient, base_url: str = "https://api.evelstar.com/api"):
        """
        Client for Evelstar API
        :param auth_client: Instance of FirebaseAuthClient
        :param base_url: Base URL of the API
        """
        self._auth_client = auth_client
        self._client = AsyncClient(
            base_url=base_url,
            timeout=30,
            headers={
                "User-Agent": "python-evelstar-api/1.0",
                "Referer": "https://app.evelstar.com",
            },
        )

    async def fetch(self, method: str, endpoint_url: str, headers: dict | None = None, auth: bool = True, **kwargs) -> dict:
        """
        Method that fetches data from the API
        :param method: HTTP method
        :param endpoint_url: API endpoint URL
        :param headers: Additional headers
        :param auth: Whether to use the access token for authentication
        :param kwargs: Additional request parameters
        :return: dict
        """
        headers = headers or {}

        if auth:
            headers["Authorization"] = self._auth_client.access_token

        response = await self._client.request(method, endpoint_url, headers=headers, **kwargs)
        response.raise_for_status()

        if response.content:
            return response.json()

    async def get_me(self) -> dict:
        """
        Method that fetches the user's data
        :return: dict
        """
        return await self.fetch("GET", "/v1/users/me")

    async def get_invoices(self, limit: int = 10, page: object = 1, query: str | None = None) -> dict:
        """
        Method that fetches the user's invoices
        :param limit: Number of invoices per page
        :param page: Page number
        :param query: Query string to filter invoices
        :return: dict
        """
        return await self.fetch("GET", "/v1/invoices/user", params={"limit": limit, "page": page, "query": query})

    async def get_invoice(self, invoice_id: str) -> dict:
        """
        Method that fetches the invoice data
        :param invoice_id: Invoice ID
        :return: dict
        """
        return await self.fetch("GET", f"/v1/invoices/{invoice_id}")

    async def upload_invoice(self, file: tuple[str, BytesIO, str], invoice: Invoice) -> dict:
        """
        Method that uploads the invoice to the server
        :param file: Tuple with the file name, file object and file content type
        :param invoice: Invoice details
        :return: dict
        """
        return await self.fetch("POST", "/v1/invoices", files={"file": file}, data=invoice.model_dump(mode="json", by_alias=True))

    async def close(self) -> None:
        """
        Method that closes the client
        """
        await self._client.aclose()
