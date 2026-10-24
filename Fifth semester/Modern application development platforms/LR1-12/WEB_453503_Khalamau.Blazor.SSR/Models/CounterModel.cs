using System.ComponentModel.DataAnnotations;

namespace WEB_453503_Khalamau.Blazor.SSR.Models;

public class CounterModel
{
    [Range(1, 10, ErrorMessage = "Значение должно быть целым числом от 1 до 10.")]
    public int Value { get; set; }
}
