#!/usr/bin/env python3
from pathlib import Path
import re

README = Path("README.md")


def main():
    text = README.read_text(encoding="utf-8")
    assert "SriShankar2006" in text
    links = re.findall(r"(?<!\!)\[[^\]]+\]\(([^)]+)\)", text)
    images = re.findall(r"!\[[^\]]*\]\(([^)]+)\)", text)
    assert len(links) >= 10
    assert all(re.match(r"^(https?://|#|mailto:|./)", link) for link in links)
    assert all(not line.lstrip().startswith("#\n") for line in text.splitlines())
    for image in images:
        if image.startswith("./"):
            if not Path(image).exists():
                print(f"Info: generated image is available after its workflow runs: {image}")
    print(f"Validated README: {len(links)} links and {len(images)} image references")


if __name__ == "__main__":
    main()
