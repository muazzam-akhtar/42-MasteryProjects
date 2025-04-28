#include "computor.hpp"

Term	Computor::parseTerm(const std::string &term)
{
	Term	t = {0.0, 0};
	std::string	currentTerm;
	double		res = 1.0;
	char		*ptr;

	if (term.empty())
		return (t);
	for (size_t i = 0; i < term.length(); i++)
	{
		while (std::isdigit(term[i]) || term[i] == '-' || term[i] == '.')
			currentTerm += term[i++];
		if (currentTerm.length() > 0)
		{
			if (currentTerm == "-")
				res = -res;
			else
				res *= std::strtod(currentTerm.c_str(), &ptr);
			currentTerm = "";
		}
		if (term[i] == 'X')
		{
			if (term[i + 1] == '^' && std::isdigit(term[i + 2]))
			{
				int	count = 0;
				for (count = i + 2; std::isdigit(term[count]); count++);
				t.exponent = strtol(term.substr(i + 2, count).c_str(), &ptr, 10);
				i += count;
			}
			else
				t.exponent = 1;
		}
	}
	t.coefficient = res;
	return (t);
}

std::vector<Term> Computor::parsePolynomial(const std::string &polynomial)
{
	std::vector<Term>	terms;
	std::string	currentTerm = "";

	terms.push_back(parseTerm(currentTerm));
	for (size_t i = 0; i < polynomial.length(); i++)
	{
		if (polynomial[i] == '+' || polynomial[i] == '-')
		{
			if (i > 0)
			{
				Term t = parseTerm(currentTerm);
				if (terms.size() == 0)
					terms.push_back(t);
				else
				{
					for (size_t c = 0; c < terms.size(); c++)
					{
						if (terms[c].exponent == t.exponent)
						{
							terms[c].coefficient += t.coefficient;
							break;
						}
						else if (c == terms.size() - 1)
						{
							terms.push_back(t);
							break;
						}
					}
				}
			}
			currentTerm = std::string(1, polynomial[i]);
		}
		else
			currentTerm += polynomial[i];
	}
	Term t = parseTerm(currentTerm);
	if (terms.size() == 0)
		terms.push_back(t);
	else
	{
		for (size_t c = 0; c < terms.size(); c++)
		{
			if (terms[c].exponent == t.exponent)
			{
				terms[c].coefficient += t.coefficient;
				break;
			}
			else if (c == terms.size() - 1)
			{
				terms.push_back(t);
				break;
			}
		}
	}
	return (terms);
}

void	Computor::displayPolynomial(const std::vector<Term> &eq)
{
	for (std::vector<Term>::const_iterator it = eq.begin(); it != eq.end(); ++it)
	{
		if (it != eq.begin())
			std::cout << (((*it).getCoefficient() >= 0) ? " + " : " - ");
		if (it == eq.begin())
			std::cout << (*it).getCoefficient();
		else
			std::cout << std::fabs((*it).getCoefficient());
		if ((*it).getExponent() > 0)
		{
			std::cout << " * X";
			if ((*it).getExponent() > 1)
				std::cout << "^" << (*it).getExponent();
		}
	}
}

std::string	Computor::setColor(int color)
{
	std::string	ret;

	ret = "\033[" + std::to_string(color) + "m";
	return (ret);
}