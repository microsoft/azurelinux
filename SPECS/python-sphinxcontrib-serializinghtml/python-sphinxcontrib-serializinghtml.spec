%global pypi_name sphinxcontrib-serializinghtml

Summary:        Sphinx extension for serialized HTML
Name:           python-%{pypi_name}
Version:        1.1.5
Release:        5%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://www.sphinx-doc.org/en/master/
Source0:        https://files.pythonhosted.org/packages/b5/72/835d6fadb9e5d02304cf39b18f93d227cd93abd3c41ebf58e6853eeb1455/%{pypi_name}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  gettext
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

%if %{with_check}
BuildRequires:  python3-pip
BuildRequires:  python3-pytest
%endif

%description
sphinxcontrib-serializinghtml is a sphinx extension which outputs "serialized"
HTML files (json and pickle).

%package -n     python3-%{pypi_name}
%{?python_provide:%python_provide python3-%{pypi_name}}
Summary:        %{summary}

%description -n python3-%{pypi_name}
sphinxcontrib-serializinghtml is a sphinx extension which outputs "serialized"
HTML files (json and pickle).

%prep
%autosetup -n %{pypi_name}-%{version}
find -name '*.mo' -delete

%build
for po in $(find -name '*.po'); do
  msgfmt --output-file=${po%.po}.mo ${po}
done
%py3_build

%install
%py3_install

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
pip3 install Sphinx
%pytest

%files -n python3-%{pypi_name} -f sphinxcontrib.serializinghtml.lang
%license LICENSE
%doc README.rst
%{python3_sitelib}/sphinxcontrib/
%{python3_sitelib}/sphinxcontrib_serializinghtml-%{version}-py%{python3_version}-*.pth
%{python3_sitelib}/sphinxcontrib_serializinghtml-%{version}-py%{python3_version}.egg-info/

%changelog
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
