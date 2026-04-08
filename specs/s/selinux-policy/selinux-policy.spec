## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autochangelog
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Conditionals for policy types (all built by default)
%bcond targeted 1
%bcond minimum  1
%bcond mls      1

# github repo with selinux-policy sources
%global giturl https://github.com/fedora-selinux/selinux-policy
%global commit 08735516ec1c70d4a1de713c6af4b7c7de0de20b
%global shortcommit %(c=%{commit}; echo ${c:0:7})

%define distro redhat
%define polyinstatiate n
%define monolithic n

%define POLICYVER 35
%define POLICYCOREUTILSVER 3.9
%define CHECKPOLICYVER 3.9
# To be updated after major policy changes
%define STABLEVER 42.10
Summary: SELinux policy configuration
Name: selinux-policy
Version: 42.24
Release: 1%{?dist}
License: GPL-2.0-or-later
Source: %{giturl}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
Source1: Makefile.devel
Source2: selinux-policy.conf

# Tool helps during policy development, to expand system m4 macros to raw allow rules
# Git repo: https://github.com/fedora-selinux/macro-expander.git
Source3: macro-expander

# Include SELinux policy for container from separate container-selinux repo
# Git repo: https://github.com/containers/container-selinux.git
Source4: container-selinux.tgz

# modules enabled in -minimum policy
Source16: modules-minimum.lst

Source36: selinux-check-proper-disable.service

# Script to convert /var/run file context entries to /run
Source37: varrun-convert.sh
# Configuration files to dnf-protect targeted and/or mls subpackages
Source38: selinux-policy-targeted.conf
Source39: selinux-policy-mls.conf
# Script to convert /usr/sbin file context entries to /usr/bin
Source40: binsbin-convert.sh

# Provide rpm macros for packages installing SELinux modules
Source5: rpm.macros

Url: %{giturl}
BuildArch: noarch
BuildRequires: python3 gawk checkpolicy >= %{CHECKPOLICYVER} m4 policycoreutils-devel >= %{POLICYCOREUTILSVER} bzip2
BuildRequires: make
BuildRequires: systemd-rpm-macros
BuildRequires: groff
Requires(pre): policycoreutils >= %{POLICYCOREUTILSVER}
Requires(post): /bin/awk /usr/bin/sha512sum
Requires(meta): (rpm-plugin-selinux if rpm-libs)
Requires: selinux-policy-any = %{version}-%{release}
Provides: selinux-policy-base = %{version}-%{release}
Provides: selinux-policy-stable = %{STABLEVER}
Suggests: selinux-policy-targeted

%description
SELinux core policy package.
Originally based off of reference policy,
the policy has been adjusted to provide support for Fedora.

%files
%{!?_licensedir:%global license %%doc}
%license COPYING
%dir %{_datadir}/selinux
%dir %{_datadir}/selinux/packages
%dir %{_sysconfdir}/selinux
%ghost %config(noreplace) %{_sysconfdir}/selinux/config
%ghost %{_sysconfdir}/sysconfig/selinux
%{_usr}/lib/tmpfiles.d/selinux-policy.conf
%{_rpmconfigdir}/macros.d/macros.selinux-policy
%{_unitdir}/selinux-check-proper-disable.service
%{_libexecdir}/selinux/binsbin-convert.sh
%{_libexecdir}/selinux/varrun-convert.sh

%package sandbox
Summary: SELinux sandbox policy
Requires(pre): selinux-policy-base = %{version}-%{release}
Requires(pre): selinux-policy-targeted = %{version}-%{release}

%description sandbox
SELinux sandbox policy for use with the sandbox utility.

%files sandbox
%verify(not md5 size mtime) %{_datadir}/selinux/packages/sandbox.pp

%post sandbox
rm -f %{_sysconfdir}/selinux/*/modules/active/modules/sandbox.pp.disabled 2>/dev/null
rm -f %{_sharedstatedir}/selinux/*/active/modules/disabled/sandbox 2>/dev/null
semodule -n -X 100 -i %{_datadir}/selinux/packages/sandbox.pp 2> /dev/null
if selinuxenabled ; then
    load_policy
fi;
exit 0

%preun sandbox
if [ $1 -eq 0 ] ; then
    semodule -n -d sandbox 2>/dev/null
    if selinuxenabled ; then
        load_policy
    fi;
fi;
exit 0

%package devel
Summary: SELinux policy development files
Requires(pre): selinux-policy = %{version}-%{release}
Requires: selinux-policy = %{version}-%{release}
Requires: m4 checkpolicy >= %{CHECKPOLICYVER}
Requires: /usr/bin/make
Requires(post): policycoreutils-devel >= %{POLICYCOREUTILSVER}

%description devel
SELinux policy development package.
This package contains:
- interfaces, macros, and patterns for policy development
- a policy example
- the macro-expander utility
and some additional files.

%files devel
%{_bindir}/macro-expander
%dir %{_datadir}/selinux/devel
%dir %{_datadir}/selinux/devel/include
%{_datadir}/selinux/devel/include/*
%exclude %{_datadir}/selinux/devel/include/contrib/container.if
%exclude %{_datadir}/selinux/devel/include/contrib/tabrmd.if
%dir %{_datadir}/selinux/devel/html
%{_datadir}/selinux/devel/html/*html
%{_datadir}/selinux/devel/html/*css
%{_datadir}/selinux/devel/Makefile
%{_datadir}/selinux/devel/example.*
%{_datadir}/selinux/devel/policy.*
%ghost %verify(not md5 size mode mtime) %{_sharedstatedir}/sepolgen/interface_info

%post devel
selinuxenabled && sepolgen-ifgen 2>/dev/null
exit 0

%package doc
Summary: SELinux policy documentation
Requires(pre): selinux-policy = %{version}-%{release}
Requires: selinux-policy = %{version}-%{release}

%description doc
SELinux policy documentation package.
This package contains manual pages and documentation of the policy modules.

%files doc
%{_mandir}/man*/*
%exclude %{_mandir}/man8/container_selinux.8.gz
%doc %{_datadir}/doc/%{name}

%define common_params DISTRO=%{distro} UBAC=n DIRECT_INITRC=n MONOLITHIC=%{monolithic} MLS_CATS=1024 MCS_CATS=1024

%define makeCmds() \
%make_build %common_params UNK_PERMS=%3 NAME=%1 TYPE=%2 bare \
%make_build %common_params UNK_PERMS=%3 NAME=%1 TYPE=%2 conf \
install -p -m0644 ./dist/%1/booleans.conf ./policy/booleans.conf \
install -p -m0644 ./dist/%1/users ./policy/users \

%define makeModulesConf() \
install -p -m0644 ./dist/%1/modules.conf ./policy/modules.conf \

