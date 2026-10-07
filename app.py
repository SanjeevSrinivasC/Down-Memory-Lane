"""
Down Memory Lane - a Slack bot that turns text requests into "childhood photos"
using your own Flux LoRA model (trained on your face) hosted on Replicate.

Usage in Slack:
    @Down Memory Lane my 5-year-old self on a beach
"""

import logging
import os
import re

import replicate
import requests
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

load_dotenv()
logging.basicConfig(level=logging.INFO)

# ---- Configuration (all values come from the .env file) ----
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]    # starts with xoxb-
SLACK_APP_TOKEN = os.environ["SLACK_APP_TOKEN"]    # starts with xapp-
REPLICATE_MODEL = os.environ["REPLICATE_MODEL"]    # your-username/model-name:version-id
TRIGGER_WORD = os.environ.get("TRIGGER_WORD", "TOK")
LORA_SCALE = float(os.environ.get("LORA_SCALE", "0.9"))
# REPLICATE_API_TOKEN is read automatically by the replicate library.

app = App(token=SLACK_BOT_TOKEN)

# Finds the age in requests like "my 5-year-old self" or "2 year old me"
AGE_PATTERN = re.compile(r"(\d{1,2})\s*-?\s*(?:year|yr)s?[\s-]*old", re.IGNORECASE)
# Removes the whole "my 5-year-old self" phrase so we can describe the subject ourselves
AGE_PHRASE = re.compile(
    r"\b(?:my|your)?\s*\d{1,2}\s*-?\s*(?:year|yr)s?[\s-]*old\s*(?:self|me)?\b",
    re.IGNORECASE,
)


def build_prompt(user_text: str) -> str:
    """Turn a casual Slack request into a detailed prompt for the Flux LoRA model."""
    match = AGE_PATTERN.search(user_text)
    age = match.group(1) if match else None

    scene = AGE_PHRASE.sub("", user_text)
    scene = re.sub(r"\s+", " ", scene).strip(" ,.")
    scene_part = f", {scene}" if scene else ""

    subject = f"{TRIGGER_WORD} as a {age}-year-old child" if age else f"{TRIGGER_WORD} as a young child"

    return (
        f"A realistic old family photograph of {subject}{scene_part}. "
        "Candid childhood snapshot, natural light, soft film grain, "
        "sharp focus on the child's face, nostalgic family photo album style"
    )


def generate_image(prompt: str) -> bytes:
    """Call your trained model on Replicate and return the image as bytes."""
    output = replicate.run(
        REPLICATE_MODEL,
        input={
            "prompt": prompt,
            "num_outputs": 1,
            "aspect_ratio": "1:1",
            "output_format": "png",
            "lora_scale": LORA_SCALE,
            "guidance_scale": 3,
            "num_inference_steps": 28,
        },
    )
    item = output[0] if isinstance(output, list) else output

    if hasattr(item, "read"):  # newer replicate library returns a file object
        return item.read()

    resp = requests.get(str(item), timeout=60)  # older library returns a URL
    resp.raise_for_status()
    return resp.content


@app.event("app_mention")
def handle_mention(event, say, client, logger):
    channel = event["channel"]
    # Reply inside the thread (start a new thread if the mention wasn't in one)
    thread_ts = event.get("thread_ts") or event["ts"]
    request_text = re.sub(r"<@[^>]+>", "", event.get("text", "")).strip()

    if not request_text:
        say(
            text="Tell me which memory to create! Example: `@Down Memory Lane my 5-year-old self on a beach`",
            thread_ts=thread_ts,
        )
        return

    say(
        text=f":hourglass_flowing_sand: Creating your memory: _{request_text}_ (usually 20-60 seconds)",
        thread_ts=thread_ts,
    )

    try:
        prompt = build_prompt(request_text)
        logger.info("Prompt sent to model: %s", prompt)

        image_bytes = generate_image(prompt)

        client.files_upload_v2(
            channel=channel,
            thread_ts=thread_ts,
            file=image_bytes,
            filename="memory.png",
            title=request_text[:80],
            initial_comment=":camera_with_flash: Here's your memory!",
        )
    except Exception as err:
        logger.exception("Image generation failed")
        say(text=f":warning: Sorry, I couldn't create that one. ({err})", thread_ts=thread_ts)


if __name__ == "__main__":
    print("Down Memory Lane bot is running... (press Ctrl+C to stop)")
    SocketModeHandler(app, SLACK_APP_TOKEN).start()
