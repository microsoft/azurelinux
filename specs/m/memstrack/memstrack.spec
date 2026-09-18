# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# vim: syntax=spec
%global gitcommit 560379ee67db48382ccc3ab3de866e239fd74ca8
%global gitshortcommit %(c=%{gitcommit}; echo ${c:0:7})

Name:           memstrack
Version:        0.2.5
Release:        7%{?dist}
Summary:        A memory allocation tracer, like a hot spot analyzer for memory allocation
License:        GPL-3.0-only
URL:            https://github.com/ryncsn/memstrack
VCS:            git+git@github.com:ryncsn/memstrack.git
BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  ncurses-devel

Source:         https://github.com/ryncsn/memstrack/archive/%{gitcommit}/memstrack-%{gitshortcommit}.tar.gz

%description
A memory allocation tracer, like a hot spot analyzer for memory allocation

%prep
%setup -q -n memstrack-%{gitcommit}

%build
%{set_build_flags}
%{make_build}

%install
mkdir -p %{buildroot}/%{_bindir}
install -p -m 755 memstrack %{buildroot}/%{_bindir}

%files
%doc README.md
%license LICENSE
%{_bindir}/memstrack

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jan 28 2023 Kairui Song <ryncsn@gmail.com> - 0.2.5-1
- Update to upstream latest release.
- Fix crash when wrong reporter type is used.
- Fix a few tracing error.

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Dec 09 2021 Kairui Song <ryncsn@gmail.com> - 0.2.4-1
- Update to upstream latest release, fix minor TUI bugs.

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sat Jul 17 2021 Kairui Song <kasong@redhat.com> - 0.2.3-1
- Update to upstream latest release

* Mon Feb 08 2021 Kairui Song <kasong@redhat.com> - 0.2.2-1
- Update to upstream latest release

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jan 11 2021 Timm Bäder <tbaeder@redhat.com> - 0.1.12-2
- Use %%make_build macro
  https://docs.fedoraproject.org/en-US/packaging-guidelines/#_parallel_make

* Sun Aug 30 2020 Kairui Song <kasong@redhat.com> - 0.1.12-1
- Update to upstream latest release

* Thu Jul 30 2020 Kairui Song <kasong@redhat.com> - 0.1.9-1
- Update to upstream latest release

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat Jun 06 2020 Kairui Song <kasong@redhat.com> - 0.1.8-1
- Update to upstream latest release

* Sat May 30 2020 Kairui Song <ryncsn@gmail.com> - 0.1.5-1
- Update to upstream latest release

* Tue Apr 21 2020 Kairui Song <ryncsn@gmail.com> - 0.1.2-1
- Update to upstream latest release

* Sun Mar 15 2020 Kairui Song <ryncsn@gmail.com> - 0-1.20200310gitee02de2
- First release
