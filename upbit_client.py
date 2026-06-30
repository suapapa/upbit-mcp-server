from typing import Any

from upbit import APIError, APIStatusError, AsyncUpbit, UpbitError

from config import UPBIT_ACCESS_KEY, UPBIT_SECRET_KEY

_public_client: AsyncUpbit | None = None
_authenticated_client: AsyncUpbit | None = None


def get_public_client() -> AsyncUpbit:
    global _public_client
    if _public_client is None:
        _public_client = AsyncUpbit()
    return _public_client


def get_authenticated_client() -> AsyncUpbit:
    global _authenticated_client
    if _authenticated_client is None:
        _authenticated_client = AsyncUpbit(
            access_key=UPBIT_ACCESS_KEY,
            secret_key=UPBIT_SECRET_KEY,
        )
    return _authenticated_client


def to_serializable(obj: Any) -> Any:
    if obj is None:
        return None
    if hasattr(obj, "model_dump"):
        return obj.model_dump()
    if isinstance(obj, list):
        return [to_serializable(item) for item in obj]
    if isinstance(obj, dict):
        return {key: to_serializable(value) for key, value in obj.items()}
    if hasattr(obj, "items"):
        return [to_serializable(item) for item in obj.items]
    return obj


def format_api_error(error: Exception) -> str:
    if isinstance(error, APIStatusError):
        return f"업비트 API 오류: {error.status_code} - {error.message}"
    if isinstance(error, APIError):
        return f"업비트 API 오류: {error.message}"
    if isinstance(error, UpbitError):
        return f"업비트 API 오류: {str(error)}"
    return f"API 호출 중 오류 발생: {str(error)}"