%define installCmds() \
%make_build %common_params UNK_PERMS=%3 NAME=%1 TYPE=%2 base.pp \
%make_build %common_params UNK_PERMS=%3 NAME=%1 TYPE=%2 validate modules \
make %common_params UNK_PERMS=%3 NAME=%1 TYPE=%2 DESTDIR=%{buildroot} install \
make %common_params UNK_PERMS=%3 NAME=%1 TYPE=%2 DESTDIR=%{buildroot} install-appconfig \
make %common_params UNK_PERMS=%3 NAME=%1 TYPE=%2 DESTDIR=%{buildroot} SEMODULE="semodule -p %{buildroot} -X 100 " load \
%{__mkdir} -p %{buildroot}%{_sysconfdir}/selinux/%1/logins \
touch %{buildroot}%{_sysconfdir}/selinux/%1/contexts/files/file_contexts.subs \
install -p -m0644 ./config/file_contexts.subs_dist %{buildroot}%{_sysconfdir}/selinux/%1/contexts/files \
install -p -m0644 ./dist/%1/setrans.conf %{buildroot}%{_sysconfdir}/selinux/%1/setrans.conf \
install -p -m0644 ./dist/customizable_types %{buildroot}%{_sysconfdir}/selinux/%1/contexts/customizable_types \
touch %{buildroot}%{_sysconfdir}/selinux/%1/contexts/files/file_contexts.bin \
touch %{buildroot}%{_sysconfdir}/selinux/%1/contexts/files/file_contexts.local \
touch %{buildroot}%{_sysconfdir}/selinux/%1/contexts/files/file_contexts.local.bin \
install -p -m0644 ./dist/booleans.subs_dist %{buildroot}%{_sysconfdir}/selinux/%1 \
rm -f %{buildroot}%{_datadir}/selinux/%1/*pp*  \
sha512sum %{buildroot}%{_sysconfdir}/selinux/%1/policy/policy.%{POLICYVER} | cut -d' ' -f 1 > %{buildroot}%{_sysconfdir}/selinux/%1/.policy.sha512; \
rm -rf %{buildroot}%{_sysconfdir}/selinux/%1/contexts/netfilter_contexts  \
rm -rf %{buildroot}%{_sysconfdir}/selinux/%1/modules/active/policy.kern \
rm -f %{buildroot}%{_sharedstatedir}/selinux/%1/active/*.linked \
%nil

%define fileList() \
%defattr(-,root,root) \
%dir %{_sysconfdir}/selinux/%1 \
%config(noreplace) %{_sysconfdir}/selinux/%1/setrans.conf \
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/selinux/%1/seusers \
%dir %{_sysconfdir}/selinux/%1/logins \
%dir %{_sharedstatedir}/selinux/%1/active \
%verify(not md5 size mtime) %{_sharedstatedir}/selinux/%1/semanage.read.LOCK \
%verify(not md5 size mtime) %{_sharedstatedir}/selinux/%1/semanage.trans.LOCK \
%dir %attr(700,root,root) %dir %{_sharedstatedir}/selinux/%1/active/modules \
%verify(not md5 size mtime) %{_sharedstatedir}/selinux/%1/active/modules/100/base \
%dir %{_sysconfdir}/selinux/%1/policy/ \
%verify(not md5 size mtime) %{_sysconfdir}/selinux/%1/policy/policy.%{POLICYVER} \
%{_sysconfdir}/selinux/%1/.policy.sha512 \
%dir %{_sysconfdir}/selinux/%1/contexts \
%config %verify(not md5 size mtime) %{_sysconfdir}/selinux/%1/contexts/customizable_types \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/securetty_types \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/dbus_contexts \
%config %{_sysconfdir}/selinux/%1/contexts/x_contexts \
%config %{_sysconfdir}/selinux/%1/contexts/default_contexts \
%config %{_sysconfdir}/selinux/%1/contexts/virtual_domain_context \
%config %{_sysconfdir}/selinux/%1/contexts/virtual_image_context \
%config %{_sysconfdir}/selinux/%1/contexts/lxc_contexts \
%config %{_sysconfdir}/selinux/%1/contexts/systemd_contexts \
%config %{_sysconfdir}/selinux/%1/contexts/sepgsql_contexts \
%config %{_sysconfdir}/selinux/%1/contexts/openssh_contexts \
%config %{_sysconfdir}/selinux/%1/contexts/snapperd_contexts \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/default_type \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/failsafe_context \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/initrc_context \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/removable_context \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/userhelper_context \
%dir %{_sysconfdir}/selinux/%1/contexts/files \
%verify(not md5 size mtime) %{_sysconfdir}/selinux/%1/contexts/files/file_contexts \
%ghost %{_sysconfdir}/selinux/%1/contexts/files/file_contexts.bin \
%verify(not md5 size mtime) %{_sysconfdir}/selinux/%1/contexts/files/file_contexts.homedirs \
%ghost %{_sysconfdir}/selinux/%1/contexts/files/file_contexts.homedirs.bin \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/files/file_contexts.local \
%ghost %{_sysconfdir}/selinux/%1/contexts/files/file_contexts.local.bin \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/files/file_contexts.subs \
%{_sysconfdir}/selinux/%1/contexts/files/file_contexts.subs_dist \
%{_sysconfdir}/selinux/%1/booleans.subs_dist \
%config %{_sysconfdir}/selinux/%1/contexts/files/media \
%dir %{_sysconfdir}/selinux/%1/contexts/users \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/users/root \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/users/guest_u \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/users/xguest_u \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/users/user_u \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/users/staff_u \
%dir %{_datadir}/selinux/%1 \
%{_datadir}/selinux/%1/base.lst \
%{_datadir}/selinux/%1/modules.lst \
%{_datadir}/selinux/%1/nonbasemodules.lst \
%dir %{_sharedstatedir}/selinux/%1 \
%verify(not md5 size mtime) %{_sharedstatedir}/selinux/%1/active/commit_num \
%verify(not md5 size mtime) %{_sharedstatedir}/selinux/%1/active/users_extra \
%verify(not md5 size mtime) %{_sharedstatedir}/selinux/%1/active/homedir_template \
%verify(not md5 size mtime) %{_sharedstatedir}/selinux/%1/active/seusers \
%verify(not md5 size mtime) %{_sharedstatedir}/selinux/%1/active/file_contexts \
%verify(not md5 size mtime) %{_sharedstatedir}/selinux/%1/active/policy.kern \
%ghost %{_sharedstatedir}/selinux/%1/active/policy.linked \
%ghost %{_sharedstatedir}/selinux/%1/active/seusers.linked \
%ghost %{_sharedstatedir}/selinux/%1/active/users_extra.linked \
%verify(not md5 size mtime) %{_sharedstatedir}/selinux/%1/active/file_contexts.homedirs \
%verify(not md5 size mtime) %{_sharedstatedir}/selinux/%1/active/modules_checksum \
%ghost %verify(not mode md5 size mtime) %{_sharedstatedir}/selinux/%1/active/modules/400/extra_binsbin \
%ghost %verify(not mode md5 size mtime) %{_sharedstatedir}/selinux/%1/active/modules/400/extra_binsbin/cil \
%ghost %verify(not mode md5 size mtime) %{_sharedstatedir}/selinux/%1/active/modules/400/extra_binsbin/lang_ext \
%ghost %verify(not mode md5 size mtime) %{_sharedstatedir}/selinux/%1/active/modules/400/extra_varrun \
%ghost %verify(not mode md5 size mtime) %{_sharedstatedir}/selinux/%1/active/modules/400/extra_varrun/cil \
%ghost %verify(not mode md5 size mtime) %{_sharedstatedir}/selinux/%1/active/modules/400/extra_varrun/lang_ext \
%nil

%define relabel() \
if [ -s %{_sysconfdir}/selinux/config ]; then \
    . %{_sysconfdir}/selinux/config &> /dev/null || true; \
fi; \
FILE_CONTEXT=%{_sysconfdir}/selinux/%1/contexts/files/file_contexts; \
if selinuxenabled && [ "${SELINUXTYPE}" = %1 -a -f ${FILE_CONTEXT}.pre ]; then \
     fixfiles -C ${FILE_CONTEXT}.pre restore &> /dev/null > /dev/null; \
     rm -f ${FILE_CONTEXT}.pre; \
fi; \
# rebuilding the rpm database still can sometimes result in an incorrect context \
restorecon -R /usr/lib/sysimage/rpm \
# In some scenarios, /usr/bin/httpd is labelled incorrectly after sbin merge. \
# Relabel all files under /usr/bin, in case they got installed before policy \
# was updated and the labels were incorrect. \
restorecon -R /usr/bin /usr/sbin \
if restorecon -e /run/media -R /root /var/log /var/run /etc/passwd* /etc/group* /etc/*shadow* 2> /dev/null;then \
    continue; \
fi;

%define preInstall() \
if [ $1 -ne 1 ] && [ -s %{_sysconfdir}/selinux/config ]; then \
     for MOD_NAME in ganesha ipa_custodia kdbus; do \
        if [ -d %{_sharedstatedir}/selinux/%1/active/modules/100/$MOD_NAME ]; then \
           semodule -n -d $MOD_NAME 2> /dev/null; \
        fi; \
     done; \
     . %{_sysconfdir}/selinux/config; \
     FILE_CONTEXT=%{_sysconfdir}/selinux/%1/contexts/files/file_contexts; \
     if [ "${SELINUXTYPE}" = %1 -a -f ${FILE_CONTEXT} ]; then \
        [ -f ${FILE_CONTEXT}.pre ] || cp -f ${FILE_CONTEXT} ${FILE_CONTEXT}.pre; \
     fi; \
     touch %{_sysconfdir}/selinux/%1/.rebuild; \
     if [ -e %{_sysconfdir}/selinux/%1/.policy.sha512 ]; then \
        POLICY_FILE=`ls %{_sysconfdir}/selinux/%1/policy/policy.* | sort | head -1` \
        sha512=`sha512sum $POLICY_FILE | cut -d ' ' -f 1`; \
	checksha512=`cat %{_sysconfdir}/selinux/%1/.policy.sha512`; \
	if [ "$sha512" == "$checksha512" ] ; then \
		rm %{_sysconfdir}/selinux/%1/.rebuild; \
	fi; \
   fi; \
fi;

%define postInstall() \
if [ -s %{_sysconfdir}/selinux/config ]; then \
    . %{_sysconfdir}/selinux/config &> /dev/null || true; \
fi; \
if [ -e %{_sysconfdir}/selinux/%2/.rebuild ]; then \
   rm %{_sysconfdir}/selinux/%2/.rebuild; \
fi; \
semodule -B -n -s %2 2> /dev/null; \
[ "${SELINUXTYPE}" == "%2" ] && selinuxenabled && load_policy; \
if [ %1 -eq 1 ]; then \
   restorecon -R /root /var/log /run /etc/passwd* /etc/group* /etc/*shadow* 2> /dev/null; \
else \
%relabel %2 \
fi;

%define modulesList() \
awk '$1 !~ "/^#/" && $2 == "=" && $3 == "module" { printf "%%s ", $1 }' ./policy/modules.conf > %{buildroot}%{_datadir}/selinux/%1/modules.lst \
awk '$1 !~ "/^#/" && $2 == "=" && $3 == "base" { printf "%%s ", $1 }' ./policy/modules.conf > %{buildroot}%{_datadir}/selinux/%1/base.lst \

%define nonBaseModulesList() \
modules=`cat %{buildroot}%{_datadir}/selinux/%1/modules.lst` \
for i in $modules; do \
    if [ $i != "sandbox" ];then \
        echo "%verify(not md5 size mtime) %{_sharedstatedir}/selinux/%1/active/modules/100/$i" >> %{buildroot}%{_datadir}/selinux/%1/nonbasemodules.lst \
    fi; \
done;

# Make sure the config is consistent with what packages are installed in the system
# this covers cases when system is installed with selinux-policy-{mls,minimal}
# or selinux-policy-{targeted,mls,minimal} where switched but the machine has not
# been rebooted yet.
# The macro should be called at the beginning of "post" (to make sure load_policy does not fail)
# and in "posttrans" (to make sure that the store is consistent when all package transitions are done)
# Parameter determines the policy type to be set in case of miss-configuration (if backup value is not usable)
# Steps:
# * load values from config and its backup
# * check whether SELINUXTYPE from backup is usable and make sure that it's set in the config if so
# * use "targeted" if it's being installed and BACKUP_SELINUXTYPE cannot be used
# * check whether SELINUXTYPE in the config is usable and change it to newly installed policy if it isn't
%define checkConfigConsistency() \
if [ -f %{_sysconfdir}/selinux/.config_backup ]; then \
    . %{_sysconfdir}/selinux/.config_backup; \
else \
    BACKUP_SELINUXTYPE=targeted; \
fi; \
if [ -s %{_sysconfdir}/selinux/config ]; then \
    . %{_sysconfdir}/selinux/config; \
    if ls %{_sysconfdir}/selinux/$BACKUP_SELINUXTYPE/policy/policy.* &>/dev/null; then \
        if [ "$BACKUP_SELINUXTYPE" != "$SELINUXTYPE" ]; then \
            sed -i 's/^SELINUXTYPE=.*/SELINUXTYPE='"$BACKUP_SELINUXTYPE"'/g' %{_sysconfdir}/selinux/config; \
        fi; \
    elif [ "%1" = "targeted" ]; then \
        if [ "%1" != "$SELINUXTYPE" ]; then \
            sed -i 's/^SELINUXTYPE=.*/SELINUXTYPE=%1/g' %{_sysconfdir}/selinux/config; \
        fi; \
    elif ! ls  %{_sysconfdir}/selinux/$SELINUXTYPE/policy/policy.* &>/dev/null; then \
        if [ "%1" != "$SELINUXTYPE" ]; then \
            sed -i 's/^SELINUXTYPE=.*/SELINUXTYPE=%1/g' %{_sysconfdir}/selinux/config; \
        fi; \
    fi; \
fi;

# Create hidden backup of /etc/selinux/config and prepend BACKUP_ to names
# of variables inside so that they are easy to use later
# This should be done in "pretrans" because config content can change during RPM operations
# The macro has to be used in a script slot with "-p <lua>"
%define backupConfigLua() \
local sysconfdir = rpm.expand("%{_sysconfdir}") \
local config_file = sysconfdir .. "/selinux/config" \
local config_backup = sysconfdir .. "/selinux/.config_backup" \
os.remove(config_backup) \
if posix.stat(config_file) then \
    local f = assert(io.open(config_file, "r"), "Failed to read " .. config_file) \
    local content = f:read("*all") \
    f:close() \
    local backup = content:gsub("SELINUX", "BACKUP_SELINUX") \
    local bf = assert(io.open(config_backup, "w"), "Failed to open " .. config_backup) \
    bf:write(backup) \
    bf:close() \
end

# Remove the local_varrun SELinux module
%define removeVarrunModuleLua() \
if posix.access ("%{_sharedstatedir}/selinux/%1/active/modules/400/extra_varrun/cil", "r") then \
  os.execute ("rm -rf %{_sharedstatedir}/selinux/%1/active/modules/400/extra_varrun") \
end

# Remove the local_binsbin SELinux module
%define removeBinsbinModuleLua() \
if posix.access ("%{_sharedstatedir}/selinux/%1/active/modules/400/extra_binsbin/cil", "r") then \
  os.execute ("rm -rf %{_sharedstatedir}/selinux/%1/active/modules/400/extra_binsbin") \
end

%build

%prep
%autosetup -p 1 -n %{name}-%{commit}
tar -C policy/modules/contrib -xf %{SOURCE4}

%install
# Build targeted policy
%{__rm} -fR %{buildroot}
mkdir -p %{buildroot}%{_sysconfdir}/selinux
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
touch %{buildroot}%{_sysconfdir}/selinux/config
touch %{buildroot}%{_sysconfdir}/sysconfig/selinux
mkdir -p %{buildroot}%{_usr}/lib/tmpfiles.d/
install -p -m0644 %{SOURCE2} %{buildroot}%{_usr}/lib/tmpfiles.d/
mkdir -p %{buildroot}%{_bindir}
install -p -m 755 %{SOURCE3} %{buildroot}%{_bindir}/
mkdir -p %{buildroot}%{_libexecdir}/selinux
install -p -m 755  %{SOURCE37} %{buildroot}%{_libexecdir}/selinux
install -p -m 755  %{SOURCE40} %{buildroot}%{_libexecdir}/selinux

