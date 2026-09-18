local pg = require("pyproject_getopt")

local M = {}


-- Helpers

local function assert_defined(name)
    assert(
        rpm.expand("%{defined __pyproject_opt_" .. name .. "}") == "1",
        "expected __pyproject_opt_" .. name .. " to be defined"
    )
end

local function assert_undefined(name)
    assert(
        rpm.expand("%{undefined __pyproject_opt_" .. name .. "}") == "1",
        "expected __pyproject_opt_" .. name .. " to be undefined"
    )
end

local function assert_value(name, expected)
    local actual = rpm.expand("%{?__pyproject_opt_" .. name .. "}")
    assert(
        actual == expected,
        "expected __pyproject_opt_" .. name .. "=" .. expected .. ", got " .. actual
    )
end

local function assert_optflag(name, expected)
    local actual = rpm.expand("%{?__pyproject_optflag_" .. name .. "}")
    assert(
        actual == expected,
        "expected __pyproject_optflag_" .. name .. "=" .. expected .. ", got " .. actual
    )
end

local function assert_optflag_undefined(name)
    assert(
        rpm.expand("%{undefined __pyproject_optflag_" .. name .. "}") == "1",
        "expected __pyproject_optflag_" .. name .. " to be undefined"
    )
end

local function assert_positional(expected)
    local actual = rpm.expand("%{?__pyproject_positional_args}")
    assert(
        actual == expected,
        "expected positional=" .. expected .. ", got " .. actual
    )
end

local function assert_errors(fn)
    local ok = pcall(fn)
    assert(not ok, "expected an error but call succeeded")
end

local function skip(reason)
    print("SKIP: " .. reason)
end


-- Specs
-- The specs here were copied from the implementation of the macros
-- when this test was added. But no need to keep them in sync,
-- as long as we test what needs to be tested.

local SAVE_FILES_SPEC = {
    {short="l", long="assert-license"},
    {short="L", long="no-assert-license"},
    {short="M", long="allow-no-modules"},
}

local WHEEL_SPEC = {
    {short="C", long="config-settings", value=true, separator=","},
    {short="d", long="directory", value=true},
}

local BUILDREQUIRES_SPEC = {
    {short="r", long="runtime"},
    {short="R", long="no-runtime"},
    {short="x", long="extras", value=true, separator=","},
    {short="t", long="tox"},
    {short="N", long="no-use-build-system"},
    {short="w", long="wheel"},
    {short="p", long="pyproject-dependencies"},
    {short="e", long="toxenv", value=true, separator=","},
    {short="g", long="dependency-groups", value=true, separator=","},
    {short="C", long="config-settings", value=true, separator=","},
    {short="d", long="directory", value=true},
}

local BUILDREQUIRES_EXCLUSIONS = {
    {"R", {"r", "x", "e", "t", "w", "p"}},
    {"N", {"r", "x", "e", "t", "w", "p", "C"}},
    {"w", {"p"}},
}

local CHECK_IMPORT_SPEC = {
    {short="e", long="exclude", value=true, separator=" -e "},
    {short="t", long="top-level-only"},
}

local TOX_SPEC = {
    {short="e", long="toxenv", value=true, separator=","},
}


-- Short flags

function M.test_single_flag()
    pg.getopt(SAVE_FILES_SPEC, nil, {"-l"}, "test")
    assert_defined("l")
    assert_undefined("L")
    assert_undefined("M")
end

function M.test_multiple_flags()
    pg.getopt(SAVE_FILES_SPEC, nil, {"-l", "-M"}, "test")
    assert_defined("l")
    assert_defined("M")
    assert_undefined("L")
end

function M.test_repeated_flag()
    pg.getopt(SAVE_FILES_SPEC, nil, {"-l", "-l"}, "test")
    assert_defined("l")
end

function M.test_bundled_flags()
    pg.getopt(SAVE_FILES_SPEC, nil, {"-lM"}, "test")
    assert_defined("l")
    assert_defined("M")
end


-- Long flags

function M.test_single_long_flag()
    pg.getopt(SAVE_FILES_SPEC, nil, {"--assert-license"}, "test")
    assert_defined("l")
    assert_undefined("L")
end

function M.test_multiple_long_flags()
    pg.getopt(SAVE_FILES_SPEC, nil, {"--assert-license", "--allow-no-modules"}, "test")
    assert_defined("l")
    assert_defined("M")
end


-- Value options

function M.test_short_with_value()
    pg.getopt(WHEEL_SPEC, nil, {"-d", "foo"}, "test")
    assert_value("d", "foo")
