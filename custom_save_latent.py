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
        # Ensure the directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Prepare metadata
        prompt_info = json.dumps(prompt) if prompt else ""
        metadata = {"prompt": prompt_info}
        if extra_pnginfo:
            for x in extra_pnginfo:
                metadata[x] = json.dumps(extra_pnginfo[x])

        # Save the latent (overwriting if it exists)
        output = {"latent_tensor": samples["samples"], "latent_format_version_0": torch.tensor([])}
        if os.path.exists(file_path):
            os.remove(file_path)  # Remove the existing file
        comfy.utils.save_torch_file(output, file_path, metadata=metadata)
        return {}

# Define NODE_CLASS_MAPPINGS
NODE_CLASS_MAPPINGS = {
    "CustomSaveLatent": CustomSaveLatent
}
