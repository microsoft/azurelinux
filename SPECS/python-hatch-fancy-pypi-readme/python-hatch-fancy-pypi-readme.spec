Name:           python-hatch-fancy-pypi-readme
Version:        24.1.0
Release:        4%{?dist}
Summary:        Hatch plugin for writing fancy PyPI readmes

License:        MIT
URL:            https://github.com/hynek/hatch-fancy-pypi-readme
Source0:        https://files.pythonhosted.org/packages/b4/c2/c9094283a07dd96c5a8f7a5f1910259d40d2e29223b95dd875a6ca13b58f/hatch_fancy_pypi_readme-%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-hatchling
BuildRequires:  python3-hatch-vcs
BuildRequires:  python3-packaging
BuildRequires:  python3-pathspec
BuildRequires:  python3-pytest
BuildRequires:  python3-pip
BuildRequires:  python3-setuptools
BuildRequires:  python3-setuptools_scm
BuildRequires:  python3-trove-classifiers
BuildRequires:  python3-wheel

%global common_description %{expand:
This provides a Hatch metadata plugin for everyone who cares about the
first impression of their project's PyPI landing page. It allows you to
define your PyPI project description in terms of concatenated fragments
that are based on static strings, files, and most importantly: parts of
files defined using cut-off points or regular expressions.}

%description %{common_description}


%package -n python3-hatch-fancy-pypi-readme
Summary:        %{summary}

%description -n python3-hatch-fancy-pypi-readme %{common_description}


%prep
%autosetup -n hatch_fancy_pypi_readme-%{version} -p1

# https://github.com/hynek/hatch-fancy-pypi-readme/commit/6c06d7244183c5b71aed905c9950e3206e5f0a9e
# Drop unwanted build dependencies that upstream already dropped
sed -i 's/ \"pytest-icdiff\", \"coverage\[toml\]\", //g' pyproject.toml

%generate_buildrequires
%pyproject_buildrequires %{?!rhel:-x tests}

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files hatch_fancy_pypi_readme

%check
pip3 install iniconfig
%pyproject_check_import
# test_end_to_end need network access
%pytest -v -k "not test_end_to_end"

%files -n python3-hatch-fancy-pypi-readme -f %{pyproject_files}
%license LICENSE.txt
%license %{python3_sitelib}/hatch_fancy_pypi_readme-%{version}.dist-info/licenses/LICENSE.txt
%doc README.md
%doc %{python3_sitelib}/hatch_fancy_pypi_readme-%{version}.dist-info/licenses/AUTHORS.md
%{_bindir}/hatch-fancy-pypi-readme

%changelog
* Tue Mar 05 2024 Osama Esmail <osamaesmail@microsoft.com> - 24.1.0-4
- Initial CBL-Mariner import from Fedora 40 (license: MIT).
- Remove toml.
- License verified.

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 24.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 24.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jan 11 2024 Parag Nemade <pnemade AT redhat DOT com> - 24.1.0-1
- Update to 24.1.0 version (#2256321)

* Fri Sep 08 2023 Maxwell G <maxwell@gtmx.me> - 23.1.0-1
- Update to 23.1.0.

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 22.3.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 15 2023 Python Maint <python-maint@redhat.com> - 22.3.0-5
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 22.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Sep 19 2022 Parag Nemade <pnemade AT redhat DOT com> - 22.3.0-3
- Updated as per suggestions given for this package review (#2123618)

* Mon Sep 05 2022 Parag Nemade <pnemade AT redhat DOT com> - 22.3.0-2
- Updated as per suggestions given for this package review (#2123618)

* Fri Sep 02 2022 Parag Nemade <pnemade AT redhat DOT com> - 22.3.0-1
- Initial release