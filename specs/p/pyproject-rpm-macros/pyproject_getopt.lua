local M = {}


local function error_out(macro_name, message)
    rpm.expand("%{error:%%" .. macro_name .. ": " .. message .. "}")
end


local function option_repr(spec)
    return "-" .. spec.short .. "/--" .. spec.long
end


local function error_mutually_exclusive(macro_name, a, b)
    error_out(macro_name,
              option_repr(a) .. " and " .. option_repr(b) ..
              " are mutually exclusive")
end


-- Append a value to found[short]. Errors if repeated without a separator.
local function record_value(macro_name, spec, label, val, found)
    if found[spec.short] then
        if not spec.separator then
            error_out(macro_name, "option " .. label .. " cannot be repeated")
            return false
        end
    else
        found[spec.short] = {}
    end
    found[spec.short][#found[spec.short] + 1] = val
    return true
end


-- Build a token table from RPM macro arguments (%1, %2, ..., %{%#}).
-- This preserves %{quote:...} quoting, unlike splitting %** on whitespace.
-- Can be replaced by the native RPM Lua args table when we no longer support c9s.
function M.rpm_args()
    local args = {}
    local nargs = tonumber(rpm.expand("%#"))
    for n = 1, nargs do
        args[n] = rpm.expand("%" .. n)
    end
    return args
end


-- RPM may embed newlines within tokens (from %{expand:} or line continuations).
-- Split such tokens on newlines, strip trailing backslashes and whitespace
-- (from \-newline continuations inside %{macro:} syntax), and discard
-- whitespace/backslash-only fragments.
-- Intentional empty strings (e.g. from -d "") are preserved.
local function normalize_tokens(tokens)
    local filtered = {}
    for _, t in ipairs(tokens) do
        if t:find("\n") then
            for part in (t .. "\n"):gmatch("([^\n]*)\n") do
                local stripped = part:gsub("[%s\\]+$", "")
                if stripped ~= "" then
                    filtered[#filtered + 1] = stripped
                end
            end
        elseif not t:find("^[%s\\]+$") then
            filtered[#filtered + 1] = t
        end
    end
    return filtered
end


local function build_lookup(opt_spec)
    local by_short = {}
    local by_long = {}
    for _, spec in ipairs(opt_spec) do
        by_short[spec.short] = spec
        by_long[spec.long] = spec
    end
    return by_short, by_long
end


-- Store an option's value. If val is nil, consume the next token.
-- Returns the updated token index, or nil on error.
local function consume_value(macro_name, spec, label, val, tokens, i, found)
    if val == nil then
        i = i + 1
        if i > #tokens then
            error_out(macro_name, "option " .. label .. " requires a value")
            return nil
        end
        val = tokens[i]
    end
    if not record_value(macro_name, spec, label, val, found) then
        return nil
    end
    return i
end


-- Process a --long-option token. Handles --name, --name=val, and --name val.
local function handle_long_option(macro_name, token, tokens, i, by_long, found)
    local rest = token:sub(3)
    local eq = rest:find("=", 1, true)
    local name, val
    if eq then
        name = rest:sub(1, eq - 1)
        val = rest:sub(eq + 1)
    else
        name = rest
    end

    local spec = by_long[name]
    if not spec then
        error_out(macro_name, "unknown option: --" .. name)
        return nil
    end

    if spec.value then
        return consume_value(macro_name, spec, "--" .. name, val, tokens, i, found)
    else
        if val ~= nil then
            error_out(macro_name, "option --" .. name .. " does not take a value")
            return nil
        end
        found[spec.short] = true
        return i
    end
end


-- Process a short option token. Handles -x, -xval, -x val, and bundled -xyz.
local function handle_short_options(macro_name, token, tokens, i, by_short, found)
    local j = 2
    while j <= #token do
        local ch = token:sub(j, j)
        local spec = by_short[ch]
        if not spec then
            error_out(macro_name, "unknown option: -" .. ch)
            return nil
        end

        if spec.value then
            local val
            if j < #token then
                val = token:sub(j + 1)
                j = #token
            end
            i = consume_value(macro_name, spec, "-" .. ch, val, tokens, i, found)
            if not i then return nil end
        else
            found[spec.short] = true
        end
        j = j + 1
    end

    return i
end


-- Parse a token list into found options and positional arguments.
-- Returns {found={short_char=true_or_values_table}, positional={...}}, or nil on error.
local function parse(macro_name, tokens, by_short, by_long)
    local found = {}
    local positional = {}
    local i = 1

    while i <= #tokens do
        local token = tokens[i]

        if token == "--" then
            for j = i + 1, #tokens do
                positional[#positional + 1] = tokens[j]
            end
            break
        elseif token:sub(1, 2) == "--" then
            i = handle_long_option(macro_name, token, tokens, i, by_long, found)
            if not i then return nil end
        elseif token:sub(1, 1) == "-" and #token > 1 then
            i = handle_short_options(macro_name, token, tokens, i, by_short, found)
            if not i then return nil end
        else
            positional[#positional + 1] = token
        end

        i = i + 1
    end

    return {found = found, positional = positional}
end


-- Verify no mutually exclusive options were used together. Returns false on violation.
local function check_exclusions(macro_name, found, by_short, exclusion_rules)
    for _, rule in ipairs(exclusion_rules) do
        local opt = rule[1]
        local conflicts = rule[2]
        if found[opt] then
            for _, c in ipairs(conflicts) do
                if found[c] then
                    error_mutually_exclusive(macro_name, by_short[opt], by_short[c])
                    return false
                end
            end
        end
    end
    return true
end


local function cleanup_macros(opt_spec)
    for _, spec in ipairs(opt_spec) do
        rpm.undefine("__pyproject_opt_" .. spec.short)
        rpm.undefine("__pyproject_optflag_" .. spec.short)
    end
    rpm.undefine("__pyproject_positional_args")
end


-- On RPM 4.20+, %{quote:} is transparent (no \x1f delimiters in expanded output).
-- On older RPM, %{quote:} leaks \x1f into shell commands, so we skip quoting there.
M._use_quote = rpm.vercmp(rpm.expand("0%{?rpmversion}"), "4.19.90") >= 0

-- Quote a single value for safe embedding in an rpm.define() call.
-- On RPM 4.20+, empty values or values with spaces are wrapped in %{quote:}.
-- On older RPM, empty values are represented as %{nil}, values with spaces are verbatim.
local function quote_value(v)
    if M._use_quote and (v == "" or v:find("%s")) then
        return "%{quote:" .. v .. "}"
    elseif v == "" then
        return "%{nil}"
    else
        return v
    end
end

-- Apply quote_value to each element, return a new table.
local function quote_values(values)
    local parts = {}
    for _, v in ipairs(values) do
        parts[#parts + 1] = quote_value(v)
    end
    return parts
end

-- Define %__pyproject_opt_{short}, %__pyproject_optflag_{short}, and
-- %__pyproject_positional_args from a parse result.
-- Takes a table {found, opt_spec, positional}.
-- opt: Flags get %{nil} (defined but empty), value options get each individual
--      value joined by separator.
-- optflag: Ready-to-forward form: "-X" for flags, "-X value" for value options.
-- See the quote_value function about how values are quoted.
local function define_macros(state)
    for _, spec in ipairs(state.opt_spec) do
        if state.found[spec.short] then
            if spec.value then
                local parts = quote_values(state.found[spec.short])
                local value = table.concat(parts, spec.separator)
                rpm.define("__pyproject_opt_" .. spec.short .. " " .. value)
                rpm.define("__pyproject_optflag_" .. spec.short .. " -" .. spec.short .. " " .. value)
            else
                rpm.define("__pyproject_opt_" .. spec.short .. " %{nil}")
                rpm.define("__pyproject_optflag_" .. spec.short .. " -" .. spec.short)
            end
        end
    end
    if #state.positional > 0 then
        local parts = quote_values(state.positional)
        rpm.define("__pyproject_positional_args " .. table.concat(parts, " "))
    end
end


-- Save/restore stack for nested getopt calls.
-- rpm.define()/rpm.undefine() are global (not scoped to parametric macros),
-- so an inner getopt cleanup clobbers outer values. We save the structured
-- parse result and re-run define_macros() in restore(), avoiding any
-- rpm.expand() round-trip that would strip %{quote:} wrappers.
local _current = nil  -- {found, opt_spec, positional} from the most recent getopt()
local _save_stack = {} -- stack of {found, opt_spec, positional} tables

function M.restore()
    if _current then
        cleanup_macros(_current.opt_spec)
    end
    _current = table.remove(_save_stack)
    if not _current then return end
    define_macros(_current)
end


-- Parse and validate macro options, define %__pyproject_opt_* and %__pyproject_positional_args.
-- opt_spec: list of {short=, long=, value=bool, separator=string} tables.
--   value: option takes an argument.
--   separator: allow repeats and join values with this string. Without it, repeats with values are an error.
-- exclusion_rules: optional list of {short_char, {conflicting_short_chars...}} pairs.
-- tokens and macro_name default to the current RPM macro's arguments and name.
function M.getopt(opt_spec, exclusion_rules, tokens, macro_name)
    tokens = normalize_tokens(tokens or M.rpm_args())
    macro_name = macro_name or rpm.expand("%0")
    local by_short, by_long = build_lookup(opt_spec)
    _save_stack[#_save_stack + 1] = _current
    cleanup_macros(opt_spec)

    local result = parse(macro_name, tokens, by_short, by_long)
    if not result then return end

    if exclusion_rules then
        if not check_exclusions(macro_name, result.found, by_short, exclusion_rules) then
            return
        end
    end

    _current = {found = result.found, opt_spec = opt_spec, positional = result.positional}
    define_macros(_current)
end

return M
