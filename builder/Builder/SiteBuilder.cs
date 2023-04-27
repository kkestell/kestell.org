using System.Collections.Concurrent;
using System.Diagnostics;
using System.Globalization;
using System.Text;
using System.Text.RegularExpressions;
using HandlebarsDotNet;
using Markdig;
using YamlDotNet.Core;
using YamlDotNet.Core.Events;
using YamlDotNet.Serialization;
using YamlDotNet.Serialization.NamingConventions;

namespace Builder;

internal class SiteBuilder
{
    private readonly BuildOptions buildOptions;
    private readonly TextInfo textInfo;
    private readonly IDeserializer yamlDeserializer;
    private readonly MarkdownPipeline markdownPipeline;
    private readonly HandlebarsTemplate<object, object> pageTemplate;
    private readonly HandlebarsTemplate<object, object> homeTemplate;

    public SiteBuilder(BuildOptions buildOptions)
    {
        this.buildOptions = buildOptions;
        
        textInfo = new CultureInfo("en-US", false).TextInfo;

        yamlDeserializer = new DeserializerBuilder()
            .WithNamingConvention(CamelCaseNamingConvention.Instance)
            .Build();

        markdownPipeline = new MarkdownPipelineBuilder()
            .UseYamlFrontMatter()
            .UseCustomContainers() 
            .UseEmphasisExtras()
            .UseGridTables()
            .UseMediaLinks()
            .UsePipeTables()
            .UseGenericAttributes()
            .UseDefinitionLists()
            .UseSmartyPants()
            .UseAutoIdentifiers()
            .UseAutoLinks()
            .Build();

        pageTemplate = Handlebars.Compile(File.ReadAllText(Path.Combine(buildOptions.TemplateDirectory.FullName, "page.hbs")));
        homeTemplate = Handlebars.Compile(File.ReadAllText(Path.Combine(buildOptions.TemplateDirectory.FullName, "home.hbs")));
    }

    public void Build()
    {
        var sw = new Stopwatch();
        sw.Start();

        if (Directory.Exists("dist"))
            Directory.Delete("dist", true);
    
        Directory.CreateDirectory("dist");

        var files = Directory.GetFiles(buildOptions.ContentDirectory.FullName, "*.md", SearchOption.AllDirectories);

        var pages = new ConcurrentBag<Page>();

        Parallel.ForEach(files, file =>
        {
            var page = BuildPage(file);
            
            if (page is not null)
                pages.Add(page);
        });

        BuildHomepage(pages.ToList());

        CopyDirectory(buildOptions.StaticDirectory.FullName, Path.Combine(buildOptions.OutputDirectory.FullName, "static"), true);

        sw.Stop();
        Console.WriteLine($"Built in {sw.ElapsedMilliseconds}ms");
    }

    private void GeneratePdf(string markdownFile, string outputFile)
    {
        var tempFile = Path.Combine(Path.GetTempPath(), Path.GetRandomFileName());

        File.Copy(markdownFile, tempFile, true);

        var content = File.ReadAllText(tempFile);

        // FIXME: Yuck!
        var absoluteImagePath = Path.Combine(buildOptions.StaticDirectory.FullName, "images");
        content = content.Replace("/static/images", absoluteImagePath);

        File.WriteAllText(tempFile, content);

        var startInfo = new ProcessStartInfo
        {
            FileName = "pandoc",
            Arguments = $"{tempFile} --pdf-engine=xelatex --template={Path.Combine(buildOptions.TemplateDirectory.FullName, "default.latex")} --variable \"geometry=margin=0.75in\" --highlight-style=monochrome -o {outputFile}",
            RedirectStandardOutput = true,
            RedirectStandardError = true,
            UseShellExecute = false,
            CreateNoWindow = true,
            WorkingDirectory = buildOptions.ContentDirectory.FullName
        };

        var process = new Process { StartInfo = startInfo };
        process.Start();
        process.WaitForExit();

        if (process.ExitCode != 0)
        {
            throw new Exception($"pandoc failed with exit code {process.ExitCode} and error {process.StandardError.ReadToEnd()} when converting {markdownFile} to {outputFile}");
        }

        File.Delete(tempFile);

        Console.WriteLine($"{markdownFile} -> {outputFile}");
    }
    
    private Page? BuildPage(string file)
    {
        var content = File.ReadAllText(file);
        var pageMeta = ParseMetadata(content);

        bool.TryParse(pageMeta["draft"], out var draft);
        if (draft)
            return null;

        var html = Markdown.ToHtml(content, markdownPipeline);

        var relativePath = Path.GetRelativePath(buildOptions.ContentDirectory.FullName, file);
        var outputHtmlFile = Path.ChangeExtension(Path.Combine(buildOptions.OutputDirectory.FullName, relativePath), ".html");
        var outputPdfFile = Path.ChangeExtension(Path.Combine(buildOptions.OutputDirectory.FullName, relativePath), ".pdf");
        
        Directory.CreateDirectory(Path.GetDirectoryName(outputHtmlFile)!);

        var path = Path.GetRelativePath(buildOptions.OutputDirectory.FullName, outputHtmlFile);
       
        var page = new Page
        {
            Meta = pageMeta,
            Content = html,
            Pdf = Path.GetFileName(outputPdfFile),
            GeneratedAt = DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss"),
            Path = path
        };
        
        var renderedHtml = pageTemplate(new { Page = page });

        File.WriteAllText(outputHtmlFile, renderedHtml);
        
        Console.WriteLine($"{file} -> {outputHtmlFile}");

        GeneratePdf(file, outputPdfFile);

        return page;
    }
    
