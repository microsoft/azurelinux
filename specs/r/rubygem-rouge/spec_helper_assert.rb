module Minitest
	module Assertions

	alias_method :assert_orig, :assert
	alias_method :refute_orig, :refute

	def assert(test = nil, msg = nil, &block)
	  if block_given?
	    assert_orig yield
	  else
	    assert_orig test, msg
	  end
	end

	def refute(test = nil, msg = nil, &block)
	  if block_given?
	    refute_orig yield
	  else
	    refute_orig test, msg
	  end
	end

	end
end
