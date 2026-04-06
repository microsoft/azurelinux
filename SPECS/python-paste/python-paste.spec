# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global desc These provide several pieces of "middleware" (or filters) that can be nested\
to build web applications.  Each piece of middleware uses the WSGI (PEP 333)\
interface, and should be compatible with other middleware based on those\
interfaces.
%global sum Tools for using a Web Server Gateway Interface stack

Name:           python-paste
Version:        3.10.1
Release:        11%{?dist}
BuildArch:      noarch

# Most of the code is MIT
# paste/exceptions/collector.py is ZPLv2.0
# paste/evalexception/media/MochiKit.packed.js AFL (2.1) or MIT
# paste/lint.py MIT or Apache v2
# PySourceColor.py, Python
# Automatically converted from old format: MIT and ZPLv2.0 and Python and (AFL or MIT) and (MIT or ASL 2.0) - review is highly recommended.
License:        LicenseRef-Callaway-MIT AND ZPL-2.0 AND LicenseRef-Callaway-Python AND (LicenseRef-Callaway-AFL OR LicenseRef-Callaway-MIT) AND (LicenseRef-Callaway-MIT OR Apache-2.0)
Summary:        %sum
URL:            https://github.com/pasteorg/paste
#Source0:        %%{pypi_source}
Source0:        https://github.com/pasteorg/paste/archive/%{version}/Paste-%{version}.tar.gz
Patch1:         paste-import-urlparse.patch


BuildRequires:  python3-devel
BuildRequires:  python3-pyOpenSSL
BuildRequires:  python3-pytest
BuildRequires:  python3-six >= 1.4.0
# required for tests
BuildRequires:  python3-openid
BuildRequires:  python3-paste-deploy


%description
%desc


%package -n python3-paste
Summary:        Tools for using a Web Server Gateway Interface stack


Requires: python3-pyOpenSSL
Requires: python3-setuptools
Requires: python3-six


%description -n python3-paste
%{desc}


%prep
%autosetup -n paste-%{version} -p1

# Paste-2.0.3 seems to have a few .py.orig files that don't appear in upstream scm. Let's drop them.
find . -name "*.orig" -delete

# Strip #! lines that make these seem like scripts
%{__sed} -i -e '/^#!.*/,1 d' paste/util/scgiserver.py paste/debug/doctest_webapp.py

# clean docs directory
pushd docs
rm StyleGuide.txt
popd


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files paste


%check
# exclude broken modules from import tests
%pyproject_check_import -e 'paste.debug.*' -e paste.flup_session -e paste.transaction -e paste.util.scgiserver
export PYTHONPATH=$(pwd)
# We don't have access to the wider internet in the buildsystem
py.test-3 -k "not test_paste_website and not test_proxy_to_website and not test_modified"


