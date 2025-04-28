#include "computor.hpp"
#include "parsing.hpp"

static std::string removeExtraSpaces(const std::string& str)
{
	std::string result = str;

	for (size_t i = 0; i < result.length(); i++)
	{
		if (std::isspace(result[i]))
		{
			result.erase(i, 1);
			i--;
		}
		if (result[i] == 'x')
			result[i] = 'X';
	}
	return result;
}

static int	printError(int code)
{
	std::map<int, std::string>	_list;

	_list.insert(std::pair<int, std::string>(2, "Invalid Characters in Input!\n"));
	_list.insert(std::pair<int, std::string>(3, "Operator spotted at the wrong spot!\n"));
	_list.insert(std::pair<int, std::string>(4, "Format not valid!\n"));
	_list.insert(std::pair<int, std::string>(5, "Empty String!\n"));
	_list.insert(std::pair<int, std::string>(6, "Exponential Power requires only one digit!\n"));
	_list.insert(std::pair<int, std::string>(7, "Equal sign should be only one in the string!\n"));
	_list.insert(std::pair<int, std::string>(8, "Multiplication of X^exp with X^exp not allowed!\n"));

	std::cerr << _list[code];
	return (EXIT_FAILURE);
}

int main(int argc, char **argv)
{
	int	code = 0;

	if (argc == 2)
	{
		std::string	input = removeExtraSpaces(argv[1]);
		if (input.length() == 0)
		{
			std::cerr << "\033[" << RED;
			std::cerr << "m" << input << "Error in Input: ";
			return (printError(5));
		}
		Parsing	parse(input);
		code = parse.CheckValidity();
		if (code > 0)
		{
			std::cerr << "\033[" << RED;
			std::cerr << "m" << "Error in Input: "; 
			return (printError(code));
		}
		Computor	data(input);
		return (EXIT_SUCCESS);
	}
	else
	{
		std::cerr << "\033[" << RED;
		std::cerr << "m" << "Invalid Number of Arguments!" << std::endl;
	}
	return (EXIT_FAILURE);
}