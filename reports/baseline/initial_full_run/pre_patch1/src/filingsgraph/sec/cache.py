from pathlib import Path
import hashlib

class FileCache:
    def __init__(self, root: str | Path):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def path_for(self, key: str, suffix: str = ".bin") -> Path:
        digest = hashlib.sha256(key.encode("utf-8")).hexdigest()
        return self.root / f"{digest}{suffix}"

    def get(self, key: str, suffix: str = ".bin") -> bytes | None:
        p = self.path_for(key, suffix)
        return p.read_bytes() if p.exists() else None

    def put(self, key: str, data: bytes, suffix: str = ".bin") -> Path:
        p = self.path_for(key, suffix)
        p.write_bytes(data)
        return p
