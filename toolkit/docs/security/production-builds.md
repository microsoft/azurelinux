# Production Build Recommendations

When building images or ISOs for production deployment, enable explicit GPG signature verification to ensure all packages have completed the signing process:

```bash
sudo make image VALIDATE_IMAGE_GPG=y CONFIG_FILE=<your-config>
```

This validates that all RPM packages fetched during image generation have valid GPG signatures from the expected signing keys.

## Build Workflow

A typical production workflow separates package building from image generation:

1. **Build packages** - Compile packages from source
2. **Sign packages** - Sign built packages with your GPG key
3. **Build images** - Generate images with `VALIDATE_IMAGE_GPG=y` to enforce all packages are signed

This separation ensures unsigned or improperly signed packages cannot be included in final images.

## Related Variables

| Variable | Description |
|:---------|:------------|
| `VALIDATE_IMAGE_GPG` | Set to `y` to require valid GPG signatures on all image packages |
| `IMAGE_GPG_VALIDATION_KEYS` | GPG key files for signature validation |
| `VALIDATE_TOOLCHAIN_GPG` | Automatically enabled when downloading pre-built toolchain |
| `TOOLCHAIN_GPG_VALIDATION_KEYS` | GPG key files for toolchain validation |

See [build variables](../building/building.md#all-build-variables) for full details.
