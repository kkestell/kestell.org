using Microsoft.Extensions.FileProviders;

namespace Builder;

internal class ServeCommandHandler
{
    private readonly Watcher watcher;
    private readonly SiteBuilder builder;
    private readonly ServeOptions options;

    public ServeCommandHandler(ServeCommand command)
    {
        options = new ServeOptions(command);
        watcher = new Watcher(options.RootDirectory.FullName);
        builder = new SiteBuilder(options);

        watcher.Changed += Build;
        watcher.Created += Build;
        watcher.Deleted += Rebuild;
        watcher.Renamed += Rebuild;
    }

    private void Build(object? sender, FileSystemEventArgs e)
    {
        try
        {
            Console.WriteLine($"{e.Name}");
            
            if (e.Name.EndsWith(".md"))
                builder.BuildSingle(e.FullPath);
            else
                builder.Build();
        }
        catch (Exception exception)
        {
            Console.WriteLine(exception);
        }
    }

    private void Rebuild(object? sender, FileSystemEventArgs e)
    {
        try
        {
            Console.WriteLine($"{e.Name}");
            builder.Build();
        }
        catch (Exception exception)
        {
            Console.WriteLine(exception);
        }
    }
    
    public int Run()
    {
        try
        {
            builder.Build();
            Console.WriteLine($"Listening on http://localhost:{options.Port}...");
            CreateHostBuilder(options).Build().Run();
        }
        catch (Exception e)
        {
            Console.WriteLine(e);
            return 1;
        }
        
        return 0;
    }
    
    private static IHostBuilder CreateHostBuilder(ServeOptions serveOptions) =>
        Host.CreateDefaultBuilder()
            // .ConfigureLogging(logging =>
            // {
            //     logging.ClearProviders();
            //     logging.SetMinimumLevel(LogLevel.None);
            // })        
            .ConfigureWebHostDefaults(webBuilder =>
            {
                webBuilder.UseUrls($"http://localhost:{serveOptions.Port}");
                webBuilder.ConfigureServices(services => { services.AddDirectoryBrowser(); });
                webBuilder.Configure(app =>
                {
                    if (!Directory.Exists(serveOptions.OutputDirectory.FullName))
                    {
                        Directory.CreateDirectory(serveOptions.OutputDirectory.FullName);
                    }

                    app.UseFileServer(new FileServerOptions
                    {
                        FileProvider = new PhysicalFileProvider(serveOptions.OutputDirectory.FullName),
                        EnableDirectoryBrowsing = true
                    });
                });
            });
}