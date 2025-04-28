#include "parsing.hpp"

Parsing::Parsing(const std::string &str) : _str(str), allowedChars("0123456789*+-/.X^= "),
_digitVals("0123456789.- "), _varVals("0123456789X^ "), _validChars("0123456789X^"),
_validOps("+-*"), _validDouble("0123456789.-") {}

Parsing::~Parsing() {}

int	Parsing::ValidDouble(const std::string &str)
{
	size_t	i = 0;

	for (i = 0; i < str.length() && _validDouble.find(str[i]) != std::string::npos && (str[i] != '-' || i == 0); i++);
	try
	{
		double	number = std::strtod(str.substr(0, i).c_str(), NULL);
		std::ostringstream	oss1;
		if (str.substr(0, i).find_first_of(".") != std::string::npos)
		{
			oss1 << std::fixed << std::setprecision(i - str.substr(0,
				i).find_first_of(".") - 1) << number;
		}
		else
			oss1 << number;
		if (i == oss1.str().length() + 2 && str[i - 2] == '.' && str[i - 1] == '0')
			return (EXIT_SUCCESS);
		if (oss1.str().length() != i)
			return (EXIT_FAILURE);
		return (EXIT_SUCCESS);
	}
	catch (const std::invalid_argument& e)
	{
		return (EXIT_FAILURE);
	}
	catch (const std::out_of_range& e)
	{
		return (EXIT_FAILURE);
	}
}

int	Parsing::ValidOp(const std::string &str)
{
	size_t	i = 0;
	for (i = 0; i < str.length() && _validOps.find(str[i]) != std::string::npos; i++);
	if (i > 1)
		return (EXIT_FAILURE);
	if (str[0] == '+' || str[0] == '-' || str[0] == '*')
		return (EXIT_SUCCESS);
	return (EXIT_FAILURE);
}

int	Parsing::ValidVar(const std::string &str)
{
	size_t i = 0;
	for (i = 0; i < str.length() && _validChars.find(str[i]) != std::string::npos; i++);
	if (i > 0)
	{
		char	*end;
		if (i == 1)
			return (str[0] == 'X' ? EXIT_SUCCESS : EXIT_FAILURE);
		else if (i == 3)
			return (str[0] == 'X' && str[1] == '^' && std::isdigit(str[2])
				&& std::strtol(str.substr(2, 1).c_str(), &end, 10 ) >= 0
				&& std::strtol(str.substr(2, 1).c_str(), &end, 10)
				<= 9  ? EXIT_SUCCESS : EXIT_FAILURE);
		else
		{
			for (size_t j = 2; j < i; j++)
			{
				if (!std::isdigit(str[j]))
					return (EXIT_FAILURE);
			}
			return (EXIT_SUCCESS);
		}
	}
	return (EXIT_FAILURE);
}

int	Parsing::ValidatingOps(const std::string &str, size_t *i)
{
	if (ValidOp(&str[*i]))
		return (EXIT_FAILURE);
	if (str.find(' ', *i) == std::string::npos)
	{
		if (str[(*i)] == '+' || str[(*i)] == '-' || str[(*i)] == '*')
			return (EXIT_SUCCESS);
	}
	if (str.find(' ', *i) == std::string::npos)
		return (EXIT_FAILURE);
	return (EXIT_SUCCESS);
}

int Parsing::CheckPoly(const std::string& str)
{
	for (size_t i = 0; i < str.length(); i++)
	{
		if (allowedChars.find(str[i]) == std::string::npos)
			return this->code = 2;
	}
	if (str.empty() || allowedChars.find(str[0]) == std::string::npos)
		return (this->code = 2);
	for (size_t i = 0; i < str.length(); i++)
	{
		while (!ValidDouble(&str[i]))
		{
			bool	spaceTrig = false;
			while (_digitVals.find(str[i]) != std::string::npos)
			{
				if (spaceTrig == true && str[i] != ' ')
					return (this->code = 4);
				i++;
				if (str[i] == ' ')
				{
					i++;
					break;
				}
			}
			if (i == str.length())
				return (EXIT_SUCCESS);
			if (ValidatingOps(str, &i))
				return (this->code = 3);
			i++;
		}
		if (!ValidVar(&str[i]))
		{
			bool	spaceTrig = false;
			while (_varVals.find(str[i]) != std::string::npos)
			{
				if (spaceTrig == true && str[i] != ' ')
					return (this->code = 4);
				i++;
				if (str[i] == ' ')
					spaceTrig = true;
			}
			if (i == str.length())
				return (EXIT_SUCCESS);
			if (ValidatingOps(str, &i))
				return (this->code = 3);
		}
		else if (str[i] == ' ')
			continue;
		else
			return (this->code = 4);
	}
	return (this->code = 4);
}

int	Parsing::CheckXDeg(const std::string &str)
{
	std::string cleanedPoly = str;
	size_t	start = 0;
	for (size_t i = 0; i < cleanedPoly.length(); i++)
	{
		if (cleanedPoly[i] == ' ')
		{
			cleanedPoly.erase(i, 1);
			i--;
		}
	}
	for (size_t i = 0; i < cleanedPoly.length(); i++)
	{
		if (cleanedPoly[i] == '+' || cleanedPoly[i] == '-')
		{
			std::string	tmp = cleanedPoly.substr(start, i - start);
			if (tmp.find('X') != std::string::npos && tmp.find_first_of('X') != tmp.find_last_of('X'))
				return (this->code = 8);
			start = i + 1;
		}
	}
	std::string	tmp = cleanedPoly.substr(start, cleanedPoly.length() - start);
	if (tmp.find('X') != std::string::npos && tmp.find_first_of('X') != tmp.find_last_of('X'))
		return (this->code = 8);
	return (EXIT_SUCCESS);
}

int	Parsing::CheckValidity()
{
	if (_str.find("=") != std::string::npos)
	{
		if (_str.find_first_of("=") != _str.find_last_of("="))
			return (7);
		std::string	split = _str.substr(0, _str.find_first_of("="));
		if ((CheckPoly(_str.substr(0, _str.find_first_of("=")))
			|| CheckXDeg(_str.substr(0, _str.find_first_of("="))))
			|| (CheckPoly(_str.substr(_str.find_first_of("=") + 1))
			|| CheckXDeg(_str.substr(0, _str.find_first_of("=")))))
			return (this->code);

	}
	else if (CheckPoly(_str) || CheckXDeg(_str))
		return (this->code);
	return (EXIT_SUCCESS);
}