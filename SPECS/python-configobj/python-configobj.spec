Summary:        Config file reading, writing and validation
Name:           python-configobj
Version:        5.0.6
Release:        7%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages/Python
URL:            https://github.com/DiffSK/configobj
# Source to be fixed as part of https://microsoft.visualstudio.com/OS/_workitems/edit/25936171.
Source0:        https://files.pythonhosted.org/packages/64/61/079eb60459c44929e684fa7d9e2fdca403f67d64dd9dbac27296be2e0fab/configobj-%{version}.tar.gz
Source1:        LICENSE.BSD
BuildArch:      noarch

%description
Config file reading, writing and validation

%package -n     python3-configobj
Summary:        Config file reading, writing and validation
BuildRequires:  python3-devel
Requires:       python3
Requires:       python3-six

%description -n python3-configobj
ConfigObj is a simple but powerful config file reader and writer: an ini file round tripper. Its main feature is that it is very easy to use, with a straightforward programmer’s interface and a simple syntax for config files.

%prep
%autosetup -n configobj-%{version}
cp %{SOURCE1} ./

%build
%py3_build

%install
%py3_install

%check
%python3 validate.py

%files -n python3-configobj
%defattr(-,root,root)
%license LICENSE.BSD
%{python3_sitelib}/*

%changelog
* Wed Oct 20 2021 Olivia Crain <oliviacrain@microsoft.com> - 5.0.6-7
- Add license to python3 package
- Remove python2 package
- Lint spec

* Wed May 27 2020 Nick Samson <nisamson@microsoft.com> - 5.0.6-6
- Added License file and %%license invocation

* Thu Apr 09 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 5.0.6-5
- Initial CBL-Mariner import from Photon (license: Apache2).
- Fixed "Source0" tag.
- License verified.
- Removed "%%define sha1".
- Making %%setup quiet.

* Mon May 15 2017 Kumar Kaushik <kaushikk@vmware.com> - 5.0.6-4
- Adding python 3 support.

* Mon Oct 03 2016 ChangLee <changLee@vmware.com> - 5.0.6-3
- Modified %check

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 5.0.6-2
- GA - Bump release of all rpms

* Wed Mar 04 2015 Mahmoud Bassiouny <mbassiouny@vmware.com>
- Initial packaging for Photon