%files -n python3-paste -f %{pyproject_files}
%doc docs/*
%{python3_sitelib}/Paste-%{version}-py%{python3_version}-nspkg.pth


%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 3.10.1-11
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 3.10.1-10
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.10.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jul 14 2025 Ján ONDREJ (SAL) <ondrejj(at)salstar.sk> - 3.10.1-8
- Migrate from py_build/py_install to pyproject macros (bz#2378583)

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 3.10.1-7
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.10.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Dec 25 2024 Ján ONDREJ (SAL) <ondrejj(at)salstar.sk> - 3.10.1-5
- Remove dependency on python-tempita

* Wed Sep 04 2024 Miroslav Suchý <msuchy@redhat.com> - 3.10.1-4
- convert license to SPDX

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.10.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 3.10.1-2
- Rebuilt for Python 3.13

* Thu May 02 2024 Ján ONDREJ (SAL) <ondrejj(at)salstar.sk> - 3.10.1-1
- Update to upstream.
- Update URL according to redirection on github.
- Source URL updated to github, unable to download from pypi.
- CGI warnings have been disabled, no cgi used in this version.

* Mon Apr 29 2024 Ján ONDREJ (SAL) <ondrejj(at)salstar.sk> - 3.10.0-1
- Update to upstream.

* Fri Apr 05 2024 Ján ONDREJ (SAL) <ondrejj(at)salstar.sk> - 3.9.0-1
- Update to upstream.

* Mon Mar 18 2024 Ján ONDREJ (SAL) <ondrejj(at)salstar.sk> - 3.8.0-1
- Update to upstream.

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Oct 21 2023 Ján ONDREJ (SAL) <ondrejj(at)salstar.sk> - 3.7.1-1
- Update to upstream.

* Mon Oct 16 2023 Ján ONDREJ (SAL) <ondrejj(at)salstar.sk> - 3.6.1-1
- Update to upstream.

* Tue Oct 03 2023 Ján ONDREJ (SAL) <ondrejj(at)salstar.sk> - 3.6.0-1
- Update to upstream.

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 14 2023 Python Maint <python-maint@redhat.com> - 3.5.3-2
- Rebuilt for Python 3.12

* Tue May 02 2023 Ján ONDREJ (SAL) <ondrejj(at)salstar.sk> - 3.5.3-1
- Update to upstream.

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jan 07 2023 Kevin Fenzi <kevin@scrye.com> - 3.5.2-1
- Update to 3.5.2. Fixes rhbz#2100061

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jun 14 2022 Python Maint <python-maint@redhat.com> - 3.5.0-7
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 3.5.0-4
- Rebuilt for Python 3.10

* Mon Feb 08 2021 Charalampos Stratakis <cstratak@redhat.com> - 3.5.0-3
- Remove redundant nose dependency

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Nov 02 2020 Joel Capitao <jcapitao@redhat.com> - 3.5.0-1
- Update to 3.5.0 (#1882460)

* Thu Sep 10 2020 Yatin Karel <ykarel@redhat.com> - 3.4.4-1
- Update to 3.4.4 (#1844011)

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun May 24 2020 Miro Hrončok <mhroncok@redhat.com> - 3.4.0-2
- Rebuilt for Python 3.9

* Wed Feb 19 2020 Randy Barlow <bowlofeggs@fedoraproject.org> - 3.4.0-1
- Update to 3.4.0 (#1789359).
- https://github.com/cdent/paste/blob/3.4.0/docs/news.txt

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Jan 07 2020 Randy Barlow <bowlofeggs@fedoraproject.org> - 3.2.4-1
- Update to 3.2.4 (#1776547).
- https://github.com/cdent/paste/blob/3.2.4/docs/news.txt

* Mon Oct 14 2019 Randy Barlow <bowlofeggs@fedoraproject.org> - 3.2.2-1
- Update to 3.2.2 (#1761382).
- https://github.com/cdent/paste/blob/3.2.2/docs/news.txt

* Fri Sep 27 2019 Randy Barlow <bowlofeggs@fedoraproject.org> - 3.2.1-1
- Update to 3.2.1 (#1755413).

* Tue Sep 17 2019 Randy Barlow <bowlofeggs@fedoraproject.org> - 3.2.0-1
- Update to 3.2.0 (#1749324).
- https://github.com/cdent/paste/blob/3.2.0/docs/news.txt

* Tue Sep 17 2019 Randy Barlow <bowlofeggs@fedoraproject.org> - 3.1.1-2
- Drop python2-paste (#1751087).

* Tue Sep 03 2019 Randy Barlow <bowlofeggs@fedoraproject.org> - 3.1.1-1
- Update to 3.1.1 (#1742275).
- https://github.com/cdent/paste/blob/master/docs/news.txt

* Sat Aug 17 2019 Miro Hrončok <mhroncok@redhat.com> - 3.0.8-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Mar 28 2019 Randy Barlow <bowlofeggs@fedoraproject.org> - 3.0.8-1
- Update to 3.0.8 (#1684199).
- Update the URL to the new home on GitHub.

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jun 18 2018 Miro Hrončok <mhroncok@redhat.com> - 2.0.3-7
- Rebuilt for Python 3.7

* Fri Jun 08 2018 Miro Hrončok <mhroncok@redhat.com> - 2.0.3-6
- Fix build on Python 3.7 (#1583818)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Jan 26 2018 Iryna Shcherbina <ishcherb@redhat.com> - 2.0.3-4
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)
