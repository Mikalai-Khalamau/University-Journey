using System.Globalization;

namespace Khalamau_453503.UI.ValueConverters;

public class IdToImageConverter : IValueConverter
{
    private const string Placeholder = "pizza_placeholder.png"; // Должен лежать в Resources/Images/

    public object Convert(object value, Type targetType, object parameter, CultureInfo culture)
    {
        if (value is not int id || id <= 0)
            return Placeholder;

        string imagesFolder = Path.Combine(FileSystem.Current.AppDataDirectory, "Images");
        string imagePath = Path.Combine(imagesFolder, $"{id}.jpg");

        return File.Exists(imagePath) ? imagePath : Placeholder;
    }

    public object ConvertBack(object value, Type targetType, object parameter, CultureInfo culture)
        => throw new NotImplementedException();
}