namespace WEB_453503_Khalamau.UI.Services.FileService;

public interface IFileService
{
    Task<string> SaveFileAsync(IFormFile file);
}
