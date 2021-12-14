%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_version: %define python3_version %(python3 -c "import sys; sys.stdout.write(sys.version[:3])")}
%{!?__python3: %global __python3 /usr/bin/python3}

# what it's called on pypi
%global srcname sniffio
# what it's imported as
%global libname sniffio
# name of egg info directory
%global eggname sniffio
# package name fragment
%global pkgname sniffio

%global _description \
You're writing a library.  You've decided to be ambitious, and support multiple\
async I/O packages, like Trio, and asyncio, and ... You've written a bunch of\
clever code to handle all the differences.  But... how do you know which piece\
of clever code to run?  This is a tiny package whose only purpose is to let you\
detect which async library your code is running under.

Summary:        Sniff out which async library your code is running under
Name:           python-%{pkgname}
Version:        1.1.0
Release:        9%{?dist}
License:        MIT or ASL 2.0
URL:            https://github.com/python-trio/sniffio
#Source0:       https://files.pythonhosted.org/packages/source/s/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
Source0:        https://files.pythonhosted.org/packages/source/s/%{pypi_name}/%{name}-%{version}.tar.gz
BuildArch:      noarch

%description %{_description}

%package -n python3-%{pkgname}
Summary:        %{summary}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pytest
BuildRequires:  python3-curio
%{?python_provide:%python_provide python%{python3_pkgversion}-%{pkgname}}

%description -n python3-%{pkgname} %{_description}

%prep
%autosetup -n %{srcname}-%{version}
rm -rf %{eggname}.egg-info

%build
%py3_build

%install
%py3_install

%check
py.test-%{python3_version} --verbose

%files -n python3-%{pkgname}
%license LICENSE LICENSE.MIT LICENSE.APACHE2
%doc README.rst
%{python3_sitelib}/%{libname}
%{python3_sitelib}/%{eggname}-%{version}-py%{python3_version}.egg-info

%changelog
* Tue Jan 12 2021 Steve Laughman <steve.laughman@microsoft.com> - 1.1.0-9
- Correction to files declaration
* Tue Dec 08 2020 Steve Laughman <steve.laughman@microsoft.com> - 1.1.0-8
- Initial CBL-Mariner import from Fedora 33 (license: MIT)
* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild
* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 1.1.0-6
- Rebuilt for Python 3.9
* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild
* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.1.0-4
- Rebuilt for Python 3.8.0rc1 (#1748018)
* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.1.0-3
- Rebuilt for Python 3.8
* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild
* Tue May 14 2019 Carl George <carl@george.computer> - 1.1.0-1
- Latest upstream
* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild
* Wed Sep 12 2018 Carl George <carl@george.computer> - 1.0.0-1
- Initial package