from pydantic import BaseModel


class Folder(BaseModel):
    name: str


class FolderParams(Folder):
    public_key: str
    path: str


class SearchParams(BaseModel):
    disk_url: str
    searched_dirs: list[str] | None = []
    row_len: int | None = 4
    width: int | None = 400
    height: int | None = 400
    gap: int | None = 25
    bg_color: tuple[int, int, int] | None = (255, 255, 255)
    max_images_per_page: int | None = 40


class FinalLink(BaseModel):
    link: str | None


class ErrorResponse(BaseModel):
    error: str
