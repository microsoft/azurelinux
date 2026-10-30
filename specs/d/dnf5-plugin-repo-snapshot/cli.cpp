// SPDX-License-Identifier: MIT
#include "snapshot.hpp"

#include <dnf5/context.hpp>
#include <dnf5/iplugin.hpp>
#include <libdnf5-cli/argument_parser.hpp>
#include <libdnf5-cli/argument_parser_errors.hpp>
#include <libdnf5/base/base.hpp>
#include <libdnf5/conf/vars.hpp>
#include <libdnf5/plugin/plugin_info.hpp>
#include <libdnf5/utils/bgettext/bgettext-mark.h>

#include <cstring>
#include <stdexcept>
#include <vector>

namespace {

class SnapshotCli final : public dnf5::IPlugin {
public:
    using IPlugin::IPlugin;

    dnf5::PluginAPIVersion get_api_version() const noexcept override { return dnf5::PLUGIN_API_VERSION; }
    const char * get_name() const noexcept override { return snapshot::PLUGIN_NAME; }
    dnf5::PluginVersion get_version() const noexcept override { return {2, 0, 0}; }
    const char * const * get_attributes() const noexcept override {
        static const char * const attributes[]{"description", nullptr};
        return attributes;
    }
    const char * get_attribute(const char * name) const noexcept override {
        return std::strcmp(name, "description") == 0 ? "Repository publication-time cutoff" : nullptr;
    }
    std::vector<std::unique_ptr<dnf5::Command>> create_commands() override { return {}; }
    void finish() noexcept override {}

    void post_base_setup() {
        auto & context = get_context();
        auto & base = context.get_base();
        if (!base.get_vars()->contains(snapshot::TIME_VAR)) {
            return;
        }
        // The CLI validates the request while parsing, but only Base::setup() reveals the
        // backend actually loaded and the effective configuration before repository activity.
        bool backend_ready = false;
        for (const auto & info : base.get_plugins_info()) {
            if (!info.is_loaded() || !info.get_real_name() ||
                std::strcmp(info.get_real_name(), snapshot::PLUGIN_NAME) != 0) {
                continue;
            }
            const auto api = info.get_api_version();
            const auto version = info.get_version();
            backend_ready = api.major == 2 && api.minor >= 2 && version.major == 2 && version.minor == 0;
            if (backend_ready) {
                break;
            }
        }
        if (!backend_ready) {
            throw std::runtime_error(
                "snapshot: --snapshot-time requires a loaded, compatible repo_snapshot backend (plugin 2.0.x, API "
                "2.2+)");
        }
        if (!base.get_config().get_disable_excludes_option().get_value().empty()) {
            throw std::runtime_error("snapshot: --snapshot-time cannot be combined with disable_excludes");
        }
        const auto invocation = context.get_argument_parser().get_selected_command()->get_invocation();
        if (base.get_config().get_downloadonly_option().get_value() ||
            (invocation.size() == 2 && invocation[1] == "upgrade" && !base.get_config().get_destdir_option().empty())) {
            throw std::runtime_error("snapshot: --snapshot-time cannot use download-only mode or upgrade --destdir");
        }
        if (invocation.size() == 2 && (invocation[1] == "install" || invocation[1] == "upgrade") &&
            (base.get_config().get_skip_broken_option().get_value() ||
             base.get_config().get_skip_unavailable_option().get_value())) {
            throw std::runtime_error("snapshot: --snapshot-time cannot skip broken or unavailable packages");
        }
    }

