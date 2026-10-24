namespace Khalamau_453503.Domain.Entities;

public class Pizza : Entity
{
    public string Name { get; set; } = string.Empty;      
    public string ImagePath { get; set; } = string.Empty; 
    public int Time { get; set; }
    public int OrderId { get; set; }
    public Order? Order { get; set; } 
}