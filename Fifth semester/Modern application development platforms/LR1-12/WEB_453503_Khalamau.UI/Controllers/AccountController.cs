using System.Text;
using System.Text.Json;
using Microsoft.AspNetCore.Authentication;
using Microsoft.AspNetCore.Authentication.Cookies;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Options;
using WEB_453503_Khalamau.UI.HelperClasses;
using WEB_453503_Khalamau.UI.Models;
using WEB_453503_Khalamau.UI.Services.Authentication;
using WEB_453503_Khalamau.UI.Services.FileService;

namespace WEB_453503_Khalamau.UI.Controllers;

public class AccountController(
    HttpClient httpClient,
    ITokenAccessor tokenAccessor,
    IOptions<KeycloakData> options,
    IFileService fileService) : Controller
{
    [HttpGet]
    public IActionResult Register()
    {
        return View(new RegisterUserViewModel());
    }

    [HttpPost]
    [AutoValidateAntiforgeryToken]
    public async Task<IActionResult> Register(RegisterUserViewModel user)
    {
        if (!ModelState.IsValid)
        {
            return View(user);
        }

        try
        {
            await tokenAccessor.SetAuthorizationHeaderAsync(httpClient, true);
        }
        catch (Exception)
        {
            return Unauthorized();
        }

        var avatarUrl = "Images/default-profile-picture.png";
        if (user.Avatar is not null)
        {
            avatarUrl = await fileService.SaveFileAsync(user.Avatar);
        }

        var newUser = new CreateUserModel();
        newUser.Attributes.Add("avatar", avatarUrl);
        newUser.Email = user.Email;
        newUser.Username = user.Email;
        newUser.Credentials.Add(new UserCredentials { Value = user.Password });

        var requestUri = $"{options.Value.Host}/admin/realms/{options.Value.Realm}/users";

        var serializerOptions = new JsonSerializerOptions
        {
            PropertyNamingPolicy = JsonNamingPolicy.CamelCase
        };
        var userData = JsonSerializer.Serialize(newUser, serializerOptions);
        HttpContent content = new StringContent(userData, Encoding.UTF8, "application/json");

        var response = await httpClient.PostAsync(requestUri, content);

        if (response.IsSuccessStatusCode)
        {
            return Redirect(Url.Action("Index", "Home")!);
        }

        var error = await response.Content.ReadAsStringAsync();
        ModelState.AddModelError(string.Empty, $"Ошибка регистрации: {response.StatusCode}. {error}");
        return View(user);
    }

    [HttpGet]
    public IActionResult AccessDenied()
    {
        return View();
    }

    [HttpGet]
    public async Task Login()
    {
        await HttpContext.ChallengeAsync(
            "keycloak",
            new AuthenticationProperties { RedirectUri = Url.Action("Index", "Home") });
    }

    [HttpPost]
    [AutoValidateAntiforgeryToken]
    public async Task Logout()
    {
        // Сессию НЕ чистим: иначе вместе с ней стирается корзина из сессии.
        await HttpContext.SignOutAsync(CookieAuthenticationDefaults.AuthenticationScheme);
        await HttpContext.SignOutAsync("keycloak",
            new AuthenticationProperties { RedirectUri = Url.Action("Index", "Home") });
    }

    private class CreateUserModel
    {
        public Dictionary<string, string> Attributes { get; set; } = new();
        public string Username { get; set; } = string.Empty;
        public string Email { get; set; } = string.Empty;
        public bool Enabled { get; set; } = true;
        public bool EmailVerified { get; set; } = true;
        public List<UserCredentials> Credentials { get; set; } = new();
    }

    private class UserCredentials
    {
        public string Type { get; set; } = "password";
        public bool Temporary { get; set; }
        public string Value { get; set; } = string.Empty;
    }
}
