# Got the intial spec and patches from Fedora and modified the spec.
Summary:        Python bindings for PAM (Pluggable Authentication Modules).
Name:           PyPAM
Version:        0.5.0
Release:        9%{?dist}
License:        LGPLv2
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages/Python
# Note that the upstream URL is dead. Project seems to have been abandoned by authors.
URL:            http://www.pangalactic.org/PyPAM
Source0:        https://src.fedoraproject.org/repo/pkgs/%{name}/%{name}-%{version}.tar.gz/f1e7c2c56421dda28a75ace59a3c8871/%{name}-%{version}.tar.gz
Patch0:         PyPAM-dlopen.patch
Patch1:         PyPAM-0.5.0-dealloc.patch
Patch2:         PyPAM-0.5.0-nofree.patch
Patch3:         PyPAM-0.5.0-memory-errors.patch
Patch4:         PyPAM-0.5.0-return-value.patch
Patch5:         PyPAM-python3-support.patch
BuildRequires:  pam-devel
BuildRequires:  python3-devel
Requires:       python3
Provides:       python3-%{name} = %{version}-%{release}

%description
Python bindings for PAM (Pluggable Authentication Modules).

%prep
%autosetup -p 1

%build
%py3_build

%install
%py3_install

%check
PATH=%{buildroot}%{_bindir}:${PATH} \
  PYTHONPATH=%{buildroot}%{python3_sitelib} \
  python3 tests/PamTest.py

%files
%defattr(-,root,root,-)
%license COPYING
%{python3_sitelib}/*

%changelog
* Wed Oct 20 2021 Olivia Crain <oliviacrain@microsoft.com> - 0.5.0-9
- Remove python2 package, have main package contain python3 version
- Add license to python3 package
- Align python3 support patch file prefix level with other patches
- Lint spec

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 0.5.0-8
- Added %%license line automatically

* Tue Apr 28 2020 Emre Girgin <mrgirgin@microsoft.com> - 0.5.0-7
- Renaming Linux-PAM to pam

* Mon Apr 27 2020 Nick Samson <nisamson@microsoft.com> - 0.5.0-6
- Updated Source0, License verified, %%define sha removed

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 0.5.0-5
- Initial CBL-Mariner import from Photon (license: Apache2).

* Thu Jan 10 2019 Alexey Makhalov <amakhalov@vmware.com> - 0.5.0-4
- Added BuildRequires python2-devel.
- Moved all buildRequires to the main package.

* Thu Jun 22 2017 Dheeraj Shetty <dheerajs@vmware.com> - 0.5.0-3
- Fix the check section

* Wed May 31 2017 Dheeraj Shetty <dheerajs@vmware.com> - 0.5.0-2
- Changing python_sitelib to python2

* Tue Apr 11 2017 Xiaolin Li <xiaolinl@vmware.com> - 0.5.0-1
- Initial packaging for Photon.
