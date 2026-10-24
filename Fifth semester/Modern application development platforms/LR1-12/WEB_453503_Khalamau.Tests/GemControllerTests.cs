using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using NSubstitute;
using WEB_453503_Khalamau.Domain.Entities;
using WEB_453503_Khalamau.Domain.Models;
using WEB_453503_Khalamau.UI.Controllers;
using WEB_453503_Khalamau.UI.Services.GemService;
using WEB_453503_Khalamau.UI.Services.GemTypeService;
using Xunit;

namespace WEB_453503_Khalamau.Tests;

public class GemControllerTests
{
    [Fact]
    public async Task Index_ReturnsNotFound_WhenCategoryServiceFails()
    {
        // Arrange
        var gemService = Substitute.For<IGemService>();
        var gemTypeService = Substitute.For<IGemTypeService>();

        gemTypeService.GetGemTypeListAsync().Returns(ResponseData<List<GemType>>.Error("Error"));

        var controller = new GemController(gemService, gemTypeService)
        {
            ControllerContext = new ControllerContext
            {
                HttpContext = new DefaultHttpContext()
            }
        };

        // Act
        var result = await controller.Index(null, 1);

        // Assert
        Assert.IsType<NotFoundObjectResult>(result);
    }

    [Fact]
    public async Task Index_ReturnsNotFound_WhenGemServiceFails()
    {
        // Arrange
        var gemService = Substitute.For<IGemService>();
        var gemTypeService = Substitute.For<IGemTypeService>();

        var categories = new List<GemType> { new() { Id = 1, Name = "Test", NormalizedName = "test" } };
        gemTypeService.GetGemTypeListAsync().Returns(ResponseData<List<GemType>>.Ok(categories));
        gemService.GetGemListAsync(Arg.Any<string?>(), Arg.Any<int>()).Returns(ResponseData<ListModel<Gem>>.Error("Error"));

        var controller = new GemController(gemService, gemTypeService)
        {
            ControllerContext = new ControllerContext
            {
                HttpContext = new DefaultHttpContext()
            }
        };

        // Act
        var result = await controller.Index(null, 1);

        // Assert
        Assert.IsType<NotFoundObjectResult>(result);
    }

    [Fact]
    public async Task Index_ReturnsViewWithCorrectData_OnSuccess()
    {
        // Arrange
        var gemService = Substitute.For<IGemService>();
        var gemTypeService = Substitute.For<IGemTypeService>();

        var categories = new List<GemType> { new() { Id = 1, Name = "Precious", NormalizedName = "precious" } };
        var gems = new ListModel<Gem>
        {
            Items = new List<Gem> { new() { Id = 1, Name = "Diamond" } },
            PageNo = 1,
            PageSize = 3,
            TotalCount = 1
        };

        gemTypeService.GetGemTypeListAsync().Returns(ResponseData<List<GemType>>.Ok(categories));
        gemService.GetGemListAsync("precious", 1).Returns(ResponseData<ListModel<Gem>>.Ok(gems));

        var controller = new GemController(gemService, gemTypeService)
        {
            ControllerContext = new ControllerContext
            {
                HttpContext = new DefaultHttpContext()
            }
        };

        // Act
        var result = await controller.Index("precious", 1);

        // Assert
        var viewResult = Assert.IsType<ViewResult>(result);
        var model = Assert.IsAssignableFrom<ListModel<Gem>>(viewResult.Model);

        Assert.Equal(categories, controller.ViewData["categories"]);
        Assert.Equal("Precious", controller.ViewData["currentCategory"]);
        Assert.Single(model.Items);
    }

    [Fact]
    public async Task Index_SetsAllCategory_WhenCategoryIsNull()
    {
        // Arrange
        var gemService = Substitute.For<IGemService>();
        var gemTypeService = Substitute.For<IGemTypeService>();

        var categories = new List<GemType> { new() { Id = 1, Name = "Precious", NormalizedName = "precious" } };
        var gems = new ListModel<Gem>
        {
            Items = new List<Gem>(),
            PageNo = 1,
            PageSize = 3,
            TotalCount = 0
        };

        gemTypeService.GetGemTypeListAsync().Returns(ResponseData<List<GemType>>.Ok(categories));
        gemService.GetGemListAsync(null, 1).Returns(ResponseData<ListModel<Gem>>.Ok(gems));

        var controller = new GemController(gemService, gemTypeService)
        {
            ControllerContext = new ControllerContext
            {
                HttpContext = new DefaultHttpContext()
            }
        };

        // Act
        var result = await controller.Index(null, 1);

        // Assert
        var viewResult = Assert.IsType<ViewResult>(result);
        Assert.Equal("Все", controller.ViewData["currentCategory"]);
    }
}
