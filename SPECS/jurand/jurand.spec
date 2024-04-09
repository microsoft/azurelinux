Name:           jurand
Version:        1.3.2
Release:        4%{?dist}
Summary:        A tool for manipulating Java symbols
License:        Apache-2.0
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/fedora-java/jurand

Source0:        https://github.com/fedora-java/jurand/archive/refs/tags/%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  gcc-c++

BuildRequires:  diffutils
BuildRequires:  make
BuildRequires:  rubygem-asciidoctor

Obsoletes:      javapackages-extra < 6.2.0

%description
The tool can be used for patching .java sources in cases where using sed is
insufficient due to Java language syntax. The tool follows Java language rules
rather than applying simple regular expressions on the source code.

%prep
%setup -q

%build
%{make_build} test-compile manpages

%install
export buildroot=%{buildroot}
export bindir=%{_bindir}
export rpmmacrodir=%{_rpmmacrodir}
export mandir=%{_mandir}/man7

./install.sh

%check
make test

%files -f target/installed_files
%dir %{_rpmconfigdir}
%dir %{_rpmmacrodir}
%license LICENSE NOTICE
%doc README.adoc

%changelog
* Thu Mar 21 2024 Riken Maharjan <rmaharjan@microsoft.com> - 1.3.2-4
- Initial CBL-Mariner import from Fedora 40 (license: MIT).
- License Verified

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Nov 21 2023 Marian Koncek <mkoncek@redhat.com> - 1.3.2-1
- Update to upstream version 1.3.2

* Wed Aug 30 2023 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.3.1-3
- Obsolete javapackages-extra

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Mar 23 2023 Marian Koncek <mkoncek@redhat.com> - 1.3.1-1
- Update to upstream version 1.3.1

* Wed Mar 15 2023 Marian Koncek <mkoncek@redhat.com> - 1.3.0-1
- Update to upstream version 1.3.0

* Wed Mar 08 2023 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.2.0-2
- Skip interface keyword as annotation in name matching only

* Wed Mar 08 2023 Marian Koncek <mkoncek@redhat.com> - 1.2.0-1
- Update to upstream version 1.2.0

* Tue Mar 07 2023 Marian Koncek <mkoncek@redhat.com> - 1.1.0-1
- Update to upstream version 1.1.0

* Fri Mar 03 2023 Marian Koncek <mkoncek@redhat.com> - 1.0.2-1
- Update to upstream version 1.0.2

* Wed Mar 01 2023 Marian Koncek <mkoncek@redhat.com> - 1.0.0-1
- Initial build