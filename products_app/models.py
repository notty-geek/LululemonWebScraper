from pydantic import BaseModel
from typing import List, Optional


class Product(BaseModel):
    displayName: str
    price: Optional[str]
    category: Optional[str]
    images: List[str]
    availableSizes: List[str]
    colors: List[str]
    skuDetails: List[str]
    productURL: Optional[str]

    def to_dict(self):
        return self.dict()
