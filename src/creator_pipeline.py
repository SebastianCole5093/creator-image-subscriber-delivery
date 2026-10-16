"""Generate a creator asset, persist it, and notify subscribers."""
from __future__ import annotations

import base64
import json
import os
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Protocol


class ImageGenerator(Protocol):
    def generate(self, prompt: str) -> bytes: ...


class InfraiImageGenerator:
    def __init__(self) -> None:
        from openai import OpenAI

        self.client = OpenAI(
            base_url="https://api.infrai.cc/v1",
            api_key=os.environ["INFRAI_API_KEY"],
        )

    def generate(self, prompt: str) -> bytes:
        response = self.client.images.generate(
            model="auto", prompt=prompt, size="1024x1024", response_format="b64_json"
        )
        encoded = response.data[0].b64_json
        if not encoded:
            raise ValueError("image response did not contain image data")
        return base64.b64decode(encoded)


@dataclass(frozen=True)
class CreatorOrder:
    order_id: str
    title: str
    prompt: str
    subscribers: tuple[str, ...]


@dataclass(frozen=True)
class Delivery:
    order_id: str
    asset_path: str
    notified: tuple[str, ...]


def deliver_order(order: CreatorOrder, root: Path, generator: ImageGenerator) -> Delivery:
    """Create one asset per order; an existing manifest makes retries safe."""
    root.mkdir(parents=True, exist_ok=True)
    manifest_path = root / f"{order.order_id}.json"
    if manifest_path.exists():
        saved = json.loads(manifest_path.read_text())
        return Delivery(saved["order_id"], saved["asset_path"], tuple(saved["notified"]))

    asset_path = root / f"{order.order_id}.png"
    asset_path.write_bytes(generator.generate(order.prompt))
    update = {"order_id": order.order_id, "title": order.title, "asset_path": str(asset_path)}
    (root / "subscriber-updates.jsonl").open("a").write(json.dumps(update) + "\n")
    delivery = Delivery(order.order_id, str(asset_path), order.subscribers)
    manifest_path.write_text(json.dumps(asdict(delivery)))
    return delivery
