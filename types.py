from typing import List, Set, Tuple, Dict, Optional


def get_full_name(first_name: str, last_name: str):
  full_name = first_name.title() + " " + last_name.title()
  return full_name


print(get_full_name("john", "doe"))


def get_name_with_age(name: str, age: int):
  name_with_age = name + " is this old: " + str(age)
  return name_with_age


print(get_name_with_age("john", 99))


def get_items(item_a: str, item_b: int, item_c: float, item_d: bool, item_e: bytes):
  return item_a, item_b, item_c, item_d, item_d, item_e


def process_items(items: List[str]):
  for item in items:
    print(item)


def process_items(items_t: Tuple[int, int, str], items_s: Set[bytes]):
  return items_t, items_s


def process_items(prices: Dict[str, float]):
  for item_name, item_price in prices.items():
    print(item_name)
    print(item_price)


def say_hi(name: Optional[str] = None):
  if name is not None:
    print(f"Hey {name}!")
  else:
    print("Hello World")
