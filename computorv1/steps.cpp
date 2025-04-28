#include "computor.hpp"

void	Computor::printSimplify(const std::vector<Term> &leftPoly, const std::vector<Term> &rightPoly)
{
	std::cout << "Original Input: ";
	displayPolynomial(leftPoly);
	std::cout << " = ";
	if (rightPoly.size() != 0)
		displayPolynomial(rightPoly);
	else
		std::cout << "0";
	std::cout << std::endl;
	std::cout << "Subtracting L.H.S from R.H.S \n";
	displayPolynomial(leftPoly);
	if (rightPoly.size() > 0)
	{
		std::cout << " ";
		std::vector<Term>	tmp = rightPoly;
		for (size_t	i = 0; i < tmp.size(); i++)
			tmp[i].coefficient = -tmp[i].coefficient;
		if (tmp.size() > 0)
		{
			std::cout << (tmp[0].coefficient < 0.0 ? "- " : "+ ");
			tmp[0].coefficient = std::fabs(tmp[0].coefficient);
			displayPolynomial(tmp);
		}
		std::cout << " = 0\n\n";
		return ;
	}
	std::cout << " = 0\n" << std::endl;
}

void	Computor::printGCD(double gcd)
{
	std::vector<Term>	tmp;
	if (gcd != 1.0)
	{
		std::cout << "After Simplification: ";
		for (size_t i = 0; i < this->_data.size(); i++)
		{
			if (std::fabs(this->_data[i].getCoefficient()) != 0.0)
				tmp.push_back(this->_data[i]);
		}
		displayPolynomial(tmp);
		std::cout << " = 0" << "\nDividing the equation with GCD.\n";
		std::cout << "Here, GCD: " << gcd << std::endl << std::endl;
	}
}