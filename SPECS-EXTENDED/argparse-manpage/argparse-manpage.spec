Vendor:         Microsoft Corporation
Distribution:   Mariner

%global sum()   Build manual page from %* ArgumentParser object
%global desc \
Generate manual page an automatic way from ArgumentParser object, so the \
manpage 1:1 corresponds to the automatically generated --help output.  The \
manpage generator needs to known the location of the object, user can \
specify that by (a) the module name or corresponding python filename and \
(b) the object name or the function name which returns the object. \
There is a limited support for (deprecated) optparse objects, too.


Name:           argparse-manpage
Version:        1.5
Release:        3%{?dist}
Summary:        %{sum Python}
BuildArch:      noarch

License:        ASL 2.0
URL:            https://github.com/praiskup/%{name}
Source0:        %pypi_source

BuildRequires: python3-setuptools python3-devel
%if %{with_check}
BuildRequires: python3-pip
%endif
Requires: python3-%{name} = %{version}-%{release}

%description
%desc

%package -n     python3-%name
Summary:        %{sum Python 3}

%description -n python3-%name
%{desc}

%prep
%setup -q

%build
%py3_build


%install
%py3_install



%check
pip3 install pytest==7.1.2 six==1.16.0
%__python3 -m pytest


%files
%license LICENSE
%{_bindir}/argparse-manpage
%{_mandir}/man1/argparse-manpage.1.*
%{python3_sitelib}/build_manpages/cli

%files -n python3-%name
%license LICENSE
%{python3_sitelib}/build_manpages
%{python3_sitelib}/argparse_manpage-%{version}*.egg-info
%exclude %{python3_sitelib}/build_manpages/cli


%changelog
* Tue May 03 2022 Muhammad Falak <mwani@microsoft.com> - 1.5-3
- Drop BR on pytest, six & pip install deps to enable ptest
- License verified

* Tue Aug 10 2021 Olivia Crain <oliviacrain@microsoft.com> - 1.5-2
- Initial CBL-Mariner import from Fedora 33 (license: MIT).
- Remove python2 support, distro specific macros

* Mon Dec 14 2020 Pavel Raiskup <praiskup@redhat.com> - 1.5-1
- new release

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 1.4-3
- Rebuilt for Python 3.9

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jan 24 2020 Pavel Raiskup <praiskup@redhat.com> - 1.4-1
- new release to fix testsuite against Python 3.9

* Tue Jan 07 2020 Pavel Raiskup <praiskup@redhat.com> - 1.3-1
- new release

* Sat Sep 07 2019 Pavel Raiskup <praiskup@redhat.com> - 1.2.2-1
- new release

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.1-6
- Rebuilt for Python 3.8

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Oct 02 2018 Pavel Raiskup <praiskup@redhat.com> - 1.1-3
- drop python3 on F30+ (rhbz#1634992)

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jun 25 2018 Pavel Raiskup <praiskup@redhat.com> - 1.1-1
- v1.1

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.0.0-2
- Rebuilt for Python 3.7

* Mon Feb 19 2018 Pavel Raiskup <praiskup@redhat.com> - 1.0.0-1
- initial RPM packaging
