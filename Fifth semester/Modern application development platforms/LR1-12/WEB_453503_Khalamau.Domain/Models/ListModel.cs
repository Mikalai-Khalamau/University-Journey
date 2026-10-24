namespace WEB_453503_Khalamau.Domain.Models;

public class ListModel<T>
{
    public IEnumerable<T> Items { get; set; } = Enumerable.Empty<T>();
    public int PageNo { get; set; } = 1;
    public int PageSize { get; set; } = 3;
    public int TotalCount { get; set; }

    public int TotalPages => (int)Math.Ceiling(TotalCount / (double)(PageSize > 0 ? PageSize : 1));
    public int CurrentPage => PageNo;
}
