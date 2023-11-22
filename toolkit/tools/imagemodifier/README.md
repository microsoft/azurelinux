# Mariner Image Modifier

The Mariner Image Modifier (EMU) is a tool derived from Mariner Image Customizer (MIC).
This is invoked inside a chroot envirtonment where the desired filesystems are mounted, 
EMU uses the same api as MIC.


## Getting started

1. Create a customization config file.

   For example:

    ```yaml
    Users:
    - Name: user
      Password: password
    ```

3. Run the Mariner Image Modifier tool.

   For example:

    ```bash
    sudo ./imagemodifier \
      --config-file <config-file.yaml>
    ```

   Where:
   - `<config-file.yaml>`: The configuration file created in Step 1.
