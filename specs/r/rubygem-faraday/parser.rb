module MultipartParser
  # A low level parser for multipart messages,
  # based on the node-formidable parser.
  class Parser

    def initialize
      @boundary = nil
      @boundary_chars = nil
      @lookbehind = nil
      @state = :parser_uninitialized
      @index = 0  # Index into boundary or header
      @flags = {}
      @marks = {} # Keep track of different parts
      @callbacks = {}
    end

    # Initializes the parser, using the given boundary
    def init_with_boundary(boundary)
      @boundary = "\r\n--" + boundary
      @lookbehind = "\0"*(@boundary.length + 8)
      @state = :start

      @boundary_chars = {}
      @boundary.each_byte do |b|
        @boundary_chars[b.chr] = true
      end
    end

    # Registers a callback to be called when the
    # given event occurs. Each callback is expected to
    # take three parameters: buffer, start_index, and end_index.
    # All of these parameters may be null, depending on the callback.
    # Valid callbacks are:
    # :end
    # :header_field
    # :header_value
    # :header_end
    # :headers_end
    # :part_begin
    # :part_data
    # :part_end
    def on(event, &callback)
      @callbacks[event] = callback
    end

    # Writes data to the parser.
    # Returns the number of bytes parsed.
    # In practise, this means that if the return value
    # is less than the buffer length, a parse error occured.
    def write(buffer)
      i = 0
      buffer_length = buffer.length
      index = @index
      flags = @flags.dup
      state = @state
      lookbehind = @lookbehind
      boundary = @boundary
      boundary_chars = @boundary_chars
      boundary_length = @boundary.length
      boundary_end = boundary_length - 1

      while i < buffer_length
        c = buffer[i, 1]
        case state
          when :parser_uninitialized
            return i;
          when :start
            index = 0;
            state = :start_boundary
          when :start_boundary # Differs in that it has no preceeding \r\n
            if index == boundary_length - 2
              return i unless c == "\r"
              index += 1
            elsif index - 1 == boundary_length - 2
              return i unless c == "\n"
              # Boundary read successfully, begin next part
              callback(:part_begin)
              state = :header_field_start
            else
              return i unless c == boundary[index+2, 1] # Unexpected character
              index += 1
            end
            i += 1
          when :header_field_start
            state = :header_field
            @marks[:header_field] = i
            index = 0
          when :header_field
            if c == "\r"
              @marks.delete :header_field
              state = :headers_almost_done
            else
              index += 1
              unless c == "-" # Skip hyphens
                if c == ":"
                  return i if index == 1 # Empty header field
                  data_callback(:header_field, buffer, i, :clear => true)
                  state = :header_value_start
                else
                  cl = c.downcase
                  return i if cl < "a" || cl > "z"
                end
              end
            end
            i += 1
          when :header_value_start
            if c == " " # Skip spaces
              i += 1
            else
              @marks[:header_value] = i
              state = :header_value
            end
          when :header_value
            if c == "\r"
              data_callback(:header_value, buffer, i, :clear => true)
              callback(:header_end)
              state = :header_value_almost_done
            end
            i += 1
          when :header_value_almost_done
            return i unless c == "\n"
            state = :header_field_start
            i += 1
          when :headers_almost_done
            return i unless c == "\n"
            callback(:headers_end)
            state = :part_data_start
            i += 1
          when :part_data_start
            state = :part_data
            @marks[:part_data] = i
          when :part_data
            prev_index = index

            if index == 0
              # Boyer-Moore derived algorithm to safely skip non-boundary data
              # See http://debuggable.com/posts/parsing-file-uploads-at-500-
              # mb-s-with-node-js:4c03862e-351c-4faa-bb67-4365cbdd56cb
              while i + boundary_length <= buffer_length
                break if boundary_chars.has_key? buffer[i + boundary_end].chr
                i += boundary_length
              end
              c = buffer[i, 1]
            end

            if index < boundary_length
              if boundary[index, 1] == c
                if index == 0
                  data_callback(:part_data, buffer, i, :clear => true)
                end
                index += 1
              else # It was not the boundary we found, after all
                index = 0
              end
            elsif index == boundary_length
              index += 1
              if c == "\r"
                flags[:part_boundary] = true
              elsif c == "-"
                flags[:last_boundary] = true
              else # We did not find a boundary after all
                index = 0
              end
            elsif index - 1 == boundary_length
              if flags[:part_boundary]
                index = 0
                if c == "\n"
                  flags.delete :part_boundary
                  callback(:part_end)
                  callback(:part_begin)
                  state = :header_field_start
                  i += 1
                  next # Ugly way to break out of the case statement
                end
              elsif flags[:last_boundary]
                if c == "-"
                  callback(:part_end)
                  callback(:end)
                  state = :end
                else
                  index = 0 # False alarm
                end
              else
                index = 0
              end
            end

            if index > 0
              # When matching a possible boundary, keep a lookbehind
              # reference in case it turns out to be a false lead
              lookbehind[index-1] = c
            elsif prev_index > 0
              # If our boundary turns out to be rubbish,
              # the captured lookbehind belongs to part_data
              callback(:part_data, lookbehind, 0, prev_index)
              @marks[:part_data] = i

              # Reconsider the current character as it might be the
              # beginning of a new sequence.
              i -= 1
            end

            i += 1
          when :end
            i += 1
          else
            return i;
        end
      end

      data_callback(:header_field, buffer, buffer_length)
      data_callback(:header_value, buffer, buffer_length)
      data_callback(:part_data, buffer, buffer_length)

      @index = index
      @state = state
      @flags = flags

      return buffer_length
    end

    private

    # Issues a callback.
    def callback(event, buffer = nil, start = nil, the_end = nil)
      return if !start.nil? && start == the_end
      if @callbacks.has_key? event
        @callbacks[event].call(buffer, start, the_end)
      end
    end

    # Issues a data callback,
    # The only valid options is :clear,
    # which, if true, will reset the appropriate mark to 0,
    # If not specified, the mark will be removed.
    def data_callback(data_type, buffer, the_end, options = {})
      return unless @marks.has_key? data_type
      callback(data_type, buffer, @marks[data_type], the_end)
      unless options[:clear]
        @marks[data_type] = 0
      else
        @marks.delete data_type
      end
    end
  end
end
