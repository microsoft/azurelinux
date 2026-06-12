%global pip_module_name argparse_manpage

Name:           argparse-manpage
Version:        4.7
Release:        1%{?dist}
Summary:        Build manual page from Python ArgumentParser object
BuildArch:      noarch

License:        Apache-2.0
URL:            https://github.com/praiskup/%{name}
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Source0:        %{pypi_source %{pip_module_name}}

BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros
BuildRequires:  python3-pip
BuildRequires:  python3-wheel
BuildRequires:  python3-tomli
BuildRequires:  python3-pytest

Requires:       python3-%{name} = %{version}-%{release}

%description
Generate manual page an automatic way from ArgumentParser object, so the
manpage 1:1 corresponds to the automatically generated --help output.  The
manpage generator needs to known the location of the object, user can
specify that by (a) the module name or corresponding python filename and
(b) the object name or the function name which returns the object.
There is a limited support for (deprecated) optparse objects, too.


%package -n     python3-%{name}
Summary:        Build manual page from Python 3 ArgumentParser object

%description -n python3-%{name}
Generate manual page an automatic way from ArgumentParser object, so the
manpage 1:1 corresponds to the automatically generated --help output.  The
manpage generator needs to known the location of the object, user can
specify that by (a) the module name or corresponding python filename and
(b) the object name or the function name which returns the object.
There is a limited support for (deprecated) optparse objects, too.


%pyproject_extras_subpkg -n python3-%{name} setuptools


%prep
%autosetup -n %{pip_module_name}-%{version}

%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install


%check
# Disable pip build isolation to make the tests work in offline environment
# Fixes https://bugzilla.redhat.com/2417959
export PIP_NO_BUILD_ISOLATION=0
%pytest -vv


%files
%license LICENSE
%{_bindir}/argparse-manpage
%{_mandir}/man1/argparse-manpage.1.*
%{python3_sitelib}/argparse_manpage/cli.py


%files -n python3-%{name}
%license LICENSE
%{python3_sitelib}/build_manpages
%{python3_sitelib}/argparse_manpage
%{python3_sitelib}/argparse_manpage-*dist-info
%exclude %{python3_sitelib}/argparse_manpage/cli.py


%changelog
* Fri May 08 2026 Sandeep Karambelkar <skarambelkar@microsoft.com> - 4.7-1
- Initial Azure Linux import from Fedora 44 (license: MIT)
- License Verified
