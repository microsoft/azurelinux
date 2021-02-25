# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Creates a container (default mariner_cross_compile:mcc) from the gcc libs and busybox

# ====== Arguments ======
# -c        clean up any existing images with the same name, and associated containers
# -h        help message
# -n=NAME   use a custom name for the image

# ====== Prerequisites ======
# Both the gcc and busybox builds must have been completed, and are in /opt/cross

installDir="/opt/cross"
buildDir="$HOME/cross"
scriptDir="$( cd "$( dirname "$0" )" && pwd )"
dockerBuildDir=${scriptDir}/dockerbuild

cross_image_tag="mcc"
cross_image_name="mariner_cross_compile"
cleanup="false"

usage() {
    echo "Usage: $(basename "$0") [OPTION]..."
    echo "  -c          clear any old versions of the image, and all associated containers"
    echo "  -h          print this message"
    echo "  -n=NAME     set a custom name for the image"
}

while getopts 'chn:' opt; do
    case "${opt}" in
        c) cleanup="true" ;;
        h) usage
           exit 0 ;;
        n) cross_image_name="${OPTARG}" ;;
        *) echo "Unknown arg '${opt}'"
           usage
           exit 1 ;;
    esac
done

rm -rf ${dockerBuildDir}

if [ "${cleanup}" = true ]; then
    cross_images=$(docker images -q "*:${cross_image_tag}")
    if [ -n "${cross_images}" ]; then
        for image in ${cross_images}; do
            echo "Removing existing container with ID: ${image}"
            cross_containers="$(docker container ls -aq --filter ancestor=${image})"
            echo "Removing containers which use that image: ${cross_containers}"
            [ -n "${cross_containers}" ] && docker rm ${cross_containers}
            docker image rm -f ${image}
        done
    fi
fi

echo "Configuring QEMU multi arch support"
docker run --rm --privileged multiarch/qemu-user-static --reset -p yes

echo "Creating base container"
mkdir ${dockerBuildDir}
cp ${scriptDir}/Dockerfile                      ${dockerBuildDir}/
cp -r ${installDir}/aarch64-mariner-linux-gnu/sysroot   ${dockerBuildDir}/

docker build -t ${cross_image_name}:${cross_image_tag} ${dockerBuildDir}

rm -rf ${dockerBuildDir}

echo "Run 'docker run -it ${cross_image_name}:${cross_image_tag} /bin/sh' to start an interactive container"