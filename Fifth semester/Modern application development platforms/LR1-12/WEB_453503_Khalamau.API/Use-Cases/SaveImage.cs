using MediatR;

namespace WEB_453503_Khalamau.API.Use_Cases;

public sealed record SaveImage(IFormFile file) : IRequest<string>;

public class SaveImageHandler(
    IWebHostEnvironment env,
    IHttpContextAccessor httpContextAccessor)
    : IRequestHandler<SaveImage, string>
{
    public async Task<string> Handle(SaveImage request, CancellationToken cancellationToken)
    {
        var imagesFolder = Path.Combine(env.WebRootPath, "Images");
        Directory.CreateDirectory(imagesFolder);

        var extension = Path.GetExtension(request.file.FileName);
        if (string.IsNullOrWhiteSpace(extension))
        {
            extension = ".jpg";
        }

        var fileName = $"{Guid.NewGuid():N}{extension}";
        var filePath = Path.Combine(imagesFolder, fileName);

        await using (var stream = File.Create(filePath))
        {
            await request.file.CopyToAsync(stream, cancellationToken);
        }

        var httpContext = httpContextAccessor.HttpContext
            ?? throw new InvalidOperationException("HttpContext недоступен для формирования URL изображения");

        return $"{httpContext.Request.Scheme}://{httpContext.Request.Host}/Images/{fileName}";
    }
}
