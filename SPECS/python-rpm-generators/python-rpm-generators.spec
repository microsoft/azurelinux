Name:           python-rpm-generators
Summary:        Dependency generators for Python RPMs
Version:        14
Release:        12%{?dist}
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Applications/System
# See individual licenses above Source declarations
# Originally, this was simplified to GPL-2.0-or-later, but "effective license" analysis is no longer allowed
License:        GPL-2.0-or-later AND LGPL-2.1-or-later AND (LicenseRef-Fedora-Public-Domain OR LGPL-2.1-or-later OR GPL-2.0-or-later)
Url:            https://src.fedoraproject.org/python-rpm-generators

# Originally the following files were part of RPM, so the license is inherited: GPL-2.0-or-later
# The COPYING file is grabbed from the last commit that changed the files
Source0:        https://raw.githubusercontent.com/rpm-software-management/rpm/102eab50b3d0d6546dfe082eac0ade21e6b3dbf1/COPYING
Source1:        https://src.fedoraproject.org/rpms/python-rpm-generators/blob/f40/f/python.attr
Source2:        https://src.fedoraproject.org/rpms/python-rpm-generators/blob/f40/f/pythondist.attr
# This was crafted in-place as a fork of python.attr, hence also GPL-2.0-or-later
Source3:        https://src.fedoraproject.org/rpms/python-rpm-generators/blob/f40/f/pythonname.attr
# This one is also originally from RPM, but it has its own license declaration: LGPL-2.1-or-later
Source4:        https://src.fedoraproject.org/rpms/python-rpm-generators/blob/f40/f/pythondistdeps.py
# This was crafted in-place with the following license declaration:
#  LicenseRef-Fedora-Public-Domain OR CC0-1.0 OR LGPL-2.1-or-later OR GPL-2.0-or-later
# Note that CC0-1.0 is not allowed for code in Fedora, so we skip it in the package License tag
Source5:        https://src.fedoraproject.org/rpms/python-rpm-generators/blob/f40/f/pythonbundles.py

BuildArch:      noarch

%description
%{summary}.

%package -n python3-rpm-generators
Summary:        %{summary}
Requires:       python3-packaging
Requires:       rpm
# This contains the Lua functions we use. (Provided by azurelinux-rpm-macros)
Requires:       python-srpm-macros

%description -n python3-rpm-generators
%{summary}.

%prep
%autosetup -c -T
cp -a %{sources} .

%install
install -Dpm0644 -t %{buildroot}%{_fileattrsdir} *.attr
install -Dpm0755 -t %{buildroot}%{_rpmconfigdir} *.py

%files -n python3-rpm-generators
%license COPYING
%{_fileattrsdir}/python.attr
%{_fileattrsdir}/pythondist.attr
%{_fileattrsdir}/pythonname.attr
%{_rpmconfigdir}/pythondistdeps.py
%{_rpmconfigdir}/pythonbundles.py

%changelog
* Thu Mar 14 2024 Pawel Winogrodzki <pawelwi@microsoft.com> - 14-12
- Enabling Python requires generator.

* Mon Mar 04 2024 Andrew Phelps <anphel@microsoft.com> - 14-11
- Promote from SPECS-EXTENDED to SPECS
- Refresh from Fedora 40 (license: MIT)
- License verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 10-5
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jan 17 2020 Miro Hrončok <mhroncok@redhat.com> - 10-3
- Also provide pythonXdist() with PEP 503 normalized names (#1791530)

* Fri Jan 03 2020 Miro Hrončok <mhroncok@redhat.com> - 10-2
- Fix more complicated requirement expressions by adding parenthesis

* Wed Jan 01 2020 Miro Hrončok <mhroncok@redhat.com> - 10-1
- Handle version ending with ".*" (#1758141)
- Handle compatible-release operator "~=" (#1758141)
- Use rich deps for semantically versioned dependencies
- Match Python version if minor has multiple digits (e.g. 3.10, #1777382)
- Only add setuptools requirement for egg-info packages

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jun 24 2019 Tomas Orsava <torsava@redhat.com> - 9-1
- Canonicalize Python versions and properly handle != spec

* Wed Apr 17 2019 Miro Hrončok <mhroncok@redhat.com> - 8-1
- console_scripts entry points to require setuptools
  https://github.com/rpm-software-management/rpm/pull/666

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Dec 20 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 7-1
- Enable requires generator

* Wed Oct 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 6-1
- Tighten regex for depgen

* Sat Jul 28 2018 Miro Hrončok <mhroncok@redhat.com> - 5-4
- Use nonstandardlib for purelib definition (#1609492)

* Sat Jul 28 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 5-3
- Add pythondist generator

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Feb 11 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 5-1
- Fork upstream generators
- "Fix" support of environment markers

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.14.0-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Nov 28 2017 Tomas Orsava <torsava@redhat.com> - 4.14.0-2
- Switch bootsrapping macro to a bcond for modularity

* Fri Oct 20 2017 Tomas Orsava <torsava@redhat.com> - 4.14.0-1
- Rebase to rpm 4.14.0 final (http://rpm.org/wiki/Releases/4.14.0)
- Re-synchronize version/release macros with the rpm Fedora package

* Mon Sep 18 2017 Tomas Orsava <torsava@redhat.com> - 4.14.0-0.rc1.1
- Update to a new upstream version of RPM
- Drop upstreamed patches
- Renumber remaining patches

* Thu Aug 24 2017 Miro Hrončok <mhroncok@redhat.com> - 4.13.0.1-4
- Add patch 10: Do not provide pythonXdist for platform-python packages (rhbz#1484607)

* Tue Aug 08 2017 Tomas Orsava <torsava@redhat.com> - 4.13.0.1-3
- Add patch 9: Generate requires and provides for platform-python(abi)
  (https://fedoraproject.org/wiki/Changes/Platform_Python_Stack)

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.13.0.1-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu May 18 2017 Tomas Orsava <torsava@redhat.com> - 4.13.0.1-2
- Added a license file
- Added a dependency on rpm for the proper directory structure
- Properly owning the __pycache__ directory

* Tue May 02 2017 Tomas Orsava <torsava@redhat.com> - 4.13.0.1-1
- Splitting Python RPM generators from the `rpm` package to standalone one
