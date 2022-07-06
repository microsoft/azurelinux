Vendor:         Microsoft Corporation
Distribution:   Mariner
%global modname argcomplete

%bcond_without check

Name:          python-%{modname}
Summary:       Bash tab completion for argparse
Version:       1.10.0
Release:       6%{?dist}
License:       ASL 2.0
URL:           https://github.com/kislyuk/argcomplete
Source0:       %pypi_source argcomplete

%if %{with check}
BuildRequires: tcsh
BuildRequires: fish
%endif

BuildArch:     noarch

%global _description \
Argcomplete provides easy, extensible command line tab completion of\
arguments for your Python script.\
\
It makes two assumptions:\
\
 * You are using bash as your shell\
 * You are using argparse to manage your command line arguments/options\
\
Argcomplete is particularly useful if your program has lots of\
options or subparsers, and if your program can dynamically suggest\
completions for your argument/option values (for example, if the user\
is browsing resources over the network).

%description %{_description}

%package -n python3-%{modname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{modname}}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%if %{with check}
BuildRequires:  python3-pexpect
%endif
# pkg_resources module is used from python-argcomplete-check-easy-install-script
Requires:       python3-setuptools

%description -n python3-%{modname} %{_description}

Python 3 version.

%prep
%autosetup -n %{modname}-%{version}
# Remove useless BRs
sed -i -r -e '/tests_require = /s/"(coverage|flake8|wheel)"[, ]*//g' setup.py
# https://github.com/kislyuk/argcomplete/issues/255
# https://github.com/kislyuk/argcomplete/issues/256
sed -i -e "1s|#!.*python.*|#!%{__python3}|" test/prog scripts/*
sed -i -e "s|python |python3 |" test/test.py

%build
%py3_build

%install
%py3_install
mkdir -p %{buildroot}%{_sysconfdir}/bash_completion.d/
install -p -m0644 %{buildroot}%{python3_sitelib}/%{modname}/bash_completion.d/python-argcomplete.sh %{buildroot}%{_sysconfdir}/bash_completion.d/

%if %{with check}
%check
%{__python3} setup.py test
%endif

%files -n python3-%{modname}
%license LICENSE.rst
%doc README.rst
%{python3_sitelib}/%{modname}-*.egg-info/
%{python3_sitelib}/%{modname}/
%{_bindir}/activate-global-python-argcomplete
%{_bindir}/python-argcomplete-check-easy-install-script
%{_bindir}/python-argcomplete-tcsh
%{_bindir}/register-python-argcomplete
%{_sysconfdir}/bash_completion.d/python-argcomplete.sh

%changelog
* Mon Jul 05 2022 Daniel McIlvaney <damcilva@microsoft.com> - 1.10.0-6
- Bump release due to bump in fish to 3.5.0.
- License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.10.0-5
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.10.0-3
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Fri Aug 16 2019 Miro Hrončok <mhroncok@redhat.com> - 1.10.0-2
- Rebuilt for Python 3.8

* Thu Jul 25 2019 Pierre-Yves Chibon <pingou@pingoured.fr> - 1.10.0-1
- Update to 1.10.0
- Adjust source0 to point to pypi

* Tue Apr 02 2019 Miro Hrončok <mhroncok@redhat.com> - 1.9.5-1
- Update to 1.9.5

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Aug 12 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.9.4-1
- Update to 1.9.4
- Drop python2 subpackage

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 15 2018 Miro Hrončok <mhroncok@redhat.com> - 1.9.3-4
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.9.3-3
- Escape macros in %%changelog

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Nov 19 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.9.3-1
- Update to 1.9.3

* Wed Nov 08 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.9.2-1
- Update to 1.9.2

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 26 2017 Igor Gnatenko <ignatenko@redhat.com> - 1.8.2-1
- Update to 1.8.2

* Thu Jan 26 2017 Igor Gnatenko <ignatenko@redhat.com> - 1.8.1-1
- Update to 1.8.1

* Sat Jan 07 2017 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 1.7.0-1
- Update to 1.7.0 (RHBZ #1339845)

* Fri Dec 09 2016 Charalampos Stratakis <cstratak@redhat.com> - 1.1.1-3
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Sun Mar 27 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 1.1.1-1
- Update to 1.1.1 (RHBZ #1320348)

* Mon Feb 22 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 1.1.0-1
- Update to 1.1.0 (RHBZ #1310473)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Dec 05 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 1.0.0-3
- Ship bash completion file within RPM

* Sat Nov 14 2015 Toshio Kuratomi <toshio@fedoraproject.org> - 1.0.0-2
- A few minor changes to simplify and take care of cornercases

* Sat Nov 14 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@laptop> - 1.0.0-1
- Update to latest version (#1227119)
- Use %%license
- Update to new python packaging style
- Remove 2to3 invocation, the code is already python3 compatible
- Move scripts to python3 subpackage
- Add Provides:/usr/bin/register-python-activate so packages can depend on it

* Fri Nov 06 2015 Robert Kuska <rkuska@redhat.com> - 0.8.9-4
- Rebuilt for Python3.5 rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jun 2 2015 - Steve Traylen <steve.traylen@cern.ch> 0.8.8-2
- Add python3 package (#1225934)

* Tue Jun 02 2015 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 0.8.9-1
- Update to 0.8.9 (#1227119)

* Tue May 5 2015 - Steve Traylen <steve.traylen@cern.ch> 0.8.8-1
- Updating package to 0.8.8

* Sun Dec 14 2014 - Dale Macartney <dbmacartney@fedoraproject.org> 0.8.4-1
- Updating package to 0.8.4

* Fri Sep 12 2014 - Steve Traylen <steve.traylen@cern.ch> 0.8.1-1
- Updating package to 0.8.1

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Apr 14 2014 - Dale Macartney <dbmacartney@fedoraproject.org> 0.8.0-1
- Updating package to 0.8.0

* Sun Mar 30 2014 - Dale Macartney <dbmacartney@fedoraproject.org> 0.7.1-1
- Updating package to 0.7.1

* Mon Mar 24 2014 - Dale Macartney <dbmacartney@fedoraproject.org> 0.7.0-1
- Updating package to 0.7.0

* Mon Jan 13 2014 - Dale Macartney <dbmacartney@fedoraproject.org> 0.6.7-2
- Removing '%%exclude %%{python_sitelib}/test' fom %%files as no longer needed.

* Mon Jan 13 2014 - Dale Macartney <dbmacartney@fedoraproject.org> 0.6.7-1
- Applying latest patch of argcomplete.

* Wed Jan 8 2014 - Dale Macartney <dbmacartney@fedoraproject.org> 0.6.3-4
- Pushing new build for update as previous was not picked up.

* Wed Oct 16 2013 - Dale Macartney <dbmacartney@gmail.com> 0.6.3-3
- Correct missing files for el6

* Tue Oct 15 2013 - Dale Macartney <dbmacartney@gmail.com> 0.6.3-2
- Initial packaging for Fedora Project and including LICENSE.rst in docs

* Thu Jan 31 2013 - Marco Neciarini <marco.nenciarini@2ndquadrant.it> 0.3.5-1
- Initial packaging.
