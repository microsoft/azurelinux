Vendor:         Microsoft Corporation
Distribution:   Mariner
%bcond_without check
# https://pagure.io/koji/issue/659
%global debug_package %{nil}

Name:           rust-packaging
Version:        14
Release:        3%{?dist}
Summary:        RPM macros for building Rust packages on various architectures

License:        MIT
URL:            https://pagure.io/fedora-rust/rust2rpm
Source:         https://releases.pagure.org/fedora-rust/rust2rpm/rust2rpm-%{version}.tar.xz

ExclusiveArch:  %{rust_arches}

# gawk is needed for stripping dev-deps in macro
Requires:       gawk
Requires:       python3-rust2rpm = %{version}-%{release}
Requires:       rust-srpm-macros = %{version}
Requires:       rust
Requires:       cargo >= 1.41

%description
The package provides macros for building projects in Rust
on various architectures.

%package     -n python3-rust2rpm
Summary:        Convert Rust packages to RPM
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%if %{with check}
BuildRequires:  python3-pytest
BuildRequires:  cargo
%endif
Requires:       cargo
Provides:       rust2rpm = %{version}-%{release}
%{?python_provide:%python_provide python3-rust2rpm}

%description -n python3-rust2rpm
%{summary}.

%prep
%autosetup -n rust2rpm-%{version} -p1

%build
%py3_build

%install
%py3_install
install -D -p -m 0644 -t %{buildroot}%{_rpmmacrodir} data/macros.rust data/macros.cargo
install -D -p -m 0644 -t %{buildroot}%{_fileattrsdir} data/cargo.attr

%if %{with check}
%check
py.test-%{python3_version} -vv test.py
%endif

%files
%license LICENSE
%{_rpmmacrodir}/macros.rust
%{_rpmmacrodir}/macros.cargo
%{_fileattrsdir}/cargo.attr

%files -n python3-rust2rpm
%license LICENSE
%{_bindir}/rust2rpm
%{_bindir}/cargo-inspector
%{python3_sitelib}/rust2rpm-*.egg-info/
%{python3_sitelib}/rust2rpm/

%changelog
* Fri Oct 29 2021 Muhammad Falak <mwani@microsft.com> - 14-3
- Remove epoch

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 14-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Sat May 02 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 14-1
- Update to 14

* Mon Feb 03 2020 Josh Stone <jistone@redhat.com> - 13-3
- Use 'cargo install --no-track' with cargo 1.41

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Dec 20 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 13-1
- Update to 13

* Fri Dec 13 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 12-2
- Fixup generation of files with no-tilde

* Fri Dec 13 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 12-1
- Update to 12

* Wed Dec 04 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 11-1
- Update to 11

* Sat Sep 07 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 10-6
- Depend on setuptools in runtime

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 10-5
- Rebuilt for Python 3.8

* Sun Aug 18 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 10-4
- Ignore Cargo.lock

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jun 24 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 10-2
- Do not use awk's inplace feature

* Sun Jun 16 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 10-1
- Update to 10

* Sat Jun 08 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 9-3
- Update patches

* Sat Jun 08 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 9-2
- Backport patches from upstream

* Sun May 05 09:18:19 CEST 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 9-1
- Update to 9

* Tue Apr 23 21:18:12 CEST 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 8-1
- Update to 8

* Tue Apr 23 16:17:30 CEST 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 7-1
- Update to 7

* Sun Mar 10 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 6-28
- Install $PWD/Cargo.toml into $REG_DIR/Cargo.toml

* Sun Mar 10 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 6-27
- Restore Cargo.toml.deps into $PWD/Cargo.toml

* Sun Mar 10 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 6-26
- Strip out target dependencies too

* Sun Mar 10 2019 Igor Gnatenko <ignatnekobrain@fedoraproject.org> - 6-25
- Do not error on removing files which do not exist

* Sun Mar 10 2019 Igor Gnatenko <ignatnekobrain@fedoraproject.org> - 6-24
- Escape `\n` properly in macro file

* Sun Mar 10 2019 Igor Gnatenko <ignatnekobrain@fedoraproject.org> - 6-23
- Do not pull optional deps into BRs and trivial fixes

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 6-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jan 26 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 6-21
- Use %%version_no_tilde

* Sat Jan 26 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 6-20
- Trivial fixes for pre-release versions

* Sat Jan 26 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 6-19
- Add support for pre-release versions

* Fri Dec 07 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 6-18
- Set CARGO_HOME

* Sat Nov 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 6-17
- Update patchset

* Sat Nov 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 6-16
- Make package archful

* Fri Nov 02 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 6-15
- Support .rust2rpm.conf

* Wed Oct 31 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 6-14
- Fix syntax error

* Tue Oct 30 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 6-13
- Support multiple dependencies with same name

* Sat Oct 27 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 6-12
- Fix requirements with space

* Fri Oct 26 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 6-11
- Trivial fixes to last patchset

* Fri Oct 26 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 6-10
- Split features into subpackages

* Sun Sep 02 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 6-1
- Update to 6

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 02 2018 Miro Hrončok <mhroncok@redhat.com> - 5-10
- Rebuilt for Python 3.7

* Mon Jul 02 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 5-9
- Rebuilt for Python 3.7

* Fri Jun 22 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 5-8
- Various improvements for %%cargo_* macros

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 5-7
- Rebuilt for Python 3.7

* Wed Feb 21 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 5-6
- Pass %%__cargo_common_opts to %%cargo_install

* Tue Feb 20 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 5-5
- Explicitly require rust/cargo

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 5-3
- Fix syntax error

* Tue Jan 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 5-2
- Remove Cargo.lock

* Mon Jan 08 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 5-1
- Update to 5

* Sat Nov 04 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 4-7
- Add Obsoletes for rust-rpm-macros

* Sat Nov 04 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 4-6
- Use cp instead of install

* Sat Oct 21 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 4-5
- Generate runtime dependencyon cargo for devel subpackages

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Jul 08 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 4-2
- Include license

* Sat Jul 08 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 4-1
- Update to 4

* Fri Jun 23 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3-5
- Explicitly set rustdoc path

* Wed Jun 21 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3-4
- Mageia doesn't have C.UTF-8 lang

* Wed Jun 21 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3-3
- Switch cargo_registry to /usr/share/cargo/registry

* Wed Jun 14 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3-2
- Set C.UTF-8 for cargo inspector where python doesn't do locale coercing

* Tue Jun 13 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3-1
- Initial package
