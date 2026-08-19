# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           babeltrace2
Version:        2.1.2
Release: 6%{?dist}
Summary:        A trace manipulation toolkit
License:        MIT AND GPL-2.0-only
URL:            https://www.efficios.com/babeltrace
Source0:        https://www.efficios.com/files/babeltrace/babeltrace2-%{version}.tar.bz2
Source1:        https://www.efficios.com/files/babeltrace/babeltrace2-%{version}.tar.bz2.asc
# gpg2 --export --export-options export-minimal 7F49314A26E0DE78427680E05F1B2A0789F12B11 > gpgkey-7F49314A26E0DE78427680E05F1B2A0789F12B11.gpg
Source2:        gpgkey-7F49314A26E0DE78427680E05F1B2A0789F12B11.gpg

BuildRequires:  autoconf >= 2.69
BuildRequires:  automake >= 1.13
BuildRequires:  bison >= 2.5
BuildRequires:  elfutils-devel >= 0.154
BuildRequires:  flex >= 2.5.35
BuildRequires:  gcc
BuildRequires:  gcc-g++
BuildRequires:  glib2-devel >= 2.28.0
BuildRequires:  gnupg2
BuildRequires:  libtool >= 2.2
BuildRequires:  make
BuildRequires:  python3-devel >= 3.4
BuildRequires:  python3-setuptools
BuildRequires:  swig >= 3.0

Requires:       libbabeltrace2%{?_isa} = %{version}-%{release}

%description
The Babeltrace 2 project offers a library with a C API, Python 3 bindings, and
a command-line tool which makes it very easy for mere mortals to view,
convert, transform, and analyze traces.

Babeltrace 2 is also the reference parser implementation of the Common Trace
Format (CTF), a very versatile trace format followed by various tracers and
tools such as LTTng and barectf.


%package -n libbabeltrace2
Summary:        A trace manipulation library

%description -n libbabeltrace2
The libbabeltrace2 package contains a library and plugin system to view,
convert, transform, and analyze traces.


%package -n libbabeltrace2-devel
Summary:        Development files for libbabeltrace2
Requires:       libbabeltrace2%{?_isa} = %{version}-%{release} glib2-devel

%description -n libbabeltrace2-devel
The libbabeltrace2-devel package contains the header files and libraries
needed to develop programs that use the libbabeltrace2 trace manipulation
library.


%package -n python3-bt2
Summary:        libbabeltrace2 Python bindings
Requires:       libbabeltrace2%{?_isa} = %{version}-%{release}

%description -n python3-bt2
The python3-bt2 package provides Python 3 bindings for libbabeltrace2.


%prep
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%autosetup -p1

%build
# Reinitialize libtool with the fedora version to remove Rpath
autoreconf -vif

export PYTHON=%{__python3}
export PYTHON_CONFIG=%{__python3}-config
%configure --disable-static \
	--enable-python-bindings \
	--enable-python-plugins \
	--enable-debug-info \
	--disable-Werror

make %{?_smp_mflags} V=1

%check
make %{?_smp_mflags} check

%install
make DESTDIR=%{buildroot} install
find %{buildroot} -type f -name "*.la" -delete
# Clean installed doc
rm -f %{buildroot}/%{_pkgdocdir}/CONTRIBUTING.adoc
rm -f %{buildroot}/%{_pkgdocdir}/LICENSE
rm -f %{buildroot}/%{_pkgdocdir}/std-ext-lib.md

%ldconfig_scriptlets  -n lib%{name}

%files
%doc ChangeLog
%doc README.adoc
%{!?_licensedir:%global license %%doc}
%license LICENSE
%{_bindir}/babeltrace2
%{_mandir}/man1/*.1*
%{_mandir}/man7/*.7*

%files -n libbabeltrace2
%{!?_licensedir:%global license %%doc}
%license LICENSE
%{_libdir}/*.so.*
%{_libdir}/babeltrace2/plugin-providers/*.so
%{_libdir}/babeltrace2/plugins/*.so

%files -n libbabeltrace2-devel
%{_prefix}/include/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/babeltrace2.pc
%{_libdir}/pkgconfig/babeltrace2-ctf-writer.pc

%files -n python3-bt2
%{python3_sitearch}/bt2
%{python3_sitearch}/bt2*.egg-info


%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 2.1.2-3
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 2.1.2-2
- Rebuilt for Python 3.14.0rc2 bytecode

* Thu Jul 24 2025 Michael Jeanson <mjeanson@efficios.com> - 2.1.2-1
- New upstream release

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 2.1.1-2
- Rebuilt for Python 3.14

* Tue Apr 15 2025 Michael Jeanson <mjeanson@efficios.com> - 2.1.1-1
- New upstream release

* Thu Jan 23 2025 Michael Jeanson <mjeanson@efficios.com> - 2.1.0-1
- New upstream release

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Oct 14 2024 Jitka Plesnikova <jplesnik@redhat.com> - 2.0.6-4
- Fix for SWIG 4.3.0

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 2.0.6-2
- Rebuilt for Python 3.13

* Tue Apr 02 2024 Kienan Stewart <kstewart@efficios.com> - 2.0.6-1
- New upstream release

* Tue Jan 23 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jun 16 2023 Michael Jeanson <mjeanson@efficios.com> - 2.0.5-3
- Fix tests on Python 3.12

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 2.0.5-2
- Rebuilt for Python 3.12

* Tue May 23 2023 Michael Jeanson <mjeanson@efficios.com> - 2.0.5-1
- New upstream release

* Mon May 08 2023 Michael Jeanson <mjeanson@efficios.com> - 2.0.4-9
- migrated to SPDX license

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jan 05 2023 Michael Jeanson <mjeanson@efficios.com> - 2.0.4-7
- Add builddep on python3-setuptools for python 3.12 (RHBZ:#2155040)

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 2.0.4-5
- Rebuilt for Python 3.11

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 2.0.4-2
- Rebuilt for Python 3.10

* Wed Feb 24 2021 Michael Jeanson <mjeanson@efficios.com> - 2.0.4-1
- New upstream release

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 2.0.3-2
- Rebuilt for Python 3.9

* Fri Apr 24 2020 Michael Jeanson <mjeanson@efficios.com> - 2.0.3-1
- New upstream release

* Thu Mar 12 2020 Michael Jeanson <mjeanson@efficios.com> - 2.0.2-1
- New upstream release

* Mon Feb 10 2020 Michael Jeanson <mjeanson@efficios.com> - 2.0.1-1
- New upstream release
