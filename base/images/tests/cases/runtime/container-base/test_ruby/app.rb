# Minimal stdlib TCP HTTP server used to validate the Ruby runtime.
require 'socket'

server = TCPServer.new('0.0.0.0', 8080)
body = File.read(File.join(__dir__, 'response.txt'))

trap("INT") { server.close; exit }

loop do
  client = server.accept
  client.gets
  client.print "HTTP/1.1 200 OK\r\n"
  client.print "Content-Type: text/plain\r\n"
  client.print "Content-Length: #{body.bytesize}\r\n"
  client.print "Connection: close\r\n"
  client.print "\r\n"
  client.print body
  client.close
end
