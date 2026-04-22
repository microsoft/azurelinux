# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           python-aiomysql
Version:        0.2.0
Release: 11%{?dist}
Summary:        MySQL driver for asyncio

License:        MIT
URL:            https://github.com/aio-libs/aiomysql
Source0:        %{url}/archive/v%{version}/aiomysql-%{version}.tar.gz
BuildArch:      noarch

%global _description %{expand:
aiomysql is a “driver” for accessing a MySQL database from the asyncio
(PEP-3156/tulip) framework. It depends on and reuses most parts of PyMySQL .
aiomysql tries to be like awesome aiopg library and preserve same api, look and
feel.}

%description %{_description}

%package -n     python3-aiomysql
Summary:        %{summary}

BuildRequires:  python3-devel

%description -n python3-aiomysql %{_description}

%pyproject_extras_subpkg -n python3-aiomysql sa rsa

%prep
%autosetup -n aiomysql-%{version}
# Upstream has pinned setuptools_scm due to the generated wheel version being wrong:
# https://github.com/aio-libs/aiomysql/commit/fb85893635d7f9c0da3b1ff8c6d0fc436357633a
# We must work with what we have.
sed -r -i 's/"(setuptools_scm.*), <.*"/"\1"/' pyproject.toml
# Furthermore, we don’t need setuptools_scm_git_archive.
sed -r -i '/"setuptools_scm_git_archive/d' pyproject.toml

%generate_buildrequires
%pyproject_buildrequires -x sa,rsa

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files aiomysql

%check
%pyproject_check_import
# Upstream testing is done with a Docker container. Setting up a MySQL server
# for testing might be possible, but not trivial. See the python-asyncmy
# package for inspiration.

%files -n python3-aiomysql -f %{pyproject_files}
# LICENSE is handled by pyproject_files; verify with “rpm -qL -p …”
%doc README.rst

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 0.2.0-10
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 0.2.0-9
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 0.2.0-7
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jun 08 2024 Python Maint <python-maint@redhat.com> - 0.2.0-4
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Sep 22 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 0.1.1-6
- Drop the BuildRequires on python3-setuptools_scm_git_archive

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 15 2023 Python Maint <python-maint@redhat.com> - 0.1.1-4
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Aug 12 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 0.1.1-2
- Add metapackage for “rsa” extra

* Thu Aug 11 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 0.1.1-1
- Update to 0.1.1 (close RHBZ#2105059)
- Switch to pyproject-rpm-macros (mandatory, since there is no more setup.py)

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.20-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 0.0.20-12
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.20-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.20-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.0.20-9
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.20-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sun Sep 20 2020 Fabian Affolter <mail@fabian-affolter.ch> - 0.0.20-7
- Add metapackage sa

* Thu Sep 03 2020 Fabian Affolter <mail@fabian-affolter.ch> - 0.0.20-6
- Fix FTBFS (rhbz#1871591)

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.20-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.0.20-4
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.20-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Jan 07 2020 Fabian Affolter <mail@fabian-affolter.ch> - 0.0.20-2
- Better use of wildcards (rhbz#1787216)

* Sun Dec 29 2019 Fabian Affolter <mail@fabian-affolter.ch> - 0.0.20-1
- Initial package for Fedora
