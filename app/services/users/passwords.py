from __future__ import annotations

import hashlib
import hmac
import secrets


class PasswordService:
    algorithm = "pbkdf2_sha256"
    iterations = 600_000
    salt_bytes = 16

    def hash_password(self, password: str) -> str:
        salt = secrets.token_hex(self.salt_bytes)
        digest = self._derive(password, salt, self.iterations)
        return f"{self.algorithm}${self.iterations}${salt}${digest}"

    def verify_password(self, password: str, password_hash: str) -> bool:
        try:
            algorithm, iterations_value, salt, expected_digest = password_hash.split("$", 3)
            iterations = int(iterations_value)
        except ValueError:
            return False

        if algorithm != self.algorithm:
            return False

        digest = self._derive(password, salt, iterations)
        return hmac.compare_digest(digest, expected_digest)

    def _derive(self, password: str, salt: str, iterations: int) -> str:
        return hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt.encode("ascii"),
            iterations,
        ).hex()
