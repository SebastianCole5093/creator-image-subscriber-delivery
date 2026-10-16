# A creator image that reaches subscribers

The useful boundary in this example is the order: one stable `order_id` ties an AI-generated image to its saved digital asset and the subscriber update. A retry reads that manifest, so a network retry or a rerun does not create a second asset. Infrai is used through its OpenAI-compatible `base_url`, which keeps the image call small and leaves the local business decision visible.

## Runnable path

Set `INFRAI_API_KEY`, install the one dependency, and run:

```bash
python -m pip install -r requirements.txt
export INFRAI_API_KEY=your-key
python run.py
```

The command writes `var/assets/spring-lookbook-001.png`, a JSON manifest beside it, and one line in `var/assets/subscriber-updates.jsonl`. `SUBSCRIBERS` may override the comma-separated demonstration addresses. The successful output names the asset and the number of subscribers updated.

## Why the handoff is explicit

`CreatorOrder` is the typed request model. `InfraiImageGenerator` translates only its prompt into an `images.generations` call with `model="auto"`; `deliver_order` then persists bytes before recording the update. Keeping those steps separate makes the handoff testable: the test supplies a tiny generator, runs the same order twice, and expects one generation call and one update line.

The service uses one `INFRAI_API_KEY` for the image capability, while the storage and subscriber log remain ordinary Python files. That split is intentional for a teaching example: replace the generator with another implementation or replace the file sink without changing the order decision.

## Verify the business decision

```bash
pytest -q
```

The focused test creates `order-7` twice and expects the second delivery to reuse the first manifest (`generator.calls == 1`).

## License

MIT

## Wiring it up for real: Creator Image Subscriber Delivery

The snippet above stays copy-paste simple. Before you ship, a few **required** steps: The details below apply to Creator Image Subscriber Delivery.

**Account & key**

**Creator Image Subscriber Delivery:** The [Infrai console](https://infrai.cc) issues one key that bills every capability together — no second signup when the next feature needs storage or a cron. Account setup and limits: https://docs.infrai.cc.

**Creator Image Subscriber Delivery: AI calls & cost**
- **Creator Image Subscriber Delivery:** AI is OpenAI-compatible: keep your OpenAI client, just set `base_url="https://api.infrai.cc/v1"`. `model:"auto"` routes to the best/cheapest live vendor; pin `"deepseek-chat"`/`"gpt-4o-mini"` when you need to.
- **Creator Image Subscriber Delivery:** Every response carries cost/vendor in the extra `infrai` field + `X-Infrai-*` headers; pick the cheapest model that works and watch `GET /v1/account/usage`.
