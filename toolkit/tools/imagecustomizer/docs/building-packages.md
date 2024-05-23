# Building custom packages

This is a guide on how to build custom packages for Azure Linux.
Once built, the RPM files can be provided to the Image Customizer tool using the
[--rpm-source](cli.md#--rpm-sourcepath) command-line arg.

This guide uses an Azure Linux container and docker to build the packages.
This avoids the complexity of using the Azure Linux toolkit (which has to be capable of
building Azure Linux from scratch, including on other Linux distros).

## Quick start

1. Create a file called `samplescript.sh` with the following contents:

   ```bash
   echo "Hello, World"
   ```

2. Create a file called `samplepackage.spec` with the following contents:

   ```rpmspec
   Summary:    A sample package
   Name:       samplepackage
   Version:    0.0.1
   Release:    1%{?dist}
   Vendor:     Contoso
   License:    Proprietary

   Source0:    samplescript.sh

   Requires:   bash

   %description
   A very descriptive description for the sample package.

   %prep

   %build

   %install
   install -D -m 755 %{SOURCE0} %{buildroot}%{_bindir}/samplescript.sh

   %files
   %{_bindir}/samplescript.sh
   ```

3. Create a file called `samplepackage.Dockerfile` with the following contents:

   Azure Linux 2.0:

   ```Dockerfile
   FROM mcr.microsoft.com/cbl-mariner/base/core:2.0

   RUN tdnf update -y
   RUN tdnf install -y rpm-build

   WORKDIR /work

   COPY samplepackage.spec .
   COPY samplescript.sh /usr/src/mariner/SOURCES/

   RUN rpmbuild -bb --build-in-place samplepackage.spec
   ```

   Azure Linux 3.0:

   ```Dockerfile
   FROM mcr.microsoft.com/azurelinux/base/core:3.0

   RUN tdnf update -y
   RUN tdnf install -y rpm-build

   WORKDIR /work

   COPY samplepackage.spec .
   COPY samplescript.sh /usr/src/azl/SOURCES/

   RUN rpmbuild -bb --build-in-place samplepackage.spec
   ```

4. Build the rpm file using docker:

   ```bash
   docker build -t samplepackage:latest -f samplepackage.Dockerfile .
   ```

5. Extract RPM file(s) from the container image:

   ```bash
   id=$(docker create samplepackage:latest)
   docker cp $id:/usr/src/mariner/RPMS ./
   docker rm -v $id
   ```

## Helpful links

- [Official documentation for RPM spec file format](https://rpm-software-management.github.io/rpm/manual/spec.html)
