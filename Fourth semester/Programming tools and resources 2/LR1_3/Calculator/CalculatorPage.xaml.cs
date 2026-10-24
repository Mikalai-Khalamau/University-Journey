using System.Globalization;
namespace Calculator;

public partial class CalculatorPage : ContentPage
{
    private string currentInput = "0";
    private double firstNumber = 0;
    private string selectedOperator = "";
    private bool isNewNumber = true;

    public CalculatorPage()
    {
        InitializeComponent();
    }

    private void DigitButton_Clicked(object sender, EventArgs e)
    {
        Button button = (Button)sender;
        string digit = button.Text;

        if (isNewNumber)
        {
            currentInput = digit;
            isNewNumber = false;
        }
        else
        {
            if (currentInput.Length < 15)
            {
                if (currentInput == "0" && digit != "0")
                    currentInput = digit;
                else
                    currentInput += digit;
            }
        }
        DisplayEntry.Text = currentInput;
    }

    private void DecimalButton_Clicked(object sender, EventArgs e)
    {
        if (isNewNumber)
        {
            currentInput = "0.";
            isNewNumber = false;
        }
        else if (!currentInput.Contains("."))
        {
            currentInput += ".";
        }
        DisplayEntry.Text = currentInput;
    }

    private void ClearEntryButton_Clicked(object sender, EventArgs e)
    {
        currentInput = "0";
        DisplayEntry.Text = currentInput;
        isNewNumber = true;
    }

    private void ClearButton_Clicked(object sender, EventArgs e)
    {
        currentInput = "0";
        firstNumber = 0;
        selectedOperator = "";
        isNewNumber = true;
        DisplayEntry.Text = currentInput;
    }

    private void BackspaceButton_Clicked(object sender, EventArgs e)
    {
        if (currentInput.Length > 1)
        {
            currentInput = currentInput.Substring(0, currentInput.Length - 1);
        }
        else
        {
            currentInput = "0";
            isNewNumber = true;
        }
        DisplayEntry.Text = currentInput;
    }

    private void PercentButton_Clicked(object sender, EventArgs e)
    {
        double number = double.Parse(currentInput, CultureInfo.InvariantCulture);
        double result = number / 100.0;
        currentInput = result.ToString(CultureInfo.InvariantCulture);
        DisplayEntry.Text = currentInput;
        isNewNumber = true;
    }

    private void OperatorButton_Clicked(object sender, EventArgs e)
    {
        Button button = (Button)sender;
        string operation = button.Text;
        double currentNumber = double.Parse(currentInput, CultureInfo.InvariantCulture);

        if (!isNewNumber && !string.IsNullOrEmpty(selectedOperator))
        {
            Calculate(currentNumber);
        }
        else
        {
            firstNumber = currentNumber;
        }

        selectedOperator = operation;
        isNewNumber = true;
    }

    private void Calculate(double secondNumber)
    {
        double result = 0;

        switch (selectedOperator)
        {
            case "+":
                result = firstNumber + secondNumber;
                break;
            case "−":
                result = firstNumber - secondNumber;
                break;
            case "×":
                result = firstNumber * secondNumber;
                break;
            case "÷":
                if (secondNumber != 0)
                    result = firstNumber / secondNumber;
                else
                {
                    DisplayEntry.Text = "Ошибка";
                    currentInput = "0";
                    firstNumber = 0;
                    selectedOperator = "";
                    isNewNumber = true;
                    return;
                }
                break;
        }

        currentInput = result.ToString(CultureInfo.InvariantCulture);
        DisplayEntry.Text = currentInput;
        firstNumber = result;
    }

    private void ReciprocalButton_Clicked(object sender, EventArgs e)
    {
        double number = double.Parse(currentInput, CultureInfo.InvariantCulture);
        if (number != 0)
        {
            double result = 1.0 / number;
            currentInput = result.ToString(CultureInfo.InvariantCulture);
            DisplayEntry.Text = currentInput;
        }
        else
        {
            DisplayEntry.Text = "Ошибка";
            currentInput = "0";
        }
        isNewNumber = true;
    }

    private void SquareButton_Clicked(object sender, EventArgs e)
    {
        double number = double.Parse(currentInput, CultureInfo.InvariantCulture);
        double result = number * number;
        currentInput = result.ToString(CultureInfo.InvariantCulture);
        DisplayEntry.Text = currentInput;
        isNewNumber = true;
    }

    private void SqrtButton_Clicked(object sender, EventArgs e)
    {
        double number = double.Parse(currentInput, CultureInfo.InvariantCulture);
        if (number >= 0)
        {
            double result = Math.Sqrt(number);
            currentInput = result.ToString(CultureInfo.InvariantCulture);
            DisplayEntry.Text = currentInput;
        }
        else
        {
            DisplayEntry.Text = "Ошибка";
            currentInput = "0";
        }
        isNewNumber = true;
    }

    private void PowerButton_Clicked(object sender, EventArgs e)
    {
        double number = double.Parse(currentInput, CultureInfo.InvariantCulture);
        double result = Math.Pow(10, number);
        currentInput = result.ToString(CultureInfo.InvariantCulture);
        DisplayEntry.Text = currentInput;
        isNewNumber = true;
    }

    private void NegateButton_Clicked(object sender, EventArgs e)
    {
        if (currentInput != "0" && currentInput != "-0")
        {
            if (currentInput.StartsWith("-"))
                currentInput = currentInput.Substring(1);
            else
                currentInput = "-" + currentInput;
            DisplayEntry.Text = currentInput;
        }
    }

    private void EqualsButton_Clicked(object sender, EventArgs e)
    {
        if (!string.IsNullOrEmpty(selectedOperator))
        {
            double secondNumber = double.Parse(currentInput, CultureInfo.InvariantCulture);
            Calculate(secondNumber);
            selectedOperator = "";
            isNewNumber = true;
        }
    }
}