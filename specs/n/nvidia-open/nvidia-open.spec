# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:       nvidia-open
Version:    610.57.04
Release:    1%{?dist}
Summary:    NVIDIA Driver meta-package
License:    NVIDIA License
URL:        http://nvidia.com
Vendor:     NVIDIA
Packager:   NVIDIA

BuildArch:  noarch

Provides:   nvidia-drivers = %{version}

# These must be defined after version is defined:
%global     branch %(echo %version | cut -d. -f1)

Provides:   cuda-drivers = %{version}
Obsoletes:  cuda-drivers < %{version}

Provides:   cuda-drivers-branch = %{version}
Obsoletes:  cuda-drivers-branch < %{version}

Provides:   cuda-drivers-%{branch} = %{version}
Obsoletes:  cuda-drivers-%{branch} < %{version}

Provides:   %{name}-%{branch} = %{version}
Obsoletes:  %{name}-%{branch} < %{version}

Requires:   nvidia-kmod = %{version}
Requires:   nvidia-driver-cuda = %{version}
Requires:   libnvidia-ml = %{version}

%description
NVIDIA Driver meta-package, Open GPU kernel modules, latest version
Meta-package containing all the available packages related to the NVIDIA driver.

%pretrans
if [ -x /usr/bin/nvidia-uninstall ]; then
    echo "Removing existing driver runfile install"
    /usr/bin/nvidia-uninstall -s || :
fi

%files

%changelog
