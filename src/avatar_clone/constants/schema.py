from pydantic import BaseModel, HttpUrl, constr, Field


class CloneAvatar(BaseModel):
    name: constr(min_length=1, max_length=100) = Field(
        ..., description="Name is required"
    )
    image_url: HttpUrl = Field(..., description="Image URL is required")
    platform: constr(min_length=1, max_length=50) = Field(
        ..., description="Platform is required"
    )
