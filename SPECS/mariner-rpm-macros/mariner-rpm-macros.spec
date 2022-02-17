Summary:	Mariner specific rpm macro files
Name:		mariner-rpm-macros
Version:	1.0
Release:	8%{?dist}
License:	GPL+
Group:		Development/System
Vendor:		Microsoft Corporation
Distribution:	Mariner
Source0: macros
Source1: rpmrc
Source2: default-hardened-cc1
Source3: default-hardened-ld
Source4: default-annobin-cc1
Source5: macros.check
Source6: gen-ld-script.sh

BuildArch: noarch


%global rcdir /usr/lib/rpm/mariner

%description
Mariner specific rpm macro files.

%package -n mariner-check-macros
Summary:        Mariner specific rpm macros to override default %%check behavior
License:        GPL+
Group:          Development/System

%description -n mariner-check-macros
Mariner specific rpm macros to override default %%check behavior

%prep
%setup -c -T
cp -p %{sources} .

%install
mkdir -p %{buildroot}%{rcdir}
install -p -m 644 -t %{buildroot}%{rcdir} macros rpmrc
install -p -m 444 -t %{buildroot}%{rcdir} default-hardened-*
install -p -m 444 -t %{buildroot}%{rcdir} default-annobin-*
install -p -m 755 -t %{buildroot}%{rcdir} gen-ld-script.sh

mkdir -p %{buildroot}%{_rpmconfigdir}/macros.d
install -p -m 644 -t %{buildroot}%{_rpmconfigdir}/macros.d macros.*

%files
%defattr(-,root,root)
%{rcdir}/macros
%{rcdir}/rpmrc
%{rcdir}/default-hardened-*
%{rcdir}/default-annobin-*
%{rcdir}/gen-ld-script.sh

%files -n mariner-check-macros
%{_rpmconfigdir}/macros.d/macros.check

%changelog
* Wed Feb 16 2022 Andrew Phelps <anphel@microsoft.com> - 1.0-8
- Use _topdir variable with gen-ld-script.sh

* Thu Jan 20 2022 Cameron Baird <cameronbaird@microsoft.com> - 1.0-7
- add sed step to os_install_post to remove references to module_info.ld in pkgconfigs

* Tue Nov 02 2021 Andrew Phelps <anphel@microsoft.com> - 1.0-6
- Generate module_info.ld directory as needed.

* Mon Aug 23 2021 Andrew Phelps <anphel@microsoft.com> - 1.0-5
- Add gen-ld-script.sh to generate ELF note metadata

* Wed Jun 30 2021 Andrew Phelps <anphel@microsoft.com> - 1.0-4
- Modify macros to only strip debug symbols when debug_package is enabled

* Tue Jun 23 2020 Henry Beberman <henry.beberman@microsoft.com> - 1.0-3
- Add macros.check to support non-fatal check section runs for log collection.

* Mon Jun 08 2020 Henry Beberman <henry.beberman@microsoft.com> - 1.0-2
- Add vendor folder. Add optflags related macros and rpmrc derived from Fedora 32.

* Fri May 22 2020 Ruying Chen <v-ruyche@microsoft.com> - 1.0-1
- Original version for CBL-Mariner
