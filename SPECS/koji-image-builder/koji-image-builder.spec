# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global forgeurl https://github.com/osbuild/koji-image-builder

Version:        8

%forgemeta

Name:           koji-image-builder
Release:        3%{?dist}
License:        Apache-2.0

URL:            %{forgeurl}

Source0:        %{forgesource}
BuildArch:      noarch

Summary:        Koji integration plugins for image-builder

BuildRequires:  python3-devel
BuildRequires:  python3dist(koji)
BuildRequires:  python3dist(pytest) python3dist(pytest-mock)

%description
Koji integration plugins for image-builder.

%package        hub
Summary:        Koji hub plugin for image-builder integration
Requires:       %{name} = %{version}-%{release}
Requires:       koji-hub koji-hub-plugins
Requires:       python3-jsonschema

%description    hub
Koji hub plugin for image-builder integration.

%package        builder
Summary:        Koji builder plugin for image-builder integration
Requires:       %{name} = %{version}-%{release}
Requires:       koji-builder koji-builder-plugins

%description    builder
Koji builder plugin for image-builder integration.

%package        cli
Summary:        Koji cli plugin for image-cli integration
Requires:       %{name} = %{version}-%{release}
Requires:       koji python3-koji-cli-plugins

%description    cli
Koji cli plugin for image-cli integration.

%prep
%forgesetup

%build
# nothing to do

%check
%pytest test/unit

%install
install -d %{buildroot}/%{_prefix}/lib/koji-hub-plugins
install -p -m 0755 plugin/hub/image_builder.py %{buildroot}/%{_prefix}/lib/koji-hub-plugins/
%py_byte_compile %{python3} %{buildroot}/%{_prefix}/lib/koji-hub-plugins/image_builder.py

install -d %{buildroot}/%{_prefix}/lib/koji-builder-plugins
install -p -m 0755 plugin/builder/image_builder.py %{buildroot}/%{_prefix}/lib/koji-builder-plugins/
%py_byte_compile %{python3} %{buildroot}/%{_prefix}/lib/koji-builder-plugins/image_builder.py

install -d %{buildroot}/%{python3_sitelib}/koji_cli_plugins
install -p -m 0644 plugin/cli/image_builder.py %{buildroot}%{python3_sitelib}/koji_cli_plugins/image_builder.py

%files
%license LICENSE
%doc README.md

%files hub
%{_prefix}/lib/koji-hub-plugins/image_builder.py
%{_prefix}/lib/koji-hub-plugins/__pycache__/image_builder.*

%files builder
%{_prefix}/lib/koji-builder-plugins/image_builder.py
%{_prefix}/lib/koji-builder-plugins/__pycache__/image_builder.*

%files cli
%pycached %{python3_sitelib}/koji_cli_plugins/image_builder.py

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 8-3
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 8-2
- Rebuilt for Python 3.14.0rc2 bytecode

* Thu Jul 24 2025 Packit <hello@packit.dev> - 8-1
Changes with 8
----------------
  * builder: return `release` in results (#14)
    * Author: Simon de Vlieger, Reviewers: Tomáš Hozza

— Somewhere on the Internet, 2025-07-24


* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 6-2
- Rebuilt for Python 3.14

# the changelog is distribution-specific, therefore there's just one entry
# to make rpmlint happy.

* Thu Apr 17 2025 Packit <hello@packit.dev> - 6-1
Changes with 6
----------------
  * build: include `arch` in artifact names (#12)
    * Author: Simon de Vlieger, Reviewers: Nobody

— Somewhere on the Internet, 2025-04-17


* Wed Apr 16 2025 Packit <hello@packit.dev> - 5-1
Changes with 5
----------------
  * Fixed cli pkg name in README.md (#8)
    * Author: Fabian Arrotin, Reviewers: Simon de Vlieger
  * ci: enable epel8 in packit (#6)
    * Author: Simon de Vlieger, Reviewers: Ondřej Budai
  * many: replace `$arch` and `$buildarch` variable manually (COMPOSER-2507) (#10)
    * Author: Simon de Vlieger, Reviewers: Ondřej Budai
  * readme updates (#7)
    * Author: Simon de Vlieger, Reviewers: Brian C. Lane

— Somewhere on the Internet, 2025-04-16


* Wed Apr 9 2025 Packit <hello@packit.dev> - 4-1
Changes with 4
----------------
  * ci: pull osbuild from COPR (#3)
    * Author: Simon de Vlieger, Reviewers: Nobody

— Somewhere on the Internet, 2025-04-09


* Thu Apr 3 2025 Packit <hello@packit.dev> - 3-1
Changes with 3
----------------

— Somewhere on the Internet, 2025-04-03


* Thu Apr 3 2025 Packit <hello@packit.dev> - 2-1
Changes with 2
----------------

— Somewhere on the Internet, 2025-04-03


* Mon Mar 17 2025 Simon de Vlieger <supakeen@redhat.com> - 1-1
- On this day, this project was born.
