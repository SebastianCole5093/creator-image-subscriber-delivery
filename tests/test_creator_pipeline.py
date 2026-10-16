from pathlib import Path

from src.creator_pipeline import CreatorOrder, deliver_order


class FakeGenerator:
    def __init__(self) -> None:
        self.calls = 0

    def generate(self, prompt: str) -> bytes:
        self.calls += 1
        return b"PNG"


def test_retry_reuses_existing_delivery(tmp_path: Path) -> None:
    generator = FakeGenerator()
    order = CreatorOrder("order-7", "Cover", "a cover", ("reader@example.com",))
    first = deliver_order(order, tmp_path, generator)
    second = deliver_order(order, tmp_path, generator)

    assert first == second
    assert generator.calls == 1
    assert len((tmp_path / "subscriber-updates.jsonl").read_text().splitlines()) == 1
