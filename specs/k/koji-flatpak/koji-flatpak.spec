# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global project_version 0.7
%global flatpak_module_tools_min_version 1.1

Name:           koji-flatpak
Version:        %{project_version}
Release: 6%{?dist}
Summary:        Koji plugins for building Flatpaks

License:        LGPL-2.1-only
URL:            https://pagure.io/koji-flatpak
Source0:        https://releases.pagure.org/koji-flatpak/koji-flatpak-%{project_version}.tar.gz

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools


%description
koji-flatpak adds the ability to build Flatpak containers to Koji. It has
plugins for the XMLRPC hub, the builder nodes, and for the Koji command
line.


%package common
Summary: Common files for Flatpak plugins for Koji

%description common
Common files for Flatpak plugins for Koji.


%package hub
Summary: Flatpak plugin for the Koji XMLRPC hub
Requires: %{name}-common = %{version}-%{release}
Requires: koji-hub

%description hub
koji-flatpak adds the ability to build Flatpak containers to Koji.
This is the plugin for the Koji XMLRPC hub.


%package builder
Summary: Flatpak plugin for the Koji builder nodes
Requires: %{name}-common = %{version}-%{release}
Requires: koji-builder
Requires: python3-flatpak-module-tools >= %{flatpak_module_tools_min_version}
Requires: skopeo

%description -n %{name}-builder
koji-flatpak adds the ability to build Flatpak containers to Koji.
This is the Flatpak plugin for the Koji builder nodes.


%package cli
Summary: Flatpak plugin for the Koji command line
Requires: %{name}-common = %{version}-%{release}
Requires: koji

%description cli
koji-flatpak adds the ability to build Flatpak containers to Koji.
This is the Flatpak plugin for the Koji command line.


%prep
%autosetup -p1 -n %{name}-%{project_version}


%build


%install
install -d %{buildroot}/%{_prefix}/lib/koji-hub-plugins
install -p -m 0755 koji_flatpak/plugins/flatpak_hub_plugin.py %{buildroot}/%{_prefix}/lib/koji-hub-plugins/flatpak.py
%py_byte_compile %{__python3} %{buildroot}/%{_prefix}/lib/koji-hub-plugins/flatpak.py

install -d %{buildroot}/%{_prefix}/lib/koji-builder-plugins
install -p -m 0755 koji_flatpak/plugins/flatpak_builder_plugin.py %{buildroot}/%{_prefix}/lib/koji-builder-plugins/flatpak.py
%py_byte_compile %{__python3} %{buildroot}/%{_prefix}/lib/koji-builder-plugins/flatpak.py

install -d %{buildroot}%{python3_sitelib}/koji_cli_plugins
install -p -m 0644 koji_flatpak/plugins/flatpak_cli_plugin.py %{buildroot}%{python3_sitelib}/koji_cli_plugins/flatpak.py
%py_byte_compile %{__python3} %{buildroot}%{python3_sitelib}/koji_cli_plugins/flatpak.py


%files common
%license COPYING
%doc README.md

%files hub
%{_prefix}/lib/koji-hub-plugins

%files builder
%{_prefix}/lib/koji-builder-plugins

%files cli
%{python3_sitelib}/koji_cli_plugins


%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 0.7-5
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 0.7-4
- Rebuilt for Python 3.14.0rc2 bytecode

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 0.7-2
- Rebuilt for Python 3.14

* Sun Jan 26 2025 Yaakov Selkowitz <yselkowi@redhat.com> - 0.7-1
- Version 0.7
  Add support for extension flatpaks

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 0.6-4
- Rebuilt for Python 3.13

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Oct 3 2023 Owen Taylor <otaylor@redhat.com> - 0.6-1
- Version 0.6
  Fix regression with docker:// disappearing from skopeo commands

* Tue Oct 3 2023 Owen Taylor <otaylor@redhat.com> - 0.5-1
- Version 0.5
  Fix docker:// inappropriately appearing in pull-spec strings

* Tue Oct 3 2023 Owen Taylor <otaylor@redhat.com> - 0.4-1
- Version 0.4
  Fix problem where ~ and ^ in version would result in invalid registry tags

* Mon Sep 25 2023 Owen Taylor <otaylor@redhat.com> - 0.3-1
- Version 0.3
  Handle output tarfile being <base>.oci.tar rather than <base>.oci.tar.gz (changed
  in flatpak-module-tools-1.0a8 - current code here handles both.)

* Tue Aug 22 2023 Owen Taylor <otaylor@redhat.com> - 0.2-1
- Version 0.2
  Handle case where the main package name doesn't match the corresponding source package.

* Mon Aug 14 2023 Adam Williamson <awilliam@redhat.com> - 0.1-3
- common subpackage shouldn't require koji-hub

* Fri Aug 11 2023 Owen Taylor <otaylor@redhat.com> - 0.1-2
- Fix review comments, rename subpackage koji-flatpak => koji-flatpak-common
  Add dependency on skopeo
  https://bugzilla.redhat.com/show_bug.cgi?id=2231215

* Thu Aug 10 2023 Owen Taylor <otaylor@redhat.com> - 0.1-1
- Initial version
