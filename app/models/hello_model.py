from sqlmodel import SQLModel, Field

class HelloMessage(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    content: str
    language: str