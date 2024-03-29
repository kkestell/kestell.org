using System.CommandLine;

namespace Builder;

internal class ServeCommand : BaseCommand
{
    public Option<int> Port { get; } =
        new(new[] {"--port", "-p"}, () => 1313, "Port to serve on");

    public ServeCommand() : base("serve", "Serve the site")
    {
        AddOption(Port);
        
        this.SetHandler(context =>
        {
            Result = context.ParseResult;

            try
            {
                context.ExitCode = new ServeCommandHandler(this).Run();
            }
            catch (Exception e)
            {
                Console.Error.WriteLine(e.Message);
                Console.Error.WriteLine(e.StackTrace);
                context.ExitCode = 1;
            }
        });
    }
}