    private void BuildHomepage(List<Page> pages)
    {
        var directory = ConvertPagesToSiteDirectory(pages);
        SortSiteDirectory(directory);
        var root = GenerateNestedList(directory, 1);

        var homeHtml = homeTemplate(new { Root = root });
        File.WriteAllText(Path.Combine(buildOptions.OutputDirectory.FullName, "index.html"), homeHtml);
    }
    
    private string GenerateNestedList(SiteDirectory directory, int depth)
    {
        var htmlBuilder = new StringBuilder();

        if (!string.IsNullOrEmpty(directory.Name))
        {
            var name = textInfo.ToTitleCase(directory.Name);
            
            if (depth is >= 1 and <= 6)
            {
                htmlBuilder.AppendLine($"<h{depth}>{name}</h{depth}>");
            }
            else
            {
                htmlBuilder.AppendLine($"<h6>{name}</h6>");
            }
        }

        htmlBuilder.AppendLine("<ul>");

        foreach (var node in directory.Children)
        {
            switch (node)
            {
                case SiteDirectory childDirectory:
                    htmlBuilder.AppendLine($"<li>{GenerateNestedList(childDirectory, depth + 1)}</li>");
                    break;
                case SiteFile siteFile:
                    htmlBuilder.AppendLine($"<li><a href=\"{siteFile.PageData.Path}\">{siteFile.PageData.Meta["title"]}</a></li>");
                    break;
            }
        }

        htmlBuilder.AppendLine("</ul>");

        return htmlBuilder.ToString();
    }

    private Dictionary<string, string> ParseMetadata(string content)
    {
        using var reader = new StringReader(content);
        var parser = new Parser(reader);
        parser.Consume<StreamStart>();
        parser.Consume<DocumentStart>();
        var pageMeta = yamlDeserializer.Deserialize<Dictionary<string, string>>(parser);
        return pageMeta;
    }

    private static SiteDirectory ConvertPagesToSiteDirectory(List<Page> pages)
    {
        var root = new SiteDirectory(string.Empty, new List<Node>());
        foreach (var page in pages)
        {
            AddPageToDirectory(root, page);
        }
        return root;
    }

    private static void SortSiteDirectory(SiteDirectory directory)
    {
        foreach (var node in directory.Children)
        {
            if (node is SiteDirectory childDirectory)
            {
                SortSiteDirectory(childDirectory);
            }
        }

        directory.Children = directory.Children.OrderBy(n => n is SiteDirectory ? $"0{n.Name}" : $"1{n.Name}").ToList();
    }

    private static void AddPageToDirectory(SiteDirectory root, Page page)
    {
        var pathSegments = page.Path.Split('/');

        var directory = root;
        for (var i = 0; i < pathSegments.Length - 1; i++)
        {
            var pathSegment = pathSegments[i];
            var subDirectory = directory.Children.OfType<SiteDirectory>().FirstOrDefault(sd => sd.Name == pathSegment);
            if (subDirectory == null)
            {
                subDirectory = new SiteDirectory(pathSegment, new List<Node>());
                directory.Children.Add(subDirectory);
            }
            directory = subDirectory;
        }

        var siteFile = new SiteFile(page.Meta["title"], page);
        directory.Children.Add(siteFile);
    }
    
    private static void CopyDirectory(string sourceDir, string destinationDir, bool recursive)
    {
        var dir = new DirectoryInfo(sourceDir);

        if (!dir.Exists)
            throw new DirectoryNotFoundException($"Source directory not found: {dir.FullName}");

        var dirs = dir.GetDirectories();

        Directory.CreateDirectory(destinationDir);

        Parallel.ForEach(dir.GetFiles(), file =>
        {
            var targetFilePath = Path.Combine(destinationDir, file.Name);
            using var sourceStream = new FileStream(file.FullName, FileMode.Open, FileAccess.Read, FileShare.Read);
            using var destinationStream = new FileStream(targetFilePath, FileMode.Create, FileAccess.Write, FileShare.None);
            sourceStream.CopyTo(destinationStream);
        });

        if (!recursive) return;
        
        foreach (var subDir in dirs)
        {
            var newDestinationDir = Path.Combine(destinationDir, subDir.Name);
            CopyDirectory(subDir.FullName, newDestinationDir, true);
        }
    }
}