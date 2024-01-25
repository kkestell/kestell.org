namespace Builder;

internal class ServeOptions : BuildOptions
{
    public ServeOptions(ServeCommand command) : base(command)
    {
        Port = Option(command.Port);
    }
    
    public int Port { get; }
}