using System.CommandLine;

namespace Builder;

internal class BuildOptions
{
    private readonly BaseCommand command;
    
    public DirectoryInfo RootDirectory { get; }
    public DirectoryInfo ContentDirectory { get; }
    public DirectoryInfo OutputDirectory { get; }
    public DirectoryInfo TemplateDirectory { get; }
    public DirectoryInfo StaticDirectory { get; }
    public bool BuildDrafts { get; set; }
    public bool BuildPdfs { get; set; }
    
    public BuildOptions(BaseCommand command)
    {
        this.command = command;
        
        RootDirectory = Argument(command.RootDirectory);
        OutputDirectory = Argument(command.OutputDirectory);
        ContentDirectory = new DirectoryInfo(Path.Combine(RootDirectory.FullName, "content"));
        TemplateDirectory = new DirectoryInfo(Path.Combine(RootDirectory.FullName, "templates"));
        StaticDirectory = new DirectoryInfo(Path.Combine(RootDirectory.FullName, "static"));
        BuildDrafts = Option(command.Drafts);
        BuildPdfs = Option(command.Pdfs);
    }
    
    protected T Argument<T>(Argument<T> argument) => command.Result!.GetValueForArgument(argument);

    protected T? Option<T>(Option<T> option) => command.Result!.GetValueForOption(option);
}