end

function M.test_short_value_attached()
    pg.getopt(WHEEL_SPEC, nil, {"-dfoo"}, "test")
    assert_value("d", "foo")
end

function M.test_long_with_value()
    pg.getopt(WHEEL_SPEC, nil, {"--directory", "foo"}, "test")
    assert_value("d", "foo")
end

function M.test_long_with_equals()
    pg.getopt(WHEEL_SPEC, nil, {"--directory=foo"}, "test")
    assert_value("d", "foo")
end

function M.test_value_with_spaces()
    pg.getopt(WHEEL_SPEC, nil, {"-d", "Path With Spaces"}, "test")
    assert_value("d", "Path With Spaces")
end

function M.test_long_value_with_spaces()
    pg.getopt(WHEEL_SPEC, nil, {"--directory", "Path With Spaces"}, "test")
    assert_value("d", "Path With Spaces")
end

function M.test_empty_value()
    pg.getopt(WHEEL_SPEC, nil, {"-d", ""}, "test")
    assert_defined("d")
    assert_value("d", "")
end

function M.test_empty_value_stays_single_arg()
    if not pg._use_quote then return skip("%{quote:} not transparent on this RPM") end
    pg.getopt(WHEEL_SPEC, nil, {"-d", ""}, "test")
    rpm.define([[_test_countargs(-) %#]])
    local nargs = rpm.expand("%_test_countargs %{__pyproject_opt_d}")
    assert(nargs == "1",
        "expected empty value to be 1 arg, got " .. nargs)
end

function M.test_value_with_spaces_stays_single_arg()
    if not pg._use_quote then return skip("%{quote:} not transparent on this RPM") end
    pg.getopt(WHEEL_SPEC, nil, {"-d", "Path With Spaces"}, "test")
    -- Define a macro that expands to its argument count
    rpm.define([[_test_countargs(-) %#]])
    -- Pass the stored value to another macro — it must stay as 1 argument
    local nargs = rpm.expand("%_test_countargs %{__pyproject_opt_d}")
    assert(nargs == "1",
        "expected value with spaces to be 1 arg, got " .. nargs)
end

function M.test_value_looking_like_option()
    pg.getopt(WHEEL_SPEC, nil, {"--config-settings", "--with-dashes=1"}, "test")
    assert_defined("C")
end

function M.test_short_value_attached_looking_like_option()
    pg.getopt(WHEEL_SPEC, nil, {"-C--with-dashes=1"}, "test")
    assert_defined("C")
end


-- Repeated options

function M.test_repeated_parse_option_comma_joins()
    pg.getopt(TOX_SPEC, nil, {"-e", "env1", "-e", "env2"}, "test")
    assert_value("e", "env1,env2")
end

function M.test_repeated_long_parse_option()
    pg.getopt(TOX_SPEC, nil, {"--toxenv", "env1", "--toxenv", "env2"}, "test")
    assert_value("e", "env1,env2")
end

function M.test_repeated_short_and_long_parse_option()
    pg.getopt(TOX_SPEC, nil, {"-e", "env1", "--toxenv", "env2"}, "test")
    assert_value("e", "env1,env2")
end

function M.test_repeated_long_and_short_parse_option()
    pg.getopt(TOX_SPEC, nil, {"--toxenv", "env1", "-e", "env2"}, "test")
    assert_value("e", "env1,env2")
end

function M.test_repeated_value_option_comma_joins()
    pg.getopt(WHEEL_SPEC, nil, {"-C", "a", "-C", "b"}, "test")
    assert_defined("C")
    assert_value("C", "a,b")
end


-- Positional args

function M.test_positional_only()
    pg.getopt(SAVE_FILES_SPEC, nil, {"foo", "bar"}, "test")
    assert_positional("foo bar")
end

function M.test_mixed_options_and_positional()
    pg.getopt(SAVE_FILES_SPEC, nil, {"-l", "foo", "bar"}, "test")
    assert_defined("l")
    assert_positional("foo bar")
end

function M.test_double_dash_stops_parsing()
    pg.getopt(TOX_SPEC, nil, {"-e", "env1", "--", "--not-an-opt"}, "test")
    assert_value("e", "env1")
    assert_positional("--not-an-opt")
end

function M.test_double_dash_repeated()
    pg.getopt(TOX_SPEC, nil, {"-e", "env1", "--", "a", "--", "-b", "--", "--c"}, "test")
    assert_value("e", "env1")
    assert_positional("a -- -b -- --c")
end

function M.test_no_arguments()
    pg.getopt(SAVE_FILES_SPEC, nil, {}, "test")
    assert_positional("")
    assert_undefined("l")
end

function M.test_positional_with_spaces()
    pg.getopt(SAVE_FILES_SPEC, nil, {"module with spaces", "other"}, "test")
    assert_positional("module with spaces other")
end

function M.test_empty_positional_args()
    pg.getopt(SAVE_FILES_SPEC, nil, {"", "foo", ""}, "test")
    assert_positional(" foo ")
end

function M.test_whitespace_positional_args()
    pg.getopt(SAVE_FILES_SPEC, nil, {" \t ", "foo", "\\\n"}, "test")
    assert_positional("foo")
end

function M.test_newlines_embedded_in_tokens()
    pg.getopt(CHECK_IMPORT_SPEC, nil,
        {"\n-e", "mod.a", "-e", "mod.b\n-e", "mod.c", "-e", "mod.d\n"}, "test")
    assert_value("e", "mod.a -e mod.b -e mod.c -e mod.d")
end

function M.test_trailing_backslash_stripped_after_newline_split()
    pg.getopt(WHEEL_SPEC, nil,
        {"-C\"key1=val1\" \\\n-C\"key2=val2\" \\\n-C\"key3=val3\"\n"}, "test")
    assert_value("C", "\"key1=val1\",\"key2=val2\",\"key3=val3\"")
end


-- Errors

function M.test_unknown_short_option()
    assert_errors(function() pg.getopt(SAVE_FILES_SPEC, nil, {"-z"}, "test") end)
end

function M.test_unknown_long_option()
    assert_errors(function() pg.getopt(SAVE_FILES_SPEC, nil, {"--bogus"}, "test") end)
end

function M.test_missing_value_short()
    assert_errors(function() pg.getopt(WHEEL_SPEC, nil, {"-d"}, "test") end)
end

function M.test_missing_value_long()
    assert_errors(function() pg.getopt(WHEEL_SPEC, nil, {"--directory"}, "test") end)
end

function M.test_flag_given_value()
    assert_errors(function() pg.getopt(SAVE_FILES_SPEC, nil, {"--assert-license=foo"}, "test") end)
end


-- Mutual exclusions

function M.test_R_and_x()
    assert_errors(function()
        pg.getopt(BUILDREQUIRES_SPEC, BUILDREQUIRES_EXCLUSIONS, {"-R", "-x", "testing"}, "test")
    end)
end

function M.test_long_form_exclusion()
    assert_errors(function()
        pg.getopt(BUILDREQUIRES_SPEC, BUILDREQUIRES_EXCLUSIONS, {"--no-runtime", "--extras", "testing"}, "test")
    end)
end

function M.test_N_and_C()
    assert_errors(function()
        pg.getopt(BUILDREQUIRES_SPEC, BUILDREQUIRES_EXCLUSIONS, {"-N", "-C", "foo"}, "test")
    end)
end

function M.test_w_and_p()
    assert_errors(function()
        pg.getopt(BUILDREQUIRES_SPEC, BUILDREQUIRES_EXCLUSIONS, {"--wheel", "--pyproject-dependencies"}, "test")
    end)
end

function M.test_non_conflicting_passes()
    pg.getopt(BUILDREQUIRES_SPEC, BUILDREQUIRES_EXCLUSIONS, {"-R", "-g", "tests"}, "test")
    assert_defined("R")
    assert_defined("g")
end


-- Cleanup

function M.test_options_do_not_leak_between_calls()
    local spec = {
        {short="d", long="directory", value=true},
        {short="C", long="config-settings", value=true, separator=","},
    }
    pg.getopt(spec, nil, {"-d", "foo", "-C", "bar"}, "test")
    assert_value("d", "foo")
    assert_defined("C")
    pg.getopt(spec, nil, {"-C", "baz"}, "test")
    assert_undefined("d")
    assert_defined("C")
end


-- Separator

function M.test_comma_separator()
    pg.getopt(TOX_SPEC, nil, {"-e", "env1", "-e", "env2"}, "test")
    assert_value("e", "env1,env2")
end

function M.test_custom_separator()
    pg.getopt(CHECK_IMPORT_SPEC, nil, {"--exclude", "a", "--exclude", "b"}, "test")
    assert_value("e", "a -e b")
end

function M.test_repeated_values_with_spaces_stay_separate_args()
    if not pg._use_quote then return skip("%{quote:} not transparent on this RPM") end
    pg.getopt(CHECK_IMPORT_SPEC, nil, {"--exclude", "a b", "--exclude", "c"}, "test")
    -- Each value is quoted individually, separator splits them:
    -- stored as: %{quote:a b} -e c
    -- When passed to another macro as "-e %{__pyproject_opt_e}",
    -- it should produce 4 args: -e, "a b", -e, c
    rpm.define([[_test_countargs(-) %#]])
    local nargs = rpm.expand("%_test_countargs -e %{__pyproject_opt_e}")
    assert(nargs == "4",
        "expected 4 args (-e, 'a b', -e, c), got " .. nargs)
end

function M.test_single_value_no_separator()
    pg.getopt(WHEEL_SPEC, nil, {"-d", "foo"}, "test")
    assert_value("d", "foo")
end

function M.test_repeated_without_separator_errors()
    assert_errors(function()
        pg.getopt(WHEEL_SPEC, nil, {"-d", "foo", "-d", "bar"}, "test")
    end)
end

function M.test_repeated_long_without_separator_errors()
    assert_errors(function()
        pg.getopt(WHEEL_SPEC, nil, {"--directory", "foo", "--directory", "bar"}, "test")
    end)
end


-- Optflag macros

function M.test_optflag_for_flag()
    pg.getopt(SAVE_FILES_SPEC, nil, {"-l"}, "test")
    assert_optflag("l", "-l")
    assert_optflag_undefined("M")
end

function M.test_optflag_for_value()
    pg.getopt(WHEEL_SPEC, nil, {"-d", "foo"}, "test")
    assert_optflag("d", "-d foo")
end

function M.test_optflag_for_repeated_value()
    pg.getopt(CHECK_IMPORT_SPEC, nil, {"--exclude", "a", "--exclude", "b"}, "test")
    assert_optflag("e", "-e a -e b")
end

function M.test_optflag_cleanup_between_calls()
    pg.getopt(WHEEL_SPEC, nil, {"-d", "foo"}, "test")
    assert_optflag("d", "-d foo")
    pg.getopt(WHEEL_SPEC, nil, {"-C", "bar"}, "test")
    assert_optflag_undefined("d")
    assert_optflag("C", "-C bar")
end


-- Nested macro scope: save/restore prevents inner getopt from clobbering outer values

function M.test_nested_getopt_with_restore_preserves_outer_opts()
    rpm.define([[_test_inner(-) %{lua:
        require("pyproject_getopt").getopt({
            {short="d", long="directory", value=true},
        })}inner%{lua:require("pyproject_getopt").restore()}]]
    )
    rpm.define([[_test_outer(-) %{lua:
        require("pyproject_getopt").getopt({
            {short="d", long="directory", value=true},
        })}%{_test_inner}/%{?__pyproject_opt_d}]]
    )

    local result = rpm.expand("%_test_outer -d hello")
    assert(result == "inner/hello",
        "expected 'inner/hello', got '" .. result .. "'")
end

function M.test_nested_getopt_with_restore_preserves_outer_optflags()
    rpm.define([[_test_inner2(-) %{lua:
        require("pyproject_getopt").getopt({
            {short="d", long="directory", value=true},
        })}inner%{lua:require("pyproject_getopt").restore()}]]
    )
    rpm.define([[_test_outer2(-) %{lua:
        require("pyproject_getopt").getopt({
            {short="d", long="directory", value=true},
        })}%{_test_inner2}/%{?__pyproject_optflag_d}]]
    )

    local result = rpm.expand("%_test_outer2 -d hello")
    assert(result == "inner/-d hello",
        "expected 'inner/-d hello', got '" .. result .. "'")
end

function M.test_nested_getopt_without_restore_clobbers()
    rpm.define([[_test_inner3(-) %{lua:
        require("pyproject_getopt").getopt({
            {short="d", long="directory", value=true},
        })}inner]]
    )
    rpm.define([[_test_outer3(-) %{lua:
        require("pyproject_getopt").getopt({
            {short="d", long="directory", value=true},
        })}%{_test_inner3}/%{?__pyproject_opt_d}]]
    )

    local result = rpm.expand("%_test_outer3 -d hello")
    -- Without restore(), inner getopt clobbers outer's value
    assert(result == "inner/",
        "expected 'inner/' (clobbered without restore), got '" .. result .. "'")
end

function M.test_nested_getopt_with_restore_preserves_outer_positional_args()
    rpm.define([[_test_inner4(-) %{lua:
        require("pyproject_getopt").getopt({
            {short="d", long="directory", value=true},
        })}inner%{lua:require("pyproject_getopt").restore()}]]
    )
    rpm.define([[_test_outer4(-) %{lua:
        require("pyproject_getopt").getopt({
            {short="d", long="directory", value=true},
        })}%{_test_inner4}/%{?__pyproject_positional_args}]]
    )

    local result = rpm.expand("%_test_outer4 -d hello world")
    assert(result == "inner/world",
        "expected 'inner/world', got '" .. result .. "'")
end

function M.test_nested_getopt_with_different_values()
    rpm.define([[_test_inner5(-) %{lua:
        require("pyproject_getopt").getopt({
            {short="d", long="directory", value=true},
        })}%{?__pyproject_opt_d}%{lua:require("pyproject_getopt").restore()}]]
    )
    rpm.define([[_test_outer5(-) %{lua:
        require("pyproject_getopt").getopt({
            {short="d", long="directory", value=true},
        })}%{_test_inner5 -d other}/%{?__pyproject_opt_d}]]
    )

    local result = rpm.expand("%_test_outer5 -d hello")
    assert(result == "other/hello",
        "expected 'other/hello', got '" .. result .. "'")
end

function M.test_triple_nested_getopt_restores_all_levels()
    rpm.define([[_test_innermost(-) %{lua:
        require("pyproject_getopt").getopt({
            {short="d", long="directory", value=true},
        })}%{?__pyproject_opt_d}%{lua:require("pyproject_getopt").restore()}]])
    rpm.define([[_test_middle(-) %{lua:
        require("pyproject_getopt").getopt({
            {short="d", long="directory", value=true},
        })}%{_test_innermost -d deep}+%{?__pyproject_opt_d}%{lua:require("pyproject_getopt").restore()}]])
    rpm.define([[_test_outermost(-) %{lua:
        require("pyproject_getopt").getopt({
            {short="d", long="directory", value=true},
        })}%{_test_middle -d mid}+%{?__pyproject_opt_d}]])

    local result = rpm.expand("%_test_outermost -d top")
    assert(result == "deep+mid+top",
        "expected 'deep+mid+top', got '" .. result .. "'")
end


-- Raw error functions (without pcall) for Python-side stderr checking.
-- These are not discovered by list() since they don't start with test_.

function M.raw_unknown_short_option()
    pg.getopt(SAVE_FILES_SPEC, nil, {"-z"}, "test")
end

function M.raw_unknown_long_option()
    pg.getopt(SAVE_FILES_SPEC, nil, {"--bogus"}, "test")
end

function M.raw_missing_value_short()
    pg.getopt(WHEEL_SPEC, nil, {"-d"}, "test")
end

function M.raw_flag_given_value()
    pg.getopt(SAVE_FILES_SPEC, nil, {"--assert-license=foo"}, "test")
end

function M.raw_R_and_x()
    pg.getopt(BUILDREQUIRES_SPEC, BUILDREQUIRES_EXCLUSIONS, {"-R", "-x", "testing"}, "test")
end

function M.raw_repeated_without_separator()
    pg.getopt(WHEEL_SPEC, nil, {"-d", "foo", "-d", "bar"}, "test")
end


-- RPM macro integration (uses rpm.define to create a real parametric macro)

local _MACRO_DEF = [[_test_macro(-) %{lua:require("pyproject_getopt").getopt({{short="d", long="directory", value=true}})}]]

function M.test_macro_parses_short_option()
    rpm.define(_MACRO_DEF)
    rpm.expand("%_test_macro -d hello")
    assert_value("d", "hello")
end

function M.test_macro_parses_long_option()
    rpm.define(_MACRO_DEF)
    rpm.expand("%_test_macro --directory hello")
    assert_value("d", "hello")
end

function M.test_macro_preserves_quoted_spaces()
    rpm.define(_MACRO_DEF)
    rpm.expand("%_test_macro -d %{quote:Path With Spaces}")
    assert_value("d", "Path With Spaces")
end

function M.test_macro_rejects_unknown_option()
    rpm.define(_MACRO_DEF)
    assert_errors(function() rpm.expand("%_test_macro --bogus") end)
end

function M.raw_macro_rejects_unknown_option()
    rpm.define(_MACRO_DEF)
    rpm.expand("%_test_macro --bogus")
end


-- List all tests for pytest discovery
function M.list()
    local names = {}
    for name in pairs(M) do
        if type(M[name]) == "function" and name:sub(1, 5) == "test_" then
            names[#names + 1] = name
        end
    end
    table.sort(names)
    return names
end

return M
