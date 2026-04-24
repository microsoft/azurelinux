require 'set'

LIBRUBY_SO = 'libruby.so'
PROBES_D = 'probes.d'

# These probes are excluded by VM_COLLECT_USAGE_DETAILS ifdef.
EXCLUDE_PROBES = Set.new %w(insn insn__operand)

## Detect SystemTap section headers presence

stap_headers = [
  '\.stapsdt\.base',
  '\.note\.stapsdt'
]

header_regexp = %r{ (#{stap_headers.join('|')}) }

section_headers = `readelf -S "#{LIBRUBY_SO}"`
detected_stap_headers = section_headers.scan(header_regexp).flatten

# Assume there are both headers until this is proven wrong ;)
unless detected_stap_headers.size == 2
  puts 'ERROR: SystemTap (DTrace) headers were not detected in resulting library.'
  exit false
end

## Find if every declared probe is propagated to resulting library

# Colect probes specified in probes.d file.
probes_declared = []

File.open(PROBES_D) do |file|
  file.each_line do |line|
    if probe = line[/probe (\S+)\(.*\);/, 1]
      probes_declared << probe
    end
  end
end

probes_declared = Set.new probes_declared

unless EXCLUDE_PROBES.subset? probes_declared
  puts 'ERROR: Change in SystemTap (DTrace) probes definition file detected.'
  exit false
end

probes_declared -= EXCLUDE_PROBES

# Detect probes in resulting library.
get_probes_detected = %r{
^\s*Provider:\s+ruby,\s+Name:\s+(\S+),\s+.*$
}

probes_detected = `eu-readelf -n "#{LIBRUBY_SO}"`

probes_detected = Set.new probes_detected.scan(get_probes_detected).flatten

# Both sets must be equal, otherwise something is wrong.
unless probes_declared == probes_detected
  puts 'ERROR: SystemTap (DTrace) probes were not correctly propagated into resulting library.'
  puts "       Undetected probes: #{(probes_declared - probes_detected).sort.join(', ')}\n",
       "       Additional detected probes: #{(probes_detected - probes_declared).sort.join(', ')}"

  exit false
end
