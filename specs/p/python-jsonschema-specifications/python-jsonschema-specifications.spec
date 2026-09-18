# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global pypi_name jsonschema-specifications
%global pkg_name jsonschema_specifications
%global with_tests 1

# Some documentation reqs are not yet packaged for EPEL
%if ! 0%{?rhel}
%global with_doc 1
%endif

%global common_description %{expand:
JSON support files from the JSON Schema Specifications (metaschemas,
vocabularies, etc.), packaged for runtime access from Python as a
referencing-based Schema Registry.}

Name:           python-%{pypi_name}
Summary:        JSON Schema meta-schemas and vocabularies, exposed as a Registry
Version:        2024.10.1
Release:        6%{?dist}
License:        MIT
URL:            https://github.com/python-jsonschema/jsonschema-specifications
Source0:        %{pypi_source %{pkg_name}}

BuildArch:      noarch
BuildRequires:  python3-devel

%description %{common_description}


%package -n     python3-%{pypi_name}
Summary:        %{summary}
%description -n python3-%{pypi_name} %{common_description}

%if 0%{?with_tests}
%package  -n    python3-%{pypi_name}-tests
Summary:        Tests for the JSON Schema specifications
Requires:       python3-%{pypi_name} = %{version}-%{release}

BuildRequires:  python3dist(pytest)
Requires:       python3dist(pytest)

%description -n python3-%{pypi_name}-tests
Tests for the JSON Schema specifications
%endif

%if 0%{?with_doc}
%package  -n    python3-%{pypi_name}-doc
Summary:        Documentation for the JSON Schema specifications
Group:          Documentation

BuildRequires:  python3dist(sphinx)
BuildRequires:  python3dist(sphinx-copybutton)
BuildRequires:  python3dist(sphinxext-opengraph)
BuildRequires:  python3dist(sphinxcontrib-spelling)

%description -n python3-%{pypi_name}-doc
Documentation for the JSON Schema specifications
%endif


%prep
%autosetup -n %{pkg_name}-%{version}

sed -i "/^file:.*/d" docs/requirements.in
sed -i "/^pygments-github-lexers/d" docs/requirements.in
sed -i "s/^pyenchant.*/pyenchant/" docs/requirements.in

%generate_buildrequires
%if 0%{?with_doc}
%pyproject_buildrequires docs/requirements.in
%else
%pyproject_buildrequires
%endif

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files %{pkg_name}

%if 0%{?with_doc}
# generate html docs
export PYTHONPATH="%{buildroot}/%{python3_sitelib}"
sphinx-build-3 -b html docs docs/build/html
# remove the sphinx-build-3 leftovers
rm -rf docs/build/html/.{doctrees,buildinfo}
%endif

%if 0%{?with_tests}
%check
%pytest
%endif

%files -n python3-%{pypi_name} -f %{pyproject_files}
%license COPYING
%doc README.rst
%exclude %{python3_sitelib}/%{pkg_name}/tests

%if 0%{?with_tests}
%files -n python3-%{pypi_name}-tests
%license COPYING
%{python3_sitelib}/%{pkg_name}/tests
%endif

%if 0%{?with_doc}
%files -n python3-%{pypi_name}-doc
%doc docs/build/html
%endif

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 2024.10.1-6
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 2024.10.1-5
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2024.10.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jun 04 2025 Python Maint <python-maint@redhat.com> - 2024.10.1-3
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2024.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jan 15 2025 Joel Capitao <jcapitao@redhat.com> - 2024.10.1-1
- Update to 2024.10.1 (rhbz#2255833)

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2023.11.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Jun 09 2024 Python Maint <python-maint@redhat.com> - 2023.11.2-5
- Rebuilt for Python 3.13

* Sat Jun 08 2024 Python Maint <python-maint@redhat.com> - 2023.11.2-4
- Bootstrap for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2023.11.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2023.11.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Nov 30 2023 Joel Capitao <jcapitao@redhat.com> - 2023.11.2-1
- Update to 2023.11.2 (rhbz#2252278)

* Mon Nov 20 2023 Joel Capitao <jcapitao@redhat.com> - 2023.11.1-1
- Update to 2023.11.1 (rhbz#2249692)

* Mon Aug 07 2023 Joel Capitao <jcapitao@redhat.com> - 2023.7.1-1
- Initial package.

