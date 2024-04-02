# Running ImageCustomizer in A Container

The Mariner Image Customizer users may desire to run it from within a
container. To facilitate this scenario, we are including in this folder
two scripts:
- `build-mic-container.sh` [[here](./build-mic-container.sh)]
  - builds a container holding the Mariner Image Customizer binary and
    necessary dependencies. For example:
    ```bash
    containerRegistery=mcr.azurecr.io
    containerName=imagecustomizer
    containerTag=v0.0.3

    ./build-mic-container.sh \
        -r $containerRegistery \
        -n $containerName \
        -t $containerTag
    ```

- `run-mic-container.sh` [[here](./run-mic-container.sh)]
  - runs the container and invokes the embedded Mariner Image Customizer binary
    with the provided arguments. For example:
    ```bash
    containerRegistery=mcr.azurecr.io
    containerName=imagecustomizer
    containerTag=v0.0.3

    ./run-mic-container.sh \
        -r $containerRegistery \
        -n $containerName \
        -t $containerTag \
        -i ~/my-inputs/core-3.0.20240129.1326.vhdx \
        -c ~/my-inputs/mic-config-iso.yaml \
        -f iso \
        -o ~/my-outputs/mic-$(date +'%Y%m%d-%H%M').iso \
        -l debug
    ```
