# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# The documentation and tests need furo.  But to build furo at all, we need
# this package.
%bcond bootstrap 0

%global prerel  beta2
%global giturl  https://github.com/pradyunsg/sphinx-basic-ng

Name:           python-sphinx-basic-ng
Version:        1.0.0
Release: 1.17.%{prerel}%{?dist}
Summary:        Modernized skeleton for Sphinx themes

License:        MIT
URL:            https://sphinx-basic-ng.readthedocs.io/
VCS:            git:%{giturl}.git
Source:         %{giturl}/archive/%{version}.%{prerel}/sphinx-basic-ng-%{version}.%{prerel}.tar.gz

BuildArch:      noarch

BuildRequires:  python3-devel

%if %{without bootstrap}
BuildRequires:  python-sphinx-doc
BuildRequires:  python3-docs
%endif

%global _description A modernized skeleton for Sphinx themes.

%description
%_description

%package     -n python3-sphinx-basic-ng
Summary:        Modernized skeleton for Sphinx themes

%description -n python3-sphinx-basic-ng
%_description

%if %{without bootstrap}
%package        doc
Summary:        Documentation for %{name}
# This project is MIT.  Other files bundled with the documentation have the
# following licenses:
# _static/_sphinx_javascript_frameworks_compat.js: BSD-2-Clause
# _static/basic.css: BSD-2-Clause
# _static/check-solid.svg: MIT
# _static/clipboard.min.js: MIT
# _static/copy-button.svg: MIT
# _static/copybutton.css: MIT
# _static/copybutton.js: MIT
# _static/copybutton_funcs.js: MIT
# _static/doctools.js: BSD-2-Clause
# _static/documentation_options.js: BSD-2-Clause
# _static/file.png: BSD-2-Clause
# _static/jquery*.js: MIT
# _static/language_data.js: BSD-2-Clause
# _static/minus.png: BSD-2-Clause
# _static/plus.png: BSD-2-Clause
# _static/scripts/furo*: MIT
# _static/searchtools.js: BSD-2-Clause
# _static/styles/furo*: MIT
# _static/tabs.css: MIT
# _static/tabs.js: MIT
# _static/underscore*.js: MIT
# genindex.html: BSD-2-Clause
# search.html: BSD-2-Clause
# searchindex.js: BSD-2-Clause
License:        MIT AND BSD-2-Clause

%description    doc
Documentation for %{name}.
%endif

%prep
%autosetup -n sphinx-basic-ng-%{version}.%{prerel}

%conf
# Use local objects.inv for intersphinx
sed -e 's|\("https://docs\.python\.org/3", \)None|\1"%{_docdir}/python3-docs/html/objects.inv"|' \
    -e 's|\("https://www\.sphinx-doc\.org/en/master", \)None|\1"%{_docdir}/python-sphinx-doc/html/objects.inv"|' \
    -i docs/conf.py

%generate_buildrequires
%pyproject_buildrequires %{!?with_bootstrap:-x docs}

%build
%pyproject_wheel

%if %{without bootstrap}
# Build documentation
PYTHONPATH=$PWD/src sphinx-build -b html docs html
rm -rf html/{.buildinfo,.doctrees}
%endif

%install
%pyproject_install
%pyproject_save_files -l sphinx_basic_ng

%check
# The nox tests require network access, so we do not run them
%pyproject_check_import

%files -n python3-sphinx-basic-ng -f %{pyproject_files}
%doc README.md

%if %{without bootstrap}
%files doc
%doc html
%license LICENSE
%endif

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 1.0.0-0.17.beta2
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 1.0.0-0.16.beta2
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-0.15.beta2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jun 04 2025 Python Maint <python-maint@redhat.com> - 1.0.0-0.14.beta2
- Rebuilt for Python 3.14

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 1.0.0-0.13.beta2
- Bootstrap for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-0.12.beta2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-0.11.beta2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Jun 09 2024 Python Maint <python-maint@redhat.com> - 1.0.0-0.10.beta2
- Rebuilt for Python 3.13

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 1.0.0-0.9.beta2
- Bootstrap for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-0.8.beta2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-0.7.beta2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-0.6.beta2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 18 2023 Jerry James <loganjerry@gmail.com> - 1.0.0-0.5.beta2
- Version 1.0.0.beta2

* Sun Jul 02 2023 Python Maint <python-maint@redhat.com> - 1.0.0-0.4.beta1
- Rebuilt for Python 3.12

* Wed Jun 14 2023 Python Maint <python-maint@redhat.com> - 1.0.0-0.3.beta1
- Bootstrap for Python 3.12

* Thu Feb 23 2023 Jerry James <loganjerry@gmail.com> - 1.0.0-0.2.beta1
- Dynamically generate BuildRequires

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-0.2.beta1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Dec 13 2022 Jerry James <loganjerry@gmail.com> - 1.0.0-0.1.beta1
- Verify that license tags are valid SPDX

* Fri Sep 30 2022 Jerry James <loganjerry@gmail.com> - 1.0.0-0.1.beta1
- Version 1.0.0.beta1
- Drop upstreamed -sphinx patch

* Thu Aug 25 2022 Jerry James <loganjerry@gmail.com> - 0.0.1-0.1.a12
- Initial RPM
