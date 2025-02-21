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
                "filename": ("STRING", {"default": "templatent"}),
                "save_directory": ("STRING", {"default": "custom"})
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

    def save(self, samples, filename="templatent", save_directory="custom", prompt=None, extra_pnginfo=None):
        output_dir = save_directory

        # Ensure the output directory exists
        os.makedirs(output_dir, exist_ok=True)

        # Construct the full file path
        file_path = os.path.join(output_dir, f"{filename}.latent")

        # Prepare metadata
        prompt_info = json.dumps(prompt) if prompt else ""
        metadata = {"prompt": prompt_info}
        if extra_pnginfo:
            for x in extra_pnginfo:
                metadata[x] = json.dumps(extra_pnginfo[x])

        # Save the latent
        output = {"latent_tensor": samples["samples"], "latent_format_version_0": torch.tensor([])}
        comfy.utils.save_torch_file(output, file_path, metadata=metadata)
        return {}

# Define NODE_CLASS_MAPPINGS
NODE_CLASS_MAPPINGS = {
    "CustomSaveLatent": CustomSaveLatent
}
