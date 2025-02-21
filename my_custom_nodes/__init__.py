# Import your custom node classes
from .custom_save_latent import CustomSaveLatent
from .custom_load_latent import CustomLoadLatent

# Define NODE_CLASS_MAPPINGS
NODE_CLASS_MAPPINGS = {
    "CustomSaveLatent": CustomSaveLatent,
    "CustomLoadLatent": CustomLoadLatent,
}
