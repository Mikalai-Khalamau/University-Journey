using Microsoft.AspNetCore.Mvc;
using WEB_453503_Khalamau.Domain.Entities;

namespace WEB_453503_Khalamau.UI.ViewComponents;

public class CartViewComponent(Cart cart) : ViewComponent
{
    public IViewComponentResult Invoke()
    {
        ViewBag.TotalPrice = cart.TotalPrice.ToString("N2");
        ViewBag.Count = cart.Count;
        return View();
    }
}
