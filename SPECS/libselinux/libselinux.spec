## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autochangelog
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%define ruby_inc %(pkg-config --cflags ruby)
%define libsepolver 3.9-1

Summary: SELinux library and simple utilities
Name: libselinux
Version: 3.9
Release: 5%{?dist}
License: LicenseRef-Fedora-Public-Domain
# https://github.com/SELinuxProject/selinux/wiki/Releases
Source0: https://github.com/SELinuxProject/selinux/releases/download/%{version}/libselinux-%{version}.tar.gz
Source1: https://github.com/SELinuxProject/selinux/releases/download/%{version}/libselinux-%{version}.tar.gz.asc
Source2: https://github.com/bachradsusi.gpg
Source3: selinuxconlist.8
Source4: selinuxdefcon.8

Url: https://github.com/SELinuxProject/selinux/wiki
# $ git clone https://github.com/fedora-selinux/selinux.git
# $ cd selinux
# $ git format-patch -N 3.9 -- libselinux
# $ i=1; for j in 00*patch; do printf "Patch%04d: %s\n" $i $j; i=$((i+1));done
# Patch list start
Patch0001: 0001-Use-SHA-2-instead-of-SHA-1.patch
# Patch list end
BuildRequires: gcc make
BuildRequires: ruby-devel ruby libsepol-static >= %{libsepolver} swig pcre2-devel
BuildRequires: python3 python3-devel python3-setuptools python3-pip
BuildRequires: (python3-wheel if python3-setuptools < 71)
BuildRequires: systemd
BuildRequires: gnupg2
Requires: libsepol%{?_isa} >= %{libsepolver} pcre2
Conflicts: filesystem < 3, selinux-policy-base < 3.13.1-138

%description
Security-enhanced Linux is a feature of the Linux® kernel and a number
of utilities with enhanced security functionality designed to add
mandatory access controls to Linux.  The Security-enhanced Linux
kernel contains new architectural components originally developed to
improve the security of the Flask operating system. These
architectural components provide general support for the enforcement
of many kinds of mandatory access control policies, including those
based on the concepts of Type Enforcement®, Role-based Access
Control, and Multi-level Security.

libselinux provides an API for SELinux applications to get and set
process and file security contexts and to obtain security policy
decisions.  Required for any applications that use the SELinux API.

%package utils
Summary: SELinux libselinux utilities
Requires: %{name}%{?_isa} = %{version}-%{release}

%description utils
The libselinux-utils package contains the utilities

%package -n python3-libselinux
Summary: SELinux python 3 bindings for libselinux
Requires: %{name}%{?_isa} = %{version}-%{release}
%{?python_provide:%python_provide python3-libselinux}
# Remove before F30
Provides: %{name}-python3 = %{version}-%{release}
Provides: %{name}-python3%{?_isa} = %{version}-%{release}
Obsoletes: %{name}-python3 < %{version}-%{release}

%description -n python3-libselinux
The libselinux-python3 package contains python 3 bindings for developing
SELinux applications. 

%package ruby
Summary: SELinux ruby bindings for libselinux
Requires: %{name}%{?_isa} = %{version}-%{release}
Provides: ruby(selinux)

%description ruby
The libselinux-ruby package contains the ruby bindings for developing 
SELinux applications. 

%package devel
Summary: Header files and libraries used to build SELinux
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: libsepol-devel%{?_isa} >= %{libsepolver}

%description devel
The libselinux-devel package contains the libraries and header files
needed for developing SELinux applications. 

%package static
Summary: Static libraries used to build SELinux
Requires: %{name}-devel%{?_isa} = %{version}-%{release}

%description static
The libselinux-static package contains the static libraries
needed for developing SELinux applications. 

%prep
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%autosetup -p 2 -n libselinux-%{version}

%build
export DISABLE_RPM="y"
export USE_PCRE2="y"

%set_build_flags
CFLAGS="$CFLAGS -fno-semantic-interposition"

# To support building the Python wrapper against multiple Python runtimes
# Define a function, for how to perform a "build" of the python wrapper against
# a specific runtime:
BuildPythonWrapper() {
  BinaryName=$1

  # Perform the build from the upstream Makefile:
  %make_build \
    PYTHON=$BinaryName \
    LIBDIR="%{_libdir}" \
    pywrap
}

%make_build LIBDIR="%{_libdir}" swigify
%make_build LIBDIR="%{_libdir}" all

BuildPythonWrapper %{__python3}

%make_build RUBYINC="%{ruby_inc}" SHLIBDIR="%{_libdir}" LIBDIR="%{_libdir}" LIBSEPOLA="%{_libdir}/libsepol.a" rubywrap

%install
InstallPythonWrapper() {
  BinaryName=$1

  make \
    PYTHON=$BinaryName \
    PIP_NO_BUILD_ISOLATION=0 \
    DESTDIR="%{buildroot}" LIBDIR="%{_libdir}" \
    SHLIBDIR="%{_lib}" BINDIR="%{_bindir}" \
    SBINDIR="%{_sbindir}" \
    LIBSEPOLA="%{_libdir}/libsepol.a" \
    install-pywrap
}

rm -rf %{buildroot}
mkdir -p %{buildroot}%{_tmpfilesdir}
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_includedir}
mkdir -p %{buildroot}%{_sbindir}
install -d -m 0755 %{buildroot}%{_rundir}/setrans
echo "d %{_rundir}/setrans 0755 root root" > %{buildroot}%{_tmpfilesdir}/libselinux.conf

InstallPythonWrapper %{__python3}

%make_install LIBDIR="%{_libdir}" SHLIBDIR="%{_libdir}" BINDIR="%{_bindir}" SBINDIR="%{_sbindir}"
make DESTDIR="%{buildroot}" RUBYINSTALL=%{ruby_vendorarchdir} install-rubywrap

# Nuke the files we don't want to distribute
rm -f %{buildroot}%{_sbindir}/compute_*
rm -f %{buildroot}%{_sbindir}/deftype
rm -f %{buildroot}%{_sbindir}/execcon
rm -f %{buildroot}%{_sbindir}/getenforcemode
rm -f %{buildroot}%{_sbindir}/getfilecon
rm -f %{buildroot}%{_sbindir}/getpidcon
rm -f %{buildroot}%{_sbindir}/mkdircon
rm -f %{buildroot}%{_sbindir}/policyvers
rm -f %{buildroot}%{_sbindir}/setfilecon
rm -f %{buildroot}%{_sbindir}/selinuxconfig
rm -f %{buildroot}%{_sbindir}/selinuxdisable
rm -f %{buildroot}%{_sbindir}/getseuser
rm -f %{buildroot}%{_sbindir}/togglesebool
rm -f %{buildroot}%{_sbindir}/selinux_check_securetty_context
mv %{buildroot}%{_sbindir}/getdefaultcon %{buildroot}%{_sbindir}/selinuxdefcon
mv %{buildroot}%{_sbindir}/getconlist %{buildroot}%{_sbindir}/selinuxconlist
install -d %{buildroot}%{_mandir}/man8/
install -m 644 %{SOURCE3} %{buildroot}%{_mandir}/man8/
install -m 644 %{SOURCE4} %{buildroot}%{_mandir}/man8/
rm -f %{buildroot}%{_mandir}/man8/togglesebool*

%ldconfig_scriptlets

%files
%license LICENSE
%{_libdir}/libselinux.so.*
%dir %{_rundir}/setrans/
%{_tmpfilesdir}/libselinux.conf

