%define htmldir %{_docdir}/liblognorm/html
Summary:        Fast samples-based log normalization library
Name:           liblognorm
Version:        2.0.6
Release:        2%{?dist}
License:        LGPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://www.liblognorm.com
Source0:        https://www.liblognorm.com/files/download/%{name}-%{version}.tar.gz
BuildRequires:  chrpath
BuildRequires:  gcc
BuildRequires:  libestr-devel
BuildRequires:  libfastjson-devel
BuildRequires:  pcre-devel
BuildRequires:  python3-devel
BuildRequires:  python3-sphinx

%description
Briefly described, liblognorm is a tool to normalize log data.

People who need to take a look at logs often have a common problem. Logs from
different machines (from different vendors) usually have different formats for
their logs. Even if it is the same type of log (e.g. from firewalls), the log
entries are so different, that it is pretty hard to read these. This is where
liblognorm comes into the game. With this tool you can normalize all your logs.
All you need is liblognorm and its dependencies and a sample database that fits
the logs you want to normalize.

%package        devel
Summary:        Development tools for programs using liblognorm library
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       json-c-devel%{?_isa}
Requires:       libestr-devel%{?_isa}

%description    devel
The liblognorm-devel package includes header files, libraries necessary for
developing programs which use liblognorm library.

%package        doc
Summary:        HTML documentation for liblognorm

%description    doc
This sub-package contains documentation for liblognorm in a HTML form.

%package        utils
Summary:        Lognormalizer utility for normalizing log files
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description utils
The lognormalizer is the core of liblognorm, it is a utility for normalizing
log files.

%prep
%autosetup

%build
%configure \
    --enable-regexp \
    --enable-docs \
    --docdir=%{htmldir} \
    --includedir=%{_includedir}/%{name}/

%install
%make_install INSTALL="install -p"
rm -f %{buildroot}/%{_libdir}/*.{a,la}
chrpath -d %{buildroot}%{_bindir}/lognormalizer
chrpath -d %{buildroot}%{_libdir}/liblognorm.so
rm %{buildroot}%{htmldir}/{objects.inv,.buildinfo}

%ldconfig_scriptlets

%files
%license COPYING
%doc AUTHORS ChangeLog README
%exclude %{htmldir}
%{_libdir}/lib*.so.*

%files devel
%{_libdir}/lib*.so
%{_includedir}/%{name}/*.h
%{_libdir}/pkgconfig/*.pc

%files doc
%doc %{htmldir}

%files utils
%{_bindir}/lognormalizer

%changelog
* Sun Feb 13 2022 Jon Slobodzian <joslobo@microsoft.com> - 2.0.6-2
- Add missing dependency on python-devel

* Mon Jan 10 2022 Henry Li <lihl@microsoft.com> - 2.0.6-1
- Upgrade to version 2.0.6

* Tue Jul 20 2021 Olivia Crain <oliviacrain@microsoft.com> - 2.0.3-11
- License verified
- Spec linted

* Tue Jan 12 2021 Joe Schmitt <joschmit@microsoft.com> - 2.0.3-10
- Initial CBL-Mariner import from Fedora 32 (license: MIT)
- Explicit require python3-sphinx instead of unversioned.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Oct 12 2017 Marek Tamaskovic <mtamasko@redhat.com> - 2.0.3-4
- Fix header files location
- resolves rhbz#1113573

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Mar 29 2017 Radovan Sroka <rsroka@redhat.com> - 2.0.2-1
- rebase to 2.0.3

* Thu Feb 9 2017 Radovan Sroka <rsroka@redhat.com> - 2.0.2-2
- removed forgoten commented line

* Thu Feb 9 2017 Radovan Sroka <rsroka@redhat.com> - 2.0.2-1
- rebase to 2.0.2

* Tue Oct 4 2016 Radovan Sroka <rsroka@redhat.com> - 2.0.1-1
- rebase to 2.0.1

* Tue Mar 15 2016 Radovan Sroka <rsroka@redhat.com> - 1.1.3-1
- rebase to v1.1.3

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Mar 15 2015 Tomas Heinrich <theinric@redhat.com> - 1.1.1-1
- rebase to 1.1.1 (soname bump)
  - drop liblognorm-0.3.4-pc-file.patch, not needed anymore
  - update dependencies for the new version
  - add a new subpackage for documentation
  - enable support for reqular expressions
- make build more verbose

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Jul 31 2013 Tomas Heinrich <theinric@redhat.com> - 0.3.7-1
- rebase to 0.3.7

* Wed Dec 12 2012 Mahaveer Darade <mah.darade@gmail.com> - 0.3.5-1
- upgrade to upstream version 0.3.5
- drop patch0, merged upstream
  liblognorm-0.3.4-rename-to-lognormalizer.patch
- remove trailing whitespace

* Fri Oct 05 2012 mdarade <mdarade@redhat.com> - 0.3.4-4
- Modified description of main & util package

* Thu Sep 20 2012 Mahaveer Darade <mdarade@redhat.com> - 0.3.4-3
- Renamed normalizer binary to lognormalizer
- Updated pc file to exclude lee and lestr

* Mon Aug 27 2012 mdarade <mdarade@redhat.com> - 0.3.4-2
- Updated BuildRequires to contain libestr-devel

* Wed Aug  1 2012 Milan Bartos <mbartos@redhat.com> - 0.3.4-1
- initial port
