# comfy-latent-nodes

This repository contains custom nodes for ComfyUI that facilitate saving and loading latent representations to and from specified directories.

## Features

- **CustomSaveLatent**: Save latent representations to a specified directory with a custom filename.
- **CustomLoadLatent**: Load latent representations from a specified directory based on the provided filename.

## Getting Started

### Installation

1. **Clone the Repository**:

   Navigate to the `custom_nodes` directory of your ComfyUI installation and clone the repository:

   ```bash
   cd path/to/ComfyUI/custom_nodes
   git clone https://github.com/Velour-Fog/comfy-latent-nodes.git
2. **Restart ComfyUI**:

   Restart ComfyUI to load the new custom nodes.

### Usage

#### CustomSaveLatent Node

- **Inputs**:
  - `samples`: The latent representation to be saved.
  - `file_path`: The full path to save the latent file (e.g., `input/temp.latent`).

#### CustomLoadLatent Node

- **Inputs**:
  - `file_path`: The full path to the latent file to load (e.g., `input/temp.latent`).