%files utils
%{_sbindir}/avcstat
%{_sbindir}/getenforce
%{_sbindir}/getpidprevcon
%{_sbindir}/getpolicyload
%{_sbindir}/getsebool
%{_sbindir}/matchpathcon
%{_sbindir}/sefcontext_compile
%{_sbindir}/selinuxconlist
%{_sbindir}/selinuxdefcon
%{_sbindir}/selinuxexeccon
%{_sbindir}/selinuxenabled
%{_sbindir}/setenforce
%{_sbindir}/selabel_compare
%{_sbindir}/selabel_digest
%{_sbindir}/selabel_lookup
%{_sbindir}/selabel_lookup_best_match
%{_sbindir}/selabel_partial_match
%{_sbindir}/selinux_check_access
%{_sbindir}/selabel_get_digests_all_partial_matches
%{_sbindir}/validatetrans
%{_mandir}/man5/*
%{_mandir}/man8/*

%files devel
%{_libdir}/libselinux.so
%{_libdir}/pkgconfig/libselinux.pc
%{_includedir}/selinux/
%{_mandir}/man3/*

%files static
%{_libdir}/libselinux.a

%files -n python3-libselinux
%{python3_sitearch}/selinux/
%{python3_sitearch}/selinux-%{version}*
%{python3_sitearch}/_selinux*

%files ruby
%{ruby_vendorarchdir}/selinux.so

%changelog
## START: Generated by rpmautospec
* Mon Apr 06 2026 azldev <> - 3.9-8
- Latest state for libselinux

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 3.9-7
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 3.9-6
- Rebuilt for Python 3.14.0rc2 bytecode

* Tue Jul 29 2025 Miro Hrončok <miro@hroncok.cz> - 3.9-3
- Drop unused BuildRequires on python3-wheel

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jul 16 2025 Petr Lautrbach <lautrbach@redhat.com> - 3.9-1
- SELinux userspace 3.9 release

* Mon Jun 30 2025 Petr Lautrbach <lautrbach@redhat.com> - 3.9-0.rc2.1
- SELinux userspace 3.9-rc2 release

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 3.8-3
- Rebuilt for Python 3.14

* Tue May 27 2025 Petr Lautrbach <lautrbach@redhat.com> - 3.8-2
- Prioritize local literal fcontext definitions (rhbz#2360183)

* Thu Jan 30 2025 Petr Lautrbach <lautrbach@redhat.com> - 3.8-1
- SELinux userspace 3.8 release

* Mon Jan 20 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.8-0.rc3.1.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sun Jan 12 2025 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3.8-0.rc3.1.2
- Rebuilt for the bin-sbin merge (2nd attempt)

* Wed Jan 08 2025 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.8-0.rc3.1.1
- Rebuild for https://fedoraproject.org/wiki/Changes/Ruby_3.4

* Wed Dec 18 2024 Petr Lautrbach <lautrbach@redhat.com> - 3.8-0.rc3.1
- SELinux userspace 3.8-rc3 release

* Wed Dec 04 2024 Petr Lautrbach <lautrbach@redhat.com> - 3.8-0.rc1.2
- libselinux/utils: drop reachable assert in sefcontext_compile

* Thu Nov 28 2024 Petr Lautrbach <lautrbach@redhat.com> - 3.8-0.rc1.1
- SELinux userspace 3.8-rc1 release

* Mon Nov 11 2024 Vit Mojzis <vmojzis@redhat.com> - 3.7-7
- setexecfilecon: Remove useless rc check
- matchpathcon: RESOURCE_LEAK: Variable "con"

* Thu Oct 17 2024 Petr Lautrbach <lautrbach@redhat.com> - 3.7-6.1
- fix swig bindings for 4.3.0

* Tue Sep 10 2024 Vit Mojzis <vmojzis@redhat.com> - 3.7-6
- restorecon: Include <selinux/label.h>
- Fix integer comparison issues when compiling for 32-bit
- deprecate security_disable(3)

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jul 11 2024 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3.7-4
- Rebuilt for the bin-sbin merge (again)

* Tue Jul 09 2024 Petr Lautrbach <lautrbach@redhat.com> - 3.7-3
- set free'd data to NULL (#2295428)

* Tue Jul 09 2024 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3.7-2
- Rebuilt for the bin-sbin merge

* Thu Jun 27 2024 Petr Lautrbach <lautrbach@redhat.com> - 3.7-1
- SELinux userspace 3.7 release

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 3.6-6
- Rebuilt for Python 3.13

* Mon Apr 01 2024 Christoph Erhardt <fedora@sicherha.de> - 3.6-5
- Drop unused `xz-devel` build dependency

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jan 03 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.6-2
- Rebuild for https://fedoraproject.org/wiki/Changes/Ruby_3.3

* Thu Dec 14 2023 Petr Lautrbach <lautrbach@redhat.com> - 3.6-1
- SELinux userspace 3.6 release

* Thu Nov 23 2023 Petr Lautrbach <lautrbach@redhat.com> - 3.6-0.rc2.1
- SELinux userspace 3.6-rc2 release

* Mon Nov 13 2023 Petr Lautrbach <lautrbach@redhat.com> - 3.6-0.rc1.1
- SELinux userspace 3.6-rc1 release

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 22 2023 Vit Mojzis <vmojzis@redhat.com> - 3.5-4
- Add examples to man pages

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 3.5-3
- Rebuilt for Python 3.12

* Fri May 26 2023 Miro Hrončok <mhroncok@redhat.com> - 3.5-2
- Fix build with pip 23.1.2+
- Fixes: rhbz#2209019

* Fri Feb 24 2023 Petr Lautrbach <lautrbach@redhat.com> - 3.5-1
- SELinux userspace 3.5 release

* Mon Feb 13 2023 Petr Lautrbach <lautrbach@redhat.com> - 3.5-0.rc3.1
- SELinux userspace 3.5-rc3 release

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.5-0.rc2.1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Jan 16 2023 Petr Lautrbach <lautrbach@redhat.com> - 3.5-0.rc2.1
- SELinux userspace 3.5-rc2 release

* Wed Jan 04 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.5-0.rc1.1.1
- Rebuild for https://fedoraproject.org/wiki/Changes/Ruby_3.2

* Fri Dec 23 2022 Petr Lautrbach <lautrbach@redhat.com> - 3.5-0.rc1.1
- SELinux userspace 3.5-rc1 release

* Mon Nov 21 2022 Petr Lautrbach <lautrbach@redhat.com> - 3.4-6
- Rebase on upstream f56a72ac9e86

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 3.4-4
- Rebuilt for Python 3.11

* Tue May 31 2022 Petr Lautrbach <plautrba@redhat.com> - 3.4-3
- Revert "libselinux: restorecon: pin file to avoid TOCTOU issues"

* Wed May 25 2022 Petr Lautrbach <plautrba@redhat.com> - 3.4-2
- rebuilt

* Thu May 19 2022 Petr Lautrbach <plautrba@redhat.com> - 3.4-1
- SELinux userspace 3.4 release

* Tue May 10 2022 Petr Lautrbach <plautrba@redhat.com> - 3.4-0.rc3.1
- SELinux userspace 3.4-rc3 release

* Thu Apr 21 2022 Petr Lautrbach <plautrba@redhat.com> - 3.4-0.rc2.1
- SELinux userspace 3.4-rc2 release

* Tue Apr 12 2022 Petr Lautrbach <plautrba@redhat.com> - 3.4-0.rc1.1
- SELinux userspace 3.4-rc1 release

* Thu Jan 27 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.3-4
- F-36: rebuild against ruby31

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Nov 29 2021 Petr Lautrbach <plautrba@redhat.com> - 3.3-2
- Introduce selinux_restorecon_parallel(3)

* Fri Oct 22 2021 Petr Lautrbach <plautrba@redhat.com> - 3.3-1
- SELinux userspace 3.3 release

* Fri Oct  8 2021 Petr Lautrbach <plautrba@redhat.com> - 3.3-0.rc3.1
- SELinux userspace 3.3-rc3 release

* Wed Sep 29 2021 Petr Lautrbach <plautrba@redhat.com> - 3.3-0.rc2.1
- SELinux userspace 3.3-rc2 release

* Wed Jul 28 2021 Petr Lautrbach <plautrba@redhat.com> - 3.2-4
- Rebase on upstream commit 32611aea6543

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jun 03 2021 Python Maint <python-maint@redhat.com> - 3.2-2
- Rebuilt for Python 3.10

* Mon Mar  8 2021 Petr Lautrbach <plautrba@redhat.com> - 3.2-1
- SELinux userspace 3.2 release

* Fri Feb  5 2021 Petr Lautrbach <plautrba@redhat.com> - 3.2-0.rc2.1
- SELinux userspace 3.2-rc2 release

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.2-0.rc1.1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jan 20 2021 Petr Lautrbach <plautrba@redhat.com> - 3.2-0.rc1.1
- SELinux userspace 3.2-rc1 release

* Thu Jan 07 2021 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.1-6
- F-34: rebuild against ruby 3.0

* Fri Nov 20 2020 Petr Lautrbach <plautrba@redhat.com> - 3.1-5
- selinux(8): explain that runtime disable is deprecated

* Fri Oct 30 2020 Petr Lautrbach <plautrba@redhat.com> - 3.1-4
- Use libsepol.so.2
- Convert matchpathcon to selabel_lookup()
- Change userspace AVC setenforce and policy load messages to audit
  format
- Remove trailing slash on selabel_file lookups
- Use kernel status page by default

* Wed Sep 02 2020 Jeff Law <law@redhat.com> - 3.1-3
- Re-enable LTO

* Mon Jul 13 2020 Tom Stellard <tstellar@redhat.com> - 3.1-2
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro
- Use -fno-semantic-interposition and more make macros

* Fri Jul 10 2020 Petr Lautrbach <plautrba@redhat.com> - 3.1-1
- SELinux userspace 3.1 release

* Wed Jul  1 2020 Jeff Law <law@redhat.com> - 3.0-6
- Disable LTO

* Sat May 23 2020 Miro Hrončok <mhroncok@redhat.com> - 3.0-5
- Rebuilt for Python 3.9

* Thu Mar  5 2020 Petr Lautrbach <plautrba@redhat.com> - 3.0-4
- Eliminate use of security_compute_user()

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jan 18 2020 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.0-2
- F-32: rebuild against ruby27

* Fri Dec  6 2019 Petr Lautrbach <plautrba@redhat.com> - 3.0-1
- SELinux userspace 3.0 release

* Mon Nov 11 2019 Petr Lautrbach <plautrba@redhat.com> - 3.0-0.r1.1
- SELinux userspace 3.0-rc1 release candidate

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 2.9-7
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Fri Aug 16 2019 Miro Hrončok <mhroncok@redhat.com> - 2.9-6
- Rebuilt for Python 3.8

* Mon Aug 12 2019 Petr Lautrbach <plautrba@redhat.com> - 2.9-5
- Drop python2-libselinux (#1739646)

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Jun 28 2019 Petr Lautrbach <plautrba@redhat.com> - 2.9-3
- Use standard build flags for Python bindings

* Fri May 24 2019 Petr Lautrbach <plautrba@redhat.com> - 2.9-2
- Use Python distutils to install SELinux python bindings

* Mon Mar 18 2019 Petr Lautrbach <plautrba@redhat.com> - 2.9-1
- SELinux userspace 2.9 release

* Wed Mar  6 2019 Petr Lautrbach <plautrba@redhat.com> - 2.9-0.rc2.1
- SELinux userspace 2.9-rc2 release

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.9-0.rc1.1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jan 25 2019 Petr Lautrbach <plautrba@redhat.com> - 2.9-0.rc1.1
- SELinux userspace 2.9-rc1 release

* Tue Jan 22 2019 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.8-8
- F-30: again rebuild against ruby26

* Mon Jan 21 2019 Petr Lautrbach <plautrba@redhat.com> - 2.8-7
- selinux_restorecon: Skip customized files also without -v
- Do not dereference symlink with statfs in selinux_restorecon

* Mon Jan 21 2019 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.8-6
- F-30: rebuild against ruby26

* Tue Nov 13 2018 Petr Lautrbach <plautrba@redhat.com> - 2.8-5
- Fix RESOURCE_LEAK coverity scan defects

* Tue Sep  4 2018 Petr Lautrbach <plautrba@redhat.com> - 2.8-4
- Fix the whatis line for the selinux_boolean_sub.3 manpage
- Fix line wrapping in selabel_file.5
- Fix spelling errors in manpages

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 15 2018 Miro Hrončok <mhroncok@redhat.com> - 2.8-2
- Rebuilt for Python 3.7

* Fri May 25 2018 Petr Lautrbach <plautrba@redhat.com> - 2.8-1
- SELinux userspace 2.8 release

* Mon May 14 2018 Petr Lautrbach <plautrba@redhat.com> - 2.8-0.rc3.1
- SELinux userspace 2.8-rc3 release candidate

* Fri May  4 2018 Petr Lautrbach <plautrba@redhat.com> - 2.8-0.rc2.1
- SELinux userspace 2.8-rc2 release candidate

* Mon Apr 23 2018 Petr Lautrbach <plautrba@redhat.com> - 2.8-0.rc1.1
- SELinux userspace 2.8-rc1 release candidate

* Wed Mar 21 2018 Petr Lautrbach <plautrba@redhat.com> - 2.7-13
- build: Replace PYSITEDIR with PYTHONLIBDIR

* Tue Mar 13 2018 Petr Lautrbach <plautrba@redhat.com> - 2.7-12
- Correct manpages regarding removable_context
- build: follow standard semantics for DESTDIR and PREFIX

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.7-11
- Escape macros in %%changelog

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.7-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.7-9
- Switch to %%ldconfig_scriptlets

* Tue Jan 09 2018 Iryna Shcherbina <ishcherb@redhat.com> - 2.7-8
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Jan 05 2018 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.7-7
- F-28: rebuild for ruby25

* Wed Nov 22 2017 Petr Lautrbach <plautrba@redhat.com> - 2.7-6
- Rebuild with libsepol-2.7-3

* Fri Oct 20 2017 Petr Lautrbach <plautrba@redhat.com> - 2.7-5
- Drop golang bindings
- Add support for pcre2 to pkgconfig definition

* Wed Sep 27 2017 Petr Šabata <contyk@redhat.com> - 2.7-4
- Enable the python3 subpackages on EL

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.7-3
- Also add Provides for the old name without %%_isa

* Thu Aug 10 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.7-2
- Python 2 binary package renamed to python2-libselinux
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3
- Python 3 binary package renamed to python3-libselinux

* Mon Aug 07 2017 Petr Lautrbach <plautrba@redhat.com> - 2.7-1
- Update to upstream release 2017-08-04

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.6-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Sat Jul 29 2017 Florian Weimer <fweimer@redhat.com> - 2.6-9
- Rebuild with binutils fix for ppc64le (#1475636)

* Fri Jul 28 2017 Petr Lautrbach <plautrba@redhat.com> - 2.6-8
- Always unmount selinuxfs for SELINUX=disabled

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Apr 28 2017 Petr Lautrbach <plautrba@redhat.com> - 2.6-6
- Don't finalize mount state in selinux_set_policy_root()
- Follow upstream and rename _selinux.so to _selinux.cpython-36m-x86_64-linux-gnu.so

* Thu Apr 06 2017 Petr Lautrbach <plautrba@redhat.com> - 2.6-5
- Fix setfiles progress indicator

* Wed Mar 22 2017 Petr Lautrbach <plautrba@redhat.com> - 2.6-4
- Fix segfault in selinux_restorecon_sb() (#1433577)
- Change matchpathcon usage to match with matchpathcon manpage
- Fix a corner case getsebool return value

* Tue Mar 14 2017 Petr Lautrbach <plautrba@redhat.com> - 2.6-3
- Fix 'semanage boolean -m' to modify active value

* Thu Mar 02 2017 Petr Lautrbach <plautrba@redhat.com> - 2.6-2
- Fix FTBFS - fatal error (#1427902)

* Sun Feb 12 2017 Petr Lautrbach <plautrba@redhat.com> - 2.6-1
- Update to upstream release 2016-10-14

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.5-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 01 2017 Stephen Gallagher <sgallagh@redhat.com> - 2.5-17
- Add missing %%license macro

* Fri Jan 13 2017 Vít Ondruch <vondruch@redhat.com> - 2.5-16
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.4

* Wed Jan 11 2017 Petr Lautrbach <plautrba@redhat.com> - 2.5-15
- Rewrite restorecon() python method

* Fri Dec 09 2016 Charalampos Stratakis <cstratak@redhat.com> - 2.5-14
- Rebuild for Python 3.6

* Tue Nov 22 2016 Petr Lautrbach <plautrba@redhat.com> - 2.5-13
- Fix pointer handling in realpath_not_final (#1376598)

* Mon Oct 03 2016 Petr Lautrbach <plautrba@redhat.com> 2.5-12
- Fix -Wsign-compare warnings
- Drop unused stdio_ext.h header file
- Kill logging check for selinux_enabled()
- Drop usage of _D_ALLOC_NAMLEN
- Add openrc_contexts functions
- Fix redefinition of XATTR_NAME_SELINUX
- Correct error path to always try text
- Clean up process_file()
- Handle NULL pcre study data
- Fix in tree compilation of utils that depend on libsepol

* Mon Aug 01 2016 Petr Lautrbach <plautrba@redhat.com> 2.5-11
- Rebuilt with libsepol-2.5-9

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5-10
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Mon Jun 27 2016 Petr Lautrbach <plautrba@redhat.com> - 2.5-9
- Clarify is_selinux_mls_enabled() description
- Explain how to free policy type from selinux_getpolicytype()
- Compare absolute pathname in matchpathcon -V
- Add selinux_snapperd_contexts_path()

* Fri Jun 24 2016 Petr Lautrbach <plautrba@redhat.com> - 2.5-8
- Move _selinux.so to /usr/lib64/python*/site-packages

* Thu Jun 23 2016 Petr Lautrbach <plautrba@redhat.com> - 2.5-7
- Modify audit2why analyze function to use loaded policy
- Sort object files for deterministic linking order
- Respect CC and PKG_CONFIG environment variable
- Avoid mounting /proc outside of selinux_init_load_policy()

* Fri May 06 2016 Petr Lautrbach <plautrba@redhat.com> - 2.5-6
- Fix multiple spelling errors

* Mon May 02 2016 Petr Lautrbach <plautrba@redhat.com> - 2.5-5
- Rebuilt with libsepol-2.5-5

* Fri Apr 29 2016 Petr Lautrbach <plautrba@redhat.com> - 2.5-4
- Fix typo in sefcontext_compile.8

* Fri Apr 08 2016 Petr Lautrbach <plautrba@redhat.com> - 2.5-3
- Fix location of selinuxfs mount point
- Only mount /proc if necessary
- procattr: return einval for <= 0 pid args
- procattr: return error on invalid pid_t input

* Sat Feb 27 2016 Petr Lautrbach <plautrba@redhat.com> 2.5-2
- Use fully versioned arch-specific requires

* Tue Feb 23 2016 Petr Lautrbach <plautrba@redhat.com> 2.5-1
- Update to upstream release 2016-02-23

* Sun Feb 21 2016 Petr Lautrbach <plautrba@redhat.com> 2.5-0.1.rc1
- Update to upstream rc1 release 2016-01-07

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 12 2016 Vít Ondruch <vondruch@redhat.com> - 2.4-7
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.3

