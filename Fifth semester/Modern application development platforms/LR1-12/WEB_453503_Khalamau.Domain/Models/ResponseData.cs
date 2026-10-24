namespace WEB_453503_Khalamau.Domain.Models;

public class ResponseData<T>
{
    public T? Data { get; set; }
    public bool Successfull { get; set; } = true;
    public string? ErrorMessage { get; set; }


    public static ResponseData<T> Ok(T data) =>
        new ResponseData<T> { Data = data, Successfull = true };

    public static ResponseData<T> Error(string message, T? data = default) =>
        new ResponseData<T> { ErrorMessage = message, Successfull = false, Data = data };
}