# Always create policy module package directories
mkdir -p %{buildroot}%{_datadir}/selinux/{targeted,mls,minimum,modules}/
mkdir -p %{buildroot}%{_sharedstatedir}/selinux/{targeted,mls,minimum,modules}/

mkdir -p %{buildroot}%{_datadir}/selinux/packages

mkdir -p %{buildroot}%{_sysconfdir}/dnf/protected.d/

# Install devel
make clean
%if %{with targeted}
# Build targeted policy
%makeCmds targeted mcs allow
%makeModulesConf targeted
%installCmds targeted mcs allow
# install permissivedomains.cil
semodule -p %{buildroot} -X 100 -s targeted -i \
    ./dist/permissivedomains.cil
# recreate sandbox.pp
rm -rf %{buildroot}%{_sharedstatedir}/selinux/targeted/active/modules/100/sandbox
%make_build %common_params UNK_PERMS=allow NAME=targeted TYPE=mcs sandbox.pp
mv sandbox.pp %{buildroot}%{_datadir}/selinux/packages/sandbox.pp
%modulesList targeted
%nonBaseModulesList targeted
install -p -m 644 %{SOURCE38} %{buildroot}%{_sysconfdir}/dnf/protected.d/
%endif

%if %{with minimum}
# Build minimum policy
%makeCmds minimum mcs allow
%makeModulesConf targeted
%installCmds minimum mcs allow
rm -rf %{buildroot}%{_sharedstatedir}/selinux/minimum/active/modules/100/sandbox
install -p -m 644 %{SOURCE16} %{buildroot}%{_datadir}/selinux/minimum/modules-enabled.lst
%modulesList minimum
%nonBaseModulesList minimum
%endif

%if %{with mls}
# Build mls policy
%makeCmds mls mls deny
%makeModulesConf mls
%installCmds mls mls deny
%modulesList mls
%nonBaseModulesList mls
install -p -m 644 %{SOURCE39} %{buildroot}%{_sysconfdir}/dnf/protected.d/
%endif

# remove leftovers when save-previous=true (semanage.conf) is used
rm -rf %{buildroot}%{_sharedstatedir}/selinux/{minimum,targeted,mls}/previous

make %common_params UNK_PERMS=allow NAME=targeted TYPE=mcs DESTDIR=%{buildroot} PKGNAME=%{name} install-docs
make %common_params UNK_PERMS=allow NAME=targeted TYPE=mcs DESTDIR=%{buildroot} PKGNAME=%{name} install-headers
mkdir %{buildroot}%{_datadir}/selinux/devel/
mv %{buildroot}%{_datadir}/selinux/targeted/include %{buildroot}%{_datadir}/selinux/devel/include
install -p -m 644 %{SOURCE1} %{buildroot}%{_datadir}/selinux/devel/Makefile
install -p -m 644 doc/example.* %{buildroot}%{_datadir}/selinux/devel/
install -p -m 644 doc/policy.* %{buildroot}%{_datadir}/selinux/devel/
sepolicy manpage -a -p %{buildroot}%{_mandir}/man8/ -w -r %{buildroot}
mkdir %{buildroot}%{_datadir}/selinux/devel/html
mv %{buildroot}%{_datadir}/man/man8/*.html %{buildroot}%{_datadir}/selinux/devel/html
mv %{buildroot}%{_datadir}/man/man8/style.css %{buildroot}%{_datadir}/selinux/devel/html

mkdir -p %{buildroot}%{_rpmconfigdir}/macros.d
install -p -m 644 %{SOURCE5} %{buildroot}%{_rpmconfigdir}/macros.d/macros.selinux-policy
sed -i 's/SELINUXPOLICYVERSION/%{version}/' %{buildroot}%{_rpmconfigdir}/macros.d/macros.selinux-policy
sed -i 's/SELINUXPOLICYSTABLE/%{STABLEVER}/' %{buildroot}%{_rpmconfigdir}/macros.d/macros.selinux-policy
sed -i 's@SELINUXSTOREPATH@%{_sharedstatedir}/selinux@' %{buildroot}%{_rpmconfigdir}/macros.d/macros.selinux-policy

mkdir -p %{buildroot}%{_unitdir}
install -p -m 644 %{SOURCE36} %{buildroot}%{_unitdir}

%post
%systemd_post selinux-check-proper-disable.service
if [ ! -s %{_sysconfdir}/selinux/config ]; then
#
#     New install so we will default to targeted policy
#
echo "
# This file controls the state of SELinux on the system.
# SELINUX= can take one of these three values:
#     enforcing - SELinux security policy is enforced.
#     permissive - SELinux prints warnings instead of enforcing.
#     disabled - No SELinux policy is loaded.
# See also:
# https://docs.fedoraproject.org/en-US/quick-docs/getting-started-with-selinux/#getting-started-with-selinux-selinux-states-and-modes
#
# NOTE: In earlier Fedora kernel builds, SELINUX=disabled would also
# fully disable SELinux during boot. If you need a system with SELinux
# fully disabled instead of SELinux running with no policy loaded, you
# need to pass selinux=0 to the kernel command line. You can use grubby
# to persistently set the bootloader to boot with selinux=0:
#
#    grubby --update-kernel ALL --args selinux=0
#
# To revert back to SELinux enabled:
#
#    grubby --update-kernel ALL --remove-args selinux
#
SELINUX=enforcing
# SELINUXTYPE= can take one of these three values:
#     targeted - Targeted processes are protected,
#     minimum - Modification of targeted policy. Only selected processes are protected.
#     mls - Multi Level Security protection.
SELINUXTYPE=targeted

" > %{_sysconfdir}/selinux/config

     ln -sf ../selinux/config %{_sysconfdir}/sysconfig/selinux
     restorecon %{_sysconfdir}/selinux/config 2> /dev/null || :
else
     . %{_sysconfdir}/selinux/config
fi
exit 0

%preun
%systemd_preun selinux-check-proper-disable.service

%postun
%systemd_postun selinux-check-proper-disable.service
if [ $1 = 0 ]; then
     setenforce 0 2> /dev/null
     if [ ! -s %{_sysconfdir}/selinux/config ]; then
          echo "SELINUX=disabled" > %{_sysconfdir}/selinux/config
     else
          sed -i 's/^SELINUX=.*/SELINUX=disabled/g' %{_sysconfdir}/selinux/config
     fi
fi
exit 0

%if %{with targeted}
%package targeted
Summary: SELinux targeted policy
Provides: selinux-policy-any = %{version}-%{release}
Obsoletes: selinux-policy-targeted-sources < 2
Requires(pre): policycoreutils >= %{POLICYCOREUTILSVER}
Requires(pre): coreutils
Requires(pre): selinux-policy = %{version}-%{release}
Requires: selinux-policy = %{version}-%{release}
Conflicts:  audispd-plugins <= 1.7.7-1
Obsoletes: mod_fcgid-selinux <= %{version}-%{release}
Obsoletes: cachefilesd-selinux <= 0.10-1
Conflicts:  seedit
Conflicts:  389-ds-base < 1.2.7, 389-admin < 1.1.12
Conflicts: container-selinux < 2:1.12.1-22

%description targeted
SELinux targeted policy package.

%pretrans targeted -p <lua>
%backupConfigLua
%removeVarrunModuleLua targeted
%removeBinsbinModuleLua targeted

%pre targeted
%preInstall targeted

%post targeted
%checkConfigConsistency targeted
exit 0

%posttrans targeted
%checkConfigConsistency targeted
%{_libexecdir}/selinux/varrun-convert.sh targeted
%{_libexecdir}/selinux/binsbin-convert.sh targeted
%postInstall $1 targeted
restorecon -Ri /usr/lib/sysimage/rpm /var/lib/rpm /etc/mdevctl.d
restorecon -i /usr/sbin/fapolicyd* /usr/sbin/usbguard*

%postun targeted
if [ $1 = 0 ]; then
    if [ -s %{_sysconfdir}/selinux/config ]; then
        source %{_sysconfdir}/selinux/config &> /dev/null || true
    fi
    if [ "$SELINUXTYPE" = "targeted" ]; then
        setenforce 0 2> /dev/null
        if [ ! -s %{_sysconfdir}/selinux/config ]; then
            echo "SELINUX=disabled" > %{_sysconfdir}/selinux/config
        else
            sed -i 's/^SELINUX=.*/SELINUX=disabled/g' %{_sysconfdir}/selinux/config
        fi
    fi
fi
exit 0


%triggerin -- pcre2
selinuxenabled && semodule -nB 2> /dev/null
exit 0

%triggerin -- fapolicyd-selinux
%{_libexecdir}/selinux/binsbin-convert.sh targeted
restorecon /usr/sbin/fapolicyd*

%triggerin -- usbguard-selinux
%{_libexecdir}/selinux/binsbin-convert.sh targeted
restorecon /usr/sbin/usbguard*

%triggerprein -p <lua> -- container-selinux
%removeVarrunModuleLua targeted

%triggerprein -p <lua> -- pcp-selinux
%removeVarrunModuleLua targeted

%triggerprein -p <lua> -- fapolicyd-selinux
%removeBinsbinModuleLua targeted

%triggerprein -p <lua> -- usbguard-selinux
%removeBinsbinModuleLua targeted

%triggerpostun -- pcp-selinux
%{_libexecdir}/selinux/varrun-convert.sh targeted
exit 0

%triggerpostun -- container-selinux
%{_libexecdir}/selinux/varrun-convert.sh targeted
exit 0

%triggerpostun -- fapolicyd-selinux
%{_libexecdir}/selinux/binsbin-convert.sh targeted
exit 0

%triggerpostun -- usbguard-selinux
%{_libexecdir}/selinux/binsbin-convert.sh targeted
exit 0

%files targeted -f %{buildroot}%{_datadir}/selinux/targeted/nonbasemodules.lst
%config(noreplace) %{_sysconfdir}/dnf/protected.d/selinux-policy-targeted.conf
%config(noreplace) %{_sysconfdir}/selinux/targeted/contexts/users/unconfined_u
%config(noreplace) %{_sysconfdir}/selinux/targeted/contexts/users/sysadm_u
%fileList targeted
%verify(not md5 size mtime) %{_sharedstatedir}/selinux/targeted/active/modules/100/permissivedomains
%endif

%if %{with minimum}
%package minimum
Summary: SELinux minimum policy
Provides: selinux-policy-any = %{version}-%{release}
Requires(post): policycoreutils-python-utils >= %{POLICYCOREUTILSVER}
Requires(pre): coreutils
Requires(pre): selinux-policy = %{version}-%{release}
Requires: selinux-policy = %{version}-%{release}
Conflicts:  seedit
Conflicts: container-selinux <= 1.9.0-9

%description minimum
SELinux minimum policy package.

%pretrans minimum -p <lua>
%backupConfigLua

%pre minimum
%preInstall minimum
if [ $1 -ne 1 ]; then
    semodule -s minimum --list-modules=full | awk '{ if ($4 != "disabled") print $2; }' > %{_datadir}/selinux/minimum/instmodules.lst
fi

