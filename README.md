comfy-latent-nodes
This repository contains custom nodes for ComfyUI that facilitate saving and loading latent representations to and from specified directories.

Features
CustomSaveLatent: Save latent representations to a specified directory with a custom filename.

CustomLoadLatent: Load latent representations from a specified directory based on the provided filename.

Getting Started
Installation
Clone the Repository:

Navigate to the custom_nodes directory of your ComfyUI installation and clone the repository:

bash
cd path/to/ComfyUI/custom_nodes
git clone https://github.com/Velour-Fog/comfy-latent-nodes.git
Restart ComfyUI:

Restart ComfyUI to load the new custom nodes.

Usage
CustomSaveLatent Node
Inputs:

samples: The latent representation to be saved.

filename: The name of the file to save the latent as (default: "templatent").

save_directory: The directory to save the latent in (default: "custom").

CustomLoadLatent Node
Inputs:

filename: The name of the latent file to load.

load_directory: The directory to load the latent from (default: "custom").
