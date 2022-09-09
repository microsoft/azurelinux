Summary:        This is the klipper runtime image for the integrated service load balancer
Name:           klipper-lb
Version:        0.3.5
Release:        1%{?dist}
License:        ASL 2.0
URL:            https://github.com/k3s-io/klipper-lb
Group:          Applications/Text
Vendor:         Microsoft
Distribution:   Mariner
Source0:        https://github.com/k3s-io/%{name}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
#Note that the source file should be renamed to the format {name}-%{version}.tar.gz

# No build requirements

# Below is a manually created tarball, no download link.
# Packaging everything in this tarball needed to run, since network is disabled during build time.

# How to re-build this file:
# 1. git clone https://github.com/k3s-io/%%{name}.git 
# 2. cd %%{name}
# 3. git checkout tags/v%%{version}
# 4. make
# 5. cd ..
# 6. mv %%{name} %%{name}-%%{version}
# 7. tar -cf %%{name}-%%{version}.tar.gz %%{name}-%%{version}

%description
This is the klipper runtime image for the integrated service load balancer. 

%prep
%setup -q

# Already packaged the requirements since the build is offline
# Nothing to build

# Dockerfile.dapper runs CMD ["ci"], so place it in appropriate path

%install
install -d %{buildroot}%{_bindir}
install scripts/ci %{buildroot}%{_bindir}/ci

%files
%{_bindir}/ci

%changelog
* Mon Sep 07 2022 Vinayak Gupta <guptavinayak@microsoft.com> 0.3.5-1
- Original version for CBL-Mariner
- License Verified
