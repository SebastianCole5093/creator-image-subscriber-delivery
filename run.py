import os
from pathlib import Path

from src.creator_pipeline import CreatorOrder, InfraiImageGenerator, deliver_order


def main() -> None:
    order = CreatorOrder(
        order_id="spring-lookbook-001",
        title="Spring lookbook cover",
        prompt="Editorial product image of a bright spring creator lookbook cover, clean studio light",
        subscribers=tuple(filter(None, os.getenv("SUBSCRIBERS", "alice@example.com,bob@example.com").split(","))),
    )
    result = deliver_order(order, Path("var/assets"), InfraiImageGenerator())
    print(f"asset: {result.asset_path}")
    print(f"subscribers updated: {len(result.notified)}")


if __name__ == "__main__":
    main()

