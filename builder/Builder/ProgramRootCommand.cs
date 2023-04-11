namespace Builder;

internal class RootCommand : System.CommandLine.RootCommand
{
    public RootCommand() : base("Builder")
    {
        AddCommand(new BuildCommand());
        AddCommand(new ServeCommand());
    }
}