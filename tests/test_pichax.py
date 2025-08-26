from pichax.client import PichaX

def test_transform_url():
    pichax = PichaX(api_key="key123", api_secret="secret123")
    url = pichax.transform(
        id="img123",
        expires=1725168000,
        src="https://example.com/image.jpg",
        params={
            "rotate": {"degrees": 45},
            "resize": {"w": 100, "h": 200, "mode": "fill"},
            "effects": [{"grayscale": True}, {"blur": 10}, {"sharpen": True}],
            "format": "jpeg",
            "quality": 80,
            "watermark": {"text": "Hello there"},
            "crop": {"x": 100,"y": 30,"w": 100,"h": 20}
        }
    ).get_url()

    assert "id=img123" in url
    assert "signature=" in url
    assert 'params={"rotate":{"degrees":45},"resize":{"w":100,"h":200,"mode":"fill"},"effects":[{"grayscale":true},{"blur":10},{"sharpen":true}],"format":"jpeg","quality":80,"watermark":{"text":"Hello there"},"crop":{"x":100,"y":30,"w":100,"h":20}}' in url

def test_identicon_url():
    pichax = PichaX(api_key="key123", api_secret="secret123")
    url = pichax.identicon(
        id="img123",
        expires=1725168000,
        name="PichaX"
    ).get_url()

    assert "name=" in url
    assert "key=" in url
    assert "signature=" in url
    assert "name=PichaX" in url
