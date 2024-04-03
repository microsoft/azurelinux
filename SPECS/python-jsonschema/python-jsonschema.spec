Summary:        An implementation of JSON Schema validation for Python
Name:           python-jsonschema
Version:        4.21.1
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Development/Languages/Python
URL:            https://pypi.python.org/pypi/jsonschema
Source0:        https://pypi.python.org/packages/source/j/jsonschema/jsonschema-%{version}.tar.gz
BuildArch:      noarch

%description
jsonschema is JSON Schema validator currently based on
http://tools.ietf.org/html/draft-zyp-json-schema-03

%package -n     python3-jsonschema
Summary:        An implementation of JSON Schema validation for Python
BuildRequires:  pyproject-rpm-macros
BuildRequires:  python3-devel
BuildRequires:  python3-hatchling
BuildRequires:  python3-hatch-fancy-pypi-readme
BuildRequires:  python3-hatch-vcs
BuildRequires:  python3-packaging
BuildRequires:  python3-pathspec
BuildRequires:  python3-pip
BuildRequires:  python3-pluggy
BuildRequires:  python3-setuptools
BuildRequires:  python3-setuptools_scm
BuildRequires:  python3-trove-classifiers
BuildRequires:  python3-vcversioner
BuildRequires:  python3-wheel
BuildRequires:  python3-xml
%if %{with_check}
BuildRequires:  python3-twisted
BuildRequires:  python3-typing-extensions
%endif
Requires:       python3

%description -n python3-jsonschema
jsonschema is JSON Schema validator currently based on
http://tools.ietf.org/html/draft-zyp-json-schema-03

%pyproject_extras_subpkg -n python3-jsonschema format format-nongpl

%prep
%autosetup -n jsonschema-%{version}

# Requires a checkout of the JSON-Schema-Test-Suite
# https://github.com/json-schema-org/JSON-Schema-Test-Suite
rm jsonschema/tests/test_jsonschema_test_suite.py

%generate_buildrequires
%pyproject_buildrequires
 
%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files jsonschema

%if %{with_check}
%check
pip3 install jsonschema-specifications referencing
PYTHONPATH=%{buildroot}%{python3_sitelib} trial3 jsonschema
%endif

%files -n python3-jsonschema -f %{pyproject_files}
%defattr(-,root,root)
%license COPYING json/LICENSE
%doc README.rst
%{_bindir}/jsonschema

%changelog
* Mon Feb 26 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 4.21.1-1
- Auto-upgrade to 4.21.1 - Azure Linux 3.0 - package upgrades

* Wed Oct 20 2021 Thomas Crain <thcrain@microsoft.com> - 2.6.0-6
- Remove python2 package
- Lint spec

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 2.6.0-5
- Added %%license line automatically

* Wed May 06 2020 Paul Monson <paulmon@microsoft.com> - 2.6.0-4
- Restore python-vcversioner to enable build without internet access.

* Mon Apr 13 2020 Nicolas Ontiveros <niontive@microsoft.com> - 2.6.0-3
- Don't use python-vcversioner in build.

* Wed Apr 08 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.6.0-2
- Initial CBL-Mariner import from Photon (license: Apache2).
- Switched "Source0" and "URL" tags to use https.
- License verified.

* Tue Oct 23 2018 Sujay G <gsujay@vmware.com> - 2.6.0-1
- Initial version
