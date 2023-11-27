%global debug_package %{nil}
%global __os_install_post %{nil}

# Globals which should be in a macro file.
# These should be set programatically in the future.
%global _host_arch      x86_64
%global _target_arch    aarch64

%global _tuple          %{_target_arch}-%{_vendor}-linux-gnu
%global _cross_name     %{_target_arch}-%{_vendor}-linux-gnu

# Folders which should be in our macro file
%global _opt                /opt/
%global _crossdir           /opt/cross/

# Generally we include '/usr' in most paths.
# Can we also use '/usr' for our paths? This will bring us in line with the
# %%configure macro which sets these.
%global _bindir            /bin
%global _sbindir           /sbin
%global _libdir            /lib
%global _lib64dir          /lib64
%global _libexecdir        /libexec
%global _datadir           /share
%global _docdir            /share/doc
%global _includedir        /include
%global _infodir           /share/info
%global _mandir            /share/man
%global _oldincludedir     /include

# If we want our cross compile aware packges to also support native, we
# need logic to switch modes something like this:
%if "%{_target_arch}" != "%{_host_arch}"
%global _cross_prefix       %{_crossdir}%{_tuple}/
%global _cross_sysroot      %{_crossdir}%{_tuple}/sysroot/
%global _cross_includedir   /usr/%{_host}/%{_tuple}/include/
%global _cross_infodir      %{_crossdir}%{_tuple}/share/info
%global _cross_bindir       %{_tuple}/bin
%global _cross_libdir       %{_tuple}/lib
%global _tuple_name         %{_tuple}-

%global __strip %{_cross_prefix}%{_bindir}/%{_tuple_name}strip
%global __objdump %{_cross_prefix}%{_bindir}/%{_tuple_name}objdump
%else
%global _cross_prefix       %{nil}
%global _cross_sysroot      %{nil}
%global _cross_includedir   %{_includedir}
%global _cross_infodir      %{_infodir}
%global _cross_bindir       %{_bindir}
%global _cross_libdir       %{_libdir}
%global _tuple_name         %{nil}
%endif

Summary:        Contains the GNU compiler collection, binutils, glibc, kernel headers
Name:           %{_cross_name}-cross-gcc
Version:        0.1.0
Release:        1%{?dist}
License:        GPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Tools
BuildRequires:  %{_cross_name}-binutils
BuildRequires:  %{_cross_name}-kernel-headers
BuildRequires:  %{_cross_name}-glibc-bootstrap2
BuildRequires:  %{_cross_name}-gcc-bootstrap3
BuildRequires:  grep
AutoReqProv:    no
ExclusiveArch:  x86_64
Conflicts:      %{_cross_name}-gcc-bootstrap
Conflicts:      %{_cross_name}-gcc-bootstrap2
Conflicts:      %{_cross_name}-gcc-bootstrap3
Conflicts:      %{_cross_name}-glibc-bootstrap
Conflicts:      %{_cross_name}-glibc-bootstrap2
Conflicts:      %{_cross_name}-kernel-headers
Requires:       libmpc

%description
Bundle of all files needed to cross compile with gcc including: gcc, glibc, binutils, kernel headers.

%build
# Find all non-license files and place in a manifest.
rpm -ql %{_cross_name}-binutils %{_cross_name}-kernel-headers %{_cross_name}-glibc-bootstrap2 %{_cross_name}-gcc-bootstrap3 | \
    grep --invert-match "%{_datadir}/licenses/" | \
    sort --unique > %{_cross_name}-file_manifest_with_dirs.txt

# Find all the license files, append a package specific name, and place them in a new license folder
# ie
#   "/share/licenses/aarch64-mariner-linux-gnu-glibc-bootstrap2-2.28/LICENSES"
# becomes:
#   "./licenses/glibc-LICENSES"

install -vdm 755 %{_builddir}/licenses
#binutils
for license in $(rpm -qL %{_cross_name}-binutils); do
    new_name=binutils-$(basename ${license})
    cp ${license} ./licenses/${new_name}
done
#kernel-headers
for license in $(rpm -qL %{_cross_name}-kernel-headers); do
    new_name=kernel-headers-$(basename ${license})
    cp ${license} ./licenses/${new_name}
done
#glibc
for license in $(rpm -qL %{_cross_name}-glibc-bootstrap2); do
    new_name=glibc-$(basename ${license})
    cp ${license} ./licenses/${new_name}
done
#gcc
for license in $(rpm -qL %{_cross_name}-gcc-bootstrap3); do
    new_name=gcc-$(basename ${license})
    cp ${license} ./licenses/${new_name}
done

ls ./licenses/

%install
for source_file in $(cat %{_cross_name}-file_manifest_with_dirs.txt | sort --unique); do
    target_file=%{buildroot}/${source_file}
    target_dir=$(dirname ${target_file})
    ls ${target_file} || true
    if [ -f ${target_file} -o -d ${target_file} ]; then
        echo "skipping file which already exists: '${target_file}'"
    else
        mkdir -p ${target_dir}
        cp -r ${source_file} ${target_file}
    fi

    # Create a new manifest which does not claim ownership of any directories (avoids "file listed twice" warnings)
    if [ ! -d "${source_file}" ]; then
        echo "${source_file}" >> %{_cross_name}-file_manifest.txt
    fi
done
install -D %{_cross_name}-file_manifest.txt %{buildroot}/%{_cross_prefix}/%{_cross_name}-file_manifest.txt

# Create a symlink from sysroot/usr/include to sysroot/include
# The GCC toolchain will look for header files under sysroot/usr/include
mkdir -p %{buildroot}/%{_cross_sysroot}/usr
ln -s "../include" %{buildroot}/%{_cross_sysroot}/usr

# Turning off so we don't get ldconfig errors for crossarch packages
# Add the /opt/cross libs to the ldcache
# mkdir -p %%{buildroot}%%{_sysconfdir}/ld.so.conf.d/
# echo %%{buildroot}%%{_sysconfdir}/ld.so.conf.d/%%{name}.conf
# cat > %%{buildroot}%%{_sysconfdir}/ld.so.conf.d/%%{name}.conf <<EOF
# %%{_cross_prefix}%%{_tuple}%%{_lib64dir}
# EOF
# cat %%{buildroot}%%{_sysconfdir}/ld.so.conf.d/%%{name}.conf

# %%post   -p /sbin/ldconfig
# %%postun -p /sbin/ldconfig

%files -f %{_cross_name}-file_manifest.txt
%defattr(-,root,root)
%license licenses/*
#%%{_sysconfdir}/ld.so.conf.d/%%{name}.conf
%{_cross_prefix}/%{_cross_name}-file_manifest.txt
%{_cross_sysroot}/usr

%changelog
* Tue Feb 23 2021 Daniel McIlvaney <damcilva@microsoft.com> - 0.1.0-1
- Initial version for Mariner
