Vendor:         Microsoft Corporation
Distribution:   Mariner
%global desc These provide several pieces of "middleware" (or filters) that can be nested\
to build web applications.  Each piece of middleware uses the WSGI (PEP 333)\
interface, and should be compatible with other middleware based on those\
interfaces.
%global sum Tools for using a Web Server Gateway Interface stack

Name:           python-paste
Version:        3.2.4
Release:        3%{?dist}
BuildArch:      noarch

# Most of the code is MIT
# paste/exceptions/collector.py is ZPLv2.0
# paste/evalexception/media/MochiKit.packed.js AFL (2.1) or MIT
# paste/lint.py MIT or Apache v2
# PySourceColor.py, Python
License:        MIT and ZPLv2.0 and Python and (AFL or MIT) and (MIT or ASL 2.0)
Summary:        %sum
URL:            https://github.com/cdent/paste
Source0:        https://files.pythonhosted.org/packages/source/P/Paste/Paste-%{version}.tar.gz#/python-Paste-%{version}.tar.gz


BuildRequires:  python3-devel
BuildRequires:  python3-nose
BuildRequires:  python3-pyOpenSSL
BuildRequires:  python3-pytest
BuildRequires:  python3-pytest-runner
BuildRequires:  python3-setuptools
BuildRequires:  python3-six >= 1.4.0
BuildRequires:  python3-tempita


%description
%desc


%package -n python3-paste
Summary:        Tools for using a Web Server Gateway Interface stack

%{?python_provide:%python_provide python3-paste}

Requires: python3-pyOpenSSL
Requires: python3-setuptools
Requires: python3-six
Requires: python3-tempita


%description -n python3-paste
%{desc}


%prep
%autosetup -n Paste-%{version} -p1

# Paste-2.0.3 seems to have a few .py.orig files that don't appear in upstream scm. Let's drop them.
find . -name "*.orig" -delete

# Strip #! lines that make these seem like scripts
%{__sed} -i -e '/^#!.*/,1 d' paste/util/scgiserver.py paste/debug/doctest_webapp.py

# clean docs directory
pushd docs
rm StyleGuide.txt
popd


%build
%{__python3} setup.py build


%install
%{__python3} setup.py install --skip-build --root %{buildroot}


%check
export PYTHONPATH=$(pwd)
# We don't have access to the wider internet in the buildsystem
py.test-3 -k "not test_paste_website and not test_proxy_to_website and not test_modified"


%files -n python3-paste
%license docs/license.txt
%doc docs/*
%{python3_sitelib}/paste
%{python3_sitelib}/Paste-%{version}-py%{python3_version}.egg-info
%{python3_sitelib}/Paste-%{version}-py%{python3_version}-nspkg.pth


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.2.4-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

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
