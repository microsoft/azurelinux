Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global srcname entrypoints
%global sum Discover and load entry points from installed packages

%global python3_wheelname %{srcname}-%{version}-py2.py3-none-any.whl

Name:		python-%{srcname}

# WARNING: Check if an update does not break flake8!
Version:	0.3

Release:	6%{?dist}
Summary:	%{sum}

# license clarification issue opened upstream
# https://github.com/takluyver/entrypoints/issues/10

License:	MIT

URL:		https://entrypoints.readthedocs.io/
Source0:	https://github.com/takluyver/%{srcname}/archive/%{version}/%{srcname}-%{version}.tar.gz#/python-%{srcname}-%{version}.tar.gz

BuildArch:	noarch
BuildRequires:	python3-devel
BuildRequires:	python3-pip
BuildRequires:	python3-flit
BuildRequires:	python3-sphinx

%description
Entry points are a way for Python packages to advertise objects with some
common interface. The most common examples are console_scripts entry points,
which define shell commands by identifying a Python function to run.

The entrypoints module contains functions to find and load entry points.

%package -n python3-%{srcname}
Summary:	%{sum}
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname}
Entry points are a way for Python packages to advertise objects with some
common interface. The most common examples are console_scripts entry points,
which define shell commands by identifying a Python function to run.

The entrypoints module contains functions to find and load entry points.

%package -n python-%{srcname}-doc
Summary:	Documentation for python-entrypoints

%description -n python-%{srcname}-doc
Documentation files for python-entrypoints

%prep
%autosetup -n %{srcname}-%{version}


%build
XDG_CACHE_HOME=$PWD/.cache FLIT_NO_NETWORK=1 flit build --format wheel

pushd doc
make html PYTHON="%{__python3}" SPHINXBUILD=sphinx-build-%{python3_version}
rm _build/html/.buildinfo
popd


%install
%py3_install_wheel %python3_wheelname

%files -n python3-%{srcname}
%doc doc/_build/html
%license LICENSE
%{python3_sitelib}/__pycache__/*
%{python3_sitelib}/*.py
%{python3_sitelib}/%{srcname}-%{version}.dist-info

%files -n python-%{srcname}-doc
%doc doc/_build/html
%license LICENSE

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.3-6
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.3-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Sat Aug 17 2019 Miro Hrončok <mhroncok@redhat.com> - 0.3-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Feb 26 2019 Miro Hrončok <mhroncok@redhat.com> - 0.3-1
- Update to 0.3

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Nov 28 2018 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 0.2.3-10
- Drop py2 sub-packages

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jul 07 2018 Miro Hrončok <mhroncok@redhat.com> - 0.2.3-8
- Add missing dependency on python2-configparser (#1598998)

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.2.3-7
- Fix flit invocation

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.2.3-6
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 16 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.2.3-4
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Wed Jan 03 2018 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 0.2.3-3
- Restore dist-info information (#1530098).

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 13 2017 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 0.2.3-1
- Update to 0.2.3

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jan 31 2017 Michal Cyprian <mcyprian@redhat.com> - 0.2.2-6
- Use python install wheel macros

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.2.2-5
- Rebuild for Python 3.6

* Sun Nov 06 2016 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 0.2.2-4
- Do not own pycache dir

* Mon Oct 03 2016 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 0.2.2-3
- Consolidate two doc subpackages into one

* Sun Oct 02 2016 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 0.2.2-2
- Add -doc subpackages
- Fix source url
- Add license clarification issue URL for reference

* Sat Jul 2 2016 Elliott Sales de Andrade <quantum.analyst@gmail.com> 0.2.2-1
- Initial RPM release