    void init() override {
        auto & context = get_context();
        auto & parser = context.get_argument_parser();
        auto & root = *parser.get_root_command();
        auto & group = root.get_group("global_options");
        // Validate at parse time and hand the request to repos_loaded() through private Vars.
        auto * time = parser.add_new_named_arg("snapshot-time");
        time->set_long_name("snapshot-time");
        time->set_has_value(true);
        time->set_arg_value_help("POSIX_SECONDS");
        time->set_description("Exclude repository RPMs published after this POSIX second");
        time->set_parse_hook_func(
            [&context](libdnf5::cli::ArgumentParser::NamedArg *, const char *, const char * value) {
                std::uint64_t validated;
                try {
                    validated = snapshot::parse_time(value);
                } catch (const std::exception & error) {
                    throw libdnf5::cli::ArgumentParserInvalidValueError(
                        M_("--snapshot-time: {}"), std::string(error.what()));
                }
                context.get_base().get_vars()->set(snapshot::TIME_VAR, std::to_string(validated));
                return true;
            });
        root.register_named_arg(time);
        group.register_argument(time);

        auto * exempt = parser.add_new_named_arg("snapshot-exclude-repos");
        exempt->set_long_name("snapshot-exclude-repos");
        exempt->set_has_value(true);
        exempt->set_arg_value_help("REPO_ID,...");
        exempt->set_description("Bypass the snapshot cutoff for entire named repositories (comma-separated IDs)");
        exempt->set_parse_hook_func(
            [&context](libdnf5::cli::ArgumentParser::NamedArg *, const char *, const char * value) {
                try {
                    (void)snapshot::parse_exemptions(value);
                } catch (const std::exception & error) {
                    throw libdnf5::cli::ArgumentParserInvalidValueError(
                        M_("--snapshot-exclude-repos: {}"), std::string(error.what()));
                }
                context.get_base().get_vars()->set(snapshot::EXEMPT_REPOS_VAR, value);
                return true;
            });
        root.register_named_arg(exempt);
        group.register_argument(exempt);

        const auto previous = root.get_parse_hook_func();
        root.set_parse_hook_func([&context, previous](
                                     libdnf5::cli::ArgumentParser::Command * command,
                                     const char * option,
                                     int argc,
                                     const char * const argv[]) {
            if (previous && !previous(command, option, argc, argv)) {
                return false;
            }
            auto vars = context.get_base().get_vars();
            if (!vars->contains(snapshot::TIME_VAR)) {
                if (vars->contains(snapshot::EXEMPT_REPOS_VAR)) {
                    throw libdnf5::cli::ArgumentParserInvalidValueError(
                        M_("--snapshot-exclude-repos requires --snapshot-time"));
                }
                return true;
            }
            const auto invocation = context.get_argument_parser().get_selected_command()->get_invocation();
            if (invocation.size() != 2 ||
                (invocation[1] != "install" && invocation[1] != "upgrade" && invocation[1] != "repoquery")) {
                throw libdnf5::cli::ArgumentParserInvalidValueError(
                    M_("--snapshot-time supports only repository install, upgrade, and repoquery"));
            }
            const auto & selected = *context.get_argument_parser().get_selected_command();
            std::vector<std::string> parsed_options;
            for (const auto * named : selected.get_named_args()) {
                if (named->get_parse_count() == 0) {
                    continue;
                }
                const auto & name = named->get_long_name();
                parsed_options.emplace_back(name);
                if (name == "downloadonly" || name == "store" || name == "offline" || name == "disableexcludes" ||
                    name == "disable-excludes") {
                    throw libdnf5::cli::ArgumentParserInvalidValueError(M_(
                        "--snapshot-time does not support offline, download-only, or exclusion-bypassing operations"));
                }
            }
            // Only parsed flags affect scope; install/upgrade always need available candidates.
            // This private marker tells the backend when metadata must be checked, not what to load.
            const bool requires_available = snapshot::requires_available_candidates(invocation[1], parsed_options);
            if (requires_available) {
                vars->set(snapshot::REQUIRES_AVAILABLE_VAR, "1");
            }
            return true;
        });
    }
};

}  // namespace

// DNF5 resolves these fixed, unmangled loader entry points; they bridge into the C++ plugin.
extern "C" dnf5::PluginAPIVersion dnf5_plugin_get_api_version() {
    return dnf5::PLUGIN_API_VERSION;
}
extern "C" const char * dnf5_plugin_get_name() {
    return snapshot::PLUGIN_NAME;
}
extern "C" dnf5::PluginVersion dnf5_plugin_get_version() {
    return {2, 0, 0};
}
extern "C" dnf5::IPlugin * dnf5_plugin_new_instance(dnf5::ApplicationVersion, dnf5::Context & context) {
    return new SnapshotCli(context);
}
extern "C" void dnf5_plugin_delete_instance(dnf5::IPlugin * instance) {
    delete instance;
}
extern "C" void dnf5_plugin_post_base_setup(dnf5::IPlugin * instance) {
    static_cast<SnapshotCli *>(instance)->post_base_setup();
}
