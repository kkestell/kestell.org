namespace Builder;

internal class DirectoryWatcher
{
    private readonly DirectoryInfo _watchDirectory;
    private readonly CancellationToken _stoppingToken;
    private readonly Dictionary<string, DateTime> _lastModified = [];

    public event EventHandler? OnChanged;

    public DirectoryWatcher(DirectoryInfo watchDirectory, CancellationToken stoppingToken)
    {
        _watchDirectory = watchDirectory;
        _stoppingToken = stoppingToken;
    
        Task.Run(Run, stoppingToken);
    }

    private void Run()
    {
        while (!_stoppingToken.IsCancellationRequested)
        {
            var changed = false;
            var files = _watchDirectory.EnumerateFiles("*", SearchOption.AllDirectories);

            foreach (var file in files)
            {
                // Created
                if (!_lastModified.ContainsKey(file.FullName))
                {
                    _lastModified.Add(file.FullName, file.LastWriteTimeUtc);
                    changed = true;
                    continue;
                }

                // Modified
                if (_lastModified[file.FullName] != file.LastWriteTimeUtc)
                {
                    _lastModified[file.FullName] = file.LastWriteTimeUtc;
                    changed = true;
                    continue;
                }
            }

            foreach (var key in _lastModified.Keys.ToList())
            {
                // Deleted
                if (!File.Exists(key))
                {
                    _lastModified.Remove(key);
                    changed = true;
                }
            }

            if (changed)
            {
                OnChanged?.Invoke(this, EventArgs.Empty);
            }

            Thread.Sleep(3000);
        }
    }
}
