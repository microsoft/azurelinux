%global srcname tqdm
%global _description \
tqdm (read taqadum, تقدّم) means "progress" in Arabic.\
\
Instantly make your loops show a smart progress meter - just wrap any iterable\
with "tqdm(iterable)", and you are done!
Summary:        Fast, Extensible Progress Meter
Name:           python-%{srcname}
Version:        4.63.1
Release:        1%{?dist}
License:        MPLv2.0 AND MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/tqdm/tqdm
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/%{srcname}-%{version}.tar.gz
BuildArch:      noarch

%description %{_description}

%package -n python3-%{srcname}
%{?python_provide:%python_provide python3-%{srcname}}
Summary:        %{summary}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-setuptools_scm
BuildRequires:  python3-wheel

%description -n python3-%{srcname} %{_description}

Python 3 version.

%prep
%autosetup -n %{srcname}-%{version}

%build
%py3_build

%install
%py3_install

mkdir -p %{buildroot}%{_mandir}/man1/
mv -v %{buildroot}%{python3_sitelib}/%{srcname}/%{srcname}.1 %{buildroot}%{_mandir}/man1/

%check
pip3 install tox
tox -e setup.py

%files -n python3-%{srcname}
%license LICENCE
%doc README.rst examples
%{_bindir}/%{srcname}
%{_mandir}/man1/%{srcname}.1*
%{python3_sitelib}/%{srcname}-*.egg-info/
%{python3_sitelib}/%{srcname}/


%changelog
* Mon Mar 28 2022 Jon Slobodzian <joslobo@microsoft.com> - 4.63.1-1
- Updating to version 4.63.1.

* Mon Jun 21 2021 Rachel Menge <rachelmenge@microsoft.com> - 4.50.2-2
- Initial CBL-Mariner import from Fedora 33 (license: MIT)
- License verified

* Fri Oct 09 2020 Stephen Gallagher <sgallagh@redhat.com> - 4.50.2-1
- Update to 4.50.2

* Mon Sep 28 2020 Stephen Gallagher <sgallagh@redhat.com> - 4.50.0-1
- Update to 4.50.0

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.47.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jun 29 2020 Stephen Gallagher <sgallagh@redhat.com> - 4.47.0-1
- Update to 4.47.0

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 4.45.0-2
- Rebuilt for Python 3.9

* Fri Apr 03 2020 Stephen Gallagher <sgallagh@redhat.com> - 4.45.0-1
- Update to 4.45.0

* Mon Feb 10 2020 Stephen Gallagher <sgallagh@redhat.com> - 4.42.1-1
- Update to 4.42.1

* Mon Feb 10 2020 Stephen Gallagher <sgallagh@redhat.com> - 4.41.1-1
- Update to 4.41.1

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.37.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Nov 08 2019 Stephen Gallagher <sgallagh@redhat.com> - 4.37.0-1
- Update to 4.37.0

* Wed Oct 02 2019 Stephen Gallagher <sgallagh@redhat.com> - 4.36.1-1
- Update to 4.36.1

* Wed Sep 04 2019 Stephen Gallagher <sgallagh@redhat.com> - 4.35.0-1
- Update to 4.35.0

* Fri Aug 23 2019 Stephen Gallagher <sgallagh@redhat.com> - 4.34.0-1
- Update to 4.34.0

* Thu Aug 15 2019 Orion Poplawski <orion@nwra.com> - 4.33.0-1
- Update to 4.33.0

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.28.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.28.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Nov 20 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 4.28.1-2
- Drop python2 subpackage

* Mon Nov 19 2018 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 4.28.1-1
- Update to latest upstream release

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.19.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 4.19.6-2
- Rebuilt for Python 3.7

* Tue Mar 06 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 4.19.6-1
- Update to 4.19.6

* Fri Feb 23 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 4.19.5-1
- Update to 4.19.5

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.15.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.15.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jul 23 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 4.15.0-1
- Update to 4.15.0

* Thu Jun 01 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 4.14.0-1
- Update to 4.14.0

* Sat Feb 11 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 4.11.2-1
- Update to 4.11.2

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.11.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jan 20 2017 Igor Gnatenko <ignatenko@redhat.com> - 4.11.1-1
- Update to 4.11.1

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 4.10.0-2
- Rebuild for Python 3.6

* Sun Nov 13 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 4.10.0-1
- Update to 4.10.0

* Mon Oct 31 2016 Igor Gnatenko <ignatenko@redhat.com> - 4.9.0-1
- Update to 4.9.0

* Tue Aug 16 2016 Igor Gnatenko <ignatenko@redhat.com> - 4.8.3-1
- Update to 4.8.3

* Fri Jul 22 2016 Igor Gnatenko <ignatenko@redhat.com> - 4.7.6-1
- Update to 4.7.6

* Thu Jun 23 2016 Igor Gnatenko <ignatenko@redhat.com> - 4.7.4-1
- Initial package