%post minimum
%checkConfigConsistency minimum
modules=`cat %{_datadir}/selinux/minimum/modules.lst`
basemodules=`cat %{_datadir}/selinux/minimum/base.lst`
enabledmodules=`cat %{_datadir}/selinux/minimum/modules-enabled.lst`
if [ ! -d %{_sharedstatedir}/selinux/minimum/active/modules/disabled ]; then
    mkdir %{_sharedstatedir}/selinux/minimum/active/modules/disabled
fi
if [ $1 -eq 1 ]; then
for p in $modules; do
    touch %{_sharedstatedir}/selinux/minimum/active/modules/disabled/$p
done
for p in $basemodules $enabledmodules; do
    rm -f %{_sharedstatedir}/selinux/minimum/active/modules/disabled/$p
done
semanage import -S minimum -f - << __eof
login -m  -s unconfined_u -r s0-s0:c0.c1023 __default__
login -m  -s unconfined_u -r s0-s0:c0.c1023 root
__eof
restorecon -R /root /var/log /var/run 2> /dev/null
semodule -B -s minimum 2> /dev/null
else
instpackages=`cat %{_datadir}/selinux/minimum/instmodules.lst`
for p in $packages; do
    touch %{_sharedstatedir}/selinux/minimum/active/modules/disabled/$p
done
for p in $instpackages apache dbus inetd kerberos mta nis; do
    rm -f %{_sharedstatedir}/selinux/minimum/active/modules/disabled/$p
done
semodule -B -s minimum 2> /dev/null
%relabel minimum
fi
exit 0

%posttrans minimum
%checkConfigConsistency minimum
%{_libexecdir}/selinux/varrun-convert.sh minimum
%{_libexecdir}/selinux/binsbin-convert.sh minimum
restorecon -Ri /usr/lib/sysimage/rpm /var/lib/rpm

%postun minimum
if [ $1 = 0 ]; then
    if [ -s %{_sysconfdir}/selinux/config ]; then
        source %{_sysconfdir}/selinux/config &> /dev/null || true
    fi
    if [ "$SELINUXTYPE" = "minimum" ]; then
        setenforce 0 2> /dev/null
        if [ ! -s %{_sysconfdir}/selinux/config ]; then
            echo "SELINUX=disabled" > %{_sysconfdir}/selinux/config
        else
            sed -i 's/^SELINUX=.*/SELINUX=disabled/g' %{_sysconfdir}/selinux/config
        fi
    fi
fi
exit 0

%files minimum -f %{buildroot}%{_datadir}/selinux/minimum/nonbasemodules.lst
%config(noreplace) %{_sysconfdir}/selinux/minimum/contexts/users/unconfined_u
%config(noreplace) %{_sysconfdir}/selinux/minimum/contexts/users/sysadm_u
%fileList minimum
%{_datadir}/selinux/minimum/modules-enabled.lst
%endif

%if %{with mls}
%package mls
Summary: SELinux MLS policy
Provides: selinux-policy-any = %{version}-%{release}
Obsoletes: selinux-policy-mls-sources < 2
Requires: policycoreutils-newrole >= %{POLICYCOREUTILSVER} setransd
Requires(pre): policycoreutils >= %{POLICYCOREUTILSVER}
Requires(pre): coreutils
Requires(pre): selinux-policy = %{version}-%{release}
Requires: selinux-policy = %{version}-%{release}
Conflicts:  seedit
Conflicts: container-selinux <= 1.9.0-9

%description mls
SELinux MLS (Multi Level Security) policy package.

%pretrans mls -p <lua>
%backupConfigLua

%pre mls
%preInstall mls

%post mls
%checkConfigConsistency mls
exit 0

%posttrans mls
%checkConfigConsistency mls
%{_libexecdir}/selinux/varrun-convert.sh mls
%{_libexecdir}/selinux/binsbin-convert.sh mls
%postInstall $1 mls
restorecon -Ri /usr/lib/sysimage/rpm /var/lib/rpm

%postun mls
if [ $1 = 0 ]; then
    if [ -s %{_sysconfdir}/selinux/config ]; then
        source %{_sysconfdir}/selinux/config &> /dev/null || true
    fi
    if [ "$SELINUXTYPE" = "mls" ]; then
        setenforce 0 2> /dev/null
        if [ ! -s %{_sysconfdir}/selinux/config ]; then
            echo "SELINUX=disabled" > %{_sysconfdir}/selinux/config
        else
            sed -i 's/^SELINUX=.*/SELINUX=disabled/g' %{_sysconfdir}/selinux/config
        fi
    fi
fi
exit 0

%files mls -f %{buildroot}%{_datadir}/selinux/mls/nonbasemodules.lst
%config(noreplace) %{_sysconfdir}/dnf/protected.d/selinux-policy-mls.conf
%config(noreplace) %{_sysconfdir}/selinux/mls/contexts/users/unconfined_u
%fileList mls
%endif

%changelog
## START: Generated by rpmautospec
* Mon Apr 06 2026 azldev <> - 42.24-2
- Latest state for selinux-policy

* Fri Feb 13 2026 Zdenek Pytela <zpytela@redhat.com> - 42.24-1
- Allow mdadm to use CAP_BPF during RAID monitoring
- Allow rhsmcertd read anaconda run files
- Allow rpc.mountd setuid and setgid capabilities
- Use kernel_dgram_send() for systemd_notify_t
- Allow lttng-sessiond to use sd_notify
- Label /etc/aliases.cdb with etc_aliases_t
- Add aliases.lmdb to mta_filetrans_named_content()
- Update gpg_role() interface with unix_stream_socket permissions
- Allow systemd-hostnamed to create its Varlink socket

* Wed Feb 04 2026 Zdenek Pytela <zpytela@redhat.com> - 42.23-1
- Allow thumbnailer mount on fonts cache directories
- Support confined users usage of bubblewrap
- Allow vdagent get attributes of the pidfs filesystem
- Allow sshd-session inherit limits from its parent sshd process
- Revert "Allow sshd-session inherit limits from its parent process"
- Allow sshd-session read network sysctls
- Add the fs_write_tmpfs_files() interface
- Update gpg policy for interactions with rhc-playbook-verifier
- Allow rhc_playbook_verifier_t stream connect to itself
- Update policy for rhc-worker-playbook
- Allow sudodomain connect to gkeyringd over a unix stream socket
- Allow tlshd communication to unconfined_t over a tcp socket
- Allow tlshd write generic certificates
- Allow thumbnailer connect to abrt over a unix stream socket

* Fri Jan 23 2026 Zdenek Pytela <zpytela@redhat.com> - 42.22-1
- Allow thumb_t stream connect to systemd-machined
- Allow thumb_t stream connect to systemd-homed
- Allow aide get attributes of tmpfs and devtmpfs filesystems
- Allow sshd noatsecure on sshd-session execution
- Confine rhc-worker-playbook.worker and rhc-playbook-verifier
- Allow kernel_t to read/write all domains' pipes
- Allow domain read sysfs files
- allow abrt_dump_oops to write to init sockets
- Add insights_client service interfaces
- Allow plasma login manager stop login services
- Allow NM nvme dispatcher script start systemd services

