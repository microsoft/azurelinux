ARG BASE_IMAGE
ARG AZL_ARCH
FROM ${BASE_IMAGE}
ARG AZL_ARCH

RUN dnf5 install --assumeyes --nogpgcheck --setopt=install_weak_deps=False \
    --repofrompath=azl-sdk,https://packages.microsoft.com/azurelinux/4.0/beta/sdk/${AZL_ARCH} \
    clamav-data createrepo_c python3-pytest \
    rpmlint rpminspect rpminspect-data-azurelinux rmdepcheck rpmdeplint \
    && dnf5 clean all

COPY . /opt/azl-component-tests
WORKDIR /opt/azl-component-tests
ENTRYPOINT ["python3", "-m", "pytest", "-p", "utils.pytest_plugin"]