* Thu Dec 10 2015 Petr Lautrbach <plautrba@redhat.com> - 2.4-6
- Build libselinux without rpm_execcon() (#1284019)

* Thu Oct 15 2015 Robert Kuska <rkuska@redhat.com> - 2.4-5
- Rebuilt for Python3.5 rebuild

* Wed Sep 30 2015 Petr Lautrbach <plautrba@redhat.com> 2.4-4
- Flush the class/perm string mapping cache on policy reload (#1264051)
- Fix restorecon when path has no context

* Wed Sep 02 2015 Petr Lautrbach <plautrba@redhat.com> 2.4-3
- Simplify procattr cache (#1257157,#1232371)

* Fri Aug 14 2015 Adam Jackson <ajax@redhat.com> 2.4-2
- Export ldflags into the build so hardening works

* Tue Jul 21 2015 Petr Lautrbach <plautrba@redhat.com> 2.4-1.1
- Update to 2.4 release

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue May 12 2015 Petr Lautrbach <plautrba@redhat.com> 2.3-10
- is_selinux_enabled: Add /etc/selinux/config test (#1219045)
- matchpathcon/selabel_file: Fix man pages (#1219718)

* Thu Apr 23 2015 Petr Lautrbach <plautrba@redhat.com> 2.3-9
- revert support for policy compressed with xv (#1185266)

* Tue Apr 21 2015 Petr Lautrbach <plautrba@redhat.com> 2.3-8
- selinux.py - use os.walk() instead of os.path.walk() (#1195004)
- is_selinux_enabled(): drop no-policy-loaded test (#1195074)
- fix -Wformat errors and remove deprecated mudflap option

* Mon Mar 16 2015 Than Ngo <than@redhat.com> - 2.3-7
- bump release and rebuild so that koji-shadow can rebuild it
  against new gcc on secondary arch

* Mon Jan 19 2015 Vít Ondruch <vondruch@redhat.com> - 2.3-6
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.2

* Thu Aug 21 2014 Miroslav Grepl <mgrepl@redhat.com> - 2.3-5
- Compiled file context files and the original should have the same permissions from dwalsh@redhat.com
- Add selinux_openssh_contexts_path() to get a path to /contexts/openssh_contexts

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Kalev Lember <kalevlember@gmail.com> - 2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Tue May 6 2014 Dan Walsh <dwalsh@redhat.com> - 2.3-1
- Update to upstream
	* Get rid of security_context_t and fix const declarations.
	* Refactor rpm_execcon() into a new setexecfilecon() from Guillem Jover.

* Tue May 6 2014 Miroslav Grepl <mgrepl@redhat.com> - 2.2.2-8
- Add selinux_openssh_contexts_path()

* Thu Apr 24 2014 Vít Ondruch <vondruch@redhat.com> - 2.2.2-7
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.1

* Mon Feb 24 2014 Dan Walsh <dwalsh@redhat.com>  - 2.2.2-6
- Fix spelling mistake in man page

* Thu Feb 20 2014 Dan Walsh <dwalsh@redhat.com>  - 2.2.2-5
- More go bindings
-   restorecon, getpidcon, setexeccon

* Fri Feb 14 2014 Dan Walsh <dwalsh@redhat.com>  - 2.2.2-4
- Add additional go bindings for get*con calls
- Add go bindings test command
- Modify man pages of set*con calls to mention that they are thread specific

* Fri Jan 24 2014 Dan Walsh <dwalsh@redhat.com>  - 2.2.2-3
- Move selinux.go to /usr/lib64/golang/src/pkg/github.com/selinux/selinux.go
- Add Int_to_mcs function to generate MCS labels from integers.

* Tue Jan 14 2014 Dan Walsh <dwalsh@redhat.com>  - 2.2.2-2
- Add ghost flag for /var/run/setrans

* Mon Jan 6 2014 Dan Walsh <dwalsh@redhat.com>  - 2.2.2-1
- Update to upstream
      * Fix userspace AVC handling of per-domain permissive mode.
- Verify context is not null when passed into *setfilecon_raw

* Fri Dec 27 2013 Adam Williamson <awilliam@redhat.com> - 2.2.1-6
- revert unexplained change to rhat.patch which broke SELinux disablement

* Mon Dec 23 2013 Dan Walsh <dwalsh@redhat.com> - 2.2.1-5
- Verify context is not null when passed into lsetfilecon_raw

* Wed Dec 18 2013 Dan Walsh <dwalsh@redhat.com> - 2.2.1-4
- Mv selinux.go to /usr/share/gocode/src/selinux

* Tue Dec 17 2013 Dan Walsh <dwalsh@redhat.com> - 2.2.1-3
- Add golang support to selinux.

* Thu Dec 5 2013 Dan Walsh <dwalsh@redhat.com> - 2.2.1-2
- Remove togglesebool man page

* Mon Nov 25 2013 Dan Walsh <dwalsh@redhat.com> - 2.2.1-1
- Update to upstream
	* Remove -lpthread from pkg-config file; it is not required.
- Add support for policy compressed with xv

* Thu Oct 31 2013 Dan Walsh <dwalsh@redhat.com> - 2.2-1
- Update to upstream
	* Fix avc_has_perm() returns -1 even when SELinux is in permissive mode.
	* Support overriding Makefile RANLIB from Sven Vermeulen.
	* Update pkgconfig definition from Sven Vermeulen.
	* Mount sysfs before trying to mount selinuxfs from Sven Vermeulen.
	* Fix man pages from Laurent Bigonville.
	* Support overriding PATH  and LIBBASE in Makefiles from Laurent Bigonville.
	* Fix LDFLAGS usage from Laurent Bigonville
	* Avoid shadowing stat in load_mmap from Joe MacDonald.
	* Support building on older PCRE libraries from Joe MacDonald.
	* Fix handling of temporary file in sefcontext_compile from Dan Walsh.
	* Fix procattr cache from Dan Walsh.
	* Define python constants for getenforce result from Dan Walsh.
	* Fix label substitution handling of / from Dan Walsh.
	* Add selinux_current_policy_path from Dan Walsh.
	* Change get_context_list to only return good matches from Dan Walsh.
	* Support udev-197 and higher from Sven Vermeulen and Dan Walsh.
	* Add support for local substitutions from Dan Walsh.
	* Change setfilecon to not return ENOSUP if context is already correct from Dan Walsh.
	* Python wrapper leak fixes from Dan Walsh.
	* Export SELINUX_TRANS_DIR definition in selinux.h from Dan Walsh.
	* Add selinux_systemd_contexts_path from Dan Walsh.
	* Add selinux_set_policy_root from Dan Walsh.
	* Add man page for sefcontext_compile from Dan Walsh.

* Fri Oct 4 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.13-21
- Add systemd_contexts support
- Do substitutions on a local sub followed by a dist sub

* Thu Oct 3 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.13-20
- Eliminate requirement on pthread library, by applying patch for Jakub Jelinek
Resolves #1013801

* Mon Sep 16 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.13-19
- Fix handling of libselinux getconlist with only one entry

* Tue Sep 3 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.13-17
- Add Python constants for SELinux enforcing modes

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.13-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun 28 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.13-16
- Add sefcontext_compile.8  man page
- Add Russell Coker  patch to fix man pages
- Add patches from Laurent Bigonville to fix Makefiles for debian.
- modify spec file to use %%{_prefix}/lib

* Mon May 6 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.13-15
- Fix patch that Handles substitutions for /

* Wed Apr 17 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.13-14
- Handle substitutions for /
- semanage fcontext -a -e  / /opt/rh/devtoolset-2/root

* Tue Apr 9 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.13-13
- Add Eric Paris patch to fix procattr calls after a fork.

* Tue Mar 26 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.13-12
- Move secolor.conf.5 into mcstrans package and out of libselinux

* Wed Mar 20 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.13-11
- Fix python bindings for selinux_check_access

* Tue Mar 19 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.13-10
- Fix reseting the policy root in matchpathcon

* Wed Mar 6 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.13-9
- Cleanup setfcontext_compile atomic patch
- Add matchpathcon -P /etc/selinux/mls support by allowing users to set alternate root
- Make sure we set exit codes from selinux_label calls to ENOENT or SUCCESS

* Wed Mar 6 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.13-8
- Make setfcontext_compile atomic

* Wed Mar 6 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.13-7
- Fix memory leak in set*con calls.

* Thu Feb 28 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.13-6
- Move matchpathcon to -utils package
- Remove togglesebool

* Thu Feb 21 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.13-5
- Fix selinux man page to reflect what current selinux policy is.

* Fri Feb 15 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.13-4
- Add new constant SETRANS_DIR which points to the directory where mstransd can find the socket and libvirt can write its translations files.

* Fri Feb 15 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.13-3
- Bring back selinux_current_policy_path

* Thu Feb 14 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.13-2
- Revert some changes which are causing the wrong policy version file to be created

* Thu Feb 7 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.13-1
- Update to upstream
        * audit2why: make sure path is nul terminated
        * utils: new file context regex compiler
        * label_file: use precompiled filecontext when possible
        * do not leak mmapfd
        * sefcontontext_compile: Add error handling to help debug problems in libsemanage.
        * man: make selinux.8 mention service man pages
        * audit2why: Fix segfault if finish() called twice
        * audit2why: do not leak on multiple init() calls
        * mode_to_security_class: interface to translate a mode_t in to a security class
        * audit2why: Cleanup audit2why analysys function
        * man: Fix program synopsis and function prototypes in man pages
        * man: Fix man pages formatting
        * man: Fix typo in man page
        * man: Add references and man page links to _raw function variants
        * Use ENOTSUP instead of EOPNOTSUPP for getfilecon functions
        * man: context_new(3): fix the return value description
        * selinux_status_open: handle error from sysconf
        * selinux_status_open: do not leak statusfd on exec
        * Fix errors found by coverity
        * Change boooleans.subs to booleans.subs_dist.
        * optimize set*con functions
        * pkg-config do not specifc ruby version
        * unmap file contexts on selabel_close()
        * do not leak file contexts with mmap'd backend
        * sefcontext_compile: do not leak fd on error
        * matchmediacon: do not leak fd
        * src/label_android_property: do not leak fd on error

* Sun Jan 27 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.12-20
- Update to latest patches from eparis/Upstream

* Fri Jan 25 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.12-19
- Update to latest patches from eparis/Upstream

* Wed Jan 23 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.12-18
- Try procatt speedup patch again

* Wed Jan 23 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.12-17
- Roll back procattr speedups since it seems to be screwing up systemd labeling.

* Tue Jan 22 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.12-16
- Fix tid handling for setfscreatecon, old patch still broken in libvirt

* Wed Jan 16 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.12-15
- Fix tid handling for setfscreatecon, old patch still broken in libvirt

* Mon Jan 14 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.12-14
- setfscreatecon after fork was broken by the Set*con patch.
- We needed to reset the thread variables after a fork.

* Thu Jan 10 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.12-13
- Fix setfscreatecon call to handle failure mode, which was breaking udev

* Wed Jan 9 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.12-12
- Ondrej Oprala patch to optimize set*con functions
-    Set*con now caches the security context and only re-sets it if it changes.

* Tue Jan 8 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.12-11
- Rebuild against latest libsepol

* Fri Jan 4 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.12-10
- Update to latest patches from eparis/Upstream
-    Fix errors found by coverity
-    set the sepol_compute_av_reason_buffer flag to 0.  This means calculate denials only?
-    audit2why: remove a useless policy vers variable
-    audit2why: use the new constraint information

* Mon Nov 19 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.12-9
- Rebuild with latest libsepol

* Fri Nov 16 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.12-8
- Return EPERM if login program can not reach default label for user
- Attempt to return container info from audit2why

* Thu Nov 1 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.12-7
- Apply patch from eparis to fix leaked file descriptor in new labeling code

* Fri Oct 19 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.12-6
- Add new function mode_to_security_class which takes mode instead of a string.
- Possibly will be used with coreutils.

* Mon Oct 15 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.12-5
- Add back selinuxconlist and selinuxdefcon man pages

* Mon Oct 15 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.12-4
- Fix segfault from calling audit2why.finish() multiple times

* Fri Oct 12 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.12-3
- Fix up selinux man page to reference service man pages

* Wed Sep 19 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.12-2
- Rebuild with fixed libsepol

* Thu Sep 13 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.12-1
- Update to upstream
	* Add support for lxc_contexts_path
	* utils: add service to getdefaultcon
	* libsemanage: do not set soname needlessly
	* libsemanage: remove PYTHONLIBDIR and ruby equivalent
	* boolean name equivalency
	* getsebool: support boolean name substitution
	* Add man page for new selinux_boolean_sub function.
	* expose selinux_boolean_sub
	* matchpathcon: add -m option to force file type check
	* utils: avcstat: clear sa_mask set
	* seusers: Check for strchr failure
	* booleans: initialize pointer to silence coveriety
	* stop messages when SELinux disabled
	* label_file: use PCRE instead of glibc regex functions
	* label_file: remove all typedefs
	* label_file: move definitions to include file
	* label_file: do string to mode_t conversion in a helper function
	* label_file: move error reporting back into caller
	* label_file: move stem/spec handling to header
	* label_file: drop useless ncomp field from label_file data
	* label_file: move spec_hasMetaChars to header
	* label_file: fix potential read past buffer in spec_hasMetaChars
	* label_file: move regex sorting to the header
	* label_file: add accessors for the pcre extra data
	* label_file: only run regex files one time
	* label_file: new process_file function
	* label_file: break up find_stem_from_spec
	* label_file: struct reorg
	* label_file: only run array once when sorting
	* Ensure that we only close the selinux netlink socket once.
	* improve the file_contexts.5 manual page

* Fri Aug 03 2012 David Malcolm <dmalcolm@redhat.com> - 2.1.11-6
- rebuild for https://fedoraproject.org/wiki/Features/Python_3.3

* Wed Aug  1 2012 David Malcolm <dmalcolm@redhat.com> - 2.1.11-5
- make with_python3 be conditional on fedora

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 16 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.11-3
- Move the tmpfiles.d content from /etc/tmpfiles.d to /usr/lib/tmpfiles.d

* Fri Jul 13 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.11-2
- Revert Eric Paris Patch for selinux_binary_policy_path

* Wed Jul 4 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.11-1
- Update to upstream
	* Fortify source now requires all code to be compiled with -O flag
	* asprintf return code must be checked
	* avc_netlink_recieve handle EINTR
	* audit2why: silence -Wmissing-prototypes warning
	* libsemanage: remove build warning when build swig c files
	* matchpathcon: bad handling of symlinks in /
	* seusers: remove unused lineno
	* seusers: getseuser: gracefully handle NULL service
	* New Android property labeling backend
	* label_android_property whitespace cleanups
	* additional makefile support for rubywrap

* Mon Jun 11 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.10-5
- Fix booleans.subs name, change function name to selinux_boolean_sub,
  add man page, minor fixes to the function

* Fri May 25 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.10-4
- Fix to compile with Fortify source
      * Add -O compiler flag
      * Check return code from asprintf
- Fix handling of symbolic links in / by realpath_not_final

* Tue Apr 17 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.10-3
- Add support for lxc contexts file

* Fri Mar 30 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.10-2
- Add support fot boolean subs file

* Thu Mar 29 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.10-1
- Update to upstream
	* Fix dead links to www.nsa.gov/selinux
	* Remove jump over variable declaration
	* Fix old style function definitions
	* Fix const-correctness
	* Remove unused flush_class_cache method
	* Add prototype decl for destructor
	* Add more printf format annotations
	* Add printf format attribute annotation to die() method
	* Fix const-ness of parameters & make usage() methods static
	* Enable many more gcc warnings for libselinux/src/ builds
	* utils: Enable many more gcc warnings for libselinux/utils builds
	* Change annotation on include/selinux/avc.h to avoid upsetting SWIG
	* Ensure there is a prototype for 'matchpathcon_lib_destructor'
	* Update Makefiles to handle /usrmove
	* utils: Stop separating out matchpathcon as something special
	* pkg-config to figure out where ruby include files are located
	* build with either ruby 1.9 or ruby 1.8
	* assert if avc_init() not called
	* take security_deny_unknown into account
	* security_compute_create_name(3)
	* Do not link against python library, this is considered
	* bad practice in debian
	* Hide unnecessarily-exported library destructors

* Thu Feb 16 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.9-9
- Add selinux_current_policy_path to return /sys/fs/selinux/policy if it exists
- Otherwise search for policy on disk

* Wed Feb 15 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.9-8
- Change selinux_binary_policy_path to return /sys/fs/selinux/policy
- Add selinux_installed_policy_path to return what selinux_binary_policy_path used to return
- avc_has_perm will now return yes if the machine is in permissive mode
- Make work with ruby-1.9

* Fri Feb 3 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.9-7
- avc_netlink_recieve should continue to poll if it receinves an EINTR rather

* Sun Jan 29 2012 Kay Sievers <kay@redhat.com> - 2.1.9-6
- use /sbin/ldconfig, glibc does not provide
  /usr/sbin/ldconfig in the RPM database for now

* Fri Jan 27 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.9-5
- Rebuild with cleaned up upstream to work in /usr

* Wed Jan 25 2012 Harald Hoyer <harald@redhat.com> 2.1.9-4
- install everything in /usr
  https://fedoraproject.org/wiki/Features/UsrMove

* Mon Jan 23 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.9-3
- Add Dan Berrange code cleanup patches.

* Wed Jan 4 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.9-2
- Fix selabal_open man page to refer to proper selinux_opt structure

* Wed Dec 21 2011 Dan Walsh <dwalsh@redhat.com> - 2.1.9-1
-Update to upstream
	* Fix setenforce man page to refer to selinux man page
	* Cleanup Man pages
	* merge freecon with getcon man page

* Mon Dec 19 2011 Dan Walsh <dwalsh@redhat.com> - 2.1.8-5
- Add patch from Richard Haines
      When selabel_lookup found an invalid context with validation enabled, it
      always stated it was 'file_contexts' whether media, x, db or file.
      The fix is to store the spec file name in the selabel_lookup_rec on
      selabel_open and use this as output for logs. Also a minor fix if key is
      NULL to stop seg faults.
- Fix setenforce manage page.

* Thu Dec 15 2011 Dan Walsh <dwalsh@redhat.com> - 2.1.8-4
- Rebuild with new libsepol

* Tue Dec 6 2011 Dan Walsh <dwalsh@redhat.com> - 2.1.8-2
- Fix setenforce man page, from Miroslav Grepl

* Tue Dec 6 2011 Dan Walsh <dwalsh@redhat.com> - 2.1.8-1
- Upgrade to upstream
	* selinuxswig_python.i: don't make syscall if it won't change anything
	* Remove assert in security_get_boolean_names(3)
	* Mapped compute functions now obey deny_unknown flag
	* get_default_type now sets EINVAL if no entry.
	* return EINVAL if invalid role selected
	* Updated selabel_file(5) man page
	* Updated selabel_db(5) man page
	* Updated selabel_media(5) man page
	* Updated selabel_x(5) man page
	* Add man/man5 man pages
	* Add man/man5 man pages
	* Add man/man5 man pages
	* use -W and -Werror in utils

* Tue Nov 29 2011 Dan Walsh <dwalsh@redhat.com> - 2.1.7-2
- Change python binding for restorecon to check if the context matches.
- If it does do not reset

* Fri Nov 4 2011 Dan Walsh <dwalsh@redhat.com> - 2.1.7-1
- Upgrade to upstream
	* Makefiles: syntax, convert all ${VAR} to $(VAR)
	* load_policy: handle selinux=0 and /sys/fs/selinux not exist
	* regenerate .pc on VERSION change
	* label: cosmetic cleanups
	* simple interface for access checks
	* Don't reinitialize avc_init if it has been called previously
	* seusers: fix to handle large sets of groups
	* audit2why: close fd on enomem
	* rename and export symlink_realpath
	* label_file: style changes to make Eric happy.

* Mon Oct 24 2011 Dan Walsh <dwalsh@redhat.com> - 2.1.6-4
- Apply libselinux patch to handle large groups in seusers.

* Wed Oct 19 2011 Dan Walsh <dwalsh@redhat.com> - 2.1.6-3
- Add selinux_check_access function. Needed for passwd, chfn, chsh

* Thu Sep 22 2011 Dan Walsh <dwalsh@redhat.com> - 2.1.6-2
- Handle situation where selinux=0 passed to the kernel and both /selinux and

* Mon Sep 19 2011 Dan Walsh <dwalsh@redhat.com> - 2.1.6-1
-Update to upstream
	* utils: matchpathcon: remove duplicate declaration
	* src: matchpathcon: use myprintf not fprintf
	* src: matchpathcon: make sure resolved path starts
	* put libselinux.so.1 in /lib not /usr/lib
	* tree: default make target to all not

* Wed Sep 14 2011 Dan Walsh <dwalsh@redhat.com> - 2.1.5-5
- Switch to use ":" as prefix separator rather then ";"

* Thu Sep  8 2011 Ville Skyttä <ville.skytta@iki.fi> - 2.1.5-4
- Avoid unnecessary shell invocation in %%post.

* Tue Sep 6 2011 Dan Walsh <dwalsh@redhat.com> - 2.1.5-3
- Fix handling of subset labeling that is causing segfault in restorecon

* Fri Sep 2 2011 Dan Walsh <dwalsh@redhat.com> - 2.1.5-2
- Change matchpathcon_init_prefix and selabel_open to allow multiple initial
prefixes.  Now you can specify a ";" separated list of prefixes and the
labeling system will only load regular expressions that match these prefixes.

* Tue Aug 30 2011 Dan Walsh <dwalsh@redhat.com> - 2.1.5-1
- Change matchpatcon to use proper myprintf
- Fix symlink_realpath to always include "/"
- Update to upstream
	* selinux_file_context_verify function returns wrong value.
	* move realpath helper to matchpathcon library
	* python wrapper makefile changes

* Mon Aug 22 2011 Dan Walsh <dwalsh@redhat.com> - 2.1.4-2
- Move to new Makefile that can build with or without PYTHON being set

* Thu Aug 18 2011 Dan Walsh <dwalsh@redhat.com> - 2.1.4-1
-Update to upstream
2.1.4 2011-0817
	* mapping fix for invalid class/perms after selinux_set_mapping
	* audit2why: work around python bug not defining
	* resolv symlinks and dot directories before matching

2.1.2 2011-0803
	* audit2allow: do not print statistics
	* make python bindings for restorecon work on relative path
	* fix python audit2why binding error
	* support new python3 functions
	* do not check fcontext duplicates on use
	* Patch for python3 for libselinux

2.1.1 2011-08-02
	* move .gitignore into utils
	* new setexecon utility
	* selabel_open fix processing of substitution files
	* mountpoint changing patch.
	* simplify SRCS in Makefile

2.1.1 2011-08-01
	* Remove generated files, introduce more .gitignore



* Thu Jul 28 2011 Dan Walsh <dwalsh@redhat.com> - 2.1.0-1
-Update to upstream
	* Release, minor version bump
	* Give correct names to mount points in load_policy by Dan Walsh.
	* Make sure selinux state is reported correctly if selinux is disabled or
	fails to load by Dan Walsh.
	* Fix crash if selinux_key_create was never called by Dan Walsh.
	* Add new file_context.subs_dist for distro specific filecon substitutions
	by Dan Walsh.
	* Update man pages for selinux_color_* functions by Richard Haines.

* Mon Jun 13 2011 Dan Walsh <dwalsh@redhat.com> - 2.0.102-6
- Only call dups check within selabel/matchpathcon if you are validating the
context
- This seems to speed the loading of labels by 4 times.

* Fri Apr 29 2011 Dan Walsh <dwalsh@redhat.com> - 2.0.102-5
- Move /selinux to /sys/fs/selinux
- Add selinuxexeccon
- Add realpath to matchpathcon to handle matchpathcon * type queries.

* Thu Apr 21 2011 Dan Walsh <dwalsh@redhat.com> - 2.0.102-4
- Update for latest libsepol

* Mon Apr 18 2011 Dan Walsh <dwalsh@redhat.com> - 2.0.102-3
- Update for latest libsepol

* Wed Apr 13 2011 Dan Walsh <dwalsh@redhat.com> - 2.0.102-2
- Fix restorecon python binding to accept relative paths

* Tue Apr 12 2011 Dan Walsh <dwalsh@redhat.com> - 2.0.102-1
-Update to upstream
	* Give correct names to mount points in load_policy by Dan Walsh.
	* Make sure selinux state is reported correctly if selinux is disabled or
	fails to load by Dan Walsh.
	* Fix crash if selinux_key_create was never called by Dan Walsh.
	* Add new file_context.subs_dist for distro specific filecon substitutions
	by Dan Walsh.
	* Update man pages for selinux_color_* functions by Richard Haines.

* Wed Apr 6 2011 Dan Walsh <dwalsh@redhat.com> - 2.0.101-1
- Clean up patch to make handling of constructor  cleanup more portable
  * db_language object class support for selabel_lookup from KaiGai Kohei.
  * Library destructors for thread local storage keys from Eamon Walsh.

* Tue Apr 5 2011 Dan Walsh <dwalsh@redhat.com> - 2.0.99-5
- Add distribution subs path

* Tue Apr 5 2011 Dan Walsh <dwalsh@redhat.com> - 2.0.99-4
Add patch from dbhole@redhat.com to initialize thread keys to -1
Errors were being seen in libpthread/libdl that were related
to corrupt thread specific keys. Global destructors that are called on dl
unload. During destruction delete a thread specific key without checking
if it has been initialized. Since the constructor is not called each time
(i.e. key is not initialized with pthread_key_create each time), and the
default is 0, there is a possibility that key 0 for an active thread gets
deleted. This is exactly what is happening in case of OpenJDK.

Workaround patch that initializes the key to -1. Thus if the constructor is not
called, the destructor tries to delete key -1 which is deemed invalid by
pthread_key_delete, and is ignored.

* Tue Apr 5 2011 Dan Walsh <dwalsh@redhat.com> - 2.0.99-3
- Call fini_selinuxmnt if selinux is disabled, to cause is_selinux_disabled() to report correct data

* Fri Apr 1 2011 Dan Walsh <dwalsh@redhat.com> - 2.0.99-2
- Change mount source options to use "proc" and "selinuxfs"

* Tue Mar 1 2011 Dan Walsh <dwalsh@redhat.com> - 2.0.99-1
- Update to upstream
  * Turn off default user handling when computing user contexts by Dan Walsh

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Feb 1 2011 Dan Walsh <dwalsh@redhat.com> - 2.0.98-3
- Fixup selinux man page

* Tue Jan 18 2011 Dan Walsh <dwalsh@redhat.com> - 2.0.98-2
- Fix Makefile to use pkg-config --cflags python3 to discover include paths

* Tue Dec 21 2010 Dan Walsh <dwalsh@redhat.com> - 2.0.98-1
- Update to upstream
  - Turn off fallback in to SELINUX_DEFAULTUSER in get_context_list

* Mon Dec 6 2010 Dan Walsh <dwalsh@redhat.com> - 2.0.97-1
- Update to upstream
	* Thread local storage fixes from Eamon Walsh.

* Sat Dec 4 2010 Dan Walsh <dwalsh@redhat.com> - 2.0.96-9
- Add /etc/tmpfiles.d support for /var/run/setrans

* Wed Nov 24 2010 Dan Walsh <dwalsh@redhat.com> - 2.0.96-8
- Ghost /var/run/setrans

* Wed Sep 29 2010 jkeating - 2.0.96-7
- Rebuilt for gcc bug 634757

* Thu Sep 16 2010 Adam Tkac <atkac redhat com> - 2.0.96-6
- rebuild via updated swig (#624674)

* Sun Aug 22 2010 Dan Walsh <dwalsh@redhat.com> - 2.0.96-5
- Update for python 3.2a1

* Tue Jul 27 2010 Dan Walsh <dwalsh@redhat.com> - 2.0.96-4
- Turn off fallback in to SELINUX_DEFAULTUSER in get_context_list

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 2.0.96-3
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Fri Jun 25 2010 Dan Walsh <dwalsh@redhat.com> - 2.0.96-2
- Turn off messages in audit2why

* Wed Mar 24 2010 Dan Walsh <dwalsh@redhat.com> - 2.0.96-1
- Update to upstream
	* Add const qualifiers to public API where appropriate by KaiGai Kohei.

2.0.95 2010-06-10
	* Remove duplicate slashes in paths in selabel_lookup from Chad Sellers
	* Adds a chcon method to the libselinux python bindings from Steve Lawrence
- add python3 subpackage from David Malcolm

* Wed Mar 24 2010 Dan Walsh <dwalsh@redhat.com> - 2.0.94-1
* Set errno=EINVAL for invalid contexts from Dan Walsh.

* Tue Mar 16 2010 Dan Walsh <dwalsh@redhat.com> - 2.0.93-1
- Update to upstream
	* Show strerror for security_getenforce() by Colin Waters.
	* Merged selabel database support by KaiGai Kohei.
	* Modify netlink socket blocking code by KaiGai Kohei.

* Sun Mar 7 2010 Dan Walsh <dwalsh@redhat.com> - 2.0.92-1
- Update to upstream
	* Fix from Eric Paris to fix leak on non-selinux systems.
	* regenerate swig wrappers
	* pkgconfig fix to respect LIBDIR from Dan Walsh.

* Wed Feb 24 2010 Dan Walsh <dwalsh@redhat.com> - 2.0.91-1
- Update to upstream
	* Change the AVC to only audit the permissions specified by the
	policy, excluding any permissions specified via dontaudit or not
	specified via auditallow.
	* Fix compilation of label_file.c with latest glibc headers.

* Mon Feb 22 2010 Dan Walsh <dwalsh@redhat.com> - 2.0.90-5
- Fix potential doublefree on init

* Thu Feb 18 2010 Dan Walsh <dwalsh@redhat.com> - 2.0.90-4
- Fix libselinux.pc

* Mon Jan 18 2010 Dan Walsh <dwalsh@redhat.com> - 2.0.90-3
- Fix man page for selinuxdefcon

* Mon Jan 4 2010 Dan Walsh <dwalsh@redhat.com> - 2.0.90-2
- Free memory on disabled selinux boxes

* Tue Dec 1 2009 Dan Walsh <dwalsh@redhat.com> - 2.0.90-1
- Update to upstream
	* add/reformat man pages by Guido Trentalancia <guido@trentalancia.com>.
	* Change exception.sh to be called with bash by Manoj Srivastava <srivasta@debian.org>

* Mon Nov 2 2009 Dan Walsh <dwalsh@redhat.com> - 2.0.89-2
- Fix selinuxdefcon man page

* Mon Nov 2 2009 Dan Walsh <dwalsh@redhat.com> - 2.0.89-1
- Update to upstream
	* Add pkgconfig file from Eamon Walsh.

* Thu Oct 29 2009 Dan Walsh <dwalsh@redhat.com> - 2.0.88-1
- Update to upstream
	* Rename and export selinux_reset_config()

* Tue Sep 8 2009 Dan Walsh <dwalsh@redhat.com> - 2.0.87-1
- Update to upstream
	* Add exception handling in libselinux from Dan Walsh. This uses a
	  shell script called exception.sh to generate a swig interface file.
	* make swigify
	* Make matchpathcon print <<none>> if path not found in fcontext file.

* Tue Sep 8 2009 Dan Walsh <dwalsh@redhat.com> - 2.0.86-2
- Eliminate -pthread switch in Makefile

* Tue Sep 8 2009 Dan Walsh <dwalsh@redhat.com> - 2.0.86-1
- Update to upstream
	* Removal of reference counting on userspace AVC SID's.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.85-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul 7 2009 Dan Walsh <dwalsh@redhat.com> - 2.0.85-1
- Update to upstream
	* Reverted Tomas Mraz's fix for freeing thread local storage to avoid
	pthread dependency.
	* Removed fini_context_translations() altogether.
	* Merged lazy init patch from Stephen Smalley based on original patch
	by Steve Grubb.

* Tue Jul 7 2009 Dan Walsh <dwalsh@redhat.com> - 2.0.84-1
- Update to upstream
	* Add per-service seuser support from Dan Walsh.
	* Let load_policy gracefully handle selinuxfs being mounted from Stephen Smalley.
	* Check /proc/filesystems before /proc/mounts for selinuxfs from Eric
	Paris.

* Wed Jun 24 2009 Dan Walsh <dwalsh@redhat.com> - 2.0.82-2
- Add provices ruby(selinux)

* Tue Jun 23 2009 Dan Walsh <dwalsh@redhat.com> - 2.0.82-1
- Update to upstream
	* Fix improper use of thread local storage from Tomas Mraz <tmraz@redhat.com>.
	* Label substitution support from Dan Walsh.
	* Support for labeling virtual machine images from Dan Walsh.

* Mon May 18 2009 Dan Walsh <dwalsh@redhat.com> - 2.0.81-1
- Update to upstream
	* Trim / from the end of input paths to matchpathcon from Dan Walsh.
	* Fix leak in process_line in label_file.c from Hiroshi Shinji.
	* Move matchpathcon to /sbin, add matchpathcon to clean target from Dan Walsh.
	* getdefaultcon to print just the correct match and add verbose option from Dan Walsh.

* Wed Apr 8 2009 Dan Walsh <dwalsh@redhat.com> - 2.0.80-1
- Update to upstream
	* deny_unknown wrapper function from KaiGai Kohei.
	* security_compute_av_flags API from KaiGai Kohei.
	* Netlink socket management and callbacks from KaiGai Kohei.

* Fri Apr 3 2009 Dan Walsh <dwalsh@redhat.com> - 2.0.79-6
- Fix Memory Leak

* Thu Apr 2 2009 Dan Walsh <dwalsh@redhat.com> - 2.0.79-5
- Fix crash in python

* Sun Mar 29 2009 Dan Walsh <dwalsh@redhat.com> - 2.0.79-4
- Add back in additional interfaces

* Fri Mar 27 2009 Dan Walsh <dwalsh@redhat.com> - 2.0.79-3
- Add back in av_decision to python swig

* Thu Mar 12 2009 Dan Walsh <dwalsh@redhat.com> - 2.0.79-1
- Update to upstream
	* Netlink socket handoff patch from Adam Jackson.
	* AVC caching of compute_create results by Eric Paris.

* Tue Mar 10 2009 Dan Walsh <dwalsh@redhat.com> - 2.0.78-5
- Add patch from ajax to accellerate X SELinux
- Update eparis patch

* Mon Mar 9 2009 Dan Walsh <dwalsh@redhat.com> - 2.0.78-4
- Add eparis patch to accellerate Xwindows performance

* Mon Mar 9 2009 Dan Walsh <dwalsh@redhat.com> - 2.0.78-3
- Fix URL

* Fri Mar 6 2009 Dan Walsh <dwalsh@redhat.com> - 2.0.78-2
- Add substitute pattern
- matchpathcon output <<none>> on ENOENT

* Mon Mar 2 2009 Dan Walsh <dwalsh@redhat.com> - 2.0.78-1
- Update to upstream
	* Fix incorrect conversion in discover_class code.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.77-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 18 2009 Dan Walsh <dwalsh@redhat.com> - 2.0.77-5
- Add
  - selinux_virtual_domain_context_path
  - selinux_virtual_image_context_path

* Tue Jan 6 2009 Dan Walsh <dwalsh@redhat.com> - 2.0.77-3
- Throw exeptions in python swig bindings on failures

* Tue Jan 6 2009 Dan Walsh <dwalsh@redhat.com> - 2.0.77-2
- Fix restorecon python code

* Tue Jan 6 2009 Dan Walsh <dwalsh@redhat.com> - 2.0.77-1
- Update to upstream

* Tue Dec 16 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.76-6
- Strip trailing / for matchpathcon

* Tue Dec 16 2008 Dan Walsh <dwalsh@redhat.com>l - 2.0.76-5
- Fix segfault if seusers file does not work

* Fri Dec 12 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.76-4
- Add new function getseuser which will take username and service and return
- seuser and level.  ipa will populate file in future.
- Change selinuxdefcon to return just the context by default

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.0.76-2
- Rebuild for Python 2.6

* Mon Nov 17 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.76-1
- Update to Upstream
	* Allow shell-style wildcards in x_contexts file.

* Mon Nov 17 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.75-2
- Eamon Walsh Patch - libselinux: allow shell-style wildcarding in X names
- Add Restorecon/Install python functions from Luke Macken

* Fri Nov 7 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.75-1
- Update to Upstream
	* Correct message types in AVC log messages.
	* Make matchpathcon -V pass mode from Dan Walsh.
	* Add man page for selinux_file_context_cmp from Dan Walsh.

* Tue Sep 30 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.73-1
- Update to Upstream
	* New man pages from Dan Walsh.
	* Update flask headers from refpolicy trunk from Dan Walsh.

* Fri Sep 26 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.71-6
- Fix matchpathcon -V call

* Tue Sep 9 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.71-5
- Add flask definitions for open, X and nlmsg_tty_audit

* Tue Sep 9 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.71-4
- Add missing get/setkeycreatecon man pages

* Tue Sep 9 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.71-3
- Split out utilities

* Tue Sep 9 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.71-2
- Add missing man page links for [lf]getfilecon

* Tue Aug 5 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.71-1
- Update to Upstream
	* Add group support to seusers using %%groupname syntax from Dan Walsh.
	* Mark setrans socket close-on-exec from Stephen Smalley.
	* Only apply nodups checking to base file contexts from Stephen Smalley.

* Fri Aug 1 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.70-1
- Update to Upstream
	* Merge ruby bindings from Dan Walsh.
- Add support for Linux groups to getseuserbyname

* Fri Aug 1 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.69-2
- Allow group handling in getseuser call

* Tue Jul 29 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.69-1
- Update to Upstream
	* Handle duplicate file context regexes as a fatal error from Stephen Smalley.
	  This prevents adding them via semanage.
	* Fix audit2why shadowed variables from Stephen Smalley.
	* Note that freecon NULL is legal in man page from Karel Zak.

* Wed Jul 9 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.67-4
- Add ruby support for puppet

* Tue Jul 8 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.67-3
- Rebuild for new libsepol

* Sun Jun 29 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.67-2
- Add Karel Zak patch for freecon man page

* Sun Jun 22 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.67-1
- Update to Upstream
	* New and revised AVC, label, and mapping man pages from Eamon Walsh.
	* Add swig python bindings for avc interfaces from Dan Walsh.

* Sun Jun 22 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.65-1
- Update to Upstream
	* Fix selinux_file_context_verify() and selinux_lsetfilecon_default() to call matchpathcon_init_prefix if not already initialized.
	* Add -q qualifier for -V option of matchpathcon and change it to indicate whether verification succeeded or failed via exit status.

* Fri May 16 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.64-3
- libselinux no longer neets to telnet -u in post install

* Wed May 7 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.64-2
- Add sedefaultcon and setconlist commands to dump login context

* Tue Apr 22 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.64-1
- Update to Upstream
	* Fixed selinux_set_callback man page.
	* Try loading the max of the kernel-supported version and the libsepol-supported version when no manipulation of the binary policy is needed from Stephen Smalley.
	* Fix memory leaks in matchpathcon from Eamon Walsh.

* Wed Apr 16 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.61-4
- Add Xavior Toth patch for security_id_t in swig

* Thu Apr 10 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.61-3
- Add avc.h to swig code

* Wed Apr 9 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.61-2
- Grab the latest policy for the kernel

* Tue Apr 1 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.61-1
- Update to Upstream
	* Man page typo fix from Jim Meyering.

* Sun Mar 23 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.60-1
- Update to Upstream
	* Changed selinux_init_load_policy() to not warn about a failed mount of selinuxfs if selinux was disabled in the kernel.

* Thu Mar 13 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.59-2
- Fix matchpathcon memory leak

* Fri Feb 29 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.59-1
- Update to Upstream
	* Merged new X label "poly_selection" namespace from Eamon Walsh.

* Thu Feb 28 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.58-1
- Update to Upstream
	* Merged reset_selinux_config() for load policy from Dan Walsh.

* Thu Feb 28 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.57-2
- Reload library on loading of policy to handle chroot

* Mon Feb 25 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.57-1
- Update to Upstream
	* Merged avc_has_perm() errno fix from Eamon Walsh.

* Fri Feb 22 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.56-1
- Update to Upstream
	* Regenerated Flask headers from refpolicy flask definitions.

* Wed Feb 13 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.55-1
- Update to Upstream
	* Merged compute_member AVC function and manpages from Eamon Walsh.
	* Provide more error reporting on load policy failures from Stephen Smalley.

* Fri Feb 8 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.53-1
- Update to Upstream
	* Merged new X label "poly_prop" namespace from Eamon Walsh.

* Wed Feb 6 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.52-1
- Update to Upstream
	* Disable setlocaldefs if no local boolean or users files are present from Stephen Smalley.
	* Skip userspace preservebools processing for Linux >= 2.6.22 from Stephen Smalley.

* Tue Jan 29 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.50-1
- Update to Upstream
	* Merged fix for audit2why from Dan Walsh.

* Fri Jan 25 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.49-2
- Fix audit2why to grab latest policy versus the one selected by the kernel

* Wed Jan 23 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.49-1
* Merged audit2why python binding from Dan Walsh.

* Wed Jan 23 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.48-1
* Merged updated swig bindings from Dan Walsh, including typemap for pid_t.

* Mon Jan 21 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.47-4
- Update to use libsepol-static library

* Wed Jan 16 2008 Adel Gadllah <adel.gadllah@gmail.com> - 2.0.47-3
- Move libselinux.a to -static package
- Spec cleanups

* Tue Jan 15 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.47-2
- Put back libselinux.a

* Fri Jan 11 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.47-1
- Fix memory references in audit2why and change to use tuples
- Update to Upstream
	* Fix for the avc:  granted null message bug from Stephen Smalley.

* Fri Jan 11 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.46-6
- Fix __init__.py specification

* Tue Jan 8 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.46-5
- Add audit2why python bindings

* Tue Jan 8 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.46-4
- Add pid_t typemap for swig bindings

* Thu Jan 3 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.46-3
- smp_mflag

* Thu Jan 3 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.46-2
- Fix spec file caused by spec review

* Fri Nov 30 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.46-1
- Upgrade to upstream
	* matchpathcon(8) man page update from Dan Walsh.

* Fri Nov 30 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.45-1
- Upgrade to upstream
	* dlopen libsepol.so.1 rather than libsepol.so from Stephen Smalley.
	* Based on a suggestion from Ulrich Drepper, defer regex compilation until we have a stem match, by Stephen Smalley.
	*  A further optimization would be to defer regex compilation until we have a complete match of the constant prefix of the regex - TBD.

* Thu Nov 15 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.43-1
- Upgrade to upstream
	* Regenerated Flask headers from policy.

* Thu Nov 15 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.42-1
- Upgrade to upstream
	* AVC enforcing mode override patch from Eamon Walsh.
	* Aligned attributes in AVC netlink code from Eamon Walsh.
- Move libselinux.so back into devel package, procps has been fixed

* Tue Nov 6 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.40-1
- Upgrade to upstream
	* Merged refactored AVC netlink code from Eamon Walsh.
	* Merged new X label namespaces from Eamon Walsh.
	* Bux fix and minor refactoring in string representation code.

* Fri Oct 5 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.37-1
- Upgrade to upstream
	* Merged selinux_get_callback, avc_open, empty string mapping from Eamon Walsh.

* Fri Sep 28 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.36-1
- Upgrade to upstream
	* Fix segfault resulting from missing file_contexts file.

* Thu Sep 27 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.35-2
- Fix segfault on missing file_context file

* Wed Sep 26 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.35-1
- Upgrade to upstream
	* Make netlink socket close-on-exec to avoid descriptor leakage from Dan Walsh.
	* Pass CFLAGS when using gcc for linking from Dennis Gilmore.

* Mon Sep 24 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.34-3
- Add sparc patch to from Dennis Gilmore to build on Sparc platform

* Mon Sep 24 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.34-2
- Remove leaked file descriptor

* Tue Sep 18 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.34-1
- Upgrade to latest from NSA
	* Fix selabel option flag setting for 64-bit from Stephen Smalley.

* Tue Sep 18 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.33-2
- Change matchpatcon to use syslog instead of syserror

* Thu Sep 13 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.33-1
- Upgrade to latest from NSA
	* Re-map a getxattr return value of 0 to a getfilecon return value of -1 with errno EOPNOTSUPP from Stephen Smalley.
	* Fall back to the compat code for security_class_to_string and security_av_perm_to_string from Stephen Smalley.
	* Fix swig binding for rpm_execcon from James Athey.

* Thu Sep 6 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.31-4
- Apply James Athway patch to fix rpm_execcon python binding

* Tue Aug 28 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.31-3
- Move libselinux.so back into main package, breaks procps

* Thu Aug 23 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.31-2
- Upgrade to upstream
	* Fix file_contexts.homedirs path from Todd Miller.

* Tue Aug 21 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.30-2
- Remove requirement on setransd,  Moved to selinux-policy-mls

* Fri Aug 10 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.30-1
- Move libselinux.so into devel package
- Upgrade to upstream
	* Fix segfault resulting from uninitialized print-callback pointer.
	* Added x_contexts path function patch from Eamon Walsh.
	* Fix build for EMBEDDED=y from Yuichi Nakamura.
	* Fix markup problems in selinux man pages from Dan Walsh.

* Fri Aug 3 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.29-1
- Upgrade to upstream
	* Updated version for stable branch.
	* Added x_contexts path function patch from Eamon Walsh.
	* Fix build for EMBEDDED=y from Yuichi Nakamura.
	* Fix markup problems in selinux man pages from Dan Walsh.
	* Updated av_permissions.h and flask.h to include new nscd permissions from Dan Walsh.
	* Added swigify to top-level Makefile from Dan Walsh.
	* Fix for string_to_security_class segfault on x86_64 from Stephen
	  Smalley.

* Mon Jul 23 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.24-3
- Apply Steven Smalley patch to fix segfault in string_to_security_class

* Wed Jul 18 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.24-2
- Fix matchpathcon to set default myprintf

* Mon Jul 16 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.24-1
- Upgrade to upstream
	* Fix for getfilecon() for zero-length contexts from Stephen Smalley.

* Wed Jul 11 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.23-3
- Update to match flask/access_vectors in policy

* Tue Jul 10 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.23-2
- Fix man page markup lanquage for translations

* Tue Jun 26 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.23-1
- Fix semanage segfault on x86 platform

* Thu Jun 21 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.22-1
- Upgrade to upstream
	* Labeling and callback interface patches from Eamon Walsh.

* Tue Jun 19 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.21-2
- Refactored swig

* Mon Jun 11 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.21-1
- Upgrade to upstream
	* Class and permission mapping support patches from Eamon Walsh.
	* Object class discovery support patches from Chris PeBenito.
	* Refactoring and errno support in string representation code.

* Fri Jun 1 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.18-1
- Upgrade to upstream
- Merged patch to reduce size of libselinux and remove need for libsepol for embedded systems from Yuichi Nakamura.
 This patch also turns the link-time dependency on libsepol into a runtime (dlopen) dependency even in the non-embedded case.

2.0.17 2007-05-31
	* Updated Lindent script and reindented two header files.

* Fri May 4 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.16-1
- Upgrade to upstream
	* Merged additional swig python bindings from Dan Walsh.
	* Merged helpful message when selinuxfs mount fails patch from Dax Kelson.

* Tue Apr 24 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.14-1
- Upgrade to upstream
	* Merged build fix for avc_internal.c from Joshua Brindle.

* Mon Apr 23 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.13-2
- Add get_context_list funcitions to swig file

* Thu Apr 12 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.13-1
- Upgrade to upstream
	* Merged rpm_execcon python binding fix, matchpathcon man page fix, and getsebool -a handling for EACCES from Dan Walsh.

* Thu Apr 12 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.12-2
- Add missing interface

* Wed Apr 11 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.12-1
- Upgrade to upstream
	* Merged support for getting initial contexts from James Carter.

* Mon Apr 9 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.11-1
- Upgrade to upstream
	* Merged userspace AVC patch to follow kernel's behavior for permissive mode in caching previous denials from Eamon Walsh.
	* Merged sidput(NULL) patch from Eamon Walsh.

* Thu Apr 5 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.9-2
- Make rpm_exec swig work

* Tue Mar 27 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.9-1
- Upgrade to upstream
	* Merged class/av string conversion and avc_compute_create patch from Eamon Walsh.

* Tue Mar 27 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.8-1
- Upgrade to upstream
	* Merged fix for avc.h #include's from Eamon Walsh.

* Thu Mar 22 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.7-2
- Add stdint.h to avc.h

* Mon Mar 12 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.7-1
- Merged patch to drop support for CACHETRANS=0 config option from Steve Grubb.
- Merged patch to drop support for old /etc/sysconfig/selinux and
- /etc/security policy file layout from Steve Grubb.

* Thu Mar 8 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.5-2
- Do not fail on permission denied in getsebool

* Tue Feb 27 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.5-1
- Upgrade to upstream
	* Merged init_selinuxmnt() and is_selinux_enabled() improvements from Steve Grubb.

* Wed Feb 21 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.4-1
- Upgrade to upstream
	* Removed sending of setrans init message.
	* Merged matchpathcon memory leak fix from Steve Grubb.

* Tue Feb 20 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.2-1
- Upgrade to upstream
	* Merged more swig initializers from Dan Walsh.

* Sun Feb 18 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.1-1
- Upgrade to upstream
  * Merged patch from Todd Miller to convert int types over to C99 style.

* Wed Feb 7 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.0-1
- Merged patch from Todd Miller to remove sscanf in matchpathcon.c because
  of the use of the non-standard format (original patch changed
  for style).
- Merged patch from Todd Miller to fix memory leak in matchpathcon.c.

* Fri Jan 19 2007 Dan Walsh <dwalsh@redhat.com> - 1.34.0-2
- Add context function to python to split context into 4 parts

* Fri Jan 19 2007 Dan Walsh <dwalsh@redhat.com> - 1.34.0-1
- Upgrade to upstream
	* Updated version for stable branch.

* Wed Jan 17 2007 Dan Walsh <dwalsh@redhat.com> - 1.33.6-1
- Upgrade to upstream
	* Merged man page updates to make "apropos selinux" work from Dan Walsh.

* Wed Jan 17 2007 Dan Walsh <dwalsh@redhat.com> - 1.33.5-1
- Upgrade to upstream
	* Merged getdefaultcon utility from Dan Walsh.

* Mon Jan 15 2007 Dan Walsh <dwalsh@redhat.com> - 1.33.4-3
- Add Ulrich NSCD__GETSERV and NSCD__SHMEMGRP for Uli

* Fri Jan 12 2007 Dan Walsh <dwalsh@redhat.com> - 1.33.4-2
- Add reference to selinux man page in all man pages to make apropos work
Resolves: # 217881

* Thu Jan 11 2007 Dan Walsh <dwalsh@redhat.com> - 1.33.4-1
- Upstream wanted some minor changes, upgrading to keep api the same
- Upgrade to upstream
	* Merged selinux_check_securetty_context() and support from Dan Walsh.
Resolves: #200110

* Fri Jan 5 2007 Dan Walsh <dwalsh@redhat.com> - 1.33.3-3
- Cleanup patch

* Fri Jan 5 2007 Dan Walsh <dwalsh@redhat.com> - 1.33.3-2
- Add securetty handling
Resolves: #200110

* Thu Jan 4 2007 Dan Walsh <dwalsh@redhat.com> - 1.33.3-1
- Upgrade to upstream
	* Merged patch for matchpathcon utility to use file mode information
	  when available from Dan Walsh.

* Thu Dec  7 2006 Jeremy Katz <katzj@redhat.com> - 1.33.2-4
- rebuild against python 2.5

* Wed Dec 6 2006 Dan Walsh <dwalsh@redhat.com> - 1.33.2-3
- Fix matchpathcon to lstat files

* Thu Nov 30 2006 Dan Walsh <dwalsh@redhat.com> - 1.33.2-2
- Update man page

* Tue Nov 14 2006 Dan Walsh <dwalsh@redhat.com> - 1.33.2-1
- Upgrade to upstream

* Fri Nov 3 2006 Dan Walsh <dwalsh@redhat.com> - 1.33.1-2
- Add James Antill patch for login verification of MLS Levels
-  MLS ragnes need to be checked, Eg. login/cron. This patch adds infrastructure.

* Tue Oct 24 2006 Dan Walsh <dwalsh@redhat.com> - 1.33.1-1
- Upgrade to latest from NSA
	* Merged updated flask definitions from Darrel Goeddel.
 	  This adds the context security class, and also adds
	  the string definitions for setsockcreate and polmatch.

* Tue Oct 17 2006 Dan Walsh <dwalsh@redhat.com> - 1.32-1
- Upgrade to latest from NSA
	* Updated version for release.

* Sun Oct 01 2006 Jesse Keating <jkeating@redhat.com> - 1.30.29-2
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Fri Sep  29 2006 Dan Walsh <dwalsh@redhat.com> - 1.30.29-1
- Upgrade to latest from NSA
	* Merged av_permissions.h update from Steve Grubb,
	  adding setsockcreate and polmatch definitions.

* Wed Sep 27 2006 Jeremy Katz <katzj@redhat.com> - 1.30.28-3
- really make -devel depend on libsepol-devel

* Wed Sep  27 2006 Dan Walsh <dwalsh@redhat.com> - 1.30.28-2
- Add sgrubb patch for polmatch

* Wed Sep  13 2006 Dan Walsh <dwalsh@redhat.com> - 1.30.28-1
- Upgrade to latest from NSA
	* Merged patch from Steve Smalley to fix SIGPIPE in setrans_client

* Tue Sep  5 2006 Jeremy Katz <katzj@redhat.com> - 1.30.27-2
- have -devel require libsepol-devel

* Thu Aug 24 2006 Dan Walsh <dwalsh@redhat.com> - 1.30.27-1
- Upgrade to latest from NSA
	* Merged patch to not log avc stats upon a reset from Steve Grubb.
	* Applied patch to revert compat_net setting upon policy load.
	* Merged file context homedir and local path functions from
	  Chris PeBenito.

* Fri Aug 18 2006 Jesse Keating <jkeating@redhat.com> - 1.20.26-2
- rebuilt with latest binutils to pick up 64K -z commonpagesize on ppc*
  (#203001)

* Sat Aug  12 2006 Dan Walsh <dwalsh@redhat.com> - 1.30.25-1
- Upgrade to latest from NSA
	* Merged file context homedir and local path functions from
	  Chris PeBenito.
	* Rework functions that access /proc/pid/attr to access the
	  per-thread nodes, and unify the code to simplify maintenance.

* Fri Aug  11 2006 Dan Walsh <dwalsh@redhat.com> - 1.30.24-1
- Upgrade to latest from NSA
	* Merged return value fix for *getfilecon() from Dan Walsh.
	* Merged sockcreate interfaces from Eric Paris.

* Wed Aug  9 2006 Dan Walsh <dwalsh@redhat.com> - 1.30.22-2
- Fix translation return codes to return size of buffer

* Tue Aug  1 2006 Dan Walsh <dwalsh@redhat.com> - 1.30.22-1
- Upgrade to latest from NSA
	* Merged no-tls-direct-seg-refs patch from Jeremy Katz.
	* Merged netfilter_contexts support patch from Chris PeBenito.

* Tue Aug  1 2006 Dan Walsh <dwalsh@redhat.com> - 1.30.20-1
- Upgrade to latest from NSA
	* Merged context_*_set errno patch from Jim Meyering.

* Tue Aug  1 2006 Jeremy Katz <katzj@redhat.com> - 1.30.19-5
- only build non-fpic objects with -mno-tls-direct-seg-refs

* Tue Aug  1 2006 Jeremy Katz <katzj@redhat.com> - 1.30.19-4
- build with -mno-tls-direct-seg-refs on x86 to avoid triggering
  segfaults with xen (#200783)

* Mon Jul 17 2006 Dan Walsh <dwalsh@redhat.com> 1.30.19-3
- Rebuild for new gcc

* Tue Jul 11 2006 Dan Walsh <dwalsh@redhat.com> 1.30.19-2
- Fix libselinux to not telinit during installs

* Tue Jul 4 2006 Dan Walsh <dwalsh@redhat.com> 1.30.19-1
- Upgrade to latest from NSA
	* Lindent.
	* Merged {get,set}procattrcon patch set from Eric Paris.
	* Merged re-base of keycreate patch originally by Michael LeMay from Eric Paris.
	* Regenerated Flask headers from refpolicy.
	* Merged patch from Dan Walsh with:
	  - Added selinux_file_context_{cmp,verify}.
	  - Added selinux_lsetfilecon_default.
	  - Delay translation of contexts in matchpathcon.

* Wed Jun 21 2006 Dan Walsh <dwalsh@redhat.com> 1.30.15-5
- Yet another change to matchpathcon

* Wed Jun 21 2006 Dan Walsh <dwalsh@redhat.com> 1.30.15-4
- Turn off error printing in library.  Need to compile with DEBUG to get it back

* Wed Jun 21 2006 Dan Walsh <dwalsh@redhat.com> 1.30.15-3
- Fix error reporting of matchpathcon

* Mon Jun 19 2006 Dan Walsh <dwalsh@redhat.com> 1.30.15-2
- Add function to compare file context on disk versus contexts in file_contexts file.

* Fri Jun 16 2006 Dan Walsh <dwalsh@redhat.com> 1.30.15-1
- Upgrade to latest from NSA
	* Merged patch from Dan Walsh with:
	* Added selinux_getpolicytype() function.
	* Modified setrans code to skip processing if !mls_enabled.
	* Set errno in the !selinux_mnt case.
	* Allocate large buffers from the heap, not on stack.
	  Affects is_context_customizable, selinux_init_load_policy,
	  and selinux_getenforcemode.

* Thu Jun 8 2006 Dan Walsh <dwalsh@redhat.com> 1.30.12-2
- Add selinux_getpolicytype()

* Thu Jun 1 2006 Dan Walsh <dwalsh@redhat.com> 1.30.12-1
- Upgrade to latest from NSA
	* Merged !selinux_mnt checks from Ian Kent.

* Thu Jun 1 2006 Dan Walsh <dwalsh@redhat.com> 1.30.11-2
- Check for selinux_mnt == NULL

* Tue May 30 2006 Dan Walsh <dwalsh@redhat.com> 1.30.11-1
- Merged matchmediacon and trans_to_raw_context fixes from
  Serge Hallyn.

* Fri May 26 2006 Dan Walsh <dwalsh@redhat.com> 1.30.10-4
- Remove getseuser

* Thu May 25 2006 Dan Walsh <dwalsh@redhat.com> 1.30.10-3
- Bump requires to grab latest libsepol

* Tue May 23 2006 Dan Walsh <dwalsh@redhat.com> 1.30.10-2
- Add BuildRequires for swig

* Tue May 23 2006 Dan Walsh <dwalsh@redhat.com> 1.30.10-1
- Upgrade to latest from NSA
	* Merged simple setrans client cache from Dan Walsh.
	  Merged avcstat patch from Russell Coker.
	* Modified selinux_mkload_policy() to also set /selinux/compat_net
	  appropriately for the loaded policy.

* Thu May 18 2006 Dan Walsh <dwalsh@redhat.com> 1.30.8-1
- More fixes for translation cache
- Upgrade to latest from NSA
	* Added matchpathcon_fini() function to free memory allocated by
	  matchpathcon_init().

* Wed May 17 2006 Dan Walsh <dwalsh@redhat.com> 1.30.7-2
- Add simple cache to improve translation speed

* Tue May 16 2006 Dan Walsh <dwalsh@redhat.com> 1.30.7-1
- Upgrade to latest from NSA
	* Merged setrans client cleanup patch from Steve Grubb.

* Tue May 9 2006 Dan Walsh <dwalsh@redhat.com> 1.30.6-2
- Add Russell's AVC patch to handle large numbers

* Mon May 8 2006 Dan Walsh <dwalsh@redhat.com> 1.30.6-1
- Upgrade to latest from NSA
	* Merged getfscreatecon man page fix from Dan Walsh.
	* Updated booleans(8) man page to drop references to the old
	  booleans file and to note that setsebool can be used to set
	  the boot-time defaults via -P.

* Mon May 8 2006 Dan Walsh <dwalsh@redhat.com> 1.30.5-1
- Upgrade to latest from NSA
	* Merged fix warnings patch from Karl MacMillan.
	* Merged setrans client support from Dan Walsh.
	  This removes use of libsetrans.
	* Merged patch to eliminate use of PAGE_SIZE constant from Dan Walsh.
	* Merged swig typemap fixes from Glauber de Oliveira Costa.

* Wed May 3 2006 Dan Walsh <dwalsh@redhat.com> 1.30.3-3
- Change the way translations work,  Use setransd/remove libsetrans

* Tue May 2 2006 Dan Walsh <dwalsh@redhat.com> 1.30.3-2
- Add selinuxswig fixes
- Stop using PAGE_SIZE and start using sysconf(_SC_PAGE_SIZE)

* Fri Apr 14 2006 Dan Walsh <dwalsh@redhat.com> 1.30.3-1
- Upgrade to latest from NSA
	* Added distclean target to Makefile.
	* Regenerated swig files.
	* Changed matchpathcon_init to verify that the spec file is
	  a regular file.
	* Merged python binding t_output_helper removal patch from Dan Walsh.

* Tue Apr 11 2006 Dan Walsh <dwalsh@redhat.com> 1.30.1-2
- Fix python bindings for matchpathcon
- Fix booleans man page

* Mon Mar 27 2006 Dan Walsh <dwalsh@redhat.com> 1.30.1-1
- Merged Makefile PYLIBVER definition patch from Dan Walsh.

* Fri Mar 10 2006 Dan Walsh <dwalsh@redhat.com> 1.30-1
- Make some fixes so it will build on RHEL4
- Upgrade to latest from NSA
	* Updated version for release.
	* Altered rpm_execcon fallback logic for permissive mode to also
	  handle case where /selinux/enforce is not available.

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.29.7-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.29.7-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Jan 20 2006 Dan Walsh <dwalsh@redhat.com> 1.29.7-1
- Upgrade to latest from NSA
	* Merged install-pywrap Makefile patch from Joshua Brindle.

* Wed Jan 18 2006 Dan Walsh <dwalsh@redhat.com> 1.29.6-1
- Upgrade to latest from NSA
	* Merged pywrap Makefile patch from Dan Walsh.

* Fri Jan 13 2006 Dan Walsh <dwalsh@redhat.com> 1.29.5-2
- Split out pywrap in Makefile

* Fri Jan 13 2006 Dan Walsh <dwalsh@redhat.com> 1.29.5-1
- Upgrade to latest from NSA
	* Added getseuser test program.

* Fri Jan 6 2006 Dan Walsh <dwalsh@redhat.com> 1.29.4-1
- Upgrade to latest from NSA
	* Added format attribute to myprintf in matchpathcon.c and
	  removed obsoleted rootlen variable in init_selinux_config().

* Wed Jan 4 2006 Dan Walsh <dwalsh@redhat.com> 1.29.3-2
- Build with new libsepol

* Wed Jan 4 2006 Dan Walsh <dwalsh@redhat.com> 1.29.3-1
- Upgrade to latest from NSA
	* Merged several fixes and improvements from Ulrich Drepper
	  (Red Hat), including:
	  - corrected use of getline
	  - further calls to __fsetlocking for local files
	  - use of strdupa and asprintf
	  - proper handling of dirent in booleans code
	  - use of -z relro
	  - several other optimizations
	* Merged getpidcon python wrapper from Dan Walsh (Red Hat).

* Sat Dec 24 2005 Dan Walsh <dwalsh@redhat.com> 1.29.2-4
- Add build requires line for libsepol-devel

* Tue Dec 20 2005 Dan Walsh <dwalsh@redhat.com> 1.29.2-3
- Fix swig call for getpidcon

* Mon Dec 19 2005 Dan Walsh <dwalsh@redhat.com> 1.29.2-2
- Move libselinux.so to base package

* Wed Dec 14 2005 Dan Walsh <dwalsh@redhat.com> 1.29.2-1
- Upgrade to latest from NSA
	* Merged call to finish_context_translations from Dan Walsh.
	  This eliminates a memory leak from failing to release memory
	  allocated by libsetrans.

* Sun Dec 11 2005 Dan Walsh <dwalsh@redhat.com> 1.29.1-3
- update to latest libsetrans
- Fix potential memory leak

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Dec 8 2005 Dan Walsh <dwalsh@redhat.com> 1.29.1-1
- Update to never version
	* Merged patch for swig interfaces from Dan Walsh.

* Wed Dec 7 2005 Dan Walsh <dwalsh@redhat.com> 1.28-1
- Update to never version

* Wed Dec 7 2005 Dan Walsh <dwalsh@redhat.com> 1.27.28-2
- Fix some of the python swig objects

* Thu Dec 1 2005 Dan Walsh <dwalsh@redhat.com> 1.27.28-1
- Update to latest from NSA
	* Added MATCHPATHCON_VALIDATE flag for set_matchpathcon_flags() and
	  modified matchpathcon implementation to make context validation/
	  canonicalization optional at matchpathcon_init time, deferring it
	  to a successful matchpathcon by default unless the new flag is set
	  by the caller.
	* Added matchpathcon_init_prefix() interface, and
	  reworked matchpathcon implementation to support selective
	  loading of file contexts entries based on prefix matching
	  between the pathname regex stems and the specified path
	  prefix (stem must be a prefix of the specified path prefix).

* Wed Nov 30 2005 Dan Walsh <dwalsh@redhat.com> 1.27.26-1
- Update to latest from NSA
	* Change getsebool to return on/off instead of active/inactive

* Tue Nov 29 2005 Dan Walsh <dwalsh@redhat.com> 1.27.25-1
- Update to latest from NSA
	* Added -f file_contexts option to matchpathcon util.
	  Fixed warning message in matchpathcon_init().
	* Merged Makefile python definitions patch from Dan Walsh.

* Mon Nov 28 2005 Dan Walsh <dwalsh@redhat.com> 1.27.23-1
- Update to latest from NSA
	* Merged swigify patch from Dan Walsh.

* Mon Nov 28 2005 Dan Walsh <dwalsh@redhat.com> 1.27.22-4
- Separate out libselinux-python bindings into separate rpm

* Thu Nov 17 2005 Dan Walsh <dwalsh@redhat.com> 1.27.22-3
- Read libsetrans requirement

* Thu Nov 17 2005 Dan Walsh <dwalsh@redhat.com> 1.27.22-2
- Add python bindings

* Wed Nov 16 2005 Dan Walsh <dwalsh@redhat.com> 1.27.22-1
- Update to latest from NSA
	* Merged make failure in rpm_execcon non-fatal in permissive mode
	  patch from Ivan Gyurdiev.

* Tue Nov 15 2005 Dan Walsh <dwalsh@redhat.com> 1.27.21-2
- Remove requirement for libsetrans

* Tue Nov 8 2005 Dan Walsh <dwalsh@redhat.com> 1.27.21-1
- Update to latest from NSA
	* Added MATCHPATHCON_NOTRANS flag for set_matchpathcon_flags()
	  and modified matchpathcon_init() to skip context translation
	  if it is set by the caller.

* Tue Nov 8 2005 Dan Walsh <dwalsh@redhat.com> 1.27.20-1
- Update to latest from NSA
	* Added security_canonicalize_context() interface and
	  set_matchpathcon_canoncon() interface for obtaining
	  canonical contexts.  Changed matchpathcon internals
	  to obtain canonical contexts by default.  Provided
	  fallback for kernels that lack extended selinuxfs context
	  interface.
- Patch to not translate mls when calling setfiles

* Mon Nov 7 2005 Dan Walsh <dwalsh@redhat.com> 1.27.19-1
- Update to latest from NSA
	* Merged seusers parser changes from Ivan Gyurdiev.
	* Merged setsebool to libsemanage patch from Ivan Gyurdiev.
	* Changed seusers parser to reject empty fields.

* Fri Nov 4 2005 Dan Walsh <dwalsh@redhat.com> 1.27.18-1
- Update to latest from NSA
	* Merged seusers empty level handling patch from Jonathan Kim (TCS).

* Thu Nov 3 2005 Dan Walsh <dwalsh@redhat.com> 1.27.17-4
- Rebuild for latest libsepol

* Mon Oct 31 2005 Dan Walsh <dwalsh@redhat.com> 1.27.17-2
- Rebuild for latest libsepol

* Wed Oct 26 2005 Dan Walsh <dwalsh@redhat.com> 1.27.17-1
- Change default to __default__

* Wed Oct 26 2005 Dan Walsh <dwalsh@redhat.com> 1.27.14-3
- Change default to __default__

* Tue Oct 25 2005 Dan Walsh <dwalsh@redhat.com> 1.27.14-2
- Add selinux_translations_path

* Tue Oct 25 2005 Dan Walsh <dwalsh@redhat.com> 1.27.14-1
- Update to latest from NSA
	* Merged selinux_path() and selinux_homedir_context_path()
	  functions from Joshua Brindle.

* Fri Oct 21 2005 Dan Walsh <dwalsh@redhat.com> 1.27.13-2
- Need to check for /sbin/telinit

* Thu Oct 20 2005 Dan Walsh <dwalsh@redhat.com> 1.27.13-1
- Update to latest from NSA
	* Merged fixes for make DESTDIR= builds from Joshua Brindle.

* Mon Oct 17 2005 Dan Walsh <dwalsh@redhat.com> 1.27.12-1
- Update to latest from NSA
	* Merged get_default_context_with_rolelevel and man pages from
	  Dan Walsh (Red Hat).
	* Updated call to sepol_policydb_to_image for sepol changes.
	* Changed getseuserbyname to ignore empty lines and to handle
	no matching entry in the same manner as no seusers file.

* Fri Oct 14 2005 Dan Walsh <dwalsh@redhat.com> 1.27.9-2
- Tell init to reexec itself in post script

* Fri Oct 7 2005 Dan Walsh <dwalsh@redhat.com> 1.27.9-1
- Update to latest from NSA
	* Changed selinux_mkload_policy to try downgrading the
	latest policy version available to the kernel-supported version.
	* Changed selinux_mkload_policy to fall back to the maximum
	policy version supported by libsepol if the kernel policy version
	falls outside of the supported range.

* Fri Oct 7 2005 Dan Walsh <dwalsh@redhat.com> 1.27.7-1
- Update to latest from NSA
	* Changed getseuserbyname to fall back to the Linux username and
	NULL level if seusers config file doesn't exist unless
	REQUIRESEUSERS=1 is set in /etc/selinux/config.
	* Moved seusers.conf under $SELINUXTYPE and renamed to seusers.

* Thu Oct 6 2005 Dan Walsh <dwalsh@redhat.com> 1.27.6-1
- Update to latest from NSA
	* Added selinux_init_load_policy() function as an even higher level
	interface for the initial policy load by /sbin/init.  This obsoletes
	the load_policy() function in the sysvinit-selinux.patch.
	* Added selinux_mkload_policy() function as a higher level interface
	for loading policy than the security_load_policy() interface.

* Thu Oct 6 2005 Dan Walsh <dwalsh@redhat.com> 1.27.4-1
- Update to latest from NSA
	* Merged fix for matchpathcon (regcomp error checking) from Johan
	Fischer.  Also added use of regerror to obtain the error string
	for inclusion in the error message.

* Tue Oct 4 2005 Dan Walsh <dwalsh@redhat.com> 1.27.3-1
- Update to latest from NSA
	* Changed getseuserbyname to not require (and ignore if present)
	the MLS level in seusers.conf if MLS is disabled, setting *level
	to NULL in this case.

* Mon Oct 3 2005 Dan Walsh <dwalsh@redhat.com> 1.27.2-1
- Update to latest from NSA
	* Merged getseuserbyname patch from Dan Walsh.

* Thu Sep 29 2005 Dan Walsh <dwalsh@redhat.com> 1.27.1-3
- Fix patch to satisfy upstream

* Wed Sep 28 2005 Dan Walsh <dwalsh@redhat.com> 1.27.1-2
- Update to latest from NSA
- Add getseuserbyname

* Fri Sep 16 2005 Dan Walsh <dwalsh@redhat.com> 1.26-6
- Fix patch call

* Tue Sep 13 2005 Dan Walsh <dwalsh@redhat.com> 1.26-5
- Fix strip_con call

* Tue Sep 13 2005 Dan Walsh <dwalsh@redhat.com> 1.26-3
- Go back to original libsetrans code

* Mon Sep 12 2005 Dan Walsh <dwalsh@redhat.com> 1.26-2
- Eliminate forth param from mls context when mls is not enabled.

* Tue Sep 6 2005 Dan Walsh <dwalsh@redhat.com> 1.25.7-1
- Update from NSA
	* Merged modified form of patch to avoid dlopen/dlclose by
	the static libselinux from Dan Walsh.  Users of the static libselinux
	will not have any context translation by default.

* Thu Sep 1 2005 Dan Walsh <dwalsh@redhat.com> 1.25.6-1
- Update from NSA
	* Added public functions to export context translation to
	users of libselinux (selinux_trans_to_raw_context,
	selinux_raw_to_trans_context).

* Mon Aug 29 2005 Dan Walsh <dwalsh@redhat.com> 1.25.5-1
- Update from NSA
	* Remove special definition for context_range_set; use
	common code.

* Thu Aug 25 2005 Dan Walsh <dwalsh@redhat.com> 1.25.4-1
- Update from NSA
	* Hid translation-related symbols entirely and ensured that
	raw functions have hidden definitions for internal use.
	* Allowed setting NULL via context_set* functions.
	* Allowed whitespace in MLS component of context.
	* Changed rpm_execcon to use translated functions to workaround
	lack of MLS level on upgraded systems.

* Wed Aug 24 2005 Dan Walsh <dwalsh@redhat.com> 1.25.3-2
- Allow set_comp on unset ranges

* Wed Aug 24 2005 Dan Walsh <dwalsh@redhat.com> 1.25.3-1
- Merged context translation patch, originally by TCS,
  with modifications by Dan Walsh (Red Hat).

* Wed Aug 17 2005 Dan Walsh <dwalsh@redhat.com> 1.25.2-2
- Apply translation patch

* Thu Aug 11 2005 Dan Walsh <dwalsh@redhat.com> 1.25.2-1
- Update from NSA
	* Merged several fixes for error handling paths in the
	  AVC sidtab, matchpathcon, booleans, context, and get_context_list
	  code from Serge Hallyn (IBM). Bugs found by Coverity.
	* Removed setupns; migrated to pam.
	* Merged patches to rename checkPasswdAccess() from Joshua Brindle.
	  Original symbol is temporarily retained for compatibility until
	  all callers are updated.

* Mon Jul 18 2005 Dan Walsh <dwalsh@redhat.com> 1.24.2-1
- Update makefiles

* Wed Jun 29 2005 Dan Walsh <dwalsh@redhat.com> 1.24.1-1
- Update from NSA
	* Merged security_setupns() from Chad Sellers.
- fix selinuxenabled man page

* Fri May 20 2005 Dan Walsh <dwalsh@redhat.com> 1.23.11-1
- Update from NSA
	* Merged avcstat and selinux man page from Dan Walsh.
	* Changed security_load_booleans to process booleans.local
	  even if booleans file doesn't exist.

* Fri Apr 29 2005 Dan Walsh <dwalsh@redhat.com> 1.23.10-3
- Fix avcstat to clear totals

* Fri Apr 29 2005 Dan Walsh <dwalsh@redhat.com> 1.23.10-2
- Add info to man page

* Fri Apr 29 2005 Dan Walsh <dwalsh@redhat.com> 1.23.10-1
- Update from NSA
	* Merged set_selinuxmnt patch from Bill Nottingham (Red Hat).
	* Rewrote get_ordered_context_list and helpers, including
	  changing logic to allow variable MLS fields.

* Tue Apr 26 2005 Dan Walsh <dwalsh@redhat.com> 1.23.8-1
- Update from NSA

* Thu Apr 21 2005 Dan Walsh <dwalsh@redhat.com> 1.23.7-3
- Add backin matchpathcon

* Wed Apr 13 2005 Dan Walsh <dwalsh@redhat.com> 1.23.7-2
- Fix selinux_policy_root man page

* Wed Apr 13 2005 Dan Walsh <dwalsh@redhat.com> 1.23.7-1
- Change assert(selinux_mnt) to if (!selinux_mnt) return -1;

* Mon Apr 11 2005 Dan Walsh <dwalsh@redhat.com> 1.23.6-1
- Update from NSA
	* Fixed bug in matchpathcon_filespec_destroy.

* Wed Apr 6 2005 Dan Walsh <dwalsh@redhat.com> 1.23.5-1
- Update from NSA
	* Fixed bug in rpm_execcon error handling path.

* Mon Apr 4 2005 Dan Walsh <dwalsh@redhat.com> 1.23.4-1
- Update from NSA
	* Merged fix for set_matchpathcon* functions from Andreas Steinmetz.
	* Merged fix for getconlist utility from Andreas Steinmetz.

* Tue Mar 29 2005 Dan Walsh <dwalsh@redhat.com> 1.23.2-3
- Update from NSA

* Wed Mar 23 2005 Dan Walsh <dwalsh@redhat.com> 1.23.2-2
- Better handling of booleans

* Thu Mar 17 2005 Dan Walsh <dwalsh@redhat.com> 1.23.2-1
- Update from NSA
	* Merged destructors patch from Tomas Mraz.

* Thu Mar 17 2005 Dan Walsh <dwalsh@redhat.com> 1.23.1-1
- Update from NSA
	* Added set_matchpathcon_flags() function for setting flags
	  controlling operation of matchpathcon.  MATCHPATHCON_BASEONLY
	  means only process the base file_contexts file, not
	  file_contexts.homedirs or file_contexts.local, and is for use by
	  setfiles -c.
	* Updated matchpathcon.3 man page.

* Thu Mar 10 2005 Dan Walsh <dwalsh@redhat.com> 1.22-1
- Update from NSA

* Tue Mar 8 2005 Dan Walsh <dwalsh@redhat.com> 1.21.13-1
- Update from NSA
	* Fixed bug in matchpathcon_filespec_add() - failure to clear fl_head.

* Tue Mar 1 2005 Dan Walsh <dwalsh@redhat.com> 1.21.12-1
- Update from NSA
  * Changed matchpathcon_common to ignore any non-format bits in the mode.

* Mon Feb 28 2005 Dan Walsh <dwalsh@redhat.com> 1.21.11-2
- Default matchpathcon to regular files if the user specifies a mode

* Tue Feb 22 2005 Dan Walsh <dwalsh@redhat.com> 1.21.11-1
- Update from NSA
	* Merged several fixes from Ulrich Drepper.

* Mon Feb 21 2005 Dan Walsh <dwalsh@redhat.com> 1.21.10-3
- Fix matchpathcon on eof.

* Thu Feb 17 2005 Dan Walsh <dwalsh@redhat.com> 1.21.10-1
- Update from NSA
	* Merged matchpathcon patch for file_contexts.homedir from Dan Walsh.
	* Added selinux_users_path() for path to directory containing
	  system.users and local.users.

* Thu Feb 10 2005 Dan Walsh <dwalsh@redhat.com> 1.21.9-2
- Process file_context.homedir

* Thu Feb 10 2005 Dan Walsh <dwalsh@redhat.com> 1.21.9-1
- Update from NSA
  *	 Changed relabel Makefile target to use restorecon.

* Tue Feb 8 2005 Dan Walsh <dwalsh@redhat.com> 1.21.8-1
- Update from NSA
	* Regenerated av_permissions.h.

* Wed Feb 2 2005 Dan Walsh <dwalsh@redhat.com> 1.21.7-1
- Update from NSA
	* Modified avc_dump_av to explicitly check for any permissions that
	  cannot be mapped to string names and display them as a hex value.
	* Regenerated av_permissions.h.

* Mon Jan 31 2005 Dan Walsh <dwalsh@redhat.com> 1.21.5-1
- Update from NSA
	* Generalized matchpathcon internals, exported more interfaces,
	  and moved additional code from setfiles into libselinux so that
	  setfiles can directly use matchpathcon.

* Fri Jan 28 2005 Dan Walsh <dwalsh@redhat.com> 1.21.4-1
- Update from NSA
	* Prevent overflow of spec array in matchpathcon.
	* Fixed several uses of internal functions to avoid relocations.
	* Changed rpm_execcon to check is_selinux_enabled() and fallback to
	  a regular execve if not enabled (or unable to determine due to a lack
	  of /proc, e.g. chroot'd environment).

* Wed Jan 26 2005 Dan Walsh <dwalsh@redhat.com> 1.21.2-1
- Update from NSA
	* Merged minor fix for avcstat from Dan Walsh.

* Mon Jan 24 2005 Dan Walsh <dwalsh@redhat.com> 1.21.1-3
- rpmexeccon should not fail in permissive mode.

* Fri Jan 21 2005 Dan Walsh <dwalsh@redhat.com> 1.21.1-2
- fix printf in avcstat

* Thu Jan 20 2005 Dan Walsh <dwalsh@redhat.com> 1.21.1-1
- Update from NSA

* Wed Jan 12 2005 Dan Walsh <dwalsh@redhat.com> 1.20.1-3
- Modify matchpathcon to also process file_contexts.local if it exists

* Wed Jan 12 2005 Dan Walsh <dwalsh@redhat.com> 1.20.1-2
- Add is_customizable_types function call

* Fri Jan 7 2005 Dan Walsh <dwalsh@redhat.com> 1.20.1-1
- Update to latest from upstream
	* Just changing version number to match upstream

* Wed Dec 29 2004 Dan Walsh <dwalsh@redhat.com> 1.19.4-1
- Update to latest from upstream
	* Changed matchpathcon to return -1 with errno ENOENT for
	  <<none>> entries, and also for an empty file_contexts configuration.

* Tue Dec 28 2004 Dan Walsh <dwalsh@redhat.com> 1.19.3-3
- Fix link devel libraries

* Mon Dec 27 2004 Dan Walsh <dwalsh@redhat.com> 1.19.3-2
- Fix unitialized variable in avcstat.c

* Tue Nov 30 2004 Dan Walsh <dwalsh@redhat.com> 1.19.3-1
- Upgrade to upstream
	* Removed some trivial utils that were not useful or redundant.
	* Changed BINDIR default to /usr/sbin to match change in Fedora.
	* Added security_compute_member.
	* Added man page for setcon.

* Tue Nov 30 2004 Dan Walsh <dwalsh@redhat.com> 1.19.2-1
- Upgrade to upstream

* Thu Nov 18 2004 Dan Walsh <dwalsh@redhat.com> 1.19.1-6
- Add avcstat program

* Mon Nov 15 2004 Dan Walsh <dwalsh@redhat.com> 1.19.1-4
- Add lots of missing man pages

* Fri Nov 12 2004 Dan Walsh <dwalsh@redhat.com> 1.19.1-2
- Fix output of getsebool.

* Tue Nov 9 2004 Dan Walsh <dwalsh@redhat.com> 1.19.1-1
- Update from upstream, fix setsebool -P segfault

* Fri Nov 5 2004 Steve Grubb <sgrubb@redhat.com> 1.18.1-5
- Add a patch from upstream. Fixes signed/unsigned issues, and
  incomplete structure copy.

* Thu Nov 4 2004 Dan Walsh <dwalsh@redhat.com> 1.18.1-4
- More fixes from sgrubb, better syslog

* Thu Nov 4 2004 Dan Walsh <dwalsh@redhat.com> 1.18.1-3
- Have setsebool and togglesebool log changes to syslog

* Wed Nov 3 2004 Steve Grubb <sgrubb@redhat.com> 1.18.1-2
- Add patch to make setsebool update bool on disk
- Make togglesebool have a rollback capability in case it blows up inflight

* Tue Nov 2 2004 Dan Walsh <dwalsh@redhat.com> 1.18.1-1
- Upgrade to latest from NSA

* Thu Oct 28 2004 Steve Grubb <sgrubb@redhat.com> 1.17.15-2
- Changed the location of the utilities to /usr/sbin since
  normal users can't use them anyways.

* Wed Oct 27 2004 Steve Grubb <sgrubb@redhat.com> 1.17.15-2
- Updated various utilities, removed utilities that are for testing,
  added man pages.

* Fri Oct 15 2004 Dan Walsh <dwalsh@redhat.com> 1.17.15-1
- Add -g flag to make
- Upgrade to latest  from NSA
	* Added rpm_execcon.

* Fri Oct 1 2004 Dan Walsh <dwalsh@redhat.com> 1.17.14-1
- Upgrade to latest  from NSA
	* Merged setenforce and removable context patch from Dan Walsh.
	* Merged build fix for alpha from Ulrich Drepper.
	* Removed copyright/license from selinux_netlink.h - definitions only.

* Fri Oct 1 2004 Dan Walsh <dwalsh@redhat.com> 1.17.13-3
- Change setenforce to accept Enforcing and Permissive

* Wed Sep 22 2004 Dan Walsh <dwalsh@redhat.com> 1.17.13-2
- Add alpha patch

* Mon Sep 20 2004 Dan Walsh <dwalsh@redhat.com> 1.17.13-1
- Upgrade to latest  from NSA

* Thu Sep 16 2004 Dan Walsh <dwalsh@redhat.com> 1.17.12-2
- Add selinux_removable_context_path

* Tue Sep 14 2004 Dan Walsh <dwalsh@redhat.com> 1.17.12-1
- Update from NSA
	* Add matchmediacon

* Tue Sep 14 2004 Dan Walsh <dwalsh@redhat.com> 1.17.11-1
- Update from NSA
	* Merged in matchmediacon changes.

* Fri Sep 10 2004 Dan Walsh <dwalsh@redhat.com> 1.17.10-1
- Update from NSA
	* Regenerated headers for new nscd permissions.

* Wed Sep 8 2004 Dan Walsh <dwalsh@redhat.com> 1.17.9-2
- Add matchmediacon

* Wed Sep 8 2004 Dan Walsh <dwalsh@redhat.com> 1.17.9-1
- Update from NSA
	* Added get_default_context_with_role.

* Thu Sep 2 2004 Dan Walsh <dwalsh@redhat.com> 1.17.8-2
- Clean up spec file
	* Patch from Matthias Saou

* Thu Sep 2 2004 Dan Walsh <dwalsh@redhat.com> 1.17.8-1
- Update from NSA
	* Added set_matchpathcon_printf.

* Wed Sep 1 2004 Dan Walsh <dwalsh@redhat.com> 1.17.7-1
- Update from NSA
	* Reworked av_inherit.h to allow easier re-use by kernel.

* Tue Aug 31 2004 Dan Walsh <dwalsh@redhat.com> 1.17.6-1
- Add strcasecmp in selinux_config
- Update from NSA
	* Changed avc_has_perm_noaudit to not fail on netlink errors.
	* Changed avc netlink code to check pid based on patch by Steve Grubb.
	* Merged second optimization patch from Ulrich Drepper.
	* Changed matchpathcon to skip invalid file_contexts entries.
	* Made string tables private to libselinux.
	* Merged strcat->stpcpy patch from Ulrich Drepper.
	* Merged matchpathcon man page from Dan Walsh.
	* Merged patch to eliminate PLTs for local syms from Ulrich Drepper.
	* Autobind netlink socket.
	* Dropped compatibility code from security_compute_user.
	* Merged fix for context_range_set from Chad Hanson.
	* Merged allocation failure checking patch from Chad Hanson.
	* Merged avc netlink error message patch from Colin Walters.


* Mon Aug 30 2004 Dan Walsh <dwalsh@redhat.com> 1.17.5-1
- Update from NSA
	* Merged second optimization patch from Ulrich Drepper.
	* Changed matchpathcon to skip invalid file_contexts entries.
	* Made string tables private to libselinux.
	* Merged strcat->stpcpy patch from Ulrich Drepper.
	* Merged matchpathcon man page from Dan Walsh.
	* Merged patch to eliminate PLTs for local syms from Ulrich Drepper.
	* Autobind netlink socket.
	* Dropped compatibility code from security_compute_user.
	* Merged fix for context_range_set from Chad Hanson.
	* Merged allocation failure checking patch from Chad Hanson.
	* Merged avc netlink error message patch from Colin Walters.

* Mon Aug 30 2004 Dan Walsh <dwalsh@redhat.com> 1.17.4-1
- Update from NSA
- Add optflags

* Fri Aug 27 2004 Dan Walsh <dwalsh@redhat.com> 1.17.3-1
- Update from NSA

* Thu Aug 26 2004 Dan Walsh <dwalsh@redhat.com> 1.17.2-1
- Add matchpathcon man page
- Latest from NSA
	* Merged patch to eliminate PLTs for local syms from Ulrich Drepper.
	* Autobind netlink socket.
	* Dropped compatibility code from security_compute_user.
	* Merged fix for context_range_set from Chad Hanson.
	* Merged allocation failure checking patch from Chad Hanson.
	* Merged avc netlink error message patch from Colin Walters.

* Tue Aug 24 2004 Dan Walsh <dwalsh@redhat.com> 1.17.1-1
- Latest from NSA
	* Autobind netlink socket.
	* Dropped compatibility code from security_compute_user.
	* Merged fix for context_range_set from Chad Hanson.
	* Merged allocation failure checking patch from Chad Hanson.
	* Merged avc netlink error message patch from Colin Walters.

* Sun Aug 22 2004 Dan Walsh <dwalsh@redhat.com> 1.16.1-1
- Latest from NSA

* Thu Aug 19 2004 Colin Walters <walters@redhat.com> 1.16-1
- New upstream version

* Tue Aug 17 2004 Dan Walsh <dwalsh@redhat.com> 1.15.7-1
- Latest from Upstream

* Mon Aug 16 2004 Dan Walsh <dwalsh@redhat.com> 1.15.6-1
- Fix man pages

* Mon Aug 16 2004 Dan Walsh <dwalsh@redhat.com> 1.15.5-1
- Latest from Upstream

* Fri Aug 13 2004 Dan Walsh <dwalsh@redhat.com> 1.15.4-1
- Latest from Upstream

* Thu Aug 12 2004 Dan Walsh <dwalsh@redhat.com> 1.15.3-2
- Add man page for boolean functions and SELinux

* Sun Aug 8 2004 Dan Walsh <dwalsh@redhat.com> 1.15.3-1
- Latest from NSA

* Mon Jul 19 2004 Dan Walsh <dwalsh@redhat.com> 1.15.2-1
- Latest from NSA

* Mon Jul 19 2004 Dan Walsh <dwalsh@redhat.com> 1.15.1-3
- uppercase getenforce returns, to make them match system-config-securitylevel

* Thu Jul 15 2004 Dan Walsh <dwalsh@redhat.com> 1.15.1-2
- Remove old path patch

* Thu Jul 8 2004 Dan Walsh <dwalsh@redhat.com> 1.15.1-1
- Update to latest from NSA
- Add fix to only get old path if file_context file exists in old location

* Wed Jun 30 2004 Dan Walsh <dwalsh@redhat.com> 1.14.1-1
- Update to latest from NSA

* Wed Jun 16 2004 Dan Walsh <dwalsh@redhat.com> 1.13.4-1
- add nlclass patch
- Update to latest from NSA

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sun Jun 13 2004 Dan Walsh <dwalsh@redhat.com> 1.13.3-2
- Fix selinux_config to break once it finds SELINUXTYPE.

* Fri May 28 2004 Dan Walsh <dwalsh@redhat.com> 1.13.2-1
-Update with latest from NSA

* Thu May 27 2004 Dan Walsh <dwalsh@redhat.com> 1.13.1-1
- Change to use new policy mechanism

* Mon May 17 2004 Dan Walsh <dwalsh@redhat.com> 1.12-2
- add man patch

* Fri May 14 2004 Dan Walsh <dwalsh@redhat.com> 1.12-1
- Update with latest from NSA

* Wed May 5 2004 Dan Walsh <dwalsh@redhat.com> 1.11.4-1
- Update with latest from NSA

* Thu Apr 22 2004 Dan Walsh <dwalsh@redhat.com> 1.11.3-1
- Add changes for relaxed policy
- Update to match NSA

* Thu Apr 15 2004 Dan Walsh <dwalsh@redhat.com> 1.11.2-1
- Add relaxed policy changes

* Thu Apr 15 2004 Dan Walsh <dwalsh@redhat.com> 1.11-4
- Sync with NSA

* Thu Apr 15 2004 Dan Walsh <dwalsh@redhat.com> 1.11-3
- Remove requires glibc>2.3.4

* Wed Apr 14 2004 Dan Walsh <dwalsh@redhat.com> 1.11-2
- Fix selinuxenabled man page.

* Wed Apr 7 2004 Dan Walsh <dwalsh@redhat.com> 1.11-1
- Upgrade to 1.11

* Wed Apr 7 2004 Dan Walsh <dwalsh@redhat.com> 1.10-2
- Add memleaks patch

* Wed Apr 7 2004 Dan Walsh <dwalsh@redhat.com> 1.10-1
- Upgrade to latest from NSA and add more man pages

* Thu Apr 1 2004 Dan Walsh <dwalsh@redhat.com> 1.9-1
- Update to match NSA
- Cleanup some man pages

* Tue Mar 30 2004 Dan Walsh <dwalsh@redhat.com> 1.8-1
- Upgrade to latest from NSA

* Thu Mar 25 2004 Dan Walsh <dwalsh@redhat.com> 1.6-6
- Add Russell's Man pages

* Thu Mar 25 2004 Dan Walsh <dwalsh@redhat.com> 1.6-5
- Change getenforce to also check is_selinux_enabled

* Thu Mar 25 2004 Dan Walsh <dwalsh@redhat.com> 1.6-4
- Add ownership to /usr/include/selinux

* Wed Mar 10 2004 Dan Walsh <dwalsh@redhat.com> 1.6-3
- fix location of file_contexts file.

* Wed Mar 10 2004 Dan Walsh <dwalsh@redhat.com> 1.6-2
- Fix matchpathcon to use BUFSIZ

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Feb 23 2004 Dan Walsh <dwalsh@redhat.com> 1.4-11
- add matchpathcon

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Jan 23 2004 Dan Walsh <dwalsh@redhat.com> 1.4-9
- Add rootok patch

* Wed Jan 14 2004 Dan Walsh <dwalsh@redhat.com> 1.4-8
- Updated getpeernam patch

* Tue Jan 13 2004 Dan Walsh <dwalsh@redhat.com> 1.4-7
- Add getpeernam patch

* Thu Dec 18 2003 Dan Walsh <dwalsh@redhat.com> 1.4-6
- Add getpeercon patch

* Thu Dec 18 2003 Dan Walsh <dwalsh@redhat.com> 1.4-5
- Put mntpoint patch, because found fix for SysVinit

* Wed Dec 17 2003 Dan Walsh <dwalsh@redhat.com> 1.4-4
- Add remove mntpoint patch, because it breaks SysVinit

* Wed Dec 17 2003 Dan Walsh <dwalsh@redhat.com> 1.4-3
- Add mntpoint patch for SysVinit

* Fri Dec 12 2003 Dan Walsh <dwalsh@redhat.com> 1.4-2
- Add -r -u -t to getcon

* Sat Dec 6 2003 Dan Walsh <dwalsh@redhat.com> 1.4-1
- Upgrade to latest from NSA

* Mon Oct 27 2003 Dan Walsh <dwalsh@redhat.com> 1.3-2
- Fix x86_64 build

* Wed Oct 22 2003 Dan Walsh <dwalsh@redhat.com> 1.3-1
- Latest tarball from NSA.

* Tue Oct 21 2003 Dan Walsh <dwalsh@redhat.com> 1.2-9
- Update with latest changes from NSA

* Mon Oct 20 2003 Dan Walsh <dwalsh@redhat.com> 1.2-8
- Change location of .so file

* Wed Oct 8 2003 Dan Walsh <dwalsh@redhat.com> 1.2-7
- Break out into development library

* Wed Oct  8 2003 Dan Walsh <dwalsh@redhat.com> 1.2-6
- Move location of libselinux.so to /lib

* Fri Oct  3 2003 Dan Walsh <dwalsh@redhat.com> 1.2-5
- Add selinuxenabled patch

* Wed Oct  1 2003 Dan Walsh <dwalsh@redhat.com> 1.2-4
- Update with final NSA 1.2 sources.

* Fri Sep  12 2003 Dan Walsh <dwalsh@redhat.com> 1.2-3
- Update with latest from NSA.

* Thu Aug  28 2003 Dan Walsh <dwalsh@redhat.com> 1.2-2
- Fix to build on x86_64

* Thu Aug  21 2003 Dan Walsh <dwalsh@redhat.com> 1.2-1
- update for version 1.2

* Tue May 27 2003 Dan Walsh <dwalsh@redhat.com> 1.0-1
- Initial version

## END: Generated by rpmautospec
