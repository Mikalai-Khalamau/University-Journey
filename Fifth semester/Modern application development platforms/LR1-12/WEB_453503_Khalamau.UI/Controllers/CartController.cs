using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using WEB_453503_Khalamau.Domain.Entities;
using WEB_453503_Khalamau.UI.Services.GemService;

namespace WEB_453503_Khalamau.UI.Controllers;

public class CartController(IGemService gemService, Cart cart) : Controller
{
    [HttpGet]
    public IActionResult Index()
    {
        return View(cart);
    }

    [Authorize]
    [HttpPost]
    [Route("Cart/add/{id:int}")]
    public async Task<IActionResult> Add(int id, string returnUrl)
    {
        var response = await gemService.GetGemByIdAsync(id);
        if (response.Successfull && response.Data != null)
        {
            cart.AddToCart(response.Data);
        }
        return Redirect(returnUrl);
    }

    [Authorize]
    [HttpPost]
    [Route("Cart/remove/{id:int}")]
    public IActionResult Remove(int id, string returnUrl)
    {
        cart.RemoveItems(id);
        return Redirect(returnUrl);
    }

    [Authorize]
    [HttpPost]
    [Route("Cart/clear")]
    public IActionResult Clear(string returnUrl)
    {
        cart.ClearAll();
        return Redirect(returnUrl);
    }
}
