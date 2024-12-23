Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%if 0%{?fedora} >= 36 || 0%{?rhel} > 9
%global dict_dirname hunspell
%else
%global dict_dirname myspell
%endif
 
Name:         hunspell-it
Summary:      Italian hunspell dictionaries
Version:      5.1.1
Release:      6%{?dist}
# The license text is embedded within the README files
# Here we specify the hunspell files license only as other files are not packaged 
License:      GPL-3.0-only
URL:          https://pagure.io/dizionario_italiano
Source:       %{url}/archive/%{version}/dizionario_italiano-%{version}.tar.gz
 
BuildArch:    noarch
Requires:     hunspell-filesystem
Supplements:  (hunspell and langpacks-it)
 
%description
Italian hunspell dictionaries.
 
 
%prep
%autosetup -n dizionario_italiano-%{version}
 
 
%build
# Nothing to do
 
 
%install
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/%{dict_dirname}
cp -p it_IT.dic it_IT.aff $RPM_BUILD_ROOT/%{_datadir}/%{dict_dirname}
pushd $RPM_BUILD_ROOT/%{_datadir}/%{dict_dirname}/
it_IT_aliases="it_CH"
for lang in $it_IT_aliases; do
        ln -s it_IT.aff $lang.aff
        ln -s it_IT.dic $lang.dic
done
 
 
 
%files
%license LICENSES/gpl-3.0.txt
%doc CHANGELOG.txt README.md README_it_IT.txt
%{_datadir}/%{dict_dirname}/*
 
%changelog
* Tue Dec 17 2024 Akarsh Chaudhary <v-akarshc@microsoft.com> - 5.1.1-6
- AzureLinux import from Fedora 41.
- License verified
