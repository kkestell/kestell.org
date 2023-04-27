namespace Builder;

public class Page
{
    public Dictionary<string, string> Meta { get; set; }
    public string Content { get; set; }
    public string Path { get; set; }
    public string Pdf { get; set; }
    public string GeneratedAt { get; set; }

    public string Title => Meta["title"];
    public string Description => Meta["description"];
    public string Date => Meta["date"];
}

public abstract class Node
{
    public string Name { get; set; }

    public Node(string name)
    {
        Name = name;
    }
}

public class SiteDirectory : Node
{
    public List<Node> Children { get; set; }

    public SiteDirectory(string name, List<Node> children) : base(name)
    {
        Children = children;
    }
}

public class SiteFile : Node
{
    public Page PageData { get; set; }
    
    public SiteFile(string name, Page pageData) : base(name)
    {
        PageData = pageData;
    }
}