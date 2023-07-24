namespace Builder;

internal class BuildCommandHandler
{
    private readonly BuildOptions buildOptions;

    public BuildCommandHandler(BuildCommand command)
    {
        buildOptions = new BuildOptions(command);
    }

    public int Run()
    {
        try
        {
            var siteBuilder = new SiteBuilder(buildOptions);
            siteBuilder.Build();
        }
        catch (Exception e)
        {
            Console.WriteLine(e);
            return 1;
        }
        
        return 0;
    }
}