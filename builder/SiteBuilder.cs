using System.Collections.Concurrent;
using System.Diagnostics;
using System.Globalization;
using System.Text;
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
    private readonly object lockObject = new object();

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
            .UseFootnotes()
            .Build();

        pageTemplate =
            Handlebars.Compile(File.ReadAllText(Path.Combine(buildOptions.TemplateDirectory.FullName, "page.hbs")));
        homeTemplate =
            Handlebars.Compile(File.ReadAllText(Path.Combine(buildOptions.TemplateDirectory.FullName, "home.hbs")));
    }

    public void Build()
    {
        Console.ForegroundColor = ConsoleColor.Cyan;
        Console.WriteLine($"Build started at {DateTime.Now:hh:mm:ss tt}");
        Console.ResetColor();

        var sw = new Stopwatch();
        sw.Start();

        if (buildOptions.OutputDirectory.Exists)
            buildOptions.OutputDirectory.Delete(recursive: true);
        
        buildOptions.OutputDirectory.Create();

        var files = Directory.GetFiles(buildOptions.ContentDirectory.FullName, "*.md", SearchOption.AllDirectories);

        var pages = new ConcurrentBag<Page>();

        Parallel.ForEach(files, (file) =>
        {
            try
            {
                var page = BuildPage(file);

                if (page != null)
                    pages.Add(page);
            }
            catch (Exception e)
            {
                Console.ForegroundColor = ConsoleColor.Red;
                Console.WriteLine($"✗ Failed to build {file}");
                Console.WriteLine(e);
                Console.ResetColor();
            }
        });

        BuildHomepage(pages.ToList());

        CopyFilesRecursively(
            buildOptions.StaticDirectory, 
            new DirectoryInfo(Path.Combine(buildOptions.OutputDirectory.FullName, "static")));

        if (buildOptions.OptimizeImages)
        {
            OptimizeImages();
        }

        if (buildOptions.BuildPdfs)
        {
            // Parallel.ForEach(files, GeneratePdf);
            foreach (var file in files)
            {
                try
                {
                    GeneratePdf(file);
                }
                catch (Exception e)
                {
                    Console.ForegroundColor = ConsoleColor.Red;
                    Console.WriteLine($"✗ Failed to build {file}");
                    Console.WriteLine(e);
                    Console.ResetColor();
                }
            }
        }

        sw.Stop();

        Console.ForegroundColor = ConsoleColor.Green;
        Console.WriteLine($"✓ Completed in {sw.Elapsed.TotalSeconds:0.00} seconds");
        Console.ResetColor();
    }

    private string RewriteImagePaths(string file)
    {
        var tempFile = Path.Combine(Path.GetTempPath(), Path.GetRandomFileName());

        File.Copy(file, tempFile, true);

        var content = File.ReadAllText(tempFile);

        // FIXME: Yuck!
        var absoluteImagePath = Path.Combine(buildOptions.StaticDirectory.FullName, "images");
        content = content.Replace("/static/images", absoluteImagePath);

        File.WriteAllText(tempFile, content);

        return tempFile;
    }

    private void GeneratePdf(string file)
    {
        var sw = new Stopwatch();
        sw.Start();

        var content = File.ReadAllText(file);
        var pageMeta = ParseMetadata(content);

        bool.TryParse(pageMeta["draft"], out var draft);
        if (draft && !buildOptions.BuildDrafts)
            return;

        var relativePath = Path.GetRelativePath(buildOptions.ContentDirectory.FullName, file);
        var outputFile =
            Path.ChangeExtension(Path.Combine(buildOptions.OutputDirectory.FullName, relativePath), ".pdf");

        var tempFile = RewriteImagePaths(file);

        var args =
            $"{tempFile} --pdf-engine=xelatex --include-in-header=\"{Path.Combine(buildOptions.TemplateDirectory.FullName, "header.tex")}\" --variable \"block-headings\" --highlight-style=monochrome -f markdown -t pdf -o {outputFile}";

        var startInfo = new ProcessStartInfo
        {
            FileName = "pandoc",
            Arguments = args,
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
            throw new Exception(
                $"pandoc failed with exit code {process.ExitCode} and error {process.StandardError.ReadToEnd()} when converting {file} to {outputFile}");
        }

        File.Delete(tempFile);

        sw.Stop();

        var elapsed = $"{sw.Elapsed.TotalSeconds:0.00}";

        lock (lockObject)
        {
            Console.ForegroundColor = ConsoleColor.DarkGray;
            Console.Write($"{elapsed,-4}");
            Console.ResetColor();
            Console.Write($" {Path.GetRelativePath(buildOptions.OutputDirectory.ToString(), outputFile)}");
            Console.WriteLine();
        }
    }

    private Page? BuildPage(string file)
    {
        var sw = new Stopwatch();
        sw.Start();

        var content = File.ReadAllText(file);
        var pageMeta = ParseMetadata(content);

        bool.TryParse(pageMeta["draft"], out var draft);
        if (draft && !buildOptions.BuildDrafts)
            return null;

        var html = Markdown.ToHtml(content, markdownPipeline);

        var relativePath = Path.GetRelativePath(buildOptions.ContentDirectory.FullName, file);
        var outputFile =
            Path.ChangeExtension(Path.Combine(buildOptions.OutputDirectory.FullName, relativePath), ".html");

        Directory.CreateDirectory(Path.GetDirectoryName(outputFile)!);

        var path = Path.GetRelativePath(buildOptions.OutputDirectory.FullName, outputFile);

        var page = new Page
        {
            Meta = pageMeta,
            Content = html,
            Pdf = Path.GetFileName(Path.ChangeExtension(outputFile, ".pdf")),
            GeneratedAt = DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss"),
            Path = path
        };

        var renderedHtml = pageTemplate(new { Page = page });

        File.WriteAllText(outputFile, renderedHtml);

        sw.Stop();

        var elapsed = $"{sw.Elapsed.TotalSeconds:0.00}";

        lock (lockObject)
        {
            Console.ForegroundColor = ConsoleColor.DarkGray;
            Console.Write($"{elapsed,-4}");
            Console.ResetColor();
            Console.Write($" {Path.GetRelativePath(buildOptions.OutputDirectory.ToString(), outputFile)}");
            Console.WriteLine();
        }

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
                    htmlBuilder.Append("<li>");
                    if (siteFile.PageData.Meta.ContainsKey("draft") && bool.Parse(siteFile.PageData.Meta["draft"]))
                        htmlBuilder.Append("✍️ ");
                    htmlBuilder.Append($"<a href=\"{siteFile.PageData.Path}\">{siteFile.PageData.Meta["title"]}</a>");
                    if (!string.IsNullOrEmpty(siteFile.PageData.Meta["subtitle"]))
                        htmlBuilder.Append($"<br /><span>{siteFile.PageData.Meta["subtitle"]}</span>");
                    htmlBuilder.Append("</li>\n");
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
        var pathSegments = page.Path.Split(Path.DirectorySeparatorChar);

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

    public static void CopyFilesRecursively(DirectoryInfo source, DirectoryInfo target)
    {
        foreach (DirectoryInfo dir in source.GetDirectories())
            CopyFilesRecursively(dir, target.CreateSubdirectory(dir.Name));
        foreach (FileInfo file in source.GetFiles())
            file.CopyTo(Path.Combine(target.FullName, file.Name));
    }

    // private static void CopyDirectory(string sourceDir, string destinationDir, bool recursive)
    // {
    //     var dir = new DirectoryInfo(sourceDir);
    //
    //     if (!dir.Exists)
    //         throw new DirectoryNotFoundException($"Source directory not found: {dir.FullName}");
    //
    //     var dirs = dir.GetDirectories();
    //
    //     Directory.CreateDirectory(destinationDir);
    //
    //     foreach(var file in dir.GetFiles())
    //     {
    //         var targetFilePath = Path.Combine(destinationDir, file.Name);
    //         using var sourceStream = new FileStream(file.FullName, FileMode.Open, FileAccess.Read, FileShare.Read);
    //         using var destinationStream = new FileStream(targetFilePath, FileMode.Create, FileAccess.Write, FileShare.None);
    //         sourceStream.CopyTo(destinationStream);
    //     }
    //
    //     if (!recursive) return;
    //     
    //     foreach (var subDir in dirs)
    //     {
    //         var newDestinationDir = Path.Combine(destinationDir, subDir.Name);
    //         CopyDirectory(subDir.FullName, newDestinationDir, true);
    //     }
    // }

    private void OptimizeImages()
    {
        var files = Directory.GetFiles(Path.Combine(buildOptions.OutputDirectory.FullName, "static", "images"), "*.*",
            SearchOption.AllDirectories);

        foreach (var file in files)
        {
            var sw = new Stopwatch();
            sw.Start();

            var originalSize = new FileInfo(file).Length;

            if (Path.GetExtension(file) == ".png")
            {
                PngCrush(file);
            }
            else if (Path.GetExtension(file) == ".jpg")
            {
                JpegOptim(file);
            }

            var optimizedSize = new FileInfo(file).Length;

            sw.Stop();
            var elapsed = $"{sw.Elapsed.TotalSeconds:0.00}";

            lock (lockObject)
            {
                Console.ForegroundColor = ConsoleColor.DarkGray;
                Console.Write($"{elapsed,-4}");
                Console.ResetColor();
                Console.Write(
                    $" {Path.GetRelativePath(buildOptions.OutputDirectory.ToString(), file)} {originalSize:N0} -> {optimizedSize:N0}");
                Console.WriteLine();
            }
        }
    }

    private void PngCrush(string file)
    {
        var args = $"-reduce -ow \"{file}\"";

        var startInfo = new ProcessStartInfo
        {
            FileName = "pngcrush",
            Arguments = args,
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
            Console.WriteLine(
                $"pngcrush failed with exit code {process.ExitCode} and error {process.StandardError.ReadToEnd()} when optimizing {file}");
        }
    }

    private void JpegOptim(string file)
    {
        var args = $"--strip-all --all-progressive \"{file}\"";

        var startInfo = new ProcessStartInfo
        {
            FileName = "jpegoptim",
            Arguments = args,
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
            Console.WriteLine(
                $"jpgoptim failed with exit code {process.ExitCode} and error {process.StandardError.ReadToEnd()} when optimizing {file}");
        }
    }
}