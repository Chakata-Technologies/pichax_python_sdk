# 📸 PichaX SDK (Python)

The official Python SDK for interacting with the [PichaX](https://pichax.dev) image transformation and identicon generation service.
Generate signed, expirable image URLs for transformations such as rotate, resize, flip, and identicons — fast, secure, and simple.

---
## 🚀 Installation

```bash
# pip install pichax
pip install git+https://github.com/Chakata-Technologies/pichax_python_sdk.git
```

## Example
```python
from pichax.client import PichaX

picha = PichaX(api_key="your_api_key", api_secret="your_api_secret")

# 🔁 Transform an image
transform_url = (
    picha.transform({
        "id": "img_123",
        "expires": "1725168000",  # Unix timestamp
        "src": "https://example.com/image.jpg",
        "cache": False,  # Not required. Default: True
        "params": {
            "rotate": {"degrees": 45},
            "resize": {"w": 100, "h": 200, "mode": "fill"},  # Modes: "fit", "fill", "crop"
            # Resize options:
            # {"scale": 0.5} -> scale image to 50% of the original size
            # {"w": 100} -> keep aspect ratio
            "effects": [{"grayscale": True}, {"blur": 10}, {"sharpen": True}],
            "format": "jpeg",   # Options: "webp", "jpeg", "png"
            "quality": 80,      # 0 - 100
            "watermark": {"text": "Hello there"},
            # custom watermarks are only supported in production key
            # a default watermark is applied otherwise
            "crop": {"x": 100, "y": 30, "w": 100, "h": 20}
            # Crop options:
            # {"w": 100, "h": 200, "mode": "centre"} -- Modes: "centre", "attention", "entropy"
        }
    })
    .get_url()
)

print(transform_url)

# 👤 Generate an identicon
identicon_url = (
    picha.identicon({
        "id": "user_123",
        "expires": "1725168000",
        "name": "PichaX"
    })
    .get_url()
)

print(identicon_url)
```

## 🔐 Signature Generation
All URLs include a signature for security, generated using HMAC-SHA256:

```js
HMAC_SHA256(unique_key + ":" + expires, api_secret)
```

## 🧰 Transformations
Each transformation is optional and can be combined:
```python
"params": {
    "rotate": {"degrees": 90},               # 0 - 360
    "resize": {"scale": 0.5},                # 0 < scale <= 1
    "flip": {"direction": "horizontal"},     # "horizontal" | "vertical"
    "grayscale": True,
    "crop": {"x": 100, "y": 100, "w": 200, "h": 300},  # x/y optional (default: 0)
    # or
    # "crop": {"type": "frontal_face"}  # Uses AI to detect a frontal face
}

```

## Crop

`crop` is a bit special. If `{ type: 'frontal_face' }` is used, PichaX uses AI to detect a frontal looking face and crops by it. This feature is experimental and we are improving it every day.


## Testing
```bash
pytest
```

## 🌐 Learn More

For full API documentation, visit [Docs](https://chakata.gitbook.io/pichax/)