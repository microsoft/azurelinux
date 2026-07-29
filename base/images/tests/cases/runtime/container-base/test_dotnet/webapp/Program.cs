// Minimal HttpListener server used to validate the .NET runtime.
using System.Net;
using System.Text;

var body = "Hello World!";
var listener = new HttpListener();
listener.Prefixes.Add("http://*:8080/");
listener.Start();

while (true)
{
    var context = listener.GetContext();
    var buffer = Encoding.UTF8.GetBytes(body);
    context.Response.ContentType = "text/plain";
    context.Response.ContentLength64 = buffer.Length;
    context.Response.OutputStream.Write(buffer, 0, buffer.Length);
    context.Response.Close();
}
