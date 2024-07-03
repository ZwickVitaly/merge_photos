from pydantic import BaseModel, Field


class Folder(BaseModel):
    name: str


class FolderParams(Folder):
    public_key: str
    path: str


class SearchParams(BaseModel):
    disk_url: str = Field(description="Прямая ссылка на ПУБЛИЧНЫЙ Яндекс-диск")
    searched_dirs: list[str] | None = Field(description="Список директорий, в которых следует искать.")
    row_len: int | None = Field(
        default=0, description="Длина ряда в готовом изображении. При значении <= 0 будет высчитана автоматически"
    )
    width: int | None = Field(
        ge=1, le=1600, default=400, description="Ширина каждого отдельного изображения в пикселях. 1-1600"
    )
    height: int | None = Field(
        ge=1, le=1600, default=400, description="Высота каждого отдельного изображения в пикселях. 1-1600"
    )
    gap: int | None = Field(
        default=25, ge=0, le=100, description="Разрыв между изображениями в пикселях. 0-100"
    )
    bg_color: tuple[int, int, int] | None = Field(default=(255, 255, 255), description="Цвет заднего фона в RGB")
    max_images_per_page: int | None = Field(
        default=25, ge=1, le=100, description="Максимальное количество изображений на странице. 1-100"
    )


class FinalLink(BaseModel):
    link: str | None


class ErrorResponse(BaseModel):
    error: str
