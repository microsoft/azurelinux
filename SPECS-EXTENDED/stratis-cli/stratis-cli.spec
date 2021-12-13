Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:           stratis-cli
Version:        2.0.1
Release:        2%{?dist}
Summary:        Command-line tool for interacting with the Stratis daemon

License:        ASL 2.0
URL:            https://github.com/stratis-storage/stratis-cli
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  /usr/bin/a2x
# It runs without, but totally useless
Requires:       (stratisd >= 2.0.0 with stratisd < 3.0.0)

# stratisd only available on certain arches
ExclusiveArch:  %{rust_arches} noarch
BuildArch:      noarch

%description
stratis provides a command-line interface (CLI) for
interacting with the Stratis daemon, stratisd. stratis
interacts with stratisd via D-Bus.

%prep
%autosetup

%build
%py3_build
a2x -f manpage docs/stratis.txt

%install
%py3_install
install -Dpm0644 -t %{buildroot}%{_datadir}/bash-completion/completions \
  shell-completion/bash/stratis
install -Dpm0644 -t %{buildroot}%{_datadir}/zsh/site-functions \
  shell-completion/zsh/_stratis
install -Dpm0644 -t %{buildroot}%{_mandir}/man8 docs/stratis.8

%files
%license LICENSE
%doc README.rst
%{_bindir}/stratis
%{_mandir}/man8/stratis.8*
%dir %{_datadir}/bash-completion
%dir %{_datadir}/bash-completion/completions
%{_datadir}/bash-completion/completions/stratis
%dir %{_datadir}/zsh
%dir %{_datadir}/zsh/site-functions
%{_datadir}/zsh/site-functions/_stratis
%{python3_sitelib}/stratis_cli/
%{python3_sitelib}/stratis_cli-*.egg-info/

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.0.1-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Feb 19 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 2.0.1-1
- Update to 2.0.1

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Nov 07 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.0.0-1
- Update to 2.0.0

* Sat Sep 07 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.0.4-1
- Update to 1.0.4

* Sat Nov 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.0.0-3
- Make package archful

* Thu Sep 27 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.0.0-2
- Bump stratisd req

* Thu Sep 27 2018 Andy Grover <agrover@redhat.com> - 1.0.0-1
- Update to 1.0.0

* Fri Aug 31 2018 Andy Grover <agrover@redhat.com> - 0.9.0-1
- Update to 0.9.0

* Fri Aug 3 2018 Andy Grover <agrover@redhat.com> - 0.5.5-3
- Remove zsh completions subpackage
- Own completion directories

* Thu Aug 2 2018 Andy Grover <agrover@redhat.com> - 0.5.5-1
- Update to 0.5.5
- Add zsh completions subpackage

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.5.3-2
- Rebuilt for Python 3.7

* Mon Jun 4 2018 Andy Grover <agrover@redhat.com> - 0.5.3-1
- Update to 0.5.3

* Tue May 1 2018 Andy Grover <agrover@redhat.com> - 0.5.2-1
- Update to 0.5.2

* Wed Apr 04 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.5.0-3
- Fix dependency on stratisd

* Tue Apr 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.5.0-2
- Relax stratisd dependency

* Thu Mar 08 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.5.0-1
- Update to 0.5.0

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Jan 19 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.0.5-3
- Enable usage of dependency generator

* Mon Jan 08 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.0.5-2
- Include manpage

* Mon Jan 08 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.0.5-1
- Initial package
