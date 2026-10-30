// SPDX-License-Identifier: MIT
#pragma once

#include <cstdint>
#include <optional>
#include <set>
#include <string>
#include <string_view>
#include <vector>

namespace snapshot {

// Private CLI-to-backend request handoff, not persistent configuration or repository IDs.
inline constexpr char TIME_VAR[] = "azl_snapshot_time";
inline constexpr char EXEMPT_REPOS_VAR[] = "azl_snapshot_exempt_repos";
inline constexpr char REQUIRES_AVAILABLE_VAR[] = "azl_snapshot_requires_available";
inline constexpr char PLUGIN_NAME[] = "repo_snapshot";

std::uint64_t parse_time(const std::string & value);
std::set<std::string> parse_exemptions(const std::string & value);
bool requires_available_candidates(std::string_view command, const std::vector<std::string> & parsed_options);

bool filter_package(
    std::optional<unsigned long long> file_time,
    std::optional<std::uint64_t> cutoff,
    bool installed,
    bool exempt,
    const std::string & repo_id,
    const std::string & nevra);

}  // namespace snapshot
