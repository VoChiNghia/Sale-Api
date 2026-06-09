import json
from json import JSONDecodeError
from urllib.parse import parse_qs

from starlette.datastructures import Headers
from starlette.types import ASGIApp, Message, Receive, Scope, Send


class LenientJsonBodyMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        method = scope.get("method", "").upper()
        if method not in {"POST", "PUT", "PATCH", "DELETE"}:
            await self.app(scope, receive, send)
            return

        headers = Headers(scope=scope)
        content_type = headers.get("content-type", "").split(";")[0].lower()
        if content_type not in {
            "application/json",
            "application/x-www-form-urlencoded"
        }:
            await self.app(scope, receive, send)
            return

        body = await self._read_body(receive)
        next_body, next_content_type = self._normalize_body(
            method,
            content_type,
            body
        )
        next_scope = self._with_body_headers(
            scope,
            len(next_body),
            next_content_type
        )

        sent = False

        async def replay_receive() -> Message:
            nonlocal sent
            if sent:
                return {"type": "http.request", "body": b"", "more_body": False}
            sent = True
            return {
                "type": "http.request",
                "body": next_body,
                "more_body": False
            }

        await self.app(next_scope, replay_receive, send)

    async def _read_body(self, receive: Receive) -> bytes:
        chunks: list[bytes] = []

        while True:
            message = await receive()
            if message["type"] == "http.disconnect":
                break

            chunks.append(message.get("body", b""))

            if not message.get("more_body", False):
                break

        return b"".join(chunks)

    def _normalize_body(
        self,
        method: str,
        content_type: str,
        body: bytes
    ) -> tuple[bytes, str | None]:
        if not body.strip():
            return body, None

        if content_type == "application/json":
            try:
                json.loads(body)
                return body, None
            except JSONDecodeError:
                if method == "DELETE":
                    return b"", None

        form_body = self._form_urlencoded_to_json(body)
        if form_body:
            return form_body, "application/json"

        return body, None

    def _form_urlencoded_to_json(self, body: bytes) -> bytes | None:
        try:
            text = body.decode("utf-8")
        except UnicodeDecodeError:
            return None

        if "=" not in text or "\r" in text or "\n" in text:
            return None

        parsed = parse_qs(text, keep_blank_values=True)
        if not parsed:
            return None

        data = {
            key: values[0] if len(values) == 1 else values
            for key, values in parsed.items()
        }

        return json.dumps(data).encode("utf-8")

    def _with_body_headers(
        self,
        scope: Scope,
        content_length: int,
        content_type: str | None
    ) -> Scope:
        next_scope = dict(scope)
        headers = [
            (key, value)
            for key, value in scope.get("headers", [])
            if key.lower() not in {b"content-length", b"content-type"}
        ]
        if content_type:
            headers.append((b"content-type", content_type.encode()))
        else:
            original_content_type = Headers(scope=scope).get("content-type")
            if original_content_type:
                headers.append((b"content-type", original_content_type.encode()))

        headers.append((b"content-length", str(content_length).encode()))
        next_scope["headers"] = headers
        return next_scope
