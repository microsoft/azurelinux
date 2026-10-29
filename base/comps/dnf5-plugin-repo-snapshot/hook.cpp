// SPDX-License-Identifier: MIT
#include "snapshot.hpp"

#include <libdnf5/base/base.hpp>
#include <libdnf5/conf/vars.hpp>
#include <libdnf5/plugin/iplugin.hpp>
#include <libdnf5/repo/repo_query.hpp>
#include <libdnf5/rpm/package_query.hpp>
#include <libdnf5/rpm/package_sack.hpp>
#include <libdnf5/rpm/package_set.hpp>

#include <cstring>
#include <filesystem>
#include <iostream>
#include <set>
#include <stdexcept>

namespace {

class SnapshotHook final : public libdnf5::plugin::IPlugin {
public:
    SnapshotHook(libdnf5::plugin::IPluginData & data, libdnf5::ConfigParser &) : IPlugin(data) {}
    libdnf5::PluginAPIVersion get_api_version() const noexcept override { return libdnf5::PLUGIN_API_VERSION; }
    const char * get_name() const noexcept override { return snapshot::PLUGIN_NAME; }
    libdnf5::plugin::Version get_version() const noexcept override { return {2, 0, 0}; }
    const char * const * get_attributes() const noexcept override {
        static const char * const attributes[]{"description", nullptr};
        return attributes;
    }
    const char * get_attribute(const char * name) const noexcept override {
        return std::strcmp(name, "description") == 0 ? "Repository publication-time cutoff" : nullptr;
    }

    void repos_configured() override {
        auto & base = get_base();
        const auto vars = base.get_vars();
        if (!vars->contains(snapshot::TIME_VAR) || !vars->contains(snapshot::REQUIRES_AVAILABLE_VAR)) {
            return;
        }
        if (vars->get(snapshot::TIME_VAR).priority != libdnf5::Vars::Priority::RUNTIME ||
            (vars->contains(snapshot::EXEMPT_REPOS_VAR) &&
             vars->get(snapshot::EXEMPT_REPOS_VAR).priority != libdnf5::Vars::Priority::RUNTIME)) {
            throw std::runtime_error(
                "snapshot: variables must be set by the DNF5 CLI, not an environment or varsdir fallback");
        }
        (void)snapshot::parse_time(vars->get_value(snapshot::TIME_VAR));
        libdnf5::repo::RepoQuery repos(base);
        for (auto repo : repos) {
            if (repo->get_type() == libdnf5::repo::Repo::Type::AVAILABLE && repo->is_enabled()) {
                // Before loading, make a failed refresh fatal even if a stale primary file remains cached.
                repo->get_config().get_skip_if_unavailable_option().set(libdnf5::Option::Priority::RUNTIME, false);
            }
        }
    }

    void repos_loaded() override {
        auto & base = get_base();
        const auto vars = base.get_vars();
        const bool active = vars->contains(snapshot::TIME_VAR);
        const bool has_exemptions = vars->contains(snapshot::EXEMPT_REPOS_VAR);
        // Reject varsdir/environment fallback: only the validated CLI handoff can activate policy.
        if ((active && vars->get(snapshot::TIME_VAR).priority != libdnf5::Vars::Priority::RUNTIME) ||
            (has_exemptions && vars->get(snapshot::EXEMPT_REPOS_VAR).priority != libdnf5::Vars::Priority::RUNTIME)) {
            throw std::runtime_error(
                "snapshot: variables must be set by the DNF5 CLI, not an environment or varsdir fallback");
        }
        if (!active) {
            if (has_exemptions) {
                throw std::runtime_error("snapshot: repository exemptions require --snapshot-time");
            }
            return;
        }
        // Installed-only queries need no available metadata; a marked request must check it.
        if (!vars->contains(snapshot::REQUIRES_AVAILABLE_VAR)) {
            if (has_exemptions) {
                throw std::runtime_error("snapshot: repository exemptions require available repository loading");
            }
            return;
        }
        const auto cutoff = snapshot::parse_time(vars->get_value(snapshot::TIME_VAR));
        const auto exempt = has_exemptions ? snapshot::parse_exemptions(vars->get_value(snapshot::EXEMPT_REPOS_VAR))
                                           : std::set<std::string>{};
        libdnf5::repo::RepoQuery repos(base);
        std::set<std::string> enabled;
        for (auto repo : repos) {
            if (repo->get_type() == libdnf5::repo::Repo::Type::AVAILABLE && repo->is_enabled()) {
                if (!std::filesystem::is_regular_file(repo->get_metadata_path("primary"))) {
                    throw std::runtime_error(
                        "snapshot: required repository primary metadata unavailable: " + repo->get_id());
                }
                enabled.insert(repo->get_id());
            }
        }
        if (enabled.empty()) {
            throw std::runtime_error("snapshot: no enabled repository available for constrained candidates");
        }
        for (const auto & id : exempt) {
            if (!enabled.contains(id)) {
                throw std::runtime_error("snapshot: exempt repository not enabled or not found: " + id);
            }
            std::cerr << "snapshot: bypassing publication cutoff for entire repository " << id << '\n';
        }
        // Ignore all filters while marking: a command can ignore versionlock or modular
        // exclusions later. The added snapshot exclusions do not change command filters.
        libdnf5::rpm::PackageQuery packages(base, libdnf5::sack::ExcludeFlags::IGNORE_EXCLUDES);
        packages.filter_available();
        libdnf5::rpm::PackageSet excluded(base);
        for (const auto & package : packages) {
            const auto id = package.get_repo_id();
            if (!enabled.contains(id) || exempt.contains(id) || package.is_installed()) {
                continue;
            }
            if (snapshot::filter_package(package.get_file_time(), cutoff, false, false, id, package.get_nevra())) {
                excluded.add(package);
            }
        }
        base.get_rpm_package_sack()->add_user_excludes(excluded);
    }

    void pre_add_cmdline_packages(const std::vector<std::string> & paths) override {
        // Local/URL RPM inputs have no trusted repository publication-time metadata.
        if (get_base().get_vars()->contains(snapshot::TIME_VAR)) {
            for (const auto & spec : paths) {
                if (spec.ends_with(".rpm") || spec.find("://") != std::string::npos) {
                    throw std::runtime_error("snapshot: local and URL RPM inputs are unsupported with --snapshot-time");
                }
            }
        }
    }
};

}  // namespace

// libdnf5 resolves these fixed, unmangled loader entry points into this C++ backend.
extern "C" libdnf5::PluginAPIVersion libdnf_plugin_get_api_version() {
    return libdnf5::PLUGIN_API_VERSION;
}
extern "C" const char * libdnf_plugin_get_name() {
    return snapshot::PLUGIN_NAME;
}
extern "C" libdnf5::plugin::Version libdnf_plugin_get_version() {
    return {2, 0, 0};
}
extern "C" libdnf5::plugin::IPlugin * libdnf_plugin_new_instance(
    libdnf5::LibraryVersion, libdnf5::plugin::IPluginData & data, libdnf5::ConfigParser & parser) {
    return new SnapshotHook(data, parser);
}
extern "C" void libdnf_plugin_delete_instance(libdnf5::plugin::IPlugin * instance) {
    delete instance;
}
