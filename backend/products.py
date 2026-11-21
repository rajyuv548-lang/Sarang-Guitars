
import json
from pathlib import Path

# Locate the project directory
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "guitars.json"


def load_products():
    """Load guitar catalogue from JSON."""

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            products = json.load(file)

        if not isinstance(products, list):
            raise ValueError("Guitar catalogue must contain a JSON list.")

        return products

    except FileNotFoundError:
        raise FileNotFoundError("guitars.json was not found.")

    except json.JSONDecodeError as error:
        raise ValueError(f"Invalid guitar catalogue JSON: {error}")


def get_all_products():
    return load_products()


def search_products(
    brand=None,
    category=None,
    min_price=None,
    max_price=None
):
    """Search guitars using optional filters."""

    products = load_products()
    results = []

    for guitar in products:

        if brand and brand.lower() not in guitar["brand"].lower():
            continue

        if category and category.lower() != guitar["category"].lower():
            continue

        price = guitar["price_inr"]

        if min_price is not None and price < min_price:
            continue

        if max_price is not None and price > max_price:
            continue

        results.append(guitar)

    return results


def get_product_by_name(name):
    """Find a guitar by its model name."""

    products = load_products()

    for guitar in products:
        if guitar["name"].lower() == name.lower():
            return guitar

    return None


def compare_products(name1, name2):
    """Compare two guitar models."""

    guitar1 = get_product_by_name(name1)
    guitar2 = get_product_by_name(name2)

    if not guitar1 or not guitar2:
        return None

    return {
        "guitar_1": guitar1,
        "guitar_2": guitar2
    }
