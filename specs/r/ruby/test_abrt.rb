if !!$LOADED_FEATURES.detect { |f| f =~ /abrt\.rb/ }
  exit true
else
  puts 'ERROR: ABRT hook was not loaded.'

  exit false
end
