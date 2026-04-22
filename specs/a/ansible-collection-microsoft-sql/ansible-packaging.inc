%if 0%{?rhel}
# Helper macros originally from macros.ansible by Igor Raits <ignatenkobrain>
# This file is for maintaining the compatibility with macros and other
# functionality (generators) provided by ansible-packaging on Fedora.

Provides: ansible-collection(%{collection_namespace}.%{collection_name}) = %{collection_version}

# ansible-galaxy is available by ansible-core on RHEL 8.6 and newer at buildtime.
%define ansible_collection_build() ansible-galaxy collection build
%define ansible_collection_install() ansible-galaxy collection install -n -p %{buildroot}%{_datadir}/ansible/collections %{collection_namespace}-%{collection_name}-%{version}.tar.gz

%define ansible_roles_dir %{_datadir}/ansible/roles
%define ansible_collections_dir %{_datadir}/ansible/collections/ansible_collections

# TODO: Officially deprecate this macro and add the following line to the macro
# def after the new approach has gotten more testing and adoption:
# %%{warn: %%{ansible_collection_files} is deprecated. Use %%files -f %%{ansible_collection_filelist} instead.}
%define ansible_collection_files %{shrink:
%{ansible_collections_dir}/%{collection_namespace}/
}

%define ansible_collection_filelist %{__ansible_builddir}/ansible_collection_files
%endif
