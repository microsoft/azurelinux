Summary:        RPM dependency generator hooks for MPI packages
Name:           rpm-mpi-hooks
Version:        8
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://src.fedoraproject.org/rpms/rpm-mpi-hooks
Source0:        https://src.fedoraproject.org/rpms/rpm-mpi-hooks/raw/f37/f/mpi.attr
Source1:        mpilibsymlink.attr
Source2:        mpi.prov
Source3:        mpi.req
Source4:        LICENSE
# Instead of adding a BuildRequires to every MPI implementation spec
Requires:       environment(modules)
Requires:       filesystem
BuildArch:      noarch

%description
RPM dependency generator hooks for MPI packages. This package should be added
as a BuildRequires to all mpi implementations (i.e. openmpi, mpich) as well as
a Requires to the their -devel packages.

%prep
cp -a %{SOURCE4} .


%build
# Nothing to build


%install
install -Dpm 0644 %{SOURCE0} %{buildroot}%{_rpmconfigdir}/fileattrs/mpi.attr
install -Dpm 0644 %{SOURCE1} %{buildroot}%{_rpmconfigdir}/fileattrs/mpilibsymlink.attr
install -Dpm 0755 %{SOURCE2} %{buildroot}%{_rpmconfigdir}/mpi.prov
install -Dpm 0755 %{SOURCE3} %{buildroot}%{_rpmconfigdir}/mpi.req


%files
%license LICENSE
%{_rpmconfigdir}/fileattrs/mpi.attr
%{_rpmconfigdir}/fileattrs/mpilibsymlink.attr
%{_rpmconfigdir}/mpi.req
%{_rpmconfigdir}/mpi.prov

%changelog
* Fri Feb 03 2023 Riken Maharjan <rmaharjan@microsoft.com> - 8-1
- Move from extended to Core.
- Update to 8.

* Fri Apr 29 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 6-8
- Fixing source URL.

* Mon Apr 25 2022 Mateusz Malisz <mamalisz@microsoft.com> - 6-7
- Update Source0
- License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 6-6
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Nov 15 2019 Orion Poplawski <orion@nwra.com> - 6-4
- Allow for no MPI_PYTHON{2}_SITEARCH

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Dec  4 2018 Orion Poplawski <orion@nwra.com> - 6-1
- Avoid trying to load mpi/ directory as a module
- Handle old MPI_PYTHON_SITEARCH and MPI_PYTHON3_SITEARCH conditionally for EL7

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Apr 17 2017 Orion Poplawski <orion@cora.nwra.com> - 5-1
- Exclude build-id files from symlink requires path (bug #1435690)

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu May 12 2016 Sandro Mani <manisandro@gmail.com> 4-1
- Use RPM_BUILD_ROOT directly instead of passing it as an argument
- Use MPI_PYTHON3_SITEARCH

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan 08 2016 Sandro Mani <manisandro@gmail.com> 3-5
- Add quotes around strings which may contain spaces

* Tue Dec 22 2015 Orion Poplawski <orion@cora.nwra.com> - 3-4
- Require environment(modules)

* Mon Nov 2 2015 Orion Poplawski <orion@cora.nwra.com> - 3-3
- Drop requires rpm-build, fileattrs now owned by rpm

* Mon Aug 17 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3-2
- Also handle modules for Python 3

* Mon Aug 10 2015 Sandro Mani <manisandro@gmail.com> 3-1
- Also handle binaries in $MPI_FORTRAN_MOD_DIR and $MPI_PYTHON_SITEARCH

* Sun Jul 26 2015 Sandro Mani <manisandro@gmail.com> 2-1
- Add %%__mpi_magic, %%__mpi_flags to mpi.attrs
- Add mpilibsymlink.attr

* Thu Jul 09 2015 Sandro Mani <manisandro@gmail.com> 1.0-4
- mpi.prov, mpi.req: Use "module -t avail" instead of "module avail"
- mpi.prov, mpi.req: Also look in moduledirs in %%buildroot
- mpi.attrs: add %%__libsymlink_exclude_path

* Thu Jul 09 2015 Sandro Mani <manisandro@gmail.com> 1.0-3
- Add LICENSE

* Thu Jul 09 2015 Sandro Mani <manisandro@gmail.com> 1.0-2
- BuildRequires: rpm -> rpm-build
- Change license to MIT

* Thu Jul 09 2015 Sandro Mani <manisandro@gmail.com> 1.0-1
- Initial package
