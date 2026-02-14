%define release_name Evergreen
%define is_evergreen 1

# Define this to 1 for Branched releases prior to RC
# or 0 for RC and stable releases
%define is_development 1

# TODO(azl): review -- set to a future date for now, fix before release
%define eol_date 1900-01-01

%define dist_version_major 4
%define dist_version_minor 0
%define dist_version %{dist_version_major}.%{dist_version_minor}

%if %{is_evergreen}
%define bug_version evergreen
%define releasever evergreen
%define doc_version evergreen
%else
%define bug_version %{dist_version}
%define releasever %{dist_version}
%define doc_version %{dist_version}
%endif

%bcond basic 1
%bcond cloud 1
%bcond container 1
%bcond wsl 1

# TODO(azl): review how this will get resolved
# ...global dist

Summary:        Azure Linux release files
Name:           azurelinux-release
Version:        4.0
# The numbering is 0.<r> before a given release is released,
# and then just <r>.
Release:        %autorelease %[0%{?is_development} ? "-p" : ""]
License:        MIT
URL:            https://aka.ms/azurelinux

Source1:        LICENSE

Source11:       90-default.preset
Source12:       90-default-user.preset
Source13:       99-default-disable.preset
Source14:       distro-template.swidtag
Source15:       distro-variant-template.swidtag
Source16:       20-azurelinux-defaults.conf

BuildArch:      noarch

Provides:       azurelinux-release = %{version}-%{release}
Provides:       azurelinux-release-variant = %{version}-%{release}

Provides:       system-release
Provides:       system-release(%{version})
Requires:       azurelinux-release-common = %{version}-%{release}

# azurelinux-release-common Requires: azurelinux-release-identity, so at least one
# package must provide it. This Recommends: pulls in
# azurelinux-release-identity-basic if nothing else is already doing so.
Recommends:     azurelinux-release-identity-basic


BuildRequires:  azurelinux-rpm-config
BuildRequires:  systemd-rpm-macros

%description
Azure Linux release files such as various /etc/ files that define the release
and systemd preset files that determine which services are enabled by default.

%package common
Summary: Azure Linux release files

Requires:   azurelinux-release-variant = %{version}-%{release}
Suggests:   azurelinux-release

Requires:   azurelinux-repos(%{version})
Requires:   azurelinux-release-identity = %{version}-%{release}

%if %{is_evergreen}
# Make $releasever return "evergreen" on Evergreen.
Provides:       system-release(releasever) = %{releasever}
%endif

%description common
Release files common to all variants of Azure Linux

%if %{with basic}
%package identity-basic
Summary:        Package providing the basic Azure Linux identity

RemovePathPostfixes: .basic
Provides:       azurelinux-release-identity = %{version}-%{release}
Conflicts:      azurelinux-release-identity


%description identity-basic
Provides the necessary files for a Azure Linux installation that is not identifying
itself as a particular variant.
%endif


%if %{with cloud}
%package cloud
Summary:        Base package for Azure Linux Cloud-specific default configurations

RemovePathPostfixes: .cloud
Provides:       azurelinux-release = %{version}-%{release}
Provides:       azurelinux-release-variant = %{version}-%{release}
Provides:       system-release
Provides:       system-release(%{version})
Requires:       azurelinux-release-common = %{version}-%{release}

# azurelinux-release-common Requires: azurelinux-release-identity, so at least one
# package must provide it. This Recommends: pulls in
# azurelinux-release-identity-cloud if nothing else is already doing so.
Recommends:     azurelinux-release-identity-cloud


%description cloud
Provides a base package for Azure Linux Cloud-specific configuration files to
depend on.


%package identity-cloud
Summary:        Package providing the identity for Azure Linux Cloud variant

RemovePathPostfixes: .cloud
Provides:       azurelinux-release-identity = %{version}-%{release}
Conflicts:      azurelinux-release-identity
Requires(meta): azurelinux-release-cloud = %{version}-%{release}


%description identity-cloud
Provides the necessary files for a Azure Linux installation that is identifying
itself as Azure Linux Cloud variant.
%endif


%if %{with container}
%package container
Summary:        Base package for Azure Linux container specific default configurations

RemovePathPostfixes: .container
Provides:       azurelinux-release = %{version}-%{release}
Provides:       azurelinux-release-variant = %{version}-%{release}
Provides:       system-release
Provides:       system-release(%{version})
Requires:       azurelinux-release-common = %{version}-%{release}

