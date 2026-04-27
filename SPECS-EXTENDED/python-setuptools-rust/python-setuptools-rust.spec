Vendor:         Microsoft Corporation
Distribution:   Azure Linux
# RHEL does not have packaged rust libraries
%bcond packaged_rust_libraries %{undefined rhel}
# The integration tests depend on the presence of these libraries
%bcond integration_tests %{with packaged_rust_libraries}
# Regex of integration tests to skip.
#  * html-py-ever requires unpackaged rust crates
%global integration_tests_exc '^(html-py-ever)'
 
Name:           python-setuptools-rust
Version:        1.11.1
Release:        1%{?dist}
Summary:        Setuptools Rust extension plugin
 
License:        MIT
URL:            https://github.com/PyO3/setuptools-rust
Source0:        %{pypi_source setuptools_rust}
 
BuildArch:      noarch
 
BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-wheel
BuildRequires:  %{py3_dist pytest}
%if %{with integration_tests}
BuildRequires:  %{py3_dist cffi}
%endif
 
 
%global _description %{expand:
Setuptools helpers for Rust Python extensions. Compile and distribute Python
extensions written in Rust as easily as if they were written in C.}
 
%description %{_description}
 
 
%package -n     python3-setuptools-rust
Summary:        %{summary}
Requires:       cargo
 
%description -n python3-setuptools-rust %{_description}

%prep
%autosetup -p1 -n setuptools_rust-%{version}

%build
%pyproject_wheel
 
%install
%pyproject_install
%pyproject_save_files setuptools_rust

%check
%pyproject_check_import
# Disable tests that require internet access and/or test Windows functionality
%global test_ignores %{shrink:
        not test_adjusted_local_rust_target_windows_msvc
    and not test_get_lib_name_namespace_package
}
 
%if %{without packaged_rust_libraries}
%global test_ignores %{shrink:%{test_ignores}
    and not test_metadata_contents
    and not test_metadata_cargo_log
}
%endif
 
%pytest tests/ setuptools_rust/ --import-mode importlib -k '%{test_ignores}'
 
%if %{with integration_tests}
export %{py3_test_envvars}
%global _pyproject_wheeldir dist
for example in $(ls examples/ | grep -vE %{integration_tests_exc}); do
    cd "examples/${example}"
    %pyproject_wheel
    if [ -d "tests/" ]; then
        %{python3} -m venv venv --system-site-packages
        ./venv/bin/pip install dist/*.whl
        ./venv/bin/python -Pm pytest tests/
    fi
    cd -
done
%endif

%files -n python3-setuptools-rust -f %{pyproject_files}
%doc README.md CHANGELOG.md

%changelog
* Sat Dec 20 2025 Akarsh Chaudhary <v-akarshc@microsoft.com> - 1.11.1-1
- Initial CBL-Mariner import from Fedora 44 (license: MIT).
- License verified
