import os
import json
import torch
import comfy.utils

class CustomSaveLatent:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "samples": ("LATENT", ),
                "file_path": ("STRING", {"default": "input/temp.latent"})
            },
            "hidden": {
                "prompt": "PROMPT",
                "extra_pnginfo": "EXTRA_PNGINFO"
            }
        }

    RETURN_TYPES = ()
    FUNCTION = "save"
    OUTPUT_NODE = True
    CATEGORY = "Custom"

    @classmethod
    def _comfy_root(cls) -> str:
        # two levels up from custom_nodes/your_node/
        return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

    @classmethod
    def _resolve_path(cls, file_path: str) -> str:
        # Security: prevent path traversal attacks
        if ".." in file_path or file_path.startswith(("../", "..\\")):
            raise ValueError(f"Path traversal detected in file path: {file_path}")
        
        # if relative, resolve relative to ComfyUI root
        if not os.path.isabs(file_path):
            file_path = os.path.join(cls._comfy_root(), file_path)
        
        # normalize for cross-platform use
        resolved_path = os.path.normpath(file_path)
        
        # Additional security check: ensure resolved path is within ComfyUI root
        comfy_root = cls._comfy_root()
        if not resolved_path.startswith(comfy_root):
            raise ValueError(f"Path outside ComfyUI directory not allowed: {resolved_path}")
        
        return resolved_path

    def save(self, samples, file_path="input/temp.latent", prompt=None, extra_pnginfo=None):
        try:
            # Resolve and normalize path with security checks
            file_path = self._resolve_path(file_path)

            # Make directory if present in path
            directory = os.path.dirname(file_path)
            if directory:
                os.makedirs(directory, exist_ok=True)

            # Prepare metadata
            prompt_info = json.dumps(prompt) if prompt else ""
            metadata = {"prompt": prompt_info}
            if extra_pnginfo:
                for x in extra_pnginfo:
                    metadata[x] = json.dumps(extra_pnginfo[x])

            # Build output
            output = {
                "latent_tensor": samples["samples"],
                "latent_format_version_0": torch.tensor([])
            }

            # If exists, try removing first
            alt_name_used = False
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except PermissionError:
                    root, ext = os.path.splitext(file_path)
                    file_path = root + ".new" + ext
                    alt_name_used = True

            comfy.utils.save_torch_file(output, file_path, metadata=metadata)

            # Single status message
            if os.path.exists(file_path):
                status = "alternative name" if alt_name_used else "disk"
                print(f"[CustomSaveLatent] Saved latent to {status}: {file_path}")
            else:
                print(f"[CustomSaveLatent] Warning: file was not created: {file_path}")

            return {}
        except Exception as e:
            print(f"[CustomSaveLatent] Error while saving latent: {e}")
            return {}

# Define NODE_CLASS_MAPPINGS
NODE_CLASS_MAPPINGS = {
    "CustomSaveLatent": CustomSaveLatent
}