# azurelinux-release-common Requires: azurelinux-release-identity, so at least one
# package must provide it. This Recommends: pulls in
# azurelinux-release-identity-container if nothing else is already doing so.
Recommends:     azurelinux-release-identity-container


%description container
Provides a base package for Azure Linux container specific configuration files to
depend on as well as container system defaults.


%package identity-container
Summary:        Package providing the identity for Azure Linux Container Base Image

RemovePathPostfixes: .container
Provides:       azurelinux-release-identity = %{version}-%{release}
Conflicts:      azurelinux-release-identity
Requires(meta): azurelinux-release-container = %{version}-%{release}


%description identity-container
Provides the necessary files for a Azure Linux installation that is identifying
itself as the Azure Linux Container Base Image.
%endif


%if %{with wsl}
%package wsl
Summary:        Base package for Azure Linux WSL specific default configurations

RemovePathPostfixes: .wsl
Provides:       azurelinux-release = %{version}-%{release}
Provides:       azurelinux-release-variant = %{version}-%{release}
Provides:       system-release
Provides:       system-release(%{version})
Requires:       azurelinux-release-common = %{version}-%{release}

# azurelinux-release-common Requires: azurelinux-release-identity, so at least one
# package must provide it. This Recommends: pulls in
# azurelinux-release-identity-wsl if nothing else is already doing so.
Recommends:     azurelinux-release-identity-wsl


%description wsl
Provides a base package for Azure Linux WSL specific configuration files to
depend on as well as WSL system defaults.


%package identity-wsl
Summary:        Package providing the identity for Azure Linux WSL.

RemovePathPostfixes: .wsl
Provides:       azurelinux-release-identity = %{version}-%{release}
Conflicts:      azurelinux-release-identity
Requires(meta): azurelinux-release-container = %{version}-%{release}


%description identity-wsl
Provides the necessary files for a Azure Linux installation that is identifying
itself as Azure Linux WSL.
%endif

%prep
mkdir -p licenses

%build

%install
install -d %{buildroot}%{_prefix}/lib
echo "Azure Linux release %{version} (%{release_name})" > %{buildroot}%{_prefix}/lib/azurelinux-release
echo "cpe:/o:microsoft:azurelinux:%{version}" > %{buildroot}%{_prefix}/lib/system-release-cpe

# Symlink the -release files
install -d %{buildroot}%{_sysconfdir}
ln -s ../usr/lib/azurelinux-release %{buildroot}%{_sysconfdir}/azurelinux-release
ln -s ../usr/lib/system-release-cpe %{buildroot}%{_sysconfdir}/system-release-cpe
# TODO(azl): validate
# ln -s azurelinux-release %{buildroot}%{_sysconfdir}/azurelinux-release
ln -s azurelinux-release %{buildroot}%{_sysconfdir}/system-release

