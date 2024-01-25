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

    public Option<bool> Drafts { get; } =
        new(new[] {"--drafts", "-D"}, () => false, "Include drafts");

    public Option<bool> Pdfs { get; } =
        new(new[] {"--pdfs", "-P"}, () => false, "Build PDFs");

    public Option<bool> OptimizeImages { get; } =
        new(new[] {"--optimize", "-O"}, () => false, "Optimize images");


    protected BaseCommand(string name, string? description = null) : base(name, description)
    {
        AddArgument(RootDirectory);
        AddArgument(OutputDirectory);
        AddOption(Drafts);
        AddOption(Pdfs);
        AddOption(OptimizeImages);
    }
}