<!-- FOR DRAFT REFERENCE ONLY -->

# Images

`images.toml` is the registry entry point for image manifests and should stay thin.
Each image directory owns its own `*.image.toml` manifest alongside the build definition (for example, a `.kiwi` file).

These per-image manifests now carry both azldev build registration and image metadata consumed by downstream tooling such as TEE.
The schema in `external/schemas/azldev.schema.json` has been extended accordingly, but azldev runtime support still needs to be implemented in the tool codebase.

# Notes
- 'distro` is a required field in the image manifest, but it is not used by azldev at this time. It is intended for use by downstream tooling such as TEE to categorize images by their base distribution.