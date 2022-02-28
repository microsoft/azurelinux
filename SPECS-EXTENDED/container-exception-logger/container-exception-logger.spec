Vendor:         Microsoft Corporation
Distribution:   Mariner
%global _hardened_build 1

Name: container-exception-logger
Version: 1.0.3
Release: 5%{?dist}
Summary: Logging from a container to a host

License: GPLv3+
URL: https://github.com/abrt/container-exception-logger
# source is created by:
# git clone https://github.com/abrt/container-exception-logger
# cd container-exception-logger; tito build --tgz
Source0: %{name}-%{version}.tar.gz

BuildRequires: gcc
BuildRequires: asciidoc
BuildRequires: libxslt

%description
%{name} is a tool designed to run inside of
a container which is able to get its input outside of the container.

%prep
%setup -q

%build
%{__cc} %{optflags} src/container-exception-logger.c -o src/container-exception-logger
a2x -d manpage -f manpage man/container-exception-logger.1.asciidoc

%install
mkdir -p %{buildroot}%{_bindir}
cp src/container-exception-logger %{buildroot}/%{_bindir}/container-exception-logger

mkdir -p %{buildroot}/%{_mandir}/man1
cp man/container-exception-logger.1 %{buildroot}/%{_mandir}/man1/container-exception-logger.1

%files
%{_bindir}/container-exception-logger
%{_mandir}/man1/container-exception-logger.1.*
%license COPYING

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0.3-5
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Jan 13 2020 Tom Stellard <tstellar@redhat.com> - 1.0.3-3
- Use __cc macro instead of hard-coding gcc

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jun 05 2019 Martin Kutlak <mkutlak@redhat.com> 1.0.3-1
- Use a correct command name in helper (mkutlak@redhat.com)
- Drop the setuid wrapper (mkutlak@redhat.com)
- license is actually GPLv3+ (msuchy@redhat.com)

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Mar 26 2018 Matej Habrnal <mhabrnal@redhat.com> 1.0.2-1
- Use _hardened_build macro (mhabrnal@redhat.com)
- Add license (mhabrnal@redhat.com)

* Fri Mar 23 2018 Unknown name 1.0.1-1
- new package built with tito

* Thu Mar 08 2018 Matej Habrnal <mhabrnal@redhat.com> 1.0.0-1
- init
