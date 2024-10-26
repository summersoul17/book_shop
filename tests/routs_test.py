import pytest
from httpx import AsyncClient, ASGITransport
from starlette import status

from src.database.models import BookGenre
from src.main import app

@pytest.mark.asyncio
async def test_create_delete_book_and_author():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test", follow_redirects=True) as ac:
        author_response = await ac.post(
            "/api/authors",
            json={
                "title": "Author"
            }
        )
        assert author_response.status_code == status.HTTP_200_OK
        assert author_response.json()["title"] == "Author"
        author_id = author_response.json()["id"]

        book_response = await ac.post(
            "/api/books",
            json={
                "title": "Book",
                "author_id": author_id,
                "genre": BookGenre.FANTASY,
                "count": 20,
                "description": "Description"
            }
        )

        assert book_response.status_code == status.HTTP_200_OK
        assert book_response.json()["title"] == "Book"
        assert book_response.json()["author_id"] == author_id
        assert book_response.json()["genre"] == BookGenre.FANTASY
        assert book_response.json()["count"] == 20
        assert book_response.json()["description"] == "Description"

        book_id = book_response.json()["id"]

        delete_book_response = await ac.delete(f"/api/books/{book_id}")
        delete_author_response = await ac.delete(f"/api/authors/{author_id}")

        assert delete_book_response.status_code == status.HTTP_200_OK
        assert delete_book_response.json() == {"detail": "Book deleted"}
        assert delete_author_response.status_code == status.HTTP_200_OK
        assert delete_author_response.json() == {"detail": "Author deleted"}
