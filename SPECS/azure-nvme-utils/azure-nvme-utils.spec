Name:           azure-nvme-utils
Version:        0.1.1
Release:        1%{?dist}
Summary:        Utility and udev rules to help identify Azure NVMe devices

License:        MIT
URL:            https://github.com/Azure/%{name}
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  binutils
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  glibc-devel
BuildRequires:  kernel-headers

%description
Utility and udev rules to help identify Azure NVMe devices.

%prep
%autosetup

%build
%cmake .
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

%files
/usr/sbin/azure-nvme-id
/lib/udev/rules.d/80-azure-nvme.rules

%changelog
* Mon Mar 18 2024 Chris Patterson <cpatterson@microsoft.com> - 0.1.1-1
- Original version for CBL-Mariner.
- License verified.
- Initial package.
