%global pypi_name_prefix sphinxcontrib
%global pypi_name_suffix serializinghtml
%global pypi_name %{pypi_name_prefix}-%{pypi_name_suffix}
%global pypi_name_underscore %{pypi_name_prefix}_%{pypi_name_suffix}

Summary:        Sphinx extension for serialized HTML
Name:           python-%{pypi_name}
Version:        1.1.10
Release:        1%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://www.sphinx-doc.org/en/master/
Source0:        https://files.pythonhosted.org/packages/54/13/8dd7a7ed9c58e16e20c7f4ce8e4cb6943eb580955236d0c0d00079a73c49/%{pypi_name_underscore}-%{version}.tar.gz#/%{pypi_name}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  gettext
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
BuildRequires:  python%{python3_pkgversion}-pip
BuildRequires:  python%{python3_pkgversion}-wheel
BuildRequires:  python-flit-core

%if %{with_check}
BuildRequires:  python%{python3_pkgversion}-pytest
%endif

%description
sphinxcontrib-serializinghtml is a sphinx extension which outputs "serialized"
HTML files (json and pickle).

%package -n     python%{python3_pkgversion}-%{pypi_name}
%{?python_provide:%python_provide python3-%{pypi_name}}
Summary:        %{summary}

%description -n python%{python3_pkgversion}-%{pypi_name}
sphinxcontrib-serializinghtml is a sphinx extension which outputs "serialized"
HTML files (json and pickle).

%generate_buildrequires
%pyproject_buildrequires -x test

%prep
%autosetup -n %{pypi_name_underscore}-%{version}
find -name '*.mo' -delete

%build
for po in $(find -name '*.po'); do
  msgfmt --output-file=${po%.po}.mo ${po}
done
%pyproject_wheel

%install
%pyproject_install

# Move language files to /usr/share
pushd %{buildroot}%{python3_sitelib}
for lang in `find sphinxcontrib/serializinghtml/locales -maxdepth 1 -mindepth 1 -type d -not -path '*/\.*' -printf "%f "`;
do
  test $lang == __pycache__ && continue
  install -d %{buildroot}%{_datadir}/locale/$lang/LC_MESSAGES
  mv sphinxcontrib/serializinghtml/locales/$lang/LC_MESSAGES/*.mo %{buildroot}%{_datadir}/locale/$lang/LC_MESSAGES/
done
rm -rf sphinxcontrib/serializinghtml/locales
ln -s %{_datadir}/locale sphinxcontrib/serializinghtml/locales
popd

%find_lang sphinxcontrib.serializinghtml

%check
pip3 install sphinx exceptiongroup iniconfig tomli
%pytest

%files -n python3-%{pypi_name} -f sphinxcontrib.serializinghtml.lang
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{pypi_name_prefix}/	
%{python3_sitelib}/%{pypi_name_underscore}-%{version}.dist-info/

%changelog
* Wed Feb 21 2024 Amrita Kohli <amritakohli@microsoft.com> - 1.1.10-1
- Upgrade to latest version.

* Thu Apr 07 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.1.5-5
- Installing 'python3-sphinx' through pip3 during tests to remove cyclic dependency.

* Sun Mar 27 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.1.5-4
- Initial CBL-Mariner import from Fedora 36 (license: MIT).
- License verified.

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 11 2021 Karolina Surma <ksurma@redhat.com> - 1.1.5-1
- Update to 1.1.5
Resolves: rhbz#1963359

* Thu Jun 03 2021 Python Maint <python-maint@redhat.com> - 1.1.4-5
- Rebuilt for Python 3.10

* Wed Jun 02 2021 Python Maint <python-maint@redhat.com> - 1.1.4-4
- Bootstrap for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jun 01 2020 Charalampos Stratakis <cstratak@redhat.com> - 1.1.4-1
- Update to 1.1.4 (#1808637)

* Sat May 23 2020 Miro Hrončok <mhroncok@redhat.com> - 1.1.3-8
- Rebuilt for Python 3.9

* Fri May 22 2020 Miro Hrončok <mhroncok@redhat.com> - 1.1.3-7
- Bootstrap for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.1.3-5
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Fri Aug 16 2019 Miro Hrončok <mhroncok@redhat.com> - 1.1.3-4
- Rebuilt for Python 3.8

* Thu Aug 15 2019 Miro Hrončok <mhroncok@redhat.com> - 1.1.3-3
- Bootstrap for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon May 20 2019 Miro Hrončok <mhroncok@redhat.com> - 1.1.3-1
- Update to 1.1.3 (#1697444)

* Mon Mar 04 2019 Miro Hrončok <mhroncok@redhat.com> - 1.1.1-1
- Initial package.