# Create the common os-release file
%{lua:
  function starts_with(str, start)
   return str:sub(1, #start) == start
  end
}
%define starts_with(str,prefix) (%{expand:%%{lua:print(starts_with(%1, %2) and "1" or "0")}})
%if %{starts_with "a%{release}" "a0"}
  %global prerelease \ Prerelease
%endif

# -------------------------------------------------------------------------
# Definitions for /etc/os-release and for macros in macros.dist.  These
# macros are useful for spec files where distribution-specific identifiers
# are used to customize packages.

# Name of vendor / name of distribution. Typically used to identify where
# the binary comes from in --help or --version messages of programs.
# Examples: gdb.spec, clang.spec
%global dist_vendor Microsoft Corporation
%global dist_name   Azure Linux

# The namespace for purl
# https://github.com/package-url/purl-spec
# for example as in: pkg:rpm/azurelinux/python-setuptools@69.2.0-10.azl4?arch=src"
%global dist_purl_namespace azurelinux

# URL of the homepage of the distribution
# Example: gstreamer1-plugins-base.spec
%global dist_home_url https://aka.ms/azurelinux

# Bugzilla / bug reporting URLs shown to users.
# Examples: gcc.spec
%global dist_bug_report_url https://aka.ms/azurelinux

# debuginfod server, as used in elfutils.spec.
# TODO(azl): review
%global dist_debuginfod_url ima:enforcing https://debuginfod.microsoft.com/ ima:ignore
# -------------------------------------------------------------------------

# Set the RELEASE_TYPE appropriately
%define release_type %[0%{?is_development} ? "development" : "stable"]

cat <<EOF >os-release
NAME="%{dist_name}"
VERSION="%{dist_version} (%{release_name}%{?prerelease})"
RELEASE_TYPE=%{release_type}
ID=azurelinux
VERSION_ID=%{dist_version}
VERSION_CODENAME=""
PRETTY_NAME="Azure Linux %{dist_version} (%{release_name}%{?prerelease})"
ANSI_COLOR="0;38;2;60;110;180"
LOGO=azurelinux-logo-icon
# TODO(azl): review
CPE_NAME="cpe:/o:azurelinuxproject:azurelinux:%{dist_version}"
DEFAULT_HOSTNAME="azurelinux"
HOME_URL="%{dist_home_url}"
DOCUMENTATION_URL="https://aka.ms/azurelinux"
SUPPORT_URL="https://aka.ms/azurelinux"
BUG_REPORT_URL="%{dist_bug_report_url}"
SUPPORT_END=%{eol_date}
EOF

# Create the common /etc/issue
echo "\S" > %{buildroot}%{_prefix}/lib/issue
echo "Kernel \r on \m (\l)" >> %{buildroot}%{_prefix}/lib/issue
echo >> %{buildroot}%{_prefix}/lib/issue
ln -s ../usr/lib/issue %{buildroot}%{_sysconfdir}/issue

# Create /etc/issue.net
echo "\S" > %{buildroot}%{_prefix}/lib/issue.net
echo "Kernel \r on \m (\l)" >> %{buildroot}%{_prefix}/lib/issue.net
ln -s ../usr/lib/issue.net %{buildroot}%{_sysconfdir}/issue.net

# Create /etc/issue.d
mkdir -p %{buildroot}%{_sysconfdir}/issue.d

mkdir -p %{buildroot}%{_swidtagdir}

# Create os-release files for the different variants

%if %{with basic}
# Basic
cp -p os-release \
      %{buildroot}%{_prefix}/lib/os-release.basic
%endif

%if %{with cloud}
# Cloud
cp -p os-release \
      %{buildroot}%{_prefix}/lib/os-release.cloud
echo "VARIANT=\"Cloud Variant\"" >> %{buildroot}%{_prefix}/lib/os-release.cloud
echo "VARIANT_ID=cloud" >> %{buildroot}%{_prefix}/lib/os-release.cloud
sed -i -e "s|(%{release_name}%{?prerelease})|(Cloud Variant%{?prerelease})|g" %{buildroot}%{_prefix}/lib/os-release.cloud
sed -e "s#\$version#%{bug_version}#g" -e 's/$variant/Cloud/;s/<!--.*-->//;/^$/d' %{SOURCE15} > %{buildroot}%{_swidtagdir}/com.microsoft.AzureLinux-variant.swidtag.cloud
sed -i -e "/^DEFAULT_HOSTNAME=/d" %{buildroot}%{_prefix}/lib/os-release.cloud
%endif

%if %{with container}
# Container
cp -p os-release \
      %{buildroot}%{_prefix}/lib/os-release.container
echo "VARIANT=\"Container Image\"" >> %{buildroot}%{_prefix}/lib/os-release.container
echo "VARIANT_ID=container" >> %{buildroot}%{_prefix}/lib/os-release.container
sed -i -e "s|(%{release_name}%{?prerelease})|(Container Image%{?prerelease})|g" %{buildroot}%{_prefix}/lib/os-release.container
sed -e "s#\$version#%{bug_version}#g" -e 's/$variant/Container/;s/<!--.*-->//;/^$/d' %{SOURCE15} > %{buildroot}%{_swidtagdir}/com.microsoft.AzureLinux-variant.swidtag.container
%endif

%if %{with wsl}
cp -p os-release %{buildroot}%{_prefix}/lib/os-release.wsl
echo "VARIANT=\"WSL\"" >> %{buildroot}%{_prefix}/lib/os-release.wsl
echo "VARIANT_ID=wsl" >> %{buildroot}%{_prefix}/lib/os-release.wsl
sed -i -e "s|(%{release_name}%{?prerelease})|(WSL%{?prerelease})|g" %{buildroot}%{_prefix}/lib/os-release.wsl
sed -e "s#\$version#%{bug_version}#g" -e 's/$variant/WSL/;s/<!--.*-->//;/^$/d' %{SOURCE15} > %{buildroot}%{_swidtagdir}/com.microsoft.AzureLinux-variant.swidtag.wsl
%endif

# Create the symlink for /etc/os-release
ln -s ../usr/lib/os-release %{buildroot}%{_sysconfdir}/os-release

# Set up the dist tag macros
install -d -m 755 %{buildroot}%{_rpmconfigdir}/macros.d
cat >> %{buildroot}%{_rpmconfigdir}/macros.d/macros.dist << EOF
# dist macros.

%%__bootstrap         ~bootstrap
%%azurelinux          %{dist_version}
%%azl4                1
%%distcore            .azl%%{dist_version_major}
%%dist                %%{!?distprefix0:%%{?distprefix}}%%{expand:%%{lua:for i=0,9999 do print("%%{?distprefix" .. i .."}") end}}%%{distcore}%%{?with_bootstrap:%%{__bootstrap}}%%{?buildrelease:+build%%{buildrelease}}
%%dist_vendor         %{dist_vendor}
%%dist_name           %{dist_name}
%%dist_purl_namespace %{dist_purl_namespace}
%%dist_home_url       %{dist_home_url}
%%dist_bug_report_url %{dist_bug_report_url}
%%dist_debuginfod_url %{dist_debuginfod_url}
EOF

# Install licenses
install -pm 0644 %{SOURCE1} licenses/LICENSE

# Default system wide
install -Dm0644 %{SOURCE11} -t %{buildroot}%{_prefix}/lib/systemd/system-preset/
install -Dm0644 %{SOURCE12} -t %{buildroot}%{_prefix}/lib/systemd/user-preset/
# The same file is installed in two places with identical contents
install -Dm0644 %{SOURCE13} -t %{buildroot}%{_prefix}/lib/systemd/system-preset/
install -Dm0644 %{SOURCE13} -t %{buildroot}%{_prefix}/lib/systemd/user-preset/

# Create distro-level SWID tag file
install -d %{buildroot}%{_swidtagdir}
sed -e "s#\$version#%{bug_version}#g" -e 's/<!--.*-->//;/^$/d' %{SOURCE14} > %{buildroot}%{_swidtagdir}/com.microsoft.AzureLinux-%{bug_version}.swidtag
install -d %{buildroot}%{_sysconfdir}/swid/swidtags.d
ln -s --relative %{buildroot}%{_swidtagdir} %{buildroot}%{_sysconfdir}/swid/swidtags.d/microsoft.com

# Install DNF 5 configuration defaults
install -Dm0644 %{SOURCE16} -t %{buildroot}%{_prefix}/share/dnf5/libdnf.conf.d/


%files common
%license licenses/LICENSE
%{_prefix}/lib/azurelinux-release
%{_prefix}/lib/system-release-cpe
%{_sysconfdir}/os-release
%{_sysconfdir}/azurelinux-release
# TODO(azl): review
# %{_sysconfdir}/azurelinux-release
%{_sysconfdir}/system-release
%{_sysconfdir}/system-release-cpe
%attr(0644,root,root) %{_prefix}/lib/issue
%config(noreplace) %{_sysconfdir}/issue
%attr(0644,root,root) %{_prefix}/lib/issue.net
%config(noreplace) %{_sysconfdir}/issue.net
%dir %{_sysconfdir}/issue.d
%attr(0644,root,root) %{_rpmconfigdir}/macros.d/macros.dist
%dir %{_prefix}/lib/systemd/user-preset/
%{_prefix}/lib/systemd/user-preset/90-default-user.preset
%{_prefix}/lib/systemd/user-preset/99-default-disable.preset
%dir %{_prefix}/lib/systemd/system-preset/
%{_prefix}/lib/systemd/system-preset/90-default.preset
%{_prefix}/lib/systemd/system-preset/99-default-disable.preset
%dir %{_swidtagdir}
%{_swidtagdir}/com.microsoft.AzureLinux-%{bug_version}.swidtag
%dir %{_sysconfdir}/swid
%{_sysconfdir}/swid/swidtags.d
%{_prefix}/share/dnf5/libdnf.conf.d/20-azurelinux-defaults.conf


%if %{with basic}
%files
%files identity-basic
%{_prefix}/lib/os-release.basic
%endif


%if %{with cloud}
%files cloud
%files identity-cloud
%{_prefix}/lib/os-release.cloud
%attr(0644,root,root) %{_swidtagdir}/com.microsoft.AzureLinux-variant.swidtag.cloud
%endif


%if %{with container}
%files container
%files identity-container
%{_prefix}/lib/os-release.container
%attr(0644,root,root) %{_swidtagdir}/com.microsoft.AzureLinux-variant.swidtag.container
%endif


%if %{with wsl}
%files wsl
%files identity-wsl
%{_prefix}/lib/os-release.wsl
%attr(0644,root,root) %{_swidtagdir}/com.microsoft.AzureLinux-variant.swidtag.wsl
%endif


%changelog
%autochangelog
