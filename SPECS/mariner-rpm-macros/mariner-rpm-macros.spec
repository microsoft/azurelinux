%global rcdir %{_lib}/rpm/mariner
Summary:        Mariner specific rpm macro files
Name:           mariner-rpm-macros
Version:        1.0
Release:        10%{?dist}
License:        GPL+
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/System
Source0:        macros
Source1:        rpmrc
Source2:        default-hardened-cc1
Source3:        default-hardened-ld
Source4:        default-annobin-cc1
Source5:        macros.check
Source6:        macros.python
Source7:        macros.python2
Source8:        macros.python3
Source9:        macros.python-srpm
Source10:       macros.openblas-srpm
Source11:       macros.nodejs-srpm
Source12:       macros.mono-srpm
Source13:       macros.ocaml-srpm
Source14:       macros.perl-srpm
Source15:       gpgverify
Source16:       pythondist.attr
Source17:       pythondistdeps.py
Provides:       redhat-rpm-config
Provides:       openblas-srpm-macros
Provides:       ocaml-srpm-macros
Provides:       perl-srpm-macros
BuildArch:      noarch

%description
Mariner specific rpm macro files.

%package -n mariner-check-macros
Summary:        Mariner specific rpm macros to override default %%check behavior
Group:          Development/System

%description -n mariner-check-macros
Mariner specific rpm macros to override default %%check behavior

%package -n mariner-python-macros
Summary:        Mariner python macros
Group:          Development/System
Provides:       python-srpm-macros
Provides:       python-rpm-macros
Provides:       python2-rpm-macros
Provides:       python3-rpm-macros

%description -n mariner-python-macros
Mariner python macros

%prep
%setup -q -c -T
cp -p %{sources} .

%install
mkdir -p %{buildroot}%{rcdir}
install -p -m 644 -t %{buildroot}%{rcdir} macros rpmrc
install -p -m 444 -t %{buildroot}%{rcdir} default-hardened-*
install -p -m 444 -t %{buildroot}%{rcdir} default-annobin-*
install -p -m 755 -t %{buildroot}%{rcdir} gpgverify

mkdir -p %{buildroot}%{_rpmconfigdir}/macros.d
install -p -m 644 -t %{buildroot}%{_rpmconfigdir}/macros.d macros.*
mkdir -p %{buildroot}%{_fileattrsdir} 
install -p -m 644 -t %{buildroot}%{_fileattrsdir} pythondist.attr
install -p -m 755 -t %{buildroot}%{_rpmconfigdir} pythondistdeps.py

%files
%defattr(-,root,root)
%{rcdir}/macros
%{rcdir}/rpmrc
%{rcdir}/default-hardened-*
%{rcdir}/default-annobin-*
%{rcdir}/gpgverify
%{_rpmconfigdir}/macros.d/macros.openblas-srpm
%{_rpmconfigdir}/macros.d/macros.nodejs-srpm
%{_rpmconfigdir}/macros.d/macros.mono-srpm
%{_rpmconfigdir}/macros.d/macros.ocaml-srpm
%{_rpmconfigdir}/macros.d/macros.perl-srpm

%files -n mariner-check-macros
%{_rpmconfigdir}/macros.d/macros.check

%files -n mariner-python-macros
%{_rpmconfigdir}/macros.d/macros.python*
%{_fileattrsdir}/pythondist.attr
%{_rpmconfigdir}/pythondistdeps.py

%changelog
* Mon Jan 04 2021 Ruying Chen <v-ruyche@microsoft.com> - 1.0-10
- Enable python dependency generator for dist provides.

* Wed Nov 04 2020 Joe Schmitt <joschmit@microsoft.com> - 1.0-9
- Define meson macros.

* Mon Nov 02 2020 Ruying Chen <v-ruyche@microsoft.com> - 1.0-8
- Define gpgverify macro.

* Thu Oct 22 2020 Joe Schmitt <joschmit@microsoft.com> - 1.0-7
- Define __make macro.

* Mon Sep 28 2020 Joe Schmitt <joschmit@microsoft.com> - 1.0-6
- Add backwards compatibility macros for compiling and linking.
- Define _fmoddir macro.
- Turn on perl_bootstrap by default.
- Add perl-srpm macros.

* Mon Sep 28 2020 Ruying Chen <v-ruyche@microsoft.com> - 1.0-5
- Add srpm macros.
- Add python related macros derived from Fedora 32 python-rpm-macros.

* Mon Sep 28 2020 Joe Schmitt <joschmit@microsoft.com> - 1.0-4
- Add ldconfig_scriptlets related macros derived from Fedora 32 redhat-rpm-config.

* Tue Jun 23 2020 Henry Beberman <henry.beberman@microsoft.com> - 1.0-3
- Add macros.check to support non-fatal check section runs for log collection.

* Mon Jun 08 2020 Henry Beberman <henry.beberman@microsoft.com> - 1.0-2
- Add vendor folder. Add optflags related macros and rpmrc derived from Fedora 32.

* Fri May 22 2020 Ruying Chen <v-ruyche@microsoft.com> - 1.0-1
- Original version for CBL-Mariner
