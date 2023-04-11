using System.CommandLine;
using System.CommandLine.Parsing;

namespace Builder;

internal abstract class BaseCommand : Command
{
    public ParseResult? Result;

    public Argument<DirectoryInfo> RootDirectory { get; } =
        new("root", () => new DirectoryInfo(Path.Combine(Environment.CurrentDirectory, "src")), "Root directory");

    public Argument<DirectoryInfo> OutputDirectory { get; } =
        new("out", () => new DirectoryInfo(Path.Combine(Environment.CurrentDirectory, "dist")), "Output directory");

    protected BaseCommand(string name, string? description = null) : base(name, description)
    {
        AddArgument(RootDirectory);
        AddArgument(OutputDirectory);
    }
}