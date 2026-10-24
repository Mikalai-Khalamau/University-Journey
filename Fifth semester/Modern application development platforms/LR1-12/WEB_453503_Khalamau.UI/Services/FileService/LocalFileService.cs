namespace WEB_453503_Khalamau.UI.Services.FileService;

public class LocalFileService(IWebHostEnvironment environment) : IFileService
{
    public async Task<string> SaveFileAsync(IFormFile file)
    {
        var extension = Path.GetExtension(file.FileName);
        var fileName = $"{Guid.NewGuid()}{extension}";

        var imagesFolder = Path.Combine(environment.WebRootPath, "Images");
        Directory.CreateDirectory(imagesFolder);

        var filePath = Path.Combine(imagesFolder, fileName);
        await using var stream = new FileStream(filePath, FileMode.Create);
        await file.CopyToAsync(stream);

        return $"Images/{fileName}";
    }
}
