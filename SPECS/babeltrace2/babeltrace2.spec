Summary:        A trace manipulation toolkit
Name:           babeltrace2
Version:        2.0.4
Release:        2%{?dist}
License:        MIT AND GPLv2
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment
URL:            https://babeltrace.org/
Source0:        https://www.efficios.com/files/babeltrace/%{name}-%{version}.tar.bz2
Patch0:         00-fix-lttng-live-array-access.patch
BuildRequires:  elfutils-devel >= 0.154
BuildRequires:  gcc
BuildRequires:  glib-devel >= 2.28.0
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
Requires:       glib >= 2.28.0

%description -n libbabeltrace2
The libbabeltrace2 package contains a library and plugin system to view,
convert, transform, and analyze traces.

%package -n libbabeltrace2-devel
Summary:        Development files for libbabeltrace2
Requires:       glib >= 2.28.0
Requires:       libbabeltrace2%{?_isa} = %{version}-%{release}

%description -n libbabeltrace2-devel
The libbabeltrace2-devel package contains the header files and libraries
needed to develop programs that use the libbabeltrace2 trace manipulation
library.

%prep
%autosetup -p1

%build
%configure --disable-static \
        --enable-debug-info \
        --disable-Werror

%make_build

%check
make check

%install
%make_install
find %{buildroot} -type f -name "*.la" -delete -print
# Clean installed doc
rm -fv %{buildroot}%{_docdir}/babeltrace2/*

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%license LICENSE gpl-2.0.txt mit-license.txt
%doc ChangeLog README.adoc
%{_bindir}/babeltrace2
%{_mandir}/man1/*.1*
%{_mandir}/man7/*.7*

%files -n libbabeltrace2
%defattr(-,root,root)
%{_libdir}/*.so.*
%{_libdir}/babeltrace2/plugins/*.so

%files -n libbabeltrace2-devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/babeltrace2.pc
%{_libdir}/pkgconfig/babeltrace2-ctf-writer.pc

%changelog
* Thu Feb 10 2022 Nicolas Guibourge <nicolasg@microsoft.com> - 2.0.4-2
- Re-add 00-fix-lttng-live-array-access.patch

* Mon Jan 10 2022 Nicolas Guibourge <nicolasg@microsoft.com> - 2.0.4-1
- Upgrate to 2.0.4

* Wed Oct 14 2020 Olivia Crain <oliviacrain@microsoft.com> - 2.0.1-3
- Update Source0
- License verified

* Tue Feb 11 2020 Nick Bopp <nichbop@microsoft.com> - 2.0.1-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Added runtime dependency on glib2
- Remove python requirements
- Removed ldconfig_scriptlets
- Fix installed file cleanup

* Mon Feb 10 2020 Michael Jeanson <mjeanson@efficios.com> - 2.0.1-1
- New upstream release
