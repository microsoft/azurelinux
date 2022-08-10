#
# spec file for package python-click-aliases
#
# Copyright (c) 2020 SUSE LLC
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#
Name:           python-click-aliases
Version:        1.0.1
Release:        1%{?dist}
Summary:        Command aliases for Click
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/click-contrib/click-aliases
Source0:        https://files.pythonhosted.org/packages/source/c/click-aliases/click-aliases-%{version}.tar.gz#/click-aliases-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  fdupes
BuildRequires:  python3-setuptools
BuildRequires:  python3-wheel
Requires:       python3-click
%if %{with_check}
BuildRequires:  python3-click
BuildRequires:  python3-pip
BuildRequires:  python3-pytest
%endif

%description
Command aliases for Click.

%prep
%autosetup -n click-aliases-%{version} -p1

%build
%py3_build

%install
%py3_install
%fdupes -s %{buildroot}%{python3_sitelib}

%check
export LANG=en_US.UTF-8
# test_invalid fails with new click as the quotes in output changed from single to regular ones
%{python3} -m pip install atomicwrites attrs docutils pluggy pygments six more-itertools
%pytest -k 'not test_invalid'

%files
%doc README.md
%license LICENSE
%{python3_sitelib}/*

%changelog
* Tue Jun 21 2022 Sumedh Sharma <sumsharma@microsoft.com> - 1.0.1-1
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag)
- Adding as run dependency (Requires) for package cassandra medusa for cosmosDb.
- License verified
* Mon Apr 27 2020 Tomáš Chvátal <tchvatal@suse.com>
- Disable test_invalid checks, quotes change in output
* Thu Sep 19 2019 John Vandenberg <jayvdb@gmail.com>
- Add LANG to %%check to fix build on Leap
* Mon Aug 26 2019 John Vandenberg <jayvdb@gmail.com>
- Initial spec for v1.0.1
