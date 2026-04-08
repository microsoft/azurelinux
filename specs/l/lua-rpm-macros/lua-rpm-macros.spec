# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%if 0%{?el8}
# RHEL8's lua-devel ships macros.lua and lua.attr
# skip shipping lua-rpm-macros so we don't conflict
%bcond_with rpm_macros
%else
%bcond_without rpm_macros
%endif

# Versions of lua-devel where the macros were removed
%if 0%{?fedora} >= 33 || 0%{?rhel} >= 9
%global lua_conflict 5.4.0-7
%endif
# TODO add new versions if this gets backported

%if 0%{?fedora} >= 33 || 0%{?rhel} >= 9
# requires RPM >= 4.16
%bcond_without requires_generator
%else
%bcond_with requires_generator
%endif

Name:           lua-rpm-macros
Version:        1
Release:        16%{?dist}
Summary:        The common Lua RPM macros

License:        MIT

# Macros:
Source101:      macros.lua
Source102:      macros.lua-srpm

# RPM requires generator
Source103:      lua.attr

# license text
Source200:      LICENSE

BuildArch:      noarch

# for lua_libdir and lua_pkgdir
Requires:       lua-srpm-macros = %{version}-%{release}

# files were moved from here
%{?lua_conflict:Conflicts: lua-devel < %{lua_conflict}}

%description
This package contains Lua RPM macros.

You should not need to install this package manually as lua-devel requires it.


%package -n lua-srpm-macros
Summary:        RPM macros for building Lua source packages

# For directory structure
Requires:       rpm

%description -n lua-srpm-macros
RPM macros for building Lua source packages.


%prep
%autosetup -c -T
cp -a %{sources} .
%if %{without rpm_macros}
rm macros.lua
%endif


%build


%install
mkdir -p %{buildroot}%{rpmmacrodir}
install -pm 644 macros.* %{buildroot}%{rpmmacrodir}/
%if %{with requires_generator}
install -Dpm 0644 lua.attr %{buildroot}/%{_fileattrsdir}/lua.attr
%endif


%if %{with rpm_macros}
%files
%license LICENSE
%if %{with requires_generator}
%{_fileattrsdir}/lua.attr
%endif
%{rpmmacrodir}/macros.lua
%endif

%files -n lua-srpm-macros
%license LICENSE
%{rpmmacrodir}/macros.lua-srpm


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Feb 12 2024 Nils Philippsen <nils@redhat.com> - 1-13
- Don’t set locale permanently in %%lua_requires (#2263837)

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Sep 01 2020 Miro Hrončok <mhroncok@redhat.com> - 1-3
- Modify several conditionals to support RHEL 9+ and drop ancient Fedora 17
- Add explicit conflict with older lua-devel
- Require rpm, not redhat-rpm-config

* Mon Aug 31 2020 Michel Alexandre Salim <salimma@fedoraproject.org> - 1-2
- Also move lua.attr requires generator

* Fri Aug 28 2020 Michel Alexandre Salim <salimma@fedoraproject.org> - 1-1
- Initial package
