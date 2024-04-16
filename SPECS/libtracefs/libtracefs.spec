# git tag
#%%global commit 4f24f98960c223e56329519bb90a90f0b2ad813f
#%%global commitdate 20201120
#%%global shortcommit %%(c=%%{commit}; echo ${c:0:7})

# LTO causes linking issues randomly like
# lto1: internal compiler error: resolution sub id 0x7136344381f3059f not in object file
# So disabling LTO at this moment.

%global _lto_cflags %nil

Name:           libtracefs
Version:        1.8.0
Release:        1%{?dist}
License:        LGPL-2.1-or-later AND GPL-2.0-or-later AND GPL-2.0-only
Summary:        Library for access kernel tracefs

# If upstream does not provide tarballs, to generate:
# git clone git://git.kernel.org/pub/scm/libs/libtrace/libtracefs.git
# cd libtracefs
# git archive --prefix=libtracefs-%%{version}/ -o libtracefs-%%{version}.tar.gz %%{git_commit}
URL:            https://git.kernel.org/pub/scm/libs/libtrace/libtracefs.git/
Source0:        https://git.kernel.org/pub/scm/libs/libtrace/libtracefs.git/snapshot/libtracefs-%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconfig(libtraceevent) >= 1.8.0

# The libtracefs is meant to be used by perf, trace-cmd etc. in the future, before it's ready in perf, let's add a conflict
Conflicts:      trace-cmd < 2.9.1-6

%description
libtracefs is a library for accessing kernel tracefs

%package devel
Summary: Development headers of %{name}
Requires: %{name}%{_isa} = %{version}-%{release}

%description devel
Development headers of %{name}

%prep
%autosetup -p1

%build
%set_build_flags
# parallel compiling don't always work
make -O -j1 V=1 VERBOSE=1 prefix=%{_prefix} libdir=%{_libdir} all

%install
%make_install prefix=%{_prefix} libdir=%{_libdir}
rm -rf %{buildroot}/%{_libdir}/libtracefs.a

%files
%license LICENSES/LGPL-2.1
%license LICENSES/GPL-2.0
%{_libdir}/%{name}.so.1
%{_libdir}/%{name}.so.1.8.0

%files devel
%{_includedir}/tracefs/tracefs.h
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/%{name}.so

%changelog
* Thu Feb 15 2024 Aadhar Agarwal <aadagarwal@microsoft.com> - 1.8.0-1
- Initial Azure Linux import from Fedora 40 (license: MIT)
- License Verified
