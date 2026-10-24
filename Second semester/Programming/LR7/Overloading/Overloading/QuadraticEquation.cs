namespace Overloading
{
    internal class QuadraticEquation
    {

        private int a, b, c;

        public QuadraticEquation(int a, int b, int c)
        {
            this.a = a;
            this.b = b;
            this.c = c;
        }

        public QuadraticEquation()
        {
            a = 1;
            b = -2;
            c = 1;
        }
        public int A
        {
            get => a;
            set
            {
                if (value == 0)
                {
                    throw new ArgumentException("Коэффициент при x^2 не может быть равен нулю, так как тогда уравнение не будет квадратным");
                }
                a = value;
            }
        }

        public int B
        {
            get => b;
            set => b = value;
        }

        public int C
        {
            get => c;
            set => c = value;
        }

        public List<Double> FindRoots()
        {
            List<double> roots = new List<double>();

            double discriminant = b * b - 4 * a * c;

            if (discriminant < 0)
            {
                return roots;
            }
            else if (discriminant == 0)
            {
                roots.Add(-b / (2.0 * a));
                return roots;
            }
            else
            {
                double sqrtDiscriminant = Math.Sqrt(discriminant);
                roots.Add((-b - sqrtDiscriminant) / (2.0 * a));
                roots.Add((-b + sqrtDiscriminant) / (2.0 * a));
                return roots;
            }
        }
            public override string ToString()
        {

            string partA ="",partB="", partC="";
            if (A==0)
            {
                partA = "";
            }
            else if (A==1)
            {
                partA = "x^2";
            }
            else if (A == -1)
            {
                partA = "-x^2";
            }
            else
            {
                partA = $"{A}x^2";
            }

            if (B == 1)
            {
                partB = $" + x";
            }
            else if (B == -1)
            {
                partB = $" - x";
            }
            else if (B>0)
            {
                 partB = $" + {B}x";
            }
            else if (B<0)
            {
                 partB = $" - {-B}x";
            }
            if (C > 0)
            {
                 partC = $" + {C}";
            }
            else if (C<0)
            {
                 partC = $" - {-C}";
            }
            return $"{partA}{partB}{partC} = 0";
        }

        public int this[int index]
        {
            get
            {
                switch (index)
                {
                    case 0: return A;
                    case 1: return B;
                    case 2: return C;
                    default: throw new IndexOutOfRangeException("Индекс должен быть 0 (A), 1 (B) или 2 (C)");
                }
            }
            set
            {
                switch (index)
                {
                    case 0: A = value; break;
                        case 1: B = value; break;
                        case 2: C = value; break;
                        default: throw new IndexOutOfRangeException("Индекс должен быть 0 (A), 1 (B) или 2 (C)");
                }
            }
        }

        public static QuadraticEquation operator +(QuadraticEquation eq1, QuadraticEquation eq2)
        {
            return new QuadraticEquation(eq1.A + eq2.A, eq1.B + eq2.B, eq1.C + eq2.C);
        }

        public static QuadraticEquation operator -(QuadraticEquation eq1, QuadraticEquation eq2)
        {
            return new QuadraticEquation(eq1.A-eq2.A,eq1.B-eq2.B, eq1.C-eq2.C);
        }

        public static QuadraticEquation operator *(QuadraticEquation eq,int number)
        {
            return new QuadraticEquation(eq.A*number,eq.B*number, eq.C*number);
        }

        public static QuadraticEquation operator /(QuadraticEquation eq, int number)
        {
            if (number == 0)
                throw new DivideByZeroException("Деление на ноль невозможно");
            return new QuadraticEquation(eq.A / number, eq.B / number, eq.C / number);
        }

        public static QuadraticEquation operator ++(QuadraticEquation eq)
        {
            return new QuadraticEquation(eq.A + 1, eq.B + 1, eq.C + 1);
        }

        public static QuadraticEquation operator --(QuadraticEquation eq)
        {
            return new QuadraticEquation(eq.A - 1, eq.B - 1, eq.C - 1);
        }

        public static bool operator ==(QuadraticEquation eq1, QuadraticEquation eq2)
        {
            return eq1.A==eq2.A && eq1.B==eq2.B && eq1.C==eq2.C;
        }

        public static bool operator !=(QuadraticEquation eq1, QuadraticEquation eq2)
        {
            return !(eq1==eq2);
        }
        public static bool operator true(QuadraticEquation eq)
        {
            return eq.FindRoots().Count>0;
        }

        public static bool operator false(QuadraticEquation eq)
        {
            return eq.FindRoots().Count == 0;
        }

        public static explicit operator int (QuadraticEquation eq)
        {
            return eq.A;
        }
        public static explicit operator QuadraticEquation(int a)
        {
            return new QuadraticEquation(a, 0, 0);
        }

        public override bool Equals(object? obj)
        {
            return obj is QuadraticEquation other
                && A == other.A
                && B == other.B
                && C == other.C;
        }

        public override int GetHashCode()
        {
            return HashCode.Combine(A, B, C);
        }
    }
}


