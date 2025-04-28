#include "computor.hpp"

double	Computor::getGCD(double a, double b)
{
	double eps=1e-8;

	a = std::fabs(a);
	b = std::fabs(b);
	while (b > eps)
	{
		double temp = std::fmod(a, b);
		a = b;
		b = temp;
	}
    return a;
}

int	Computor::reduce()
{
	double	gcd = getGCD(this->_data[0].getCoefficient(), this->_data[1].getCoefficient());
	int	k = 0;
	
	for (int i = 2; i < getMaxDeg() + 1; i++)
		gcd = getGCD(gcd, this->_data[i].getCoefficient());
	if (gcd != 0.0)
	{
		printGCD(gcd);
		for (int i = 0; i < getMaxDeg() + 1; i++)
			this->_data[i].coefficient /= gcd;
		for (k = getMaxDeg(); k > 0; k--)
		{
			if (this->_data[k].getCoefficient() != 0.0)
				break;
		}
	}
	std::cout << "Reduced Form: " << this->_data[k].getCoefficient() << " * X^" << k;

	for (int i = k - 1; i >= 0; i--)
	{
		double	coeff = this->_data[i].getCoefficient();

		std::cout << ((coeff < 0.0) ? " - " : " + ") << std::fabs(coeff) << " * X^" << i;
	}
	std::cout << " = 0" << std::endl;
	this->_deg = k;
	std::cout << "Degree of the polynomial: " << k << std::endl << std::endl;
	if (k <= 2)
		return (EXIT_SUCCESS);
	std::cerr << "The polynomial degree is strictly greater than 2, I can't solve\n";
	return (EXIT_FAILURE);
}

std::vector<Term> Computor::simplifyEq(const std::vector<Term> &leftPoly, const std::vector<Term> &rightPoly)
{
	std::vector<Term>	res;
	bool				found;

	printSimplify(leftPoly, rightPoly);
	for (size_t i = 0; i < leftPoly.size(); i++)
	{
		found = false;
		for (size_t j = 0; j < rightPoly.size(); j++)
		{
			if (leftPoly[i].getExponent() == rightPoly[j].getExponent())
			{
				Term	t;
				t.exponent = leftPoly[i].getExponent();
				t.coefficient = leftPoly[i].getCoefficient() - rightPoly[i].getCoefficient();
				res.push_back(t);
				found = true;
				break;
			}
		}
		if (!found)
			res.push_back(leftPoly[i]);
	}
	for (size_t i = 0; i < rightPoly.size(); i++)
	{
		found = false;
		for (size_t j = 0; j < leftPoly.size(); j++)
		{
			if (rightPoly[i].getExponent() == leftPoly[j].getExponent())
			{
				found = true;
				break;
			}
		}
		if (!found)
		{
			Term	t = rightPoly[i];
			t.coefficient = -t.coefficient;
			res.push_back(t);
		}
	}
	std::vector<Term>	n_terms;
	for (int i = 0; i < getMaxDeg() + 1; i++)
		n_terms.push_back(getTerm(res, i));
	return (n_terms);
}

void	Computor::solve(void)
{
	if (_deg == 0)
		solveConstants();
	else if (_deg == 1)
		solveLinearEqs();
	else if (_deg == 2)
		solveQuadraticEqs();
}