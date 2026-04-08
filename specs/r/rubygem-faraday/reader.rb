require 'multipart_parser/parser'

module MultipartParser
  class NotMultipartError < StandardError; end;

  # A more high level interface to MultipartParser.
  class Reader

    # Initializes a MultipartReader, that will
    # read a request with the given boundary value.
    def initialize(boundary)
      @parser = Parser.new
      @parser.init_with_boundary(boundary)
      @header_field = ''
      @header_value = ''
      @part = nil
      @ended = false
      @on_error = nil
      @on_part = nil

      init_parser_callbacks
    end

    # Returns true if the parser has finished parsing
    def ended?
      @ended
    end

    # Sets to a code block to call
    # when part headers have been parsed.
    def on_part(&callback)
      @on_part = callback
    end

    # Sets a code block to call when
    # a parser error occurs.
    def on_error(&callback)
      @on_error = callback
    end

    # Write data from the given buffer (String)
    # into the reader.
    def write(buffer)
      bytes_parsed = @parser.write(buffer)
      if bytes_parsed != buffer.size
        msg = "Parser error, #{bytes_parsed} of #{buffer.length} bytes parsed"
        @on_error.call(msg) unless @on_error.nil?
      end
    end

    # Extracts a boundary value from a Content-Type header.
    # Note that it is the header value you provide here.
    # Raises NotMultipartError if content_type is invalid.
    def self.extract_boundary_value(content_type)
      if content_type =~ /multipart/i
        if match = (content_type =~ /boundary=(?:"([^"]+)"|([^;]+))/i)
          $1 || $2
        else
          raise NotMultipartError.new("No multipart boundary")
        end
      else
        raise NotMultipartError.new("Not a multipart content type!")
      end
    end

    class Part
      attr_accessor :filename, :headers, :name, :mime

      def initialize
        @headers = {}
        @data_callback = nil
        @end_callback = nil
      end

      # Calls the data callback with the given data
      def emit_data(data)
        @data_callback.call(data) unless @data_callback.nil?
      end

      # Calls the end callback
      def emit_end
        @end_callback.call unless @end_callback.nil?
      end

      # Sets a block to be called when part data
      # is read. The block should take one parameter,
      # namely the read data.
      def on_data(&callback)
        @data_callback = callback
      end

      # Sets a block to be called when all data
      # for the part has been read.
      def on_end(&callback)
        @end_callback = callback
      end
    end

    private

    def init_parser_callbacks
      @parser.on(:part_begin) do
        @part = Part.new
        @header_field = ''
        @header_value = ''
      end

      @parser.on(:header_field) do |b, start, the_end|
        @header_field << b[start...the_end]
      end

      @parser.on(:header_value) do |b, start, the_end|
        @header_value << b[start...the_end]
      end

      @parser.on(:header_end) do
        @header_field.downcase!
        @part.headers[@header_field] = @header_value
        if @header_field == 'content-disposition'
          if @header_value =~ /name="([^"]+)"/i
            @part.name = $1
          end
          if @header_value =~ /filename="([^;]+)"/i
            match = $1
            start = (match.rindex("\\") || -1)+1
            @part.filename = match[start...(match.length)]
          end
        elsif @header_field == 'content-type'
          @part.mime = @header_value
        end
        @header_field = ''
        @header_value = ''
      end

      @parser.on(:headers_end) do
        @on_part.call(@part) unless @on_part.nil?
      end

      @parser.on(:part_data) do |b, start, the_end|
        @part.emit_data b[start...the_end]
      end

      @parser.on(:part_end) do
        @part.emit_end
      end

      @parser.on(:end) do
        @ended = true
      end
    end
  end
end
