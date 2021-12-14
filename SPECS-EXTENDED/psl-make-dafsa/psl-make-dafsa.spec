Vendor:         Microsoft Corporation
Distribution:   Mariner
#
# spec file for package psl-make-dafsa
#
# Copyright (c) 2019 SUSE LINUX GmbH, Nuernberg, Germany.
# Copyright (c) 2015 rpm@cicku.me
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


Name:           psl-make-dafsa
Version:        0.21.1
Release:        2%{?dist}
Summary:        Tool to create a binary DAFSA from a Public Suffix List
License:        BSD-3-Clause
Group:          Development/Libraries/C and C++
Url:            https://rockdaboot.github.io/libpsl
Source:         https://github.com/rockdaboot/libpsl/releases/download/%{version}/libpsl-%{version}.tar.gz
Requires:       python3
BuildArch:      noarch

%description
psl-make-dafsa converts ASCII string into C source or a binary format,
The format used is DAFSA, deterministic acyclic finate state automaton.

libpsl is capable of using this compact binary form of the Public Suffix List (PSL).

This package is a build dependency for the publicsuffix package.

%prep
%setup -q -n libpsl-%{version}
# fix env shebang to call py3 directly
sed -i -e "1s|#!.*|#!%{_bindir}/python3|" src/psl-make-dafsa

%build
:

%install
mkdir -p %{buildroot}%{_bindir}
install src/psl-make-dafsa %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_mandir}/man1
install -m 644 src/psl-make-dafsa.1 %{buildroot}%{_mandir}/man1

%files
%license src/LICENSE.chromium
%doc AUTHORS NEWS
%{_bindir}/psl-make-dafsa
%{_mandir}/man1/psl-make-dafsa.1*

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.21.1-2
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Mon Nov 30 2020 Joe Schmitt <joschmit@microsoft.com> - 0.21.1-1.3
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Remove openSUSE specific macro %%ext_man.
- Update python3-base to python3.

* Fri Jul 17 2020 Andreas Stieger <andreas.stieger@gmx.de>
- update to 0.21.1:
  * no changes for psl-make-dafsa
* Sun Jun  2 2019 Jan Engelhardt <jengelh@inai.de>
- Use noun phrase in summary.
* Sun May 19 2019 Andreas Stieger <andreas.stieger@gmx.de>
- update to 0.21.0:
  * no changes for psl-make-dafsa
* Sat Apr 28 2018 astieger@suse.com
- update to 0.20.2:
  * no changes for psl-make-dafsa
* Tue Feb 27 2018 astieger@suse.com
- update to 0.20.1:
  * no changes for psl-make-dafsa
* Thu Feb 22 2018 fvogt@suse.com
- Use %%license (boo#1082318)
* Thu Feb 22 2018 astieger@suse.com
- update to 0.20.0:
  * remove explicit plain TLD rule
* Wed Jan  3 2018 tchvatal@suse.com
- Make sure to use python3 instead of env python call
* Thu Nov  9 2017 astieger@suse.com
- update to 0.19.1:
  * psl_make_dafsa now works with python2 and python3
* Thu Jul 20 2017 astieger@suse.com
- update to 0.18.0:
  * no changes for psl-make-dafsa
* Thu Jan 19 2017 shshyukriev@suse.com
- update to 0.17.0:
  * no changes for psl-make-dafsa
* Thu Dec 15 2016 astieger@suse.com
- update to 0.16.1:
  * no changes for psl-make-dafsa
* Thu Nov 24 2016 astieger@suse.com
- package psl-make-dafsa, for converting the PSL list into the
  DAFSA binary format
- split from libpsl package to break build cycle
