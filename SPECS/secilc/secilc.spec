%global libsepolver 2.9-1

Name:           secilc
Version:        2.9
Release:        2%{?dist}
Summary:        The SELinux CIL Compiler

License:        BSD
URL:            https://github.com/SELinuxProject/selinux/wiki
Source0:        https://github.com/SELinuxProject/selinux/releases/download/20190315/secilc-2.9.tar.gz
Patch0001:	0001-Allow-setting-arguments-to-xmlto-via-environmental-v.patch

BuildRequires:  gcc
BuildRequires:  libsepol-devel >= %{libsepolver}, flex, xmlto

%description
The SELinux CIL Compiler is a compiler that converts the CIL language as
described on the CIL design wiki into a kernel binary policy file.
Please see the CIL Design Wiki at:
http://github.com/SELinuxProject/cil/wiki/
for more information about the goals and features on the CIL language.

%prep
%autosetup -p 1 -n secilc-%{version}


%build
%set_build_flags
# xmlto wants to access a network resource for validation, so skip it
make %{?_smp_mflags} LIBSEPOL_STATIC=%{_libdir}/libsepol.a XMLARGS="--skip-validation"


%install
make %{?_smp_mflags} DESTDIR="%{buildroot}" SBINDIR="%{buildroot}%{_sbindir}" LIBDIR="%{buildroot}%{_libdir}" install


%files
%{_bindir}/secilc
%{_bindir}/secil2conf
%{_mandir}/man8/secilc.8.gz
%{_mandir}/man8/secil2conf.8.gz
%license COPYING

%changelog
* Thu Aug 27 2020 Daniel Burgener <daburgen@microsoft.com> - 2.9-2
- Initial import from Fedora 31
