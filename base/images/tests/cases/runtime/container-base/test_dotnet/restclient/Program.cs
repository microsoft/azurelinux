using System;
using RestSharp;

class Program
{
    static int Main(string[] args)
    {
        var client = new RestClient("http://localhost:8080");
        var request = new RestRequest("/", Method.Get);
        var response = client.Execute(request);

        if (response.StatusCode == System.Net.HttpStatusCode.OK &&
            response.Content == "Hello World!")
        {
            Console.WriteLine("RestSharp reached the .NET server.");
            return 0;
        }

        Console.Error.WriteLine(
            $"Unexpected response: status={response.StatusCode}, body=\"{response.Content}\"");
        return 1;
    }
}