* Sat Jan 10 2026 Zdenek Pytela <zpytela@redhat.com> - 42.21-1
- Allow sshd_net_t ioctl on unix_stream_socket of sshd_session_t
- Allow sshd-session read, write, and map ica tmpfs files
- Allow aide get attributes of a filesystem with extended attributes
- Set correct label for glycin fontconfig (bsc#1253682)
- Set correct gstreamer directory label for gnome-desktop-thumbnailer (bsc#1253682)
- Logwatch zz-runtime uses uptime (bsc#1255862)
- Add auth_login_pgm_signull interface (bsc#1255862)
- Introduce systemd_cryptsetup_generator_var_run_t file type (bsc#1244459)
- Allow l2tpd_t access to netlink and sysfs
- Label miscellaneous /dev/papr-* devices
- Allow qemu-ga to skip authentication
- Revert "Allow systemd-coredump signull containers"
- Allow systemd-coredump signull containers
- Allow virtqemud setattr dri devices
- Allow irqbalance create and use netlink generic socket
- Allow thumb_t connect to XDM over a unix domain stream socket
- Allow systemd-homework to remove ~/.identity-blob
- Revert "Allow kl2tpd create and use netlink_generic_socket"

* Fri Dec 19 2025 Zdenek Pytela <zpytela@redhat.com> - 42.20-1
- Support cockpit privileged access for the staff user
- Update su_domain_type policy for kerberized su
- Allow sshd-session inherit limits from its parent process
- Allow systemd-machined read virtd process state
- Allow kl2tpd create and use netlink_generic_socket
- Update policy for redfish-finder
- Label the greetd login manager framework as a display manager
- Allow sshd-auth get attributes of sshd vsock socket
- Confine redfish_finder - host api discovery service
- Allow iptables read firewalld process state
- Allow tuned_t use its private tmpfs files
- The commit addresses the following AVC denials:

* Fri Dec 05 2025 Zdenek Pytela <zpytela@redhat.com> - 42.19-1
- Allow passwd read and write a sshd-session unnamed pipes
- Allow sshd-auth capabilities
- Allow sshd-auth read network sysctls
- Label /run/insights-client.ppid with insights_client_run_t
- fix: unbreak thumbnailing for Thunar/tumblerd
- Add files_mounton_generic_tmp_dirs() interface
- Add the rpm_signal() interface
- Allow session_bus_type get the attributes of the pidfs filesystem
- Allow pcscd get the attributes of the pidfs filesystem
- Allow sssd get the attributes of the pidfs filesystem

* Tue Dec 02 2025 Zdenek Pytela <zpytela@redhat.com> - 42.18-1
- Allow KDE Plasma Login Manager to function as a display manager
- Allow mdadm search filesystem_type directories
- Update policy for dhcpc_hook_t
- Label /usr/libexec/dhcpcd-run-hooks with dhcpc_hook_exec_t
- Allow staff role read/write cockpit-session unix stream sockets
- Allow stap server read virtual memory sysctls
- Allow system_mail_t read apache system content conditionally
- Allow login_userdomain read lastlog

* Wed Nov 26 2025 Zdenek Pytela <zpytela@redhat.com> - 42.17-1
- Allow sshd-net read and write to sshd vsock socket
- Update ktls policy
- Add comprehensive SELinux policy module for bwrap thumbnail generation
- Revert "Allow thumb_t create permission in the user namespace"
- Allow systemd-machined read svirt process state
- Allow sshd_auth_t getopt/setopt on tcp_socket (bsc#1252992)
- Allow sysadm access to TPM
- Allow tlp get the attributes of the pidfs filesystem
- Allow kmscon to read netlink_kobject_uevent_socket

* Thu Nov 20 2025 Zdenek Pytela <zpytela@redhat.com> - 42.16-1
- Allow systemd-ssh-issue read kernel sysctls
- fix: bz2279215 Allow speech-dispatcher access to user home/cache files
- Allow create kerberos files in postgresql db home
- Fix files_delete_boot_symlinks() to contain delete_lnk_files_pattern
- Allow shell comamnds in locate systemd service (bsc#1246559)
- Introduce initrc_nnp_daemon_domain interface
- Label /var/lib/cosmic-greeter with xdm_var_lib_t
- Allow setroubleshoot-fixit get attributes of xattr fs

* Wed Nov 12 2025 Zdenek Pytela <zpytela@redhat.com> - 42.15-1
- Allow insights-client manage /etc symlinks
- Allow insights-client get attributes of the rpm executable
- Allow nfsidmapd search virt lib directories
- Allow iotop stream connect to systemd-userdbd
- Allow gnome-remote-desktop read sssd public files
- Allow thumb_t stream connect to systemd-userdbd
- Allow bluez dbus API passing unix domain sockets
- Allow bluez dbus api pass sockets over dbus
- Dontaudit systemd-generator connect to sssd over a unix stream socket
- Allow init watch/watch_reads systemd-machined user ptys
- Fix syntax error in userdomain.if
- Allow ras-mc-ctl get attributes of the kmod executable

* Fri Oct 24 2025 Zdenek Pytela <zpytela@redhat.com> - 42.14-1
- Define file equivalency for /var/opt
- Allow virtnodedev_t the perfmon capability
- Allow nut_upsdrvctl_t the sys_ptrace capability
- Label /usr/lib/systemd/user/graphical-session-pre.target with xdm_unit_file_t
- systemd-sysctl: allow rw on binfm_misc_fs_t to set binfmt_misc status
- Allow cupsd to manage cupsd_rw_etc_t lnk_files
- Set temporary no-stub resolv.conf file from NetworkManager as net_conf_t
- Allow spamc read aliases file
- Mark configfs_t as mountpoint (bsc#1246080)
- Allow systemd-machined watch cgroup files

* Mon Oct 20 2025 Michael Catanzaro <mcatanzaro@redhat.com> - 42.13-2
- Fix unexpanded macro in selinux_requires

* Tue Oct 14 2025 Zdenek Pytela <zpytela@redhat.com> - 42.13-1
- Allow sshd-auth read generic proc files
- Allow sshd-auth read and write user domain ptys
- Allow logwatch read and write sendmail unix stream sockets
- Allow logwatch domain transition on rpm execution
- Allow thumb_t mounton its private tmpfs files
- Allow thumb_t create permission in the user namespace
- Allow corenet_unconfined_type name_bind to icmp_socket
- Allow systemd-networkd to manage systemd_networkd_var_lib_t files
- Allow sshd-session get attributes of sshd vsock socket

* Sat Oct 04 2025 Zdenek Pytela <zpytela@redhat.com> - 42.12-1
- Adjust guest and xguest users policy for sshd-session
- Allow valkey-server create and use netlink_rdma_socket
- Allow blueman get attributes of filesystems with extended attributes
- Update files_search_base_file_types()
- Allow geoclue get attributes of the /dev/shm filesystem
- Allow apcupsd get attributes of the /dev/shm filesystem
- Allow sshd-session read cockpit pid files

* Wed Sep 24 2025 Zdenek Pytela <zpytela@redhat.com> - 42.11-1
- Allow nfs generator create and use netlink sockets
- Conditionally allow virt guests to read certificates in user home directories
- xenstored_t needs CAP_SYS_ADMIN for XENSTORETYPE=domain (bsc#1247875)
- Allow nfs-generator create and use udp sockets
- Allow kdump search kdumpctl_tmp_t directories
- Allow init open and read user tmp files
- Fix the systemd_logind_stream_connect() interface
- Allow staff and sysadm execute iotop using sudo
- Allow sudodomains connect to systemd-logind over a unix socket

* Tue Sep 16 2025 Zdenek Pytela <zpytela@redhat.com> - 42.10-1
- Add default contexts for sshd-seesion
- Define types for new openssh executables

* Mon Sep 15 2025 Zdenek Pytela <zpytela@redhat.com> - 42.9-1
- Fix systemd_manage_unit_symlinks() interface definition
- Support coreos installation methods
- Add a new type for systemd-ssh-issue PID files
- Allow gnome-remote-desktop connect to unreserved ports
- Allow mdadm the CAP_SYS_PTRACE capability
- Allow iptables manage its private fifo_files in /tmp
- Allow auditd manage its private run dirs
- Revert "Allow virt_domain write to virt_image_t files"
- Exclude tabrmd.if from interfaces list

* Thu Sep 04 2025 Zdenek Pytela <zpytela@redhat.com> - 42.8-1
- Allow gdm create /etc/.pwd.lock with a file transition
- Allow gdm bind a socket in the /run/systemd/userdbd directory
- Allow nsswitch_domain connect to xdm over a unix domain socket
- Allow systemd homed getattr all tmpfs files (bsc#1240883)
- Allow systemd (PID 1) create lastlog entries
- Allow systemd_homework_t transition pid files to lvm_var_run_t (bsc#1240883)
- Allow gnome-remote-desktop speak with tabrmd over dbus (bsc#1244573)
- Allow nm-dispatcher iscsi and sendmail plugins get pidfs attributes
- Allow systemd-oomd watch tmpfs dirs
- Allow chronyc the setgid and setuid capabilities

* Fri Aug 29 2025 Zdenek Pytela <zpytela@redhat.com> - 42.7-1
- Label /usr/lib/systemd/systemd-ssh-issue with systemd_ssh_issue_exec_t
- Allow stalld map sysfs files
- Allow NetworkManager-dispatcher-winbind get pidfs attributes
- Allow openvpn create and use generic netlink socket
- policy_capabilities: remove estimated from released versions
- policy_capabilities: add stub for userspace_initial_context
- add netlink_xperm policy capability and nlmsg permission definitions
- policy_capabilities: add ioctl_skip_cloexec
- selinux-policy: add allow rule for tuned_ppd_t
- selinux-policy: add allow rule for switcheroo_control_t
- Label /run/audit with auditd_var_run_t

* Tue Aug 12 2025 Zdenek Pytela <zpytela@redhat.com> - 42.6-1
- Allow virtqemud start a vm which uses nbdkit
- Add nbdkit_signal() and nbdkit_signull() interfaces
- Fix insights_client interfaces names
- Add insights_core and insights_client interfaces
- dist/targeted/modules.conf: enable slrnpull module
- Allow bootupd delete symlinks in the /boot directory
- Allow systemd-coredumpd capabilities in the user namespace
- Allow openvswitch read virtqemud process state
- Allow systemd-networkd to create leases directory

* Fri Aug 08 2025 Zdenek Pytela <zpytela@redhat.com> - 42.5-1
- Apply generator template to selinux-autorelabel generator
- Support virtqemud handle hotplug hostdev devices
- Allow virtstoraged create qemu /var/run files
- Allow unconfined_domain_type cap2_userns capabilities
- Label /usr/libexec/postfix/tlsproxy with postfix_smtp_exec_t
- Remove the mysql module sources
- dist/targeted/modules.conf: Enable kmscon module (bsc#1238137)
- Update kmscon policy module to kmscon version 9 (bsc#1238137)
- Allow login to getattr pidfs
- Allow systemd to map files under /sys
- systemd: drop duplicate init_nnp_daemon_domain lines
- Fix typo
- Allow logwatch stream connect to opensmtpd
- Allow geoclue read NetworkManager pid files

* Mon Aug 04 2025 Zdenek Pytela <zpytela@redhat.com> - 42.4-1
- Allow unconfined user a file transition for creating sudo log directory
- Allow virtqemud read/write inherited dri devices
- Allow xdm_t create user namespaces
- Update policy for login_userdomain
- Add ppd_base_profile to file transition to get tuned_rw_etc_t type
- Update policy for bootupd
- Allow logwatch work with opensmtpd
- Update dovecot policy for dovecot 2.4.1
- Allow ras-mc-ctl write to sysfs files
- Allow anaconda-generator get attributes of all filesystems
- Add the rhcd_rw_fifo_files() interface
- Allow systemd-coredump the sys_chroot capability
- Allow hostapd write to socket files in /tmp
- Recognize /var/home as an alternate path for /home
- Label /var/lib/lastlog with lastlog_t

* Mon Jul 28 2025 Zdenek Pytela <zpytela@redhat.com> - 42.3-1
- Allow virtqemud write to sysfs files
- Allow irqbalance search sssd lib directories
- Allow samba-dcerpcd send sigkills to passwd
- Allow systemd-oomd watch dbus pid sock files
- Allow some confined users read and map generic log files
- Allow login_userdomain watch the /run/log/journal directory
- Allow login_userdomain dbus chat with tuned-ppd
- Allow login_userdomain dbus chat with switcheroo-control
- Allow userdomain to connect to systemd-oomd over a unix socket
- Add insights_client_delete_lib_dirs() interface

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 42.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jul 21 2025 Zdenek Pytela <zpytela@redhat.com> - 42.2-1
- Allow virtqemud_t use its private tmpfs files (bsc#1242998)
- Allow virtqemud_t setattr to /dev/userfaultfd (bsc#1242998)
- Allow virtqemud_t read and write /dev/ptmx (bsc#1242998)
- Extend virtqemud_t tcp_socket permissions (bsc#1242998)
- Allow virtqemud_t to read and write generic pty (bsc#1242998)
- Allow systemd-importd create and unlink init pid socket
- Allow virtqemud handle virt_content_t chr files
- Allow svirt read virtqemud fifo files
- All sblim-sfcbd the dac_read_search capability
- Allow sblim domain read systemd session files
- Allow sblim-sfcbd execute dnsdomainname
- Confine nfs-server generator
- Allow systemd-timedated start/stop timemaster services
- Allow "hostapd_cli ping" run as a systemd service
- Allow power-profiles-daemon get attributes of filesystems with extended attributes
- Allow 'oomctl dump' to interact with systemd-oomd
- Basic functionality for systemd-oomd
- Basic enablement for systemd-oomd
- Allow samba-bgqd send to smbd over a unix datagram socket
- Update kernel_secretmem_use()
- Add the file/watch_mountns permission

* Tue Jul 15 2025 Zdenek Pytela <zpytela@redhat.com> - 42.1-1
- Update systemd-generators policy
- Allow plymouthd_t read proc files of systemd_passwd_agent (bsc#1245470)
- Allow insights-client file transition for files in /var/tmp
- Allow tuned-ppd manage tuned log files
- Allow systemd-coredump mount on tmpfs filesystems
- Update sssd_dontaudit_read_public_files()
- Allow zram-generator raw read fixed disk device

* Fri Jul 04 2025 Zdenek Pytela <zpytela@redhat.com> - 41.45-1
- Add fs_write_cgroup_dirs() and fs_setattr_cgroup_dirs() interfaces
- Allow irqbalance execute shell if irqbalance_run_unconfined is on
- Allow openvswitch ioctl vduse devices
- Label /dev/vduse/control and /dev/vduse/NAME devices
- Allow virtstoraged the sys_rawio capability
- Allow virtqemud read insights-core state files
- Allow virtnodedev create mdevctl config dirs
- Allow virtqemud additional permissions on scsi generic chr files
- Allow local login execute gnome keyring daemon
- Allow virtqemud send a generic signal to passt
- Allow svirt-tcg read init state
- Allow irqbalance execute shell if irqbalance_run_unconfined is on
- Label /run/opendkim with dkim_milter_data_t
- Allow sa-update status systemd services
- Allow updpwd logging send audit messages
- Temporary dontaudit iio-sensor-proxy sys_admin.
- Allow iio-sensor-proxy sendto to journald over a unix datagram socket
- Revert "Allow iio-sensor-proxy sendto to journald over a unix datagram socket"

* Fri Jul 04 2025 Petr Lautrbach <lautrbach@redhat.com> - 41.44-2
- Rebuilt with SELinux userspace 3.9-rc2 release

* Tue Jun 17 2025 Zdenek Pytela <zpytela@redhat.com> - 41.44-1
- virt: allow QEMU use of the qgs daemon for attestation
- qgs: add contrib module for TDX "qgs" daemon
- kernel: add interfaces for using SGX enclaves
- Define file equivalency for /usr/etc
- Allow mongod to receive pressure stall information
- Dontaudit systemd_generator read sssd public files
- Allow plymouthd read/write input event devices
- Label 99-nvme-nbft-connect.sh with NetworkManager_dispatcher_nvme_script_t
- Allow systemd-user-runtime-dir sendto to syslogd
- Remove pcp module
- Update irqbalance policy for using unconfined scripts
- Allow utempter use terminal multiplexor
- Allow virtqemud execute ovs-vsctl with a domain transition
- Update the files_search_mnt() interface

* Wed Jun 04 2025 Zdenek Pytela <zpytela@redhat.com> - 41.43-1
- Allow nmbd read network sysctls
- Allow iio-sensor-proxy sendto to journald over a unix datagram socket
- Allow logrotate stop all systemd services
- systemd: rework systemd_manage_random_seed
- Allow tuned-ppd connect to sssd over a unix stream socket

* Tue Jun 03 2025 Zdenek Pytela <zpytela@redhat.com> - 41.42-1
- Drop config for /run/random-seed
- Update file location for systemd random-seed file
- Allow tomcat execute cracklib-check with a domain transition
- Allow sssd watch lib dirs
- Confine systemd-hibernate-resume
- Allow login_userdomain create /run/tlog directory with user_tmp_t
- Allow login_pgm read filesystem sysctls
- Allow gconfd connect to system dbus
- Allow NetworkManager manage NetworkManager_etc_rw_t symlinks

* Thu May 22 2025 Zdenek Pytela <zpytela@redhat.com> - 41.41-1
- Allow mdadm nosuid_transition
- Label plasma user service files as xdm_unit_file_t.
- Revert "Allow systemd-homed to start services."
- Allow virtstoraged write qemu runtime files
- Allow virtqemud read/write/setattr input event devices
- Allow systemd create journal pid files
- Allow networkmanager send a general signal to iptables
- Allow syslogd watch syslog_conf_t directories
- Allow systemd-machined work with its private tmp and tmpfs files
- Allow geoclue read virt lib files
- Fix files_dontaudit_delete_all_files()
- Label /run/polkit-1 with policykit_var_run_t
- Label /dev/diag as diagnostic_device_t
- Allow systemd-homed to start services.
- Allow named_t to read NetworkManager's runtime files
- Improve README* documentation

* Tue May 13 2025 Zdenek Pytela <zpytela@redhat.com> - 41.40-1
- Add missing permissions for ftpd_anon_write to manage NFS directories
- Add missing permissions for ftpd_anon_write to manage CIFS directories
- Allow nut-upsmon write systemd inhibit pipes
- Allow systemd-user-runtime-dir connect to systemd-userdbd over a unix socket
- Remove permissive domain for systemd_vsftpd_generator_t
- Change generator-specific rules to apply to systemd_generator
- Define file equivalency for /var/etc
- Allow tuned-ppd create ppd_base_profile with a file transition
- Allow lldpd connect to systemd-homed over a unix socket
- Allow sysadm_sudo_t signal rpm script
- Fix the "/var/cache/systemd/home(/.*)?" regex

* Wed Apr 30 2025 Zdenek Pytela <zpytela@redhat.com> - 41.39-1
- Allow collectd accept and listen to tcp sockets
- Allow init_t nnp domain transition to redis_t
- Allow tlshd read network sysctls
- Allow NetworkManager create and use icmp_socket
- Allow varnishd execute the prlimit64() syscall
- Allow rhsmcertd connect to systemd-machined
- Allow virt_domain write to virt_image_t files
- Allow system-dbusd list systemd-machined directories
- Allow asterisk read network sysctls
- Allow virtstoraged fsetid capability
- Allow xdm watch a mnt_t directory
- Allow collectd bind TCP sockets to the collectd port
- Allow virtqemud relabel from tmpfs lnk files
- Allow gnome-remote-desktop additional sockets permissions
- Update insights-core policy
- Update systemd-homed policy
- Allow xenstored_t manage xend_var_lib_t files (bsc#1228540)

* Thu Apr 17 2025 Zdenek Pytela <zpytela@redhat.com> - 41.38-1
- Allow init and login_pgm connect to systemd-logind over a unix socket
- Allow login_userdomain read pressure stall information
- Allow systemd-journald create and use vsock socket
- Update systemd-pcrextend policy
- Allow systemd watch/watch_reads usb ttys
- Update coreos-installer-generator policy
- Update systemd-homed policy
- Allow systemd-user-runtime-dir get/set tmpfs quotas
- Allow systemd-rfkill read nsfs files
- Dontaudit bootc-systemd-generator search sssd lib directories
- Allow systemd-user-runtime-dir delete gnome homedir content

* Fri Apr 11 2025 Zdenek Pytela <zpytela@redhat.com> - 41.37-1
- Allow tuned-ppd read sssd public files
- Allow tuned-ppd watch_reads sysfs directories
- Confine /usr/lib/systemd/systemd-user-runtime-dir
- Revert "Dontaudit systemd-logind remove all files"
- Make bootupd use bootupd_tmp_t as its private type for files in /tmp
- Label SetroubleshootPrivileged.py with setroubleshootd_exec_t
- Allow power-profiles-daemon watch sysfs directories
- systemd: allow reading /dev/cpu/0/msr
- Update the pcmsensor policy
- Allow chronyd-restricted sendto to chronyc
- Allow system_dbusd_t r/w unix stream sockets of unconfined_service_t
- Allow dovecot-deliver read mail aliases

* Mon Apr 07 2025 Zdenek Pytela <zpytela@redhat.com> - 41.36-1
- Confine systemd-factory-reset system generator
- Allow systemd debug generator read tmpfs files
- Allow gnome-shell get attributes of systemd inhibit pipes
- Allow tuned-ppd watch sysfs directories
- Fix the storage_rw_inherited_removable_device() interface
- Allow sadc read global pressure stall information
- Allow virtqemud read sblim-gatherd process state
- Allow switcheroo-control dbus chat with xdm
- Fix typo in calling unconfined_dbus_chat for switcheroo-control
- Allow sysadm_t to write to /dev/kmsg
- Allow init_t nnp domain transition to pcscd_t
- Fix the genfscon statement for pidfs filesystem
- Allow tuned-ppd dbus chat with xdm

* Fri Mar 28 2025 Zdenek Pytela <zpytela@redhat.com> - 41.35-1
- Update INSTALL to describe necessary steps to build it
- Rename the default policy to fedora-selinux
- Update COPYING to the latest version of GPLv2
- Allow traceroute_t bind rawip sockets to unreserved ports
- Revert "Allow traceroute_t bind rawip sockets to unreserved ports"
- Change the bootc system generator name to bootc-systemd-generator
- Allow mpd use the io_uring API
- Confine tuned-ppd
- Add the switcheroo module
- Label wine's windows libraries as textrel_shlib_t
- Allow systemd domains write global pressure stall information
- Add label and interfaces for kernel PSI files
- Update bootupd policy
- Update ktls policy
- Add policy for systemd-bootc-generator
- Allow blueman the kill capability

* Fri Mar 07 2025 Zdenek Pytela <zpytela@redhat.com> - 41.34-1
- Add context for plymouth debug log files
- Allow rlimit inheritance for domains transitioning to local_login_t
- Update insights-core policy
- Allow insights-core map all non-security files
- Allow insights-core map audit config and log files
- Allow insights-client manage insights_client_var_log_t files
- Remove duplicate dev_rw_dma_dev(xdm_t)
- Allow thumbnailer read and write the dma device
- Allow named_filetrans_domain filetrans raid/mdadm named content
- Allow afterburn to mount and read config drives
- Allow mptcpd the net_admin capability

* Fri Feb 07 2025 Zdenek Pytela <zpytela@redhat.com> - 41.33-1
- Allow systemd-networkd the sys_admin capability
- Update systemd-networkd policy in systemd v257
- Separate insights-core from insights-client
- Removed unused insights_client interfaces calls from other modules
- Update policy for insights_client wrt new rules for insights_core_t
- Add policy for insights-core
- Allow systemd-networkd use its private tmpfs files
- Allow boothd connect to systemd-machined over a unix socket
- Update init_explicit_domain() interface
- Allow tlp to read/write nmi_watchdog state information
- Allow power-profiles-daemon the bpf capability
- Allow svirt_t to connect to nbdkit over a unix stream socket
- Update ktlshd policy to read /proc/keys and domain keyrings
- Allow virt_domain read hardware state information unconditionally
- Allow init mounton crypto sysctl files
- Rename winbind_rpcd_* types to samba_dcerpcd_*
- Support peer-to-peer migration of vms using ssh

* Wed Feb 05 2025 Zdenek Pytela <zpytela@redhat.com> - 41.32-1
- Allow virtqemud use hostdev usb devices conditionally
- Allow virtqemud map svirt_image_t plain files
- Allow virtqemud work with nvdimm devices
- Support saving and restoring a VM to/from a block device
- Allow virtnwfilterd dbus chat with firewalld
- Dontaudit systemd-logind remove all files
- Add the files_dontaudit_read_all_dirs() interface
- Add the files_dontaudit_delete_all_files() interface
- Allow rhsmcertd notify virt-who
- Allow irqbalance to run unconfined scripts conditionally
- Fix binsbin-convert.sh to handle exceptions

* Fri Jan 31 2025 Zdenek Pytela <zpytela@redhat.com> - 41.31-1
- Allow snapperd execute systemctl in the caller domain
- Allow svirt_tcg_t to connect to nbdkit over a unix stream socket
- Allow iio-sensor-proxy read iio devices
- Label /dev/iio:device[0-9]+ devices
- Allow systemd-coredump the sys_admin capability
- Allow apcupsd's apccontrol to send messages using wall
- contrib/thumb: also allow per-user thumbnailers
- contrib/thumb: fix thunar thumbnailer (rhbz#2315893)
- Allow virt_domain to use pulseaudio - conditional
- Allow pcmsensor read nmi_watchdog state information
- Allow init_t nnp domain transition to gssproxy_t

* Mon Jan 27 2025 Zdenek Pytela <zpytela@redhat.com> - 41.30-1
- Allow systemd-generator connect to syslog over a unix stream socket
- Allow virtqemud manage fixed disk device nodes
- Allow iio-sensor-proxy connect to syslog over a unix stream socket
- Allow virtstoraged write to sysfs files
- Allow power-profiles-daemon write sysfs files
- Update iiosensorproxy policy
- Allow pcmsensor write nmi_watchdog state information
- Label /proc/sys/kernel/nmi_watchdog with sysctl_nmi_watchdog_t
- Allow virtnodedev create /etc/mdevctl.d/scripts.d with bin_t type
- Add the gpg_read_user_secrets() interface
- Allow gnome-remote-desktop read resolv.conf
- Update switcheroo policy
- Allow nfsidmap connect to systemd-homed over a unix socket
- Add the auth_write_motd_var_run_files() interface
- Add the bind_exec_named_checkconf() interface
- Add the virt_exec_virsh() interface

* Wed Jan 15 2025 Zdenek Pytela <zpytela@redhat.com> - 41.29-1
- Allow virtqemud domain transition to nbdkit
- Add nbdkit interfaces defined conditionally
- Allow samba-bgqd connect to cupsd over an unix domain stream socket
- Confine the switcheroo-control service
- Allow svirt_t read sysfs files
- Add rhsmcertd interfaces
- Add the ssh_exec_sshd() interface
- Add the gpg_domtrans_agent() interface
- Label /usr/bin/dnf5 with rpm_exec_t
- Label /dev/pmem[0-9]+ with fixed_disk_device_t
- allow kdm to create /root/.kde/ with correct label
- Change /usr/sbin entries to use /usr/bin or remove them
- Allow systemd-homed get filesystem quotas
- Allow login_userdomain getattr nsfs files
- Allow virtqemud send a generic signal to the ssh client domain
- Dontaudit request-key read /etc/passwd

* Fri Jan 03 2025 Zdenek Pytela <zpytela@redhat.com> - 41.28-1
- Update virtqemud policy regarding the svirt_tcg_t domain
- Allow virtqemud domain transition on numad execution
- Support virt live migration using ssh
- Allow virtqemud permissions needed for live migration
- Allow virtqemud the getpgid process permission
- Allow virtqemud manage nfs dirs when virt_use_nfs boolean is on
- Allow virtqemud relabelfrom virt_log_t files
- Allow virtqemud relabel tun_socket
- Add policy for systemd-import-generator
- Confine vsftpd systemd system generator
- Allow virtqemud read and write sgx_vepc devices
- Allow systemd-networkd list cgroup directories
- Allow xdm dbus chat with power-profiles-daemon
- Allow ssh_t read systemd config files
- Add Valkey rules to Redis module

* Tue Dec 17 2024 Zdenek Pytela <zpytela@redhat.com> - 41.27-1
- Update ktlsh policy
- Allow request-key to read /etc/passwd
- Allow request-key to manage all domains' keys
- Add support for the KVM guest memfd anon inodes
- Allow auditctl signal auditd
- Dontaudit systemd-coredump the sys_resource capability
- Allow traceroute_t bind rawip sockets to unreserved ports
- Fix the cups_read_pid_files() interface to use read_files_pattern
- Allow virtqemud additional permissions for tmpfs_t blk devices
- Allow virtqemud rw access to svirt_image_t chr files
- Allow virtqemud rw and setattr access to fixed block devices
- Label /etc/mdevctl.d/scripts.d with bin_t
- Allow virtqemud open svirt_devpts_t char files
- Allow virtqemud relabelfrom virt_log_t files
- Allow svirt_tcg_t read virtqemud_t fifo_files
- Allow virtqemud rw and setattr access to sev devices
- Allow virtqemud directly read and write to a fixed disk
- Allow virtqemud_t relabel virt_var_lib_t files
- Allow virtqemud_t relabel virtqemud_var_run_t sock_files
- Add gnome_filetrans_gstreamer_admin_home_content() interface
- Label /dev/swradio, /dev/v4l-subdev, /dev/v4l-touch with v4l_device_t
- Make bootupd_t permissive
- Allow init_t nnp domain transition to locate_t
- allow gdm and iiosensorproxy talk to each other via D-bus
- Allow systemd-journald getattr nsfs files
- Allow sendmail to map mail server configuration files
- Allow procmail to read mail aliases
- Allow cifs.idmap helper to set attributes on kernel keys
- Allow irqbalance setpcap capability in the user namespace
- Allow sssd_selinux_manager_t the setcap process permission
- Allow systemd-sleep manage efivarfs files
- Allow systemd-related domains getattr nsfs files
- Allow svirt_t the sys_rawio capability
- Allow alsa watch generic device directories
- Move systemd-homed interfaces to seperate optional_policy block
- Update samba-bgqd policy
- Update virtlogd policy
- Allow svirt_t the sys_rawio capability
- Allow qemu-ga the dac_override and dac_read_search capabilities
- Allow bacula execute container in the container domain
- Allow httpd get attributes of dirsrv unit files
- Allow samba-bgqd read cups config files
- Add label rshim_var_run_t for /run/rshim.pid

* Mon Dec 02 2024 Petr Lautrbach <lautrbach@redhat.com> - 41.26-2
- Rebuild with SELinux Userspace 3.8

* Tue Nov 19 2024 Zdenek Pytela <zpytela@redhat.com> - 41.26-1
- [5/5][sync from 'mysql-selinux'] Add mariadb-backup
- [4/5][sync from 'mysql-selinux'] Fix regex to also match '/var/lib/mysql/mysqlx.sock'
- [3/5][sync from 'mysql-selinux'] Allow mysqld_t to read and write to the 'memory.pressure' file in cgroup2
- [2/5][sync from 'mysql-selinux'] 2nd attempt to fix rhbz#2186996 rhbz#2221433 rhbz#2245705
- [1/5][sync from 'mysql-selinux'] Allow 'mysqld' to use '/usr/bin/hostname'
- Allow systemd-networkd read mount pid files
- Update policy for samba-bgqd
- Allow chronyd read networkmanager's pid files
- Allow staff user connect to generic tcp ports
- Allow gnome-remote-desktop dbus chat with policykit
- Allow tlp the setpgid process permission
- Update the bootupd policy
- Allow sysadm_t use the io_uring API
- Allow sysadm user dbus chat with virt-dbus
- Allow virtqemud_t read virsh_t files
- Allow virt_dbus_t connect to virtd_t over a unix stream socket
- Allow systemd-tpm2-generator read hardware state information
- Allow coreos-installer-generator execute generic programs
- Allow coreos-installer domain transition on udev execution
- Revert "Allow unconfined_t execute kmod in the kmod domain"
- Allow iio-sensor-proxy create and use unix dgram socket
- Allow virtstoraged read vm sysctls
- Support ssh connections via systemd-ssh-generator
- Label all semanage store files in /etc as semanage_store_t
- Add file transition for nvidia-modeset

* Fri Oct 25 2024 Zdenek Pytela <zpytela@redhat.com> - 41.25-1
- Allow dirsrv-snmp map dirsv_tmpfs_t files
- Label /usr/lib/node_modules_22/npm/bin with bin_t
- Add policy for /usr/libexec/samba/samba-bgqd
- Allow gnome-remote-desktop watch /etc directory
- Allow rpcd read network sysctls
- Allow journalctl connect to systemd-userdbd over a unix socket
- Allow some confined users send to lldpad over a unix dgram socket
- Allow lldpad send to unconfined_t over a unix dgram socket
- Allow lldpd connect to systemd-machined over a unix socket
- Confine the ktls service

* Wed Oct 23 2024 Zdenek Pytela <zpytela@redhat.com> - 41.24-1
- Allow dirsrv read network sysctls
- Label /run/sssd with sssd_var_run_t
- Label /etc/sysctl.d and /run/sysctl.d with system_conf_t
- Allow unconfined_t execute kmod in the kmod domain
- Allow confined users r/w to screen unix stream socket
- Label /root/.screenrc and /root/.tmux.conf with screen_home_t
- Allow virtqemud read virtd_t files
- Allow ping_t read network sysctls

* Mon Oct 21 2024 Zdenek Pytela <zpytela@redhat.com> - 41.23-1
- Allow systemd-homework connect to init over a unix socket
- Fix systemd-homed blobs directory permissions
- Allow virtqemud read sgx_vepc devices
- Allow lldpad create and use netlink_generic_socket

* Wed Oct 16 2024 Zdenek Pytela <zpytela@redhat.com> - 41.22-1
- Allow systemd-homework write to init pid socket
- Allow init create /var/cache/systemd/home
- Confine the pcm service
- Allow login_userdomain read thumb tmp files
- Update power-profiles-daemon policy
- Fix the /etc/mdevctl\.d(/.*)? regexp
- Grant rhsmcertd chown capability & userdb access
- Allow iio-sensor-proxy the bpf capability
- Allow systemd-machined the kill user-namespace capability

* Fri Oct 11 2024 Zdenek Pytela <zpytela@redhat.com> - 41.21-1
- Remove the fail2ban module sources
- Remove the linuxptp module sources
- Remove legacy rules for slrnpull
- Remove the aiccu module sources
- Remove the bcfg2 module sources
- Remove the amtu module sources
- Remove the rhev module sources
- Remove all file context entries for /bin and /lib
- Allow ptp4l the sys_admin capability
- Confine power-profiles-daemon
- Label /var/cache/systemd/home with systemd_homed_cache_t
- Allow login_userdomain connect to systemd-homed over a unix socket
- Allow boothd connect to systemd-homed over a unix socket
- Allow systemd-homed get attributes of a tmpfs filesystem
- Allow abrt-dump-journal-core connect to systemd-homed over a unix socket
- Allow aide connect to systemd-homed over a unix socket
- Label /dev/hfi1_[0-9]+ devices
- Suppress semodule's stderr

* Thu Oct 03 2024 Zdenek Pytela <zpytela@redhat.com> - 41.20-1
- Remove the openct module sources
- Remove the timidity module sources
- Enable the slrn module
- Remove i18n_input module sources
- Enable the distcc module
- Remove the ddcprobe module sources
- Remove the timedatex module sources
- Remove the djbdns module sources
- Confine iio-sensor-proxy
- Allow staff user nlmsg_write
- Update policy for xdm with confined users
- Allow virtnodedev watch mdevctl config dirs
- Allow ssh watch home config dirs
- Allow ssh map home configs files
- Allow ssh read network sysctls
- Allow chronyc sendto to chronyd-restricted
- Allow cups sys_ptrace capability in the user namespace

* Tue Sep 24 2024 Zdenek Pytela <zpytela@redhat.com> - 41.19-1
- Add policy for systemd-homed
- Remove fc entry for /usr/bin/pump
- Label /usr/bin/noping and /usr/bin/oping with ping_exec_t
- Allow accountsd read gnome-initial-setup tmp files
- Allow xdm write to gnome-initial-setup fifo files
- Allow rngd read and write generic usb devices
- Allow qatlib search the content of the kernel debugging filesystem
- Allow qatlib connect to systemd-machined over a unix socket

* Wed Sep 18 2024 Petr Lautrbach <lautrbach@redhat.com> - 41.18-1
- Drop ru man pages
- mls/modules.conf - fix typo
- Allow unprivileged user watch /run/systemd
- Allow boothd connect to kernel over a unix socket

* Mon Sep 16 2024 Zdenek Pytela <zpytela@redhat.com> - 41.17-2
- Relabel /etc/mdevctl.d

* Thu Sep 12 2024 Petr Lautrbach <lautrbach@redhat.com> - 41.17-1
- Clean up and sync securetty_types
- Bring config files from dist-git into the source repo
- Confine gnome-remote-desktop
- Allow virtstoraged execute mount programs in the mount domain
- Make mdevctl_conf_t member of the file_type attribute

* Fri Sep 06 2024 Zdenek Pytela <zpytela@redhat.com> - 41.16-1
- Label /etc/mdevctl.d with mdevctl_conf_t
- Sync users with Fedora targeted users
- Update policy for rpc-virtstorage
- Allow virtstoraged get attributes of configfs dirs
- Fix SELinux policy for sandbox X server to fix 'sandbox -X' command
- Update bootupd policy when ESP is not mounted
- Allow thumb_t map dri devices
- Allow samba use the io_uring API
- Allow the sysadm user use the secretmem API
- Allow nut-upsmon read systemd-logind session files
- Allow sysadm_t to create PF_KEY sockets
- Update bootupd policy for the removing-state-file test
- Allow coreos-installer-generator manage mdadm_conf_t files

* Thu Aug 29 2024 Zdenek Pytela <zpytela@redhat.com> - 41.15-1
- Allow setsebool_t relabel selinux data files
- Allow virtqemud relabelfrom virtqemud_var_run_t dirs
- Use better escape method for "interface"
- Allow init and systemd-logind to inherit fds from sshd
- Allow systemd-ssh-generator read sysctl files
- Sync modules.conf with Fedora targeted modules
- Allow virtqemud relabel user tmp files and socket files
- Add missing sys_chroot capability to groupadd policy
- Label /run/libvirt/qemu/channel with virtqemud_var_run_t
- Allow virtqemud relabelfrom also for file and sock_file
- Add virt_create_log() and virt_write_log() interfaces
- Call binaries without full path

* Mon Aug 12 2024 Zdenek Pytela <zpytela@redhat.com> - 41.14-1
- Update libvirt policy
- Add port 80/udp and 443/udp to http_port_t definition
- Additional updates stalld policy for bpf usage
- Label systemd-pcrextend and systemd-pcrlock properly
- Allow coreos_installer_t work with partitions
- Revert "Allow coreos-installer-generator work with partitions"
- Add policy for systemd-pcrextend
- Update policy for systemd-getty-generator
- Allow ip command write to ipsec's logs
- Allow virt_driver_domain read virtd-lxc files in /proc
- Revert "Allow svirt read virtqemud fifo files"
- Update virtqemud policy for libguestfs usage
- Allow virtproxyd create and use its private tmp files
- Allow virtproxyd read network state
- Allow virt_driver_domain create and use log files in /var/log
- Allow samba-dcerpcd work with ctdb cluster

* Tue Aug 06 2024 Zdenek Pytela <zpytela@redhat.com> - 41.13-1
- Allow NetworkManager_dispatcher_t send SIGKILL to plugins
- Allow setroubleshootd execute sendmail with a domain transition
- Allow key.dns_resolve set attributes on the kernel key ring
- Update qatlib policy for v24.02 with new features
- Label /var/lib/systemd/sleep with systemd_sleep_var_lib_t
- Allow tlp status power services
- Allow virtqemud domain transition on passt execution
- Allow virt_driver_domain connect to systemd-userdbd over a unix socket
- Allow boothd connect to systemd-userdbd over a unix socket
- Update policy for awstats scripts
- Allow bitlbee execute generic programs in system bin directories
- Allow login_userdomain read aliases file
- Allow login_userdomain read ipsec config files
- Allow login_userdomain read all pid files
- Allow rsyslog read systemd-logind session files
- Allow libvirt-dbus stream connect to virtlxcd

* Wed Jul 31 2024 Zdenek Pytela <zpytela@redhat.com> - 41.12-1
- Update bootupd policy
- Allow rhsmcertd read/write access to /dev/papr-sysparm
- Label /dev/papr-sysparm and /dev/papr-vpd
- Allow abrt-dump-journal-core connect to winbindd
- Allow systemd-hostnamed shut down nscd
- Allow systemd-pstore send a message to syslogd over a unix domain
- Allow postfix_domain map postfix_etc_t files
- Allow microcode create /sys/devices/system/cpu/microcode/reload
- Allow rhsmcertd read, write, and map ica tmpfs files
- Support SGX devices
- Allow initrc_t transition to passwd_t
- Update fstab and cryptsetup generators policy
- Allow xdm_t read and write the dma device
- Update stalld policy for bpf usage
- Allow systemd_gpt_generator to getattr on DOS directories

* Thu Jul 25 2024 Zdenek Pytela <zpytela@redhat.com> - 41.11-1
- Make cgroup_memory_pressure_t a part of the file_type attribute
- Allow ssh_t to change role to system_r
- Update policy for coreos generators
- Allow init_t nnp domain transition to firewalld_t
- Label /run/modprobe.d with modules_conf_t
- Allow virtnodedevd run udev with a domain transition
- Allow virtnodedev_t create and use virtnodedev_lock_t
- Allow virtstoraged manage files with virt_content_t type
- Allow virtqemud unmount a filesystem with extended attributes
- Allow svirt_t connect to unconfined_t over a unix domain socket

* Mon Jul 22 2024 Zdenek Pytela <zpytela@redhat.com> - 41.10-1
- Update afterburn file transition policy
- Allow systemd_generator read attributes of all filesystems
- Allow fstab-generator read and write cryptsetup-generator unit file
- Allow cryptsetup-generator read and write fstab-generator unit file
- Allow systemd_generator map files in /etc
- Allow systemd_generator read init's process state
- Allow coreos-installer-generator read sssd public files
- Allow coreos-installer-generator work with partitions
- Label /etc/mdadm.conf.d with mdadm_conf_t
- Confine coreos generators
- Label /run/metadata with afterburn_runtime_t
- Allow afterburn list ssh home directory
- Label samba certificates with samba_cert_t
- Label /run/coreos-installer-reboot with coreos_installer_var_run_t
- Allow virtqemud read virt-dbus process state
- Allow staff user dbus chat with virt-dbus
- Allow staff use watch /run/systemd
- Allow systemd_generator to write kmsg

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 41.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jul 16 2024 Zdenek Pytela <zpytela@redhat.com> - 41.9-1
- Allow virtqemud connect to sanlock over a unix stream socket
- Allow virtqemud relabel virt_var_run_t directories
- Allow svirt_tcg_t read vm sysctls
- Allow virtnodedevd connect to systemd-userdbd over a unix socket
- Allow svirt read virtqemud fifo files
- Allow svirt attach_queue to a virtqemud tun_socket
- Allow virtqemud run ssh client with a transition
- Allow virt_dbus_t connect to virtqemud_t over a unix stream socket
- Update keyutils policy
- Allow sshd_keygen_t connect to userdbd over a unix stream socket
- Allow postfix-smtpd read mysql config files
- Allow locate stream connect to systemd-userdbd
- Allow the staff user use wireshark
- Allow updatedb connect to userdbd over a unix stream socket
- Allow gpg_t set attributes of public-keys.d
- Allow gpg_t get attributes of login_userdomain stream
- Allow systemd_getty_generator_t read /proc/1/environ
- Allow systemd_getty_generator_t to read and write to tty_device_t

* Thu Jul 11 2024 Petr Lautrbach <lautrbach@redhat.com> 41.8-4
- Move %%postInstall to %%posttrans
- Use `Requires(meta): (rpm-plugin-selinux if rpm-libs)`
- Drop obsolete modules from config
- Install dnf protected files only when policy is built

* Thu Jul 11 2024 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 41.8-3
- Relabel files under /usr/bin to fix stale context after sbin merge

* Wed Jul 10 2024 Petr Lautrbach <lautrbach@redhat.com> 41.8-2
- Merge -base and -contrib

* Wed Jul 10 2024 Zdenek Pytela <zpytela@redhat.com> - 41.8-1
- Drop publicfile module
- Remove permissive domain for systemd_nsresourced_t
- Change fs_dontaudit_write_cgroup_files() to apply to cgroup_t
- Label /usr/bin/samba-gpupdate with samba_gpupdate_exec_t
- Allow to create and delete socket files created by rhsm.service
- Allow virtnetworkd exec shell when virt_hooks_unconfined is on
- Allow unconfined_service_t transition to passwd_t
- Support /var is empty
- Allow abrt-dump-journal read all non_security socket files
- Allow timemaster write to sysfs files
- Dontaudit domain write cgroup files
- Label /usr/lib/node_modules/npm/bin with bin_t
- Allow ip the setexec permission
- Allow systemd-networkd write files in /var/lib/systemd/network
- Fix typo in systemd_nsresourced_prog_run_bpf()

* Fri Jun 28 2024 Zdenek Pytela <zpytela@redhat.com> - 41.7-1
- Confine libvirt-dbus
- Allow virtqemud the kill capability in user namespace
- Allow rshim get options of the netlink class for KOBJECT_UEVENT family
- Allow dhcpcd the kill capability
- Allow systemd-networkd list /var/lib/systemd/network
- Allow sysadm_t run systemd-nsresourced bpf programs
- Update policy for systemd generators interactions
- Allow create memory.pressure files with cgroup_memory_pressure_t
- Add support for libvirt hooks

* Wed Jun 19 2024 Zdenek Pytela <zpytela@redhat.com> - 41.6-1
- Allow certmonger read and write tpm devices
- Allow all domains to connect to systemd-nsresourced over a unix socket
- Allow systemd-machined read the vsock device
- Update policy for systemd generators
- Allow ptp4l_t request that the kernel load a kernel module
- Allow sbd to trace processes in user namespace
- Allow request-key execute scripts
- Update policy for haproxyd

* Tue Jun 18 2024 Zdenek Pytela <zpytela@redhat.com> - 41.5-1
- Update policy for systemd-nsresourced
- Correct sbin-related file context entries

* Mon Jun 17 2024 Zdenek Pytela <zpytela@redhat.com> - 41.4-1
- Allow login_userdomain execute systemd-tmpfiles in the caller domain
- Allow virt_driver_domain read files labeled unconfined_t
- Allow virt_driver_domain dbus chat with policykit
- Allow virtqemud manage nfs files when virt_use_nfs boolean is on
- Add rules for interactions between generators
- Label memory.pressure files with cgroup_memory_pressure_t
- Revert "Allow some systemd services write to cgroup files"
- Update policy for systemd-nsresourced
- Label /usr/bin/ntfsck with fsadm_exec_t
- Allow systemd_fstab_generator_t read tmpfs files
- Update policy for systemd-nsresourced
- Alias /usr/sbin to /usr/bin and change all /usr/sbin paths to /usr/bin
- Remove a few lines duplicated between {dkim,milter}.fc
- Alias /bin → /usr/bin and remove redundant paths
- Drop duplicate line for /usr/sbin/unix_chkpwd
- Drop duplicate paths for /usr/sbin

* Tue Jun 11 2024 Zdenek Pytela <zpytela@redhat.com> - 41.3-1
- Update systemd-generator policy
- Remove permissive domain for bootupd_t
- Remove permissive domain for coreos_installer_t
- Remove permissive domain for afterburn_t
- Add the sap module to modules.conf
- Move unconfined_domain(sap_unconfined_t) to an optional block
- Create the sap module
- Allow systemd-coredumpd sys_admin and sys_resource capabilities
- Allow systemd-coredump read nsfs files
- Allow generators auto file transition only for plain files
- Allow systemd-hwdb write to the kernel messages device
- Escape "interface" as a file name in a virt filetrans pattern
- Allow gnome-software work for login_userdomain
- Allow systemd-machined manage runtime sockets
- Revert "Allow systemd-machined manage runtime sockets"

* Fri Jun 07 2024 Zdenek Pytela <zpytela@redhat.com> - 41.2-1
- Allow postfix_domain connect to postgresql over a unix socket
- Dontaudit systemd-coredump sys_admin capability
- Allow all domains read and write z90crypt device
- Allow tpm2 generator setfscreate
- Allow systemd (PID 1) manage systemd conf files
- Allow pulseaudio map its runtime files
- Update policy for getty-generator
- Allow systemd-hwdb send messages to kernel unix datagram sockets
- Allow systemd-machined manage runtime sockets

* Mon Jun 03 2024 Zdenek Pytela <zpytela@redhat.com> - 41.1-1
- Allow fstab-generator create unit file symlinks
- Update policy for cryptsetup-generator
- Update policy for fstab-generator
- Allow virtqemud read vm sysctls
- Allow collectd to trace processes in user namespace
- Allow bootupd search efivarfs dirs
- Add policy for systemd-mountfsd
- Add policy for systemd-nsresourced
- Update policy generators
- Add policy for anaconda-generator
- Update policy for fstab and gpt generators
- Add policy for kdump-dep-generator

## END: Generated by rpmautospec
