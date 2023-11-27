Vendor:         Microsoft Corporation
Distribution:   Mariner

Name: catatonit
Version: 0.1.7
Release: 10%{?dist}
Summary: A signal-forwarding process manager for containers
License: GPLv3+
URL: https://github.com/openSUSE/catatonit
Source0: %{url}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: file
BuildRequires: gcc
BuildRequires: git
BuildRequires: glibc-static >= 2.38-1%{?dist}
BuildRequires: libtool
BuildRequires: make

Provides: podman-%{name} = %{version}-%{release}

%description
Catatonit is a /sbin/init program for use within containers. It
forwards (almost) all signals to the spawned child, tears down
the container when the spawned child exits, and otherwise
cleans up other exited processes (zombies).

This is a reimplementation of other container init programs (such as
"tini" or "dumb-init"), but uses modern Linux facilities (such as
signalfd(2)) and has no additional features.

%prep
%autosetup -Sgit
sed -i '$d' configure.ac

%build
autoreconf -fi
%configure
%{__make} %{?_smp_mflags}

# Make sure we *always* build a static binary. Otherwise we'll break containers
# that don't have the necessary shared libs.
file ./%{name} | grep 'statically linked'
if [ $? != 0 ]; then
   echo "ERROR: %{name} binary must be statically linked!"
   exit 1
fi

%install
install -dp %{buildroot}%{_libexecdir}/%{name}
install -p %{name} %{buildroot}%{_libexecdir}/%{name}
install -dp %{buildroot}%{_libexecdir}/podman
ln -s %{_libexecdir}/%{name}/%{name} %{buildroot}%{_libexecdir}/podman/%{name}

%files
%license COPYING
%doc README.md
%dir %{_libexecdir}/%{name}
%{_libexecdir}/%{name}/%{name}
%dir %{_libexecdir}/podman
%{_libexecdir}/podman/%{name}

%changelog
* Tue Nov 07 2023 Andrew Phelps <anphel@microsoft.com> - 0.1.7-10
- Bump release to rebuild against glibc 2.38-1

* Wed Oct 04 2023 Minghe Ren <mingheren@microsoft.com> - 0.1.7-9
- Bump release to rebuild against glibc 2.35-6

* Tue Oct 03 2023 Mandeep Plaha <mandeepplaha@microsoft.com> - 0.1.7-8
- Bump release to rebuild against glibc 2.35-5

* Wed Jul 05 2023 Andrew Phelps <anphel@microsoft.com> - 0.1.7-7
- Bump release to rebuild against glibc 2.35-4

* Tue Sep 13 2022 Andy Caldwell <andycaldwell@microsoft.com> - 0.1.7-6
- Rebuilt for glibc-static 2.35-3

* Fri Mar 18 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.1.7-1
- Updating to 0.1.7 using Fedora 35 spec (license: MIT) for guidance.
- License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.1.5-4
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Mon Sep 14 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.1.5-3
- bump release - bot messed up earlier

* Wed Sep  2 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 0.1.5-1
- autobuilt v0.1.5

* Wed Apr 29 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.1.5-2
- complain if not statically linked, patch from Jindrich Novy <jnovy@redhat.com> 

* Wed Apr 29 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.1.5-1
- bump to v0.1.5
- static binary to not break containers that don't have necessary shared libs

* Wed Feb 19 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.1.4-1
- first build for review
- source copied from openSUSE @ https://build.opensuse.org/package/show/openSUSE:Factory/catatonit
