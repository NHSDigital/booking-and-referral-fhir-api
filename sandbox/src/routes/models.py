from pydantic import BaseModel
from typing import List


class Profile(BaseModel):
    profile: List[str]
