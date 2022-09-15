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
# All files needed are already present in the tarball which is directly provisioned from the repo's appropriate version
# No need to create any modified tarball

%description
This is the klipper runtime image for the integrated service load balancer. 

%prep
%setup -q

# Nothing to build as the files needed by Dockerfile in the repo, are already present in the tarball downloaded.

# Dockerfile in the package folder runs CMD ["entry"], so putting this bash script file in appropriate location.
# So that it can be executed without any problem.

%install
install -d %{buildroot}%{_bindir}
install entry %{buildroot}%{_bindir}/entry

%files
%{_bindir}/entry

%changelog
* Tue Sep 13 2022 Vinayak Gupta <guptavinayak@microsoft.com> - 0.3.5-1
- Original version for CBL-Mariner
- License Verified
