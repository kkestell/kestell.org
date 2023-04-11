using System.CommandLine;

namespace Builder;

internal class BuildCommand : BaseCommand
{
    public BuildCommand() : base("build", "Build the site")
    {
        this.SetHandler(context =>
        {
            Result = context.ParseResult;

            try
            {
                context.ExitCode = new BuildCommandHandler(this).Run();
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