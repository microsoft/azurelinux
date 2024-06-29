ARG baseimage
FROM ${baseimage}

RUN tdnf update -y && \
   tdnf install -y dnf dnf-plugins-core createrepo_c

# Download the RPMs needed by the following tests:
# - TestCustomizeImageAddPackage
RUN dnf download -y --resolve --alldeps --destdir /downloadedrpms \
    jq \
    golang

# Add repo metadata, so that the directory can be used in a .repo file.
RUN createrepo --compatibility --update /downloadedrpms
