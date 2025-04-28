#ifndef PARSING_HPP
# define PARSING_HPP

# include "computor.hpp"

class Parsing
{
	private:

		// Modified Variables
		
		std::string			_str;
		int					code;

		// Const Variables

		const std::string	allowedChars;
		const std::string	_digitVals;
		const std::string	_varVals;
		const std::string	_validChars;
		const std::string	_validOps;
		const std::string	_validDouble;

	public:

		// Constructors

		Parsing(const std::string &input);
		~Parsing();

		// Methods for Parsing
		int	CheckValidity();
		int	ValidatingOps(const std::string &, size_t *);
		int	ValidDouble(const std::string &);
		int	ValidOp(const std::string &str);
		int	ValidVar(const std::string &str);
		int	CheckPoly(const std::string &);
		int	CheckXDeg(const std::string &);
};

#endif