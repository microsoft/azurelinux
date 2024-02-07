Summary:        Core utilities for Python packages
Name:           python-packaging
Version:        23.2
Release:        1%{?dist}
License:        BSD OR ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Development/Languages/Python
URL:            https://pypi.python.org/pypi/packaging
Source0:        https://github.com/pypa/packaging/archive/refs/tags/%{version}.tar.gz#/packaging-%{version}.tar.gz

BuildArch:      noarch
 
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
BuildRequires:  python3-pip
BuildRequires:  python3-wheel

BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  pyproject-rpm-macros
BuildRequires:  unzip
 
%if %{with bootstrap}
BuildRequires:  python%{python3_pkgversion}-flit-core
%endif
 
# Upstream uses nox for testing, we specify the test deps manually as well.
%if %{with tests}
BuildRequires:  python%{python3_pkgversion}-pytest
BuildRequires:  python%{python3_pkgversion}-pretend
%endif
%if %{with docs}
BuildRequires:  python%{python3_pkgversion}-sphinx
%endif
 
 
%global _description %{expand:
python-packaging provides core utilities for Python packages like utilities for
dealing with versions, specifiers, markers etc.}
 
%description %_description
 
%package -n python%{python3_pkgversion}-%{pypi_name}
Summary:        %{summary}
 
%if %{with bootstrap}
Provides:       python%{python3_pkgversion}dist(packaging) = %{version}
Provides:       python%{python3_version}dist(packaging) = %{version}
Requires:       python(abi) = %{python3_version}
%endif
 
%description -n python%{python3_pkgversion}-%{pypi_name}  %_description
 
%if %{with docs}
%package -n python-%{pypi_name}-doc
Summary:        python-packaging documentation
 
%description -n python-%{pypi_name}-doc
Documentation for python-packaging
%endif
 
 
%prep
%autosetup -p1 -n %{pypi_name}-%{version}
 
# Do not use furo as HTML theme in docs
# furo is not available in Fedora
sed -i '/html_theme = "furo"/d' docs/conf.py
 
%if %{without bootstrap}
%generate_buildrequires
%pyproject_buildrequires -r
%endif
 
 
%build
%if %{with bootstrap}
%{python3} -m flit_core.wheel
%else
%pyproject_wheel
%endif
 
%if %{with docs}
# generate html docs
sphinx-build-3 docs html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}
# Do not bundle fonts
rm -rf html/_static/fonts/
%endif
 
 
%install
%if %{with bootstrap}
mkdir -p %{buildroot}%{python3_sitelib}
unzip dist/packaging-%{version}-py3-none-any.whl -d %{buildroot}%{python3_sitelib} -x packaging-%{version}.dist-info/RECORD
echo '%{python3_sitelib}/packaging*' > %{pyproject_files}
%else
%pyproject_install
%pyproject_save_files %{pypi_name}
%endif
 
 
%check
%{!?with_bootstrap:%pyproject_check_import}
%if %{with tests}
%pytest
%endif
 
 
%files -n python%{python3_pkgversion}-%{pypi_name} -f %{pyproject_files}
%license LICENSE LICENSE.APACHE LICENSE.BSD
%doc README.rst CHANGELOG.rst CONTRIBUTING.rst
 
 
%if %{with docs}
%files -n python-%{pypi_name}-doc
%doc html
%license LICENSE LICENSE.APACHE LICENSE.BSD
%endif
 
%changelog
* Wed Feb 07 2022 Brian Fjeldstad <bfjelds@microsoft.com> - 23.2-1
  Upgrade to 23.2-1

* Tue Feb 01 2022 Thomas Crain <thcrain@microsoft.com> - 21.3-1
- Upgrade to latest upstream version
- Use github release source instead of pypi source

* Fri Dec 03 2021 Thomas Crain <thcrain@microsoft.com> - 17.1-8
- Replace easy_install usage with pip in %%check sections

* Wed Oct 20 2021 Thomas Crain <thcrain@microsoft.com> - 17.1-7
- Add license to python3 package
- Remove python2 package
- Lint spec
- License verified

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 17.1-6
- Added %%license line automatically

* Fri Apr 17 2020 Nicolas Ontiveros <niontive@microsoft.com> - 17.1-5
- Use pyparsing in Requres and BR.

* Mon Apr 13 2020 Nick Samson <nisamson@microsoft.com> - 17.1-4
- Updated Source0, removed %%define sha1, confirmed license.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 17.1-3
- Initial CBL-Mariner import from Photon (license: Apache2).

* Fri Dec 07 2018 Tapas Kundu <tkundu@vmware.com> - 17.1-2
- Fix makecheck

* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> - 17.1-1
- Update to version 17.1

* Wed Jul 26 2017 Divya Thaluru <dthaluru@vmware.com> - 16.8-4
- Fixed rpm check errors
- Fixed runtime dependencies

* Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 16.8-3
- Fix arch

* Wed Apr 05 2017 Sarah Choi <sarahc@vmware.com> - 16.8-2
- Remove python-setuptools from BuildRequires

* Tue Apr 04 2017 Xiaolin Li <xiaolinl@vmware.com> - 16.8-1
- Initial packaging for Photon
