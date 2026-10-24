using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.Rendering; 
using WEB_453503_Khalamau.UI.Models;      
using System.Collections.Generic;          

namespace WEB_453503_Khalamau.UI.Controllers 
{
    public class HomeController : Controller
    {
        public IActionResult Index()
        {
            ViewData["LabTitle"] = "Лабораторная работа №2";

            var listData = new List<ListDemo>
            {
                new ListDemo { Id = 1, Name = "Item 1" },
                new ListDemo { Id = 2, Name = "Item 2" },
                new ListDemo { Id = 3, Name = "Item 3" }
            };

            ViewData["DemoList"] = new SelectList(listData, "Id", "Name");
            return View();
        }
    }
}