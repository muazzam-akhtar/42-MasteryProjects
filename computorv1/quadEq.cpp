#include "computor.hpp"

void	Computor::printComplexFraction(double a, double b, double c)
{
	double	disc = findDisc(a, b, c);
	double	num = floor(sqrt(std::fabs(disc)));
	double	realPart = -b / (2 * a);

	if (realPart == -0.0)
		realPart = 0.0;
	while (num > 1)
	{
		if (fmod(disc, num * num) == 0.0)
			break;
		num--;
	}
	std::cout << "\033[" << GREEN;
	std::cout << "m" << "Fraction Form: ";
	if (realPart == 0.0 || realPart == -0.0)
	{
		if ((-disc / (num * num)) == 1.0)
			std::cout << getFractionalPart(num, 2 * a) << "i or "
			<< getFractionalPart(-num, 2 * a) << "i" << std::endl;
		else
			std::cout << getFractionSqRoot(num, 2 * a, -disc)
				<< "i or " << getFractionSqRoot(-num, 2 * a, -disc) << "i" << std::endl;
	}
	else
	{
		if ((disc / (num * num)) == 1.0 || (disc / (num * num)) == -1.0)
			std::cout << getFractionalPart(-b, 2 * a) << " + " << (getFractionalPart(num, 2 * a)
			== "1" ? "" : getFractionalPart(num, 2 * a)) << "i or " << getFractionalPart(-b, 2 * a)
			<< " - " << (getFractionalPart(num, 2 * a) == "1" ? "" : getFractionalPart(num, 2 * a)) << "i\n";
		else
			std::cout << getFractionalPart(-b, 2 * a) << " + " << (getFractionSqRoot(num, 2 * a, -disc) == "1" ? "" : getFractionSqRoot(num, 2 * a, -disc))
				<< "i or " << getFractionalPart(-b, 2 * a) << " - " <<
			(getFractionSqRoot(num, 2 * a, -disc) == "1" ? "" : getFractionSqRoot(num, 2 * a, -disc)) << "i\n";
	}
}

void	Computor::printComplexDecimal(double a, double b, double c)
{
	double	disc = findDisc(a, b, c);
	double	imagePart = sqrt(std::fabs(disc)) / (2 * a);
	double	num = floor(sqrt(std::fabs(disc)));
	double	realPart = -b / (2 * a);

	if (realPart == -0.0)
		realPart = 0.0;
	while (num > 1)
	{
		if (fmod(disc, num * num) == 0.0)
			break;
		num--;
	}
	std::cout << "Decimal Form: ";
	if (realPart == 0.0 && imagePart != 0.0)
	{
		std::cout << imagePart << "i or " << -imagePart << "i\n";
	}
	else
	{
		std::cout << realPart << " + " << (std::fabs(imagePart) == 1 ? "" : doubleToStr(imagePart)) << "i" << " or " << realPart
			<< " - " << (std::fabs(imagePart) == 1 ? "" : doubleToStr(imagePart)) << "i" << std::endl;	
	}
}

void	Computor::printRealFraction(double a, double b, double c)
{
	double	disc = findDisc(a, b, c);
	double	realPart = -b / (2 * a);
	double	imagePart = sqrt(disc) / (2 * a);
	double	ans = realPart + imagePart;

	ans = ans == -0.0 ? 0.0 : ans;
	std::cout << "\033[" << GREEN;
	std::cout << "m" << "Fraction Form: ";
	if (realPart == -0.0)
		realPart = 0.0;
	if (disc == 0.0)
	{
		std::cout << (ans == -0.0 ? "0" : getFractionalPart(-b, 2 * a)) << std::endl;
		return ;
	}
	double	num = floor(sqrt(disc));
	while (num > 1)
	{
		if (fmod(disc, num * num) == 0.0)
			break;
		num--;
	}
	if ((disc / (num * num)) == 1.0)
		std::cout << getFractionalPart(-b + num, 2 * a) << " or "
		<< getFractionalPart(-b - num, 2 * a) << std::endl;
	
	else if (realPart == 0.0)
		std::cout << getFractionSqRoot(num, 2 * a, disc)
			<< " or " << " -" << getFractionSqRoot(num, 2 * a, disc) << std::endl;
	else
		std::cout << getFractionalPart(-b, 2 * a) << " + " << getFractionSqRoot(num, 2 * a, disc)
			<< " or " << getFractionalPart(-b, 2 * a) << " - " << getFractionSqRoot(num, 2 * a, disc) << std::endl;
}

void	Computor::printRealDecimal(double a, double b, double c)
{
	double	disc = findDisc(a, b, c);
	double	realPart = -b / (2 * a);
	double	imagePart = sqrt(disc) / (2 * a);
	double	ans1 = realPart + imagePart;
	double	ans2 = realPart - imagePart;

	if (realPart == -0.0)
		realPart = 0.0;
	std::cout << "Decimal Form: " << (ans1 == -0.0 ? 0.0 : ans1);
	if (ans1 != ans2)
		std::cout << " or " << (ans2 == -0.0 ? 0.0 : ans2);
	std::cout << std::endl;
}