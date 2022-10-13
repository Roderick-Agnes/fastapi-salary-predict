from pydantic import BaseModel

class InputModel(BaseModel):
    knowledge: int
    technical: int
    logical: int
    year_experience: float = 0

    def show(self):
        return self.knowledge