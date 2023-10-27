%global srcname flit

%global _description %{expand:
Flit is a simple way to put Python packages and modules on PyPI.
Flit only creates packages in the new 'wheel' format. People using older
versions of pip (<1.5) or easy_install will not be able to install them.
Flit packages a single importable module or package at a time, using the import
name as the name on PyPI. All sub-packages and data files within a package are
included automatically.
Flit requires Python 3, but you can use it to distribute modules for Python 2,
so long as they can be imported on Python 3.}

Summary:        Simplified packaging of Python modules
Name:           python-%{srcname}
Version:        3.9.0
Release:        1%{?dist}
# ./flit/log.py under ASL 2.0 license
# ./flit/upload.py under PSF license
License:        BSD AND ASL 2.0 AND Python
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://flit.readthedocs.io/en/latest/
Source0:        https://github.com/takluyver/flit/archive/%{version}/%{srcname}-%{version}.tar.gz
# For the tests
Source1:        https://pypi.org/pypi?%{3}Aaction=list_classifiers#/classifiers.lst

BuildArch:      noarch

BuildRequires:  pyproject-rpm-macros >= 0-40
BuildRequires:  python3-devel
BuildRequires:  python3-flit-core
BuildRequires:  python3-pip
BuildRequires:  python3-tomli

%if %{with_check}
BuildRequires:  python3-atomicwrites
BuildRequires:  python3-attrs
BuildRequires:  python3-docutils
BuildRequires:  python3-pygments
BuildRequires:  sudo
BuildRequires:  which

# Runtime deps, others
BuildRequires:  python3-requests
BuildRequires:  python3-responses

# Test deps that require flit to build, using 'pip3' instead:
# BuildRequires:  python3-testpath
%endif

%description %{_description}

%package -n python3-%{srcname}
%{?python_provide:%python_provide python3-%{srcname}}
Summary:        %{summary}
Requires:       python3-%{srcname}-core = %{version}
# soft dependency: (WARNING) Cannot analyze code. Pygments package not found.
Recommends:     python3-pygments

# https://pypi.python.org/pypi/tornado
# ./flit/log.py unknown version
Provides:       bundled(python3dist(tornado))

%description -n python3-%{srcname} %{_description}

%prep
%autosetup -p1 -n %{srcname}-%{version}

%build
export FLIT_NO_NETWORK=1

export PYTHONPATH=$PWD:$PWD/flit_core
%pyproject_wheel

%install
%pyproject_install

%check
if [[ ! -f "%{_bindir}/python" ]]
then
  ln -s "$(which python3)" "%{_bindir}/python"
fi

pip3 install more-itertools pluggy pytest testpath tomli_w

# flit attempts to download list of classifiers from PyPI, but not if it's cached
# test_invalid_classifier fails without the list
mkdir -p fake_cache/flit
cp %{SOURCE1} fake_cache/flit
export XDG_CACHE_HOME=$PWD/fake_cache

useradd test -G root -m
# Skipping "test_test_writable_dir_win" - Windows-only.
sudo -u test %pytest -k "not test_test_writable_dir_win"

%files -n python3-%{srcname}
%license LICENSE
%doc README.rst
%{python3_sitelib}/flit-*.dist-info/
%{python3_sitelib}/flit/
%{_bindir}/flit

%changelog
* Fri Oct 27 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.9.0-1
- Auto-upgrade to 3.9.0 - Azure Linux 3.0 - package upgrades

* Wed Jul 20 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.7.1-3
- Using pip3 to install 'testpath' for ptest runs.

* Mon Mar 28 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.7.1-2
- Initial CBL-Mariner import from Fedora 36 (license: MIT).
- License verified.

* Wed Mar 16 2022 Charalampos Stratakis <cstratak@redhat.com> - 3.7.1-1
- Update to 3.7.1
- Fixes: rhbz#2057214

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Nov 29 2021 Tomáš Hrnčiar <thrnciar@redhat.com> - 3.5.1-1
- Update to 3.5.1

* Tue Oct 26 2021 Tomáš Hrnčiar <thrnciar@redhat.com> - 3.4.0-1
- Update to 3.4.0

* Wed Aug 04 2021 Tomas Hrnciar <thrnciar@redhat.com> - 3.3.0-1
- Update to 3.3.0
- Fixes: rhbz#1988744

* Tue Jul 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.0-5
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 3.2.0-4
- Rebuilt for Python 3.10

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 3.2.0-3
- Bootstrap for Python 3.10

* Sat May 29 2021 Miro Hrončok <mhroncok@redhat.com> - 3.2.0-2
- Adapt to pyproject-rpm-macros 0-40+

* Tue Mar 30 2021 Karolina Surma <ksurma@redhat.com> - 3.2.0-1
- Update to 3.2.0
Resolves: rhbz#1940399
- Remove tests from the flip_core package

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Nov 19 2020 Miro Hrončok <mhroncok@redhat.com> - 3.0.0-2
- Replace deprecated pytoml with toml

* Mon Sep 21 2020 Tomas Hrnciar <thrnciar@redhat.com> - 3.0.0-1
- Update to 3.0.0

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun May 24 2020 Miro Hrončok <mhroncok@redhat.com> - 2.3.0-3
- Rebuilt for Python 3.9

* Sun May 24 2020 Miro Hrončok <mhroncok@redhat.com> - 2.3.0-2
- Bootstrap for Python 3.9

* Mon May 11 2020 Tomas Hrnciar <thrnciar@redhat.com> - 2.3.0-1
- Update to 2.3.0

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Jan 20 2020 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 2.2.0-1
- Update to 2.2.0

* Sat Dec 14 2019 Miro Hrončok <mhroncok@redhat.com> - 2.1.0-2
- Properly package flit-core and restore /usr/bin/flit (#1783610)

* Tue Dec 03 2019 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 2.1.0-1
- Update to 2.1.0

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.3-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Sat Aug 17 2019 Miro Hrončok <mhroncok@redhat.com> - 1.3-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 10 2019 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 1.3-1
- Update to 1.3

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Sep 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.1-1
- Update to 1.1

* Sat Aug 18 2018 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 1.0-4
- Drop pypandoc as requires

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.0-2
- Rebuilt for Python 3.7

* Sun Apr 08 2018 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 1.0-1
- Update to 1.0

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 09 2018 Miro Hrončok <mhroncok@redhat.com> - 0.13-2
- Recommend Pygments

* Sat Dec 23 2017 Mukundan Ragavan <nonamedotc@fedoraproject.org> -  0.13-1
- Update to 0.13

* Thu Nov 16 2017 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 0.12.2-1
- Update to 0.12.2

* Wed Nov 08 2017 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 0.12.1-1
- Update to 0.12.1

* Mon Nov 06 2017 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 0.12-2
- Add pytoml as dependency

* Sun Nov 05 2017 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 0.12-1
- Update to 0.12
- Add pytoml as buildrequires

* Mon Aug 14 2017 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 0.11.4-1
- Update to 0.11.4
- Drop file-encoding patch (fixed upstream)

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 13 2017 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 0.11.1-1
- Update to 0.11.1

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan 23 2017 Michal Cyprian <mcyprian@redhat.com> - 0.9-5
- Use python install wheel macro

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.9-4
- Rebuild for Python 3.6

* Thu Sep 29 2016 Mukundan Ragavan <nonamedotc@gmail.com> - 0.9-3
- Updated spec file with license comments and provides

* Sat Sep 24 2016 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 0.9-2
- spec file cleanup

* Sat Jul 2 2016 Elliott Sales de Andrade <quantum.analyst@gmail.com> 0.9-1
- Initial RPM release
