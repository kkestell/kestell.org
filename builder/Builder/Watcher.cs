namespace Builder;

public class Watcher : IDisposable
{
    private readonly FileSystemWatcher watcher;
    
    private static DateTime lastChange = DateTime.MinValue;
    
    public event EventHandler<FileSystemEventArgs>? Changed;
    public event EventHandler<FileSystemEventArgs>? Created;
    public event EventHandler<FileSystemEventArgs>? Deleted;
    public event EventHandler<RenamedEventArgs>? Renamed;
    
    public Watcher(string path)
    {
        watcher = new FileSystemWatcher(path);
        watcher.Changed += OnChanged;
        watcher.Created += OnCreated;
        watcher.Deleted += OnDeleted;
        watcher.Renamed += OnRenamed;

        watcher.Filter = "";
        watcher.IncludeSubdirectories = true;
        watcher.EnableRaisingEvents = true;
    }
    
    private void OnChanged(object sender, FileSystemEventArgs e)
    {
        if (e.ChangeType != WatcherChangeTypes.Changed)
        {
            return;
        }
        
        if (DateTime.Now.Subtract(lastChange).TotalMilliseconds < 100)
        {
            return;
        }
        
        Changed?.Invoke(sender, e);
        
        lastChange = DateTime.Now;
    }

    private void OnCreated(object sender, FileSystemEventArgs e) =>
        Created?.Invoke(sender, e);

    private void OnDeleted(object sender, FileSystemEventArgs e) =>
        Deleted?.Invoke(sender, e);
    
    private void OnRenamed(object sender, RenamedEventArgs e) =>
        Renamed?.Invoke(sender, e);
    
    public void Dispose()
    {
        watcher.Dispose();
    }
}