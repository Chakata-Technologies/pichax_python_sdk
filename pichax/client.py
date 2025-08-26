import hashlib
import hmac
import json
from urllib.parse import urlencode


class TransformUrlBuilder:
    def __init__(self, base_url, api_key, api_secret, params):
        if not params.get("params"):
            raise ValueError("At least one transformation must be specified.")
        self.api_key = api_key
        self.api_secret = api_secret
        self.params = params
        self.base_url = base_url

    def minify_json_with_watermark_preserved(self, json_str):
      # Parse the JSON string
      data = json.loads(json_str)
      def custom_default(obj):
          return obj
      # Dump minified JSON
      return json.dumps(data, separators=(',', ':'), ensure_ascii=False, default=custom_default)

    def get_url(self):
        signature = self._generate_signature()
        query = {
            "id": self.params["id"],
            "key": self.api_key,
            "expires": self.params["expires"],
            "signature": signature,
            "src": self.params["src"]
        }

        json_params = json.dumps(self.params["params"]).replace("\\","")
        trimmed_json_params = self.minify_json_with_watermark_preserved(json_params)
        transform_url = f"{self.base_url}/transform"
        return f"{transform_url}?{urlencode(query)}&params={trimmed_json_params}"

    def _generate_signature(self):
        data = f"{self.params['id']}:{self.params['expires']}"
        return hmac.new(
            self.api_secret.encode(),
            data.encode(),
            hashlib.sha256
        ).hexdigest()


class IdenticonUrlBuilder:
    def __init__(self, base_url, api_key, api_secret, params):
        self.api_key = api_key
        self.api_secret = api_secret
        self.params = params
        self.base_url = base_url

    def get_url(self):
        signature = self._generate_signature()
        query = {
            "key": self.api_key,
            "expires": self.params["expires"],
            "signature": signature,
            "name": self.params["name"],
        }
        identicon_url = f"{self.base_url}/identicon"
        return f"{identicon_url}?{urlencode(query)}"

    def _generate_signature(self):
        data = f"{self.params['id']}:{self.params['expires']}"
        return hmac.new(
            self.api_secret.encode(),
            data.encode(),
            hashlib.sha256
        ).hexdigest()


class PichaX:
    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = "https://api.pichax.dev/api/v1/generate"

    def transform(self, **kwargs):
        return TransformUrlBuilder(self.base_url, self.api_key, self.api_secret, kwargs)

    def identicon(self, **kwargs):
        return IdenticonUrlBuilder(self.base_url, self.api_key, self.api_secret, kwargs)
