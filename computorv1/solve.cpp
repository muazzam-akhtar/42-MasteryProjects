#include "computor.hpp"

void	Computor::solveConstants()
{
	double	coeff = this->_data[0].getCoefficient();

	if (coeff == 0.0)
	{
		std::cout << "\033[" << GREEN;
		std::cout << "m" << "Any Real number can be a solution\n";
	}
	else
	{
		std::cout << "\033[" << GREEN;
		std::cout << "m" "Contradictory Statement, No solution\n";
	}
}

void	Computor::solveLinearEqs()
{
	double	num = this->_data[0].getCoefficient();
	double	den = this->_data[1].getCoefficient();

	if (den < 0)
	{
		num = -num;
		den = -den;
	}
	num = -num;
	std::string	frac = getFractionalPart(num, den);
	std::cout << "Solution is:\n";
	if (num == -0 || num == 0)
	{
		std::cout << "\033[" << GREEN;
		std::cout << "m" << "Fractional Form: 0\n";

	}
	else
	{
		std::cout << "\033[" << GREEN;
		std::cout << "m" << "Fractional Form: " << frac << std::endl;
	}
	std::cout << "Decimal Form: " << (((num / den) == -0.0) ? 0.0 : (num / den)) << std::endl;
}

void	Computor::solveQuadraticEqs()
{
	double	a = this->_data[2].getCoefficient();
	double	b = this->_data[1].getCoefficient();
	double	c = this->_data[0].getCoefficient();
	if (a < 0)
	{
		a = -a;
		b = -b;
		c = -c;
	}
	double	disc = findDisc(a, b, c);
	if (disc < 0)
	{
		std::cout << "Discriminant is strictly negative, the two complex solutions are:\n";
		printComplexFraction(a, b, c);
		printComplexDecimal(a, b, c);
	}
	else
	{
		std::cout << (disc == 0.0 ? "Discriminant is zero" : "Discriminant is strictly positive") << ", " << (disc == 0.0 ? "there is only one solution:\n" : "the two solutions are:\n");
		printRealFraction(a, b, c);
		printRealDecimal(a, b, c);
	}
}