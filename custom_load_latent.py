import os
import safetensors.torch
import comfy.utils
import hashlib
import torch

class CustomLoadLatent:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "file_path": ("STRING", {"default": "input/temp.latent"})
            }
        }

    CATEGORY = "Custom"
    RETURN_TYPES = ("LATENT",)
    FUNCTION = "load"
    OUTPUT_NODE = True

    # --- path helpers (match CustomSaveLatent behavior) ---
    @staticmethod
    def _comfy_root() -> str:
        # two levels up from custom_nodes/your_node/
        return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

    @classmethod
    def _resolve_path(cls, file_path: str) -> str:
        # if relative, resolve relative to ComfyUI root
        if not os.path.isabs(file_path):
            file_path = os.path.join(cls._comfy_root(), file_path)
        # normalize for cross-platform use
        return os.path.normpath(file_path)

    # --- node runtime ---
    def load(self, file_path):
        # Resolve and normalize path (handles / or \ and relative vs absolute)
        file_path = self._resolve_path(file_path)

        # Ensure the file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"[CustomLoadLatent] File does not exist: {file_path}")

        # Optional: touch the file contents to ensure latest read (no-op here, but keeps parity with your previous logic)
        with open(file_path, 'rb') as f:
            _ = f.read(64)  # small read is enough to provoke FS refresh on some setups

        # Load latent
        try:
            latent = safetensors.torch.load_file(file_path, device="cpu")
        except Exception as e:
            raise RuntimeError(f"[CustomLoadLatent] Failed to load '{file_path}': {e}")

        if "latent_tensor" not in latent:
            raise KeyError("[CustomLoadLatent] 'latent_tensor' key not found in the file.")

        # Backward-compat multiplier (same as your original)
        multiplier = 1.0
        if "latent_format_version_0" not in latent:
            multiplier = 1.0 / 0.18215

        samples = {"samples": latent["latent_tensor"].float() * multiplier}
        return (samples,)

    # --- UI change detection ---
    @classmethod
    def IS_CHANGED(cls, file_path):
        file_path = cls._resolve_path(file_path)
        if not os.path.exists(file_path):
            # If it doesn't exist, return a unique token so the node updates when it appears
            return f"missing:{hashlib.sha256(file_path.encode('utf-8')).hexdigest()}"

        m = hashlib.sha256()
        with open(file_path, 'rb') as f:
            # Hash in chunks for large files
            for chunk in iter(lambda: f.read(1024 * 1024), b''):
                m.update(chunk)
        return m.hexdigest()

    # --- input validation for graph building ---
    @classmethod
    def VALIDATE_INPUTS(cls, file_path):
        file_path = cls._resolve_path(file_path)
        if not os.path.exists(file_path):
            return f"Invalid latent file: {file_path}"
        # Optionally verify the safetensors header before runtime load
        try:
            # Cheap probe: read just the header; load_file will throw early if corrupt
            # (safetensors doesn't expose a header-only read, so we do a try/except)
            _ = safetensors.torch.load_file(file_path, device="cpu")
        except Exception as e:
            return f"Cannot read latent file: {file_path} ({e})"
        return True

# Define NODE_CLASS_MAPPINGS
NODE_CLASS_MAPPINGS = {
    "CustomLoadLatent": CustomLoadLatent
}
