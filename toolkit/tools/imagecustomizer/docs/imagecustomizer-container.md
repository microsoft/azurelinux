# Using the Image Customizer Container

The Image Customizer container is designed to simplify the process of
customizing and configuring system images using the Mariner Image Customizer
(MIC) tool. This container can pull an OCI artifact that includes a VHDX file
and then uses the MIC tool to customize the image based on provided
configuration settings.

## Running the Container

To use the Image Customizer container, you will need to pass several parameters
and mount appropriate volumes for the image and device access. Below is a
step-by-step guide on how to run this container:

### Prepare Your Environment

Ensure that your configuration file (config.yaml) is ready and accessible. This
file should define the customization parameters for the MIC tool. Details please
see
[configuration.md](https://github.com/microsoft/azurelinux/blob/3.0-dev/toolkit/tools/imagecustomizer/docs/configuration.md).

### Run the Container

Pull the image:

```
docker pull mcr.microsoft.com/azurelinux/imagecustomizer:<tag>
```

You can use your own base image, for example:

```
docker run --rm --privileged=true \
   -v ~/image:/image:z \
   -v /dev:/dev \
   mcr.microsoft.com/azurelinux/imagecustomizer:0.3.0 \
   --image-file /baseimg.vhdx \
   --config-file /config.yaml \
   --output-image-format raw \
   --output-image-file /image/customized.raw
```

Or you can also use our default minimal-os as the base image, for example:

```
docker run --rm --privileged=true \
   -v ~/image:/image:z \
   -v /dev:/dev \
   mcr.microsoft.com/azurelinux/imagecustomizer:0.3.0 \
   /process-oci-artifact.sh \
   mcr.microsoft.com/azurelinux/image/minimal-os:latest \
   --config-file /config.yaml \
   --output-image-format raw \
   --output-image-file /image/customized.raw
```

### Check the Output

After the container executes, check the output directory on your host for the
customized image file. This file contains your customized system image.
