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

    def save(self, samples, file_path="input/temp.latent", prompt=None, extra_pnginfo=None):
        try:
            # Find the base ComfyUI directory (two levels up from this file: custom_nodes/your_node/)
            comfy_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

            # If the path is relative → resolve relative to ComfyUI root
            if not os.path.isabs(file_path):
                file_path = os.path.join(comfy_root, file_path)

            # Normalize for cross-platform use
            file_path = os.path.normpath(file_path)

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
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except PermissionError:
                    print(f"[CustomSaveLatent] Permission error removing {file_path}; using a new name.")
                    root, ext = os.path.splitext(file_path)
                    file_path = root + ".new" + ext

            print(f"[CustomSaveLatent] Saving latent to: {file_path}")
            comfy.utils.save_torch_file(output, file_path, metadata=metadata)

            if os.path.exists(file_path):
                print(f"[CustomSaveLatent] Saved latent: {file_path}")
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
