# Building custom packages

This is a guide on how to build your own packages for Azure Linux.

This guide uses an Azure Linux container to build the packages.
This method is generally a lot easier than trying to use the Azure Linux toolkit, which
is only really necessary when you need to build Azure Linux from scratch.

## Quick start

1. Create a file called `samplescript.sh` with the following contents:

   ```bash
   echo "Hello, World"
   ```

2. Create a file called `samplepackage.spec` with the following contents:

   ```rpmspec
   Summary:        A sample package
   Name:           samplepackage
   Version:        0.0.1
   Release:        1%{?dist}
   Vendor:         Contoso
   License:        Proprietary

   Source0:        samplescript.sh

   %description
   A very descriptive description for the sample package.

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

4. Build the rpm file using `docker`, by running:

   ```bash
   docker build -t samplepackage:latest -f samplepackage.Dockerfile .
   ```

5. Extract RPM file(s) from container:

   ```bash
   id=$(docker create samplepackage:latest)
   docker cp $id:/usr/src/mariner/RPMS ./
   docker rm -v $id
   ```
