from typing import List

from pydantic import BaseModel


class Profile(BaseModel):
    profile: List[str]
