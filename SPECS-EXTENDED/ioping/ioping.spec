Name:           ioping
Version:        1.1
Release:        7%{?dist}
Summary:        Simple disk I/O latency monitoring tool
Vendor:         Microsoft Corporation
Distribution:   Mariner
License:        GPLv3+
URL:            https://github.com/koct9i/ioping
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  make

%description
ioping lets you monitor I/O latency in real time. It shows disk latency in 
the same way as ping shows network latency.

%prep
%autosetup

%build
export CFLAGS="-Wextra -pedantic -funroll-loops -ftree-vectorize %{optflags}"
export LDFLAGS="%{?__global_ldflags}"
%make_build

%install
%make_install PREFIX=%{_prefix}

%files
%doc changelog README.md
%license LICENSE
%{_bindir}/ioping
%{_mandir}/man1/ioping.1*

%changelog
* Mon Dec 27 2021 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 1.1-7
- Initial CBL-Mariner import from Fedora 34 (license: MIT).
- Verified license.

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Sep 16 2018 Robin Lee <cheeselee@fedoraproject.org> - 1.1-1
- Update to 1.1

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Dec 11 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.0-1
- Update to 1.0

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jul 14 2015 Christopher Meng <rpm@cicku.me> - 0.9-1
- Update to 0.9

* Fri Jan 03 2014 Christopher Meng <rpm@cicku.me> - 0.8-2
- Do not strip debug symbols.

* Tue Dec 31 2013 Christopher Meng <rpm@cicku.me> - 0.8-1
- Update to 0.8

* Fri Nov 09 2012 Christopher Meng <rpm@cicku.me> - 0.6-1
- Initial Package.
