using Microsoft.Extensions.FileProviders;

namespace Builder;

internal class ServeCommandHandler
{
    private readonly ServeOptions _options;
    private readonly CancellationTokenSource _cancellationTokenSource = new();
    private readonly DirectoryWatcher _watcher;

    public ServeCommandHandler(ServeCommand command)
    {
        _options = new ServeOptions(command);
        _watcher = new DirectoryWatcher(_options.ContentDirectory, _cancellationTokenSource.Token);
        _watcher.OnChanged += OnChanged;
    }

    private void OnChanged(object? sender, EventArgs e)
    {
        Rebuild();
    }

    private void Rebuild()
    {
        Console.WriteLine();
        Console.ForegroundColor = ConsoleColor.DarkGray;
        Console.WriteLine(new string('─', Console.WindowWidth));
        Console.ResetColor();

        var builder = new SiteBuilder(_options);

        try
        {
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
            Console.WriteLine();
            Console.ForegroundColor = ConsoleColor.Yellow;
            Console.WriteLine($"Listening on http://localhost:{_options.Port}...");
            Console.ResetColor();          

            Rebuild();

            CreateHostBuilder(_options).Build().Run();
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