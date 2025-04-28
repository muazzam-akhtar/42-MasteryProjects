#include "computor.hpp"

Term	Computor::getTerm(const std::vector<Term> &eq, int e)
{
	Term	t = {0.0, e};
	for (size_t	i = 0; i < eq.size(); i++)
	{
		if (eq[i].getExponent() == e)
			return (eq[i]);
	}
	return (t);
}

double	Computor::findDisc(double a, double b, double c)
{
	double	disc = (std::round((b * b) - (4 * a * c)) * 1e6) / 1e6;
	if (disc == -0.0)
		disc = 0.0;
	return disc;
}

std::string Computor::format_clean_double(double value)
{
	std::ostringstream oss;
	if (std::fabs(value - std::round(value)) < 1e-8)
	{
		oss << std::fixed << std::setprecision(0) << value;
		return oss.str();
	}
	oss << value;
	return oss.str();
}

std::string				Computor::getFractionalPart(double a, double b)
{
	double				gcd = getGCD(a, b);
	double				num = a / gcd;
	double				den = b / gcd;

	std::string ret = doubleToStr(num);
	if (den != 1.0)
		ret += "/" + doubleToStr(den);
	return (ret);

}

std::string				Computor::getFractionSqRoot(double a, double b, double sq)
{
	std::string	tmp = getFractionalPart(a, b);
	if ((a / b) == 1)
		return ("√" + doubleToStr((sq / (a * a))));
	if (tmp.substr(0, tmp.find_first_of("/")) == "1")
	{
		std::string	ret = ("(√" + doubleToStr((sq / (a * a))));
		return (ret + tmp.substr(tmp.find_first_of("/")) + ")");
	}
	else if (tmp.substr(0, tmp.find_first_of("/")) == "-1")
	{
		std::string	ret = ("-(√" + doubleToStr((sq / (a * a))));
		return (ret + tmp.substr(tmp.find_first_of("/")) + ")");
	}
	if (sq / (a * a) == 1.0)
		return (tmp.substr(0, tmp.find_first_of("/")) + tmp.substr(tmp.find_first_of("/")));
	if (tmp.find_first_of("/") == std::string::npos)
		return tmp + "√" + doubleToStr(sq / (a * a));
	return ("(" + tmp.substr(0, tmp.find_first_of("/")) + "√" + doubleToStr(sq / (a * a)) + ")" + tmp.substr(tmp.find_first_of("/")));
}

std::string	Computor::doubleToStr(double num)
{
	std::ostringstream	oss;

	oss << std::fixed << std::setprecision(4) << num;
	std::string ret = oss.str();
	ret.erase(ret.find_last_not_of('0') + 1, std::string::npos);
	if (!ret.empty() && ret.back() == '.')
		ret.pop_back();
	return (ret);
}