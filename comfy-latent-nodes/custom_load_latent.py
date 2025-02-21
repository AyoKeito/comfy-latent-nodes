import os
import hashlib
import safetensors.torch

class CustomLoadLatent:
    @classmethod
    def INPUT_TYPES(cls):
        load_directory = "custom"
        # Ensure the input directory exists
        os.makedirs(load_directory, exist_ok=True)

        files = [
            f for f in os.listdir(load_directory)
            if os.path.isfile(os.path.join(load_directory, f)) and f.endswith(".latent")
        ]
        # Handle case where no files are found
        if not files:
            files = ["No latent files found"]

        return {
            "required": {
                "filename": (sorted(files), ),
                "load_directory": ("STRING", {"default": "custom"})
            }
        }

    CATEGORY = "Custom"
    RETURN_TYPES = ("LATENT", )
    FUNCTION = "load"

    def load(self, filename="templatent.latent", load_directory="custom"):
        input_dir = load_directory
        file_path = os.path.join(input_dir, filename)
        if filename == "No latent files found":
            raise FileNotFoundError(f"No latent files found in directory: {input_dir}")

        latent = safetensors.torch.load_file(file_path, device="cpu")
        multiplier = 1.0 if "latent_format_version_0" in latent else 1.0 / 0.18215
        samples = {"samples": latent["latent_tensor"].float() * multiplier}
        return (samples, )

    @classmethod
    def IS_CHANGED(cls, filename):
        image_path = os.path.join("custom", filename)
        m = hashlib.sha256()
        with open(image_path, 'rb') as f:
            m.update(f.read())
        return m.digest().hex()

    @classmethod
    def VALIDATE_INPUTS(cls, filename):
        if not os.path.exists(os.path.join("custom", filename)):
            return f"Invalid latent file: {filename}"
        return True

# Define NODE_CLASS_MAPPINGS
NODE_CLASS_MAPPINGS = {
    "CustomLoadLatent": CustomLoadLatent
}
