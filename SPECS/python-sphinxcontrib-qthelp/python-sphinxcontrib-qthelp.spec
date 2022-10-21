%global pypi_name sphinxcontrib-qthelp

Summary:        Sphinx extension for QtHelp documents
Name:           python-%{pypi_name}
Version:        1.0.3
Release:        9%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            http://sphinx-doc.org/
Source0:        %{pypi_source}
Patch0:         test_qthelp_path_fix.patch

BuildArch:      noarch

BuildRequires:  gettext
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools

%if %{with_check}
BuildRequires:  python%{python3_pkgversion}-atomicwrites
BuildRequires:  python%{python3_pkgversion}-attrs
BuildRequires:  python%{python3_pkgversion}-docutils
BuildRequires:  python%{python3_pkgversion}-pip
BuildRequires:  python%{python3_pkgversion}-pluggy
BuildRequires:  python%{python3_pkgversion}-pygments
BuildRequires:  python%{python3_pkgversion}-pytest
BuildRequires:  python%{python3_pkgversion}-six
%endif

%description
sphinxcontrib-qthelp is a sphinx extension which outputs QtHelp document.

%package -n     python%{python3_pkgversion}-%{pypi_name}
%{?python_provide:%python_provide python%{python3_pkgversion}-%{pypi_name}}
Summary:        %{summary}

%description -n python%{python3_pkgversion}-%{pypi_name}
sphinxcontrib-qthelp is a sphinx extension which outputs QtHelp document.

%prep
%autosetup -p1 -n %{pypi_name}-%{version}
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
for lang in `find sphinxcontrib/qthelp/locales -maxdepth 1 -mindepth 1 -type d -not -path '*/\.*' -printf "%f "`;
do
  test $lang == __pycache__ && continue
  install -d %{buildroot}%{_datadir}/locale/$lang/LC_MESSAGES
  mv sphinxcontrib/qthelp/locales/$lang/LC_MESSAGES/*.mo %{buildroot}%{_datadir}/locale/$lang/LC_MESSAGES/
done
rm -rf sphinxcontrib/qthelp/locales
ln -s %{_datadir}/locale sphinxcontrib/qthelp/locales
popd

%find_lang sphinxcontrib.qthelp

%check
pip3 install more-itertools Sphinx
%pytest

%files -n python%{python3_pkgversion}-%{pypi_name} -f sphinxcontrib.qthelp.lang
%license LICENSE
%doc README.rst
%{python3_sitelib}/sphinxcontrib/
%{python3_sitelib}/sphinxcontrib_qthelp-%{version}-py%{python3_version}-*.pth
%{python3_sitelib}/sphinxcontrib_qthelp-%{version}-py%{python3_version}.egg-info/

%changelog
* Mon Jun 27 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0.3-9
- Fixing ptests.

* Fri Apr 08 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0.3-8
- Initial CBL-Mariner import from Fedora 36 (license: MIT).
- Cleaning-up spec. License verified.

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jun 03 2021 Python Maint <python-maint@redhat.com> - 1.0.3-5
- Rebuilt for Python 3.10

* Wed Jun 02 2021 Python Maint <python-maint@redhat.com> - 1.0.3-4
- Bootstrap for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jun 01 2020 Charalampos Stratakis <cstratak@redhat.com> - 1.0.3-1
- Update to 1.0.3 (#1808636)

* Sat May 23 2020 Miro Hrončok <mhroncok@redhat.com> - 1.0.2-8
- Rebuilt for Python 3.9

* Fri May 22 2020 Miro Hrončok <mhroncok@redhat.com> - 1.0.2-7
- Bootstrap for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.0.2-5
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Fri Aug 16 2019 Miro Hrončok <mhroncok@redhat.com> - 1.0.2-4
- Rebuilt for Python 3.8

* Thu Aug 15 2019 Miro Hrončok <mhroncok@redhat.com> - 1.0.2-3
- Bootstrap for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Mar 01 2019 Miro Hrončok <mhroncok@redhat.com> - 1.0.2-1
- Initial package
