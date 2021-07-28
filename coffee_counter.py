#!/usr/bin/env python3

from datetime import date, datetime
from typing import Any, Optional, Union

import pandas as pd
import requests
from pydantic import BaseModel

API_URL = "https://a7a9ck.deta.dev/"


class CoffeeBag(BaseModel):
    brand: str
    name: str
    weight: float
    start: date
    finish: Optional[date] = None
    bag_id: str
    active: bool


class CoffeeUse(BaseModel):
    use_id: str
    bag_id: str
    datetime: datetime


class CoffeeCounter:
    coffee_bags: list[CoffeeBag]
    coffee_uses: list[CoffeeUse]

    BatchResponse = dict[str, dict[str, Any]]

    def __init__(self) -> None:
        self.coffee_bags = []
        self.coffee_uses = []

    def bags_response_to_bags(self, info=BatchResponse) -> list[CoffeeBag]:
        return [CoffeeBag(bag_id=k, **i) for k, i in info.items()]

    def uses_response_to_uses(self, info=BatchResponse) -> list[CoffeeUse]:
        return [CoffeeUse(use_id=k, **i) for k, i in info.items()]

    def display_failed_response(self, res: requests.Response):
        print(f"error: status code {res.status_code}")
        print(res.json())

    def get_coffee_bags(self):
        url = API_URL + "bags/"
        response = requests.get(url)
        if response.status_code == 200:
            self.coffee_bags = self.bags_response_to_bags(response.json())
        else:
            self.display_failed_response(response)

    def get_coffee_uses(self, n_last: int = 1000):
        url = API_URL + f"uses/?n_last={n_last}"
        response = requests.get(url)
        if response.status_code == 200:
            self.coffee_uses = self.uses_response_to_uses(response.json())
        else:
            self.display_failed_response(response)

    def get_coffee_data(self, n_last: int = 1000):
        self.get_coffee_bags()
        self.get_coffee_uses()

    def modellist_to_dict(
        self, models: Union[list[CoffeeUse], list[CoffeeBag]]
    ) -> dict[str, Any]:
        data: dict[str, Any] = {}
        fields = models[0].__fields__
        for field in fields:
            data[field] = [m.dict()[field] for m in models]
        return data

    def tidy_coffee_data(self) -> pd.DataFrame:

        if len(self.coffee_bags) == 0:
            self.get_coffee_bags()
        if len(self.coffee_uses) == 0:
            self.get_coffee_uses()

        uses_df = pd.DataFrame(self.modellist_to_dict(self.coffee_uses))
        bags_df = pd.DataFrame(self.modellist_to_dict(self.coffee_bags))

        return pd.merge(uses_df, bags_df, how="inner", on="bag_id")


if __name__ == "__main__":
    coffee_counter = CoffeeCounter()
    print(coffee_counter.tidy_coffee_data())
