import requests


def _post(headers: dict, url: str, data: dict, timeout: int = 10, retry: int = 3) -> requests.models.Response:
    for _ in range(retry):
        try:
            return requests.post(
                url=url,
                data=data,
                headers=headers,
                timeout=timeout,
            )
        except requests.exceptions.RequestException:
            pass
    raise requests.exceptions.RequestException


def post(uri: str, token: str, data: dict) -> requests.models.Response:
    return _post(
        url="https://zhtj.youth.cn/v1/center/" + uri,
        data=data,
        headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0",
            "Cookie": token,
        })
