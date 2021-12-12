Vendor:         Microsoft Corporation
Distribution:   Mariner
# Commit corresponding to the 5.0.0 release of the azure bundle on PyPi
%global commit 2b2cfd46758e7b9d55346f79f05592d7488c1bd0
%global shortcommit %(c=%{commit}; echo ${c:0:7})

%global srcname azure-sdk
%global _description %{expand:This project provides a set of Python packages that make it easy to access
Management (Virtual Machines, ...) or Runtime (ServiceBus using HTTP, Batch,
Monitor) components of Microsoft Azure Complete feature list of this repo and
where to find Python packages not in this repo can be found on our Azure SDK for
Python documentation.}

# Too many tests require an Internet connection
%global _with_tests 0
%global _with_doc 0

Name:           python-%{srcname}
Version:        5.0.0
Release:        2%{?dist}
Summary:        Microsoft Azure SDK for Python

# All packages are licensed under the MIT license, except
# azure-servicemanagement-legacy
License:        MIT and ASL 2.0
URL:            https://github.com/Azure/azure-sdk-for-python
Source0:        %{url}/archive/%{shortcommit}/%{srcname}-%{shortcommit}.tar.gz
# Fix Python requirement versions
Patch0:         %{name}-5.0.0-requirements.patch
# Fix tests
Patch1:         %{name}-5.0.0-tests.patch

BuildRequires:  python3-devel
BuildRequires:  %{py3_dist setuptools}
%if 0%{?_with_tests} || 0%{?_with_doc}
BuildRequires:  %{py3_dist adal}
BuildRequires:  %{py3_dist msal}
BuildRequires:  %{py3_dist msrestazure}
BuildRequires:  %{py3_dist msrest}
BuildRequires:  %{py3_dist opencensus}
BuildRequires:  %{py3_dist uamqp}
%endif
%if 0%{?_with_tests}
BuildRequires:  %{py3_dist aiodns}
BuildRequires:  %{py3_dist aiohttp}
BuildRequires:  %{py3_dist configargparse}
BuildRequires:  %{py3_dist cryptography}
BuildRequires:  %{py3_dist httpretty}
BuildRequires:  %{py3_dist mock}
BuildRequires:  %{py3_dist msal-extensions}
BuildRequires:  %{py3_dist msal}
BuildRequires:  %{py3_dist opencensus-ext-azure}
BuildRequires:  %{py3_dist opencensus-ext-threading}
BuildRequires:  %{py3_dist opentelemetry-api}
BuildRequires:  %{py3_dist opentelemetry-sdk}
BuildRequires:  %{py3_dist pyopenssl}
BuildRequires:  %{py3_dist pytest-asyncio}
BuildRequires:  %{py3_dist pytest-trio}
BuildRequires:  %{py3_dist pytest}
BuildRequires:  %{py3_dist python-dateutil}
BuildRequires:  %{py3_dist requests}
BuildRequires:  %{py3_dist six}
BuildRequires:  %{py3_dist urllib3}
BuildRequires:  %{py3_dist vcrpy}
%endif
%if 0%{?_with_doc}
BuildRequires:  fontpackages-devel
BuildRequires:  %{py3_dist recommonmark}
BuildRequires:  %{py3_dist sphinx}
BuildRequires:  %{py3_dist sphinx-rtd-theme}
%endif
BuildArch:      noarch

%description
%{_description}


%package -n python3-%{srcname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{srcname}}
Provides:       python3-azure-devtools = %{version}-%{release}
Provides:       python3-azure-storage = %{version}-%{release}
Obsoletes:      python3-azure-devtools < 1.0.0-11
Obsoletes:      python3-azure-storage < 2.1.0-4

%description -n python3-%{srcname}
%{_description}


%if 0%{?_with_doc}
%package doc
Summary:        Documentation for %{name}
Requires:       google-roboto-slab-fonts
Requires:       lato-fonts
Requires:       fontawesome-fonts
Requires:       fontawesome-fonts-web

%description doc
This package provides documentation for %{name}.
%endif


%prep
%autosetup -p0 -n %{srcname}-for-python-%{commit}

# Remove bundled egg-info
for i in $(find . -name "setup.py"); do
    rm -rf ${i%/*}/*.egg-info
done


%build
%py3_build

pushd tools/azure-devtools/
%py3_build
popd

%if 0%{?_with_doc}
PYTHONPATH=
for i in $(find . -name "setup.py"); do
    PYTHONPATH+="$PWD/${i%/*}:"
done
export PYTHONPATH=${PYTHONPATH%:}
%make_build -C doc/sphinx/ html
rm doc/sphinx/_build/html/.buildinfo

# Drop bundled web fonts in HTML documentation
pushd ./doc/sphinx/_build/html/_static/fonts/
rm fontawesome-webfont.*
ln -s %{_fontbasedir}/fontawesome/fontawesome-webfont.* .

pushd Lato/
rm *.ttf
for i in Bold BoldItalic Italic Regular; do
    ln -s %{_fontbasedir}/lato/Lato-$i.ttf lato-${i,,}.ttf
done
popd

pushd RobotoSlab/
rm *.ttf
for i in Bold Regular; do
    ln -s %{_fontbasedir}/google-roboto-slab/RobotoSlab-$i.ttf roboto-slab-v7-${i,,}.ttf
done
popd
popd
%endif


%install
%py3_install

pushd tools/azure-devtools/
%py3_install
popd


%check
%if 0%{_with_tests}
export PYTHONPATH=$RPM_BUILD_ROOT/%{python3_sitelib}/:tools/azure-sdk-tools/
for i in $(find sdk/ -name "tests"); do
    pytest-%{python3_version} ${i%/*}
done
%endif


%files -n python3-%{srcname}
%doc CONTRIBUTING.md README.rst
%license LICENSE.txt
%{python3_sitelib}/azure/
%{python3_sitelib}/azure_devtools/
%{python3_sitelib}/azure_*.egg-info/


%if 0%{?_with_doc}
%files doc
%doc doc/sphinx/_build/html/
%license LICENSE.txt
%endif


%changelog
* Mon Feb 08 2021 Joe Schmitt <joschmit@microsoft.com> - 5.0.0-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Turn off docs

* Wed Jul 01 2020 Mohamed El Morabity <melmorabity@fedoraproject.org> - 5.0.0-1
- Update to 5.0.0

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 4.0.0-10
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Wed Aug 28 2019 Mohamed El Morabity <melmorabity@fedoraproject.org> - 4.0.0-9
- Re-enable tests

* Wed Aug 28 2019 Mohamed El Morabity <melmorabity@fedoraproject.org> - 4.0.0-8
- Disable tests to rebuild package without python-azure-storage (for Python 3.8
  rebuild)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 4.0.0-7
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Apr 16 2019 Mohamed El Morabity <melmorabity@fedoraproject.org> - 4.0.0-5
- Enable Python generators
- Enable tests
- Spec cleanup

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Nov 22 2018 Mohamed El Morabity <melmorabity@fedoraproject.org> - 4.0.0-3
- Build documentation with Python 3 on Fedora
- Fix Python 3-only file deployment
- Don't glob everything under the Python sitelib directory

* Mon Aug 06 2018 Mohamed El Morabity <melmorabity@fedoraproject.org> - 4.0.0-2
- Delete all Python 3-only files from the python2 subpackage

* Mon Aug 06 2018 Mohamed El Morabity <melmorabity@fedoraproject.org> - 4.0.0-1
- Update to 4.0.0
