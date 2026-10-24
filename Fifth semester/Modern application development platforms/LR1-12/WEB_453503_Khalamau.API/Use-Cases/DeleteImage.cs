using MediatR;

namespace WEB_453503_Khalamau.API.Use_Cases;

public sealed record DeleteImage(string? ImageUrl) : IRequest;

public class DeleteImageHandler(IWebHostEnvironment env) : IRequestHandler<DeleteImage>
{
    public Task Handle(DeleteImage request, CancellationToken cancellationToken)
    {
        if (string.IsNullOrWhiteSpace(request.ImageUrl))
        {
            return Task.CompletedTask;
        }

        var fileName = Uri.TryCreate(request.ImageUrl, UriKind.Absolute, out var uri)
            ? Path.GetFileName(uri.LocalPath)
            : Path.GetFileName(request.ImageUrl);

        if (string.IsNullOrWhiteSpace(fileName))
        {
            return Task.CompletedTask;
        }

        if (fileName.Equals("noimage.jpg", StringComparison.OrdinalIgnoreCase))
        {
            return Task.CompletedTask;
        }

        var imagesFolder = Path.GetFullPath(Path.Combine(env.WebRootPath, "Images"));
        var filePath = Path.GetFullPath(Path.Combine(imagesFolder, fileName));

        if (!filePath.StartsWith(imagesFolder, StringComparison.OrdinalIgnoreCase))
        {
            return Task.CompletedTask;
        }

        if (File.Exists(filePath))
        {
            File.Delete(filePath);
        }

        return Task.CompletedTask;
    }
}
