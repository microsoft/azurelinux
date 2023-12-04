%define version_tag %(echo %{version} | cut -d. -f1-3 --output-delimiter="_")
Summary:        Python templating language
Name:           python-mako
Version:        1.2.4
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages/Python
URL:            https://www.makotemplates.org/
Source0:        https://github.com/sqlalchemy/mako/archive/refs/tags/rel_%{version_tag}.tar.gz#/%{name}-%{version}.tar.gz
BuildArch:      noarch

%if %{with_check}
BuildRequires:  python3-pip
%endif

%description
A super-fast templating language that borrows the best ideas from the existing templating languages. Mako is a template library written in Python. It provides a familiar, non-XML syntax which compiles into Python modules for maximum performance. Mako’s syntax and API borrows from the best ideas of many others, including Django templates, Cheetah, Myghty, and Genshi.

%package -n     python3-mako
Summary:        python-mako
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       python3
Requires:       python3-libs
Requires:       python3-pygments
Requires:       python3-markupsafe

%description -n python3-mako
A super-fast templating language that borrows the best ideas from the existing templating languages.
Mako is a template library written in Python. It provides a familiar, non-XML syntax which compiles
into Python modules for maximum performance. Mako’s syntax and API borrows from the best ideas of
many others, including Django templates, Cheetah, Myghty, and Genshi.

%prep
%autosetup -n mako-rel_%{version_tag}

%build
%py3_build

%install
%py3_install
ln -s mako-render %{buildroot}/%{_bindir}/mako-render3

%check
pip3 install tox
tox -e py%{python3_version_nodots}

%files -n python3-mako
%defattr(-,root,root,-)
%license LICENSE
%{python3_sitelib}/*
%{_bindir}/mako-render
%{_bindir}/mako-render3

%changelog
* Fri Oct 27 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.2.4-1
- Auto-upgrade to 1.2.4 - Azure Linux 3.0 - package upgrades

* Wed Sep 28 2022 Nicolas Guibourge <nicolasg@microsoft.com> - 1.2.2-2
- Add missing run time dependencies (python3-pygments and python3-markupsafe)

* Thu Sep 22 2022 Betty Lakes <bettylakes@microsoft.com> - 1.2.2-1
- Update version to 1.2.2 to address CVE-2022-40023

* Tue Mar 15 2022 Muhammad Falak <mwani@microsoft.com> - 1.1.5-2
- Use `py%{python3_version_nodots}` instead of harcoding `py39`

* Wed Feb 16 2022 Muhammad Falak <mwani@microsoft.com> - 1.1.5-1
- Bump version to 1.1.5
- Introduce macro to generate underscored version
- Add an explicit BR on `pip`
- Drop BR on `python3-pytest`
- Use `tox` instead of `pytest` to enable ptest

* Wed Oct 20 2021 Thomas Crain <thcrain@microsoft.com> - 1.0.7-5
- Add license to python3 package
- Remove python2 package
- Lint spec

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.0.7-4
- Added %%license line automatically

* Thu Apr 30 2020 Emre Girgin <mrgirgin@microsoft.com> - 1.0.7-3
- Renaming python-pytest to pytest

* Mon Apr 13 2020 Jon Slobodzian <joslobo@microsoft.com> - 1.0.7-2
- Initial CBL-Mariner import from Photon (license: Apache2).
- Verified license. Removed sha1. Fixed Source0 URL comment. Fixed URL.

* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> - 1.0.7-1
- Update to version 1.0.7

* Thu Jul 06 2017 Xiaolin Li <xiaolinl@vmware.com> - 1.0.6-5
- Fix make check issues.

* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> - 1.0.6-4
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.

* Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> - 1.0.6-3
- Separate the python2 and python3 specific scripts in the bin directory

* Fri Mar 03 2017 Xiaolin Li <xiaolinl@vmware.com> - 1.0.6-2
- Added python3 package.

* Fri Feb 03 2017 Vinay Kulkarni <kulkarniv@vmware.com> - 1.0.6-1
- Initial version of python-mako package for Photon.
