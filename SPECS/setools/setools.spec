%global selinux_ver 2.9-1
%global __python3	/usr/bin/python3
%define python3_sitearch %(python3 -c "from distutils.sysconfig import get_python_lib; import sys; sys.stdout.write(get_python_lib(1))")

Name:           setools
Version:        4.2.2
Release:        1%{?setools_pre_ver:.%{setools_pre_ver}}%{?dist}
Summary:        Policy analysis tools for SELinux

License:        GPLv2
URL:            https://github.com/SELinuxProject/setools
Source0:        https://github.com/SELinuxProject/setools/releases/download/%{version}/%{name}-%{version}.tar.bz2

BuildRequires:  flex,  bison
BuildRequires:  glibc-devel, gcc, git
BuildRequires:  libsepol-devel >= 2.9-1
BuildRequires:  qt5-qtbase-devel
BuildRequires:  swig
BuildRequires:  python3-Cython
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
BuildRequires:  libselinux-devel

%description
SETools is a collection of graphical tools, command-line tools, and
Python modules designed to facilitate SELinux policy analysis.

%package     console
Summary:     Policy analysis command-line tools for SELinux
License:     GPLv2
Requires:    setools-python3 = %{version}-%{release}
Requires:    libselinux >= %{selinux_ver}

%description console
SETools is a collection of graphical tools, command-line tools, and
libraries designed to facilitate SELinux policy analysis.

This package includes the following console tools:

  sediff       Compare two policies to find differences.
  seinfo       List policy components.
  sesearch     Search rules (allow, type_transition, etc.)

%package     python3
Summary:     Policy analysis tools for SELinux
Obsoletes:   setools-libs < 4.0.0
Recommends:  libselinux-python3
Requires:    python3-setuptools

%description python3
SETools is a collection of graphical tools, command-line tools, and
Python 3 modules designed to facilitate SELinux policy analysis.
%prep
%setup -n %{name}

%build
pwd
%{__python3} setup.py build_ext
%{__python3} setup.py build


%install
%{__python3} setup.py install --prefix=%{_prefix} --root=%{buildroot}

# Remove unpackaged files.  These are tools for which the dependencies
# are not yet available on mariner (python3-networkx)
rm -rf %{buildroot}/%{_bindir}/sedta
rm -rf %{buildroot}/%{_bindir}/seinfoflow
rm -rf %{buildroot}/%{_mandir}/man1/sedta*
rm -rf %{buildroot}/%{_mandir}/man1/seinfoflow*
rm -rf %{buildroot}/%{_bindir}/apol
rm -rf %{buildroot}/%{python3_sitearch}/setoolsgui
rm -rf %{buildroot}/%{_mandir}/man1/apol*

%files

%files console
%{_bindir}/sediff
%{_bindir}/seinfo
%{_bindir}/sesearch
%{_mandir}/man1/sediff*
%{_mandir}/man1/seinfo*
%{_mandir}/man1/sesearch*

%files python3
%license COPYING COPYING.GPL COPYING.LGPL
%{python3_sitearch}/setools
%{python3_sitearch}/setools-*

%changelog
* Tue Sep 01 2020 Daniel Burgener <daburgen@microsoft.com> 4.2.2-1
- Initial import from Fedora 31
