%bcond_without rpm_macros

%global lua_conflict 5.4.0-7

# requires RPM >= 4.16
%bcond_without requires_generator

Name:           lua-rpm-macros
Version:        1
Release:        6%{?dist}
Summary:        The common Lua RPM macros
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://src.stg.fedoraproject.org/rpms/lua-rpm-macros
Group:          Development/Tools
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
* Wed Jan 19 2022 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 1-6
- Initial CBL-Mariner import from Fedora 35 (license: MIT)
- License verified
- Added URL and Group
- Removed Fedora distro version specific checks.

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
