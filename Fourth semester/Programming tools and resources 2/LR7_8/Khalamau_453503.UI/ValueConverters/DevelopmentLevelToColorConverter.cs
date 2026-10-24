using System.Globalization;

namespace Khalamau_453503.UI.ValueConverters;

public class DevelopmentLevelToColorConverter : IValueConverter
{
    public object Convert(object value, Type targetType, object parameter, CultureInfo culture)
    {
        if (value is int time && time <= 15)
        {
            return Colors.Green;


        }
        return Colors.WhiteSmoke;
    }

    public object ConvertBack(object value, Type targetType, object parameter, CultureInfo culture)
    {
        throw new NotImplementedException();
    }
}