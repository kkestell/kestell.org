using Microsoft.Extensions.FileProviders;

namespace Builder;

internal class ServeCommandHandler
{
    private readonly Watcher watcher;
    private readonly ServeOptions options;

    public ServeCommandHandler(ServeCommand command)
    {
        options = new ServeOptions(command);
        
        watcher = new Watcher(options.RootDirectory.FullName);

        watcher.Changed += Rebuild;
        watcher.Created += Rebuild;
        watcher.Deleted += Rebuild;
        watcher.Renamed += Rebuild;
    }

    private void Rebuild(object? sender, FileSystemEventArgs e)
    {
        if (!string.IsNullOrEmpty(e.Name))
        {
            Console.WriteLine();
            Console.ForegroundColor = ConsoleColor.DarkGray;
            Console.WriteLine(new string('─', Console.WindowWidth));
            Console.ResetColor();
        }

        var builder = new SiteBuilder(options);

        try
        {
            builder.Build();
            // Console.WriteLine($"{e.Name}");
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
            Console.WriteLine();
            Console.ForegroundColor = ConsoleColor.Yellow;
            Console.WriteLine($"Listening on http://localhost:{options.Port}...");
            Console.ResetColor();

            // Console.ForegroundColor = ConsoleColor.DarkGray;
            // Console.WriteLine(new string('─', Console.WindowWidth));
            // Console.WriteLine();
            // Console.ResetColor();            

            Rebuild(null, new FileSystemEventArgs(WatcherChangeTypes.All, "", ""));

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
            .ConfigureLogging((hostingContext, logging) =>
            {
                logging.ClearProviders();
                logging.AddConsole();
                logging.AddFilter("Microsoft.Hosting", LogLevel.None);
                logging.AddFilter("Microsoft.AspNetCore", LogLevel.None);
            })
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