using Microsoft.AspNetCore.Mvc.Rendering;
using Microsoft.AspNetCore.Razor.TagHelpers;

namespace WEB_453503_Khalamau.UI.TagHelpers;

[HtmlTargetElement("Pager")]
public class PagerTagHelper(LinkGenerator linkGenerator, IHttpContextAccessor httpContextAccessor) : TagHelper
{
    [HtmlAttributeName("current-page")]
    public int CurrentPage { get; set; }

    [HtmlAttributeName("total-pages")]
    public int TotalPages { get; set; }

    [HtmlAttributeName("category")]
    public string? Category { get; set; }

    [HtmlAttributeName("admin")]
    public bool Admin { get; set; }

    public override void Process(TagHelperContext context, TagHelperOutput output)
    {
        output.TagName = "nav";
        output.Attributes.SetAttribute("aria-label", "Page navigation");

        var ul = new TagBuilder("ul");
        ul.AddCssClass("pagination justify-content-center");

        int prev = CurrentPage == 1 ? 1 : CurrentPage - 1;
        int next = CurrentPage == TotalPages ? TotalPages : CurrentPage + 1;

        // Previous button
        ul.InnerHtml.AppendHtml(CreateNavItem("Назад", prev, CurrentPage == 1, false));

        // Page numbers
        for (int i = 1; i <= TotalPages; i++)
        {
            ul.InnerHtml.AppendHtml(CreateNavItem(i.ToString(), i, false, CurrentPage == i));
        }

        // Next button
        ul.InnerHtml.AppendHtml(CreateNavItem("Вперед", next, CurrentPage == TotalPages, false));

        output.Content.AppendHtml(ul);
    }

    private TagBuilder CreateNavItem(string text, int pageNo, bool disabled, bool active)
    {
        var li = new TagBuilder("li");
        li.AddCssClass("page-item");
        if (disabled) li.AddCssClass("disabled");
        if (active) li.AddCssClass("active");

        var a = new TagBuilder("a");
        a.AddCssClass("page-link");

        string? url;
        if (Admin)
        {
            url = linkGenerator.GetPathByPage(
                httpContextAccessor.HttpContext!,
                page: "/Admin/Index",
                values: new { pageNo });
        }
        else
        {
            url = linkGenerator.GetPathByAction(
                httpContextAccessor.HttpContext!,
                action: "Index",
                controller: "Gem",
                values: new { type = Category, pageNo });
        }

        a.Attributes["href"] = url ?? "#";
        a.InnerHtml.Append(text);

        li.InnerHtml.AppendHtml(a);
        return li;
    }
}
