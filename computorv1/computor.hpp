#ifndef COMPUTOR_HPP
# define COMPUTOR_HPP

# define RED 31;
# define YELLOW 33;
# define BLUE 34;
# define WHITE 37;
# define GREEN 32;

# include <iostream>
# include <algorithm>
# include <iomanip>
# include <string>
# include <sstream>
# include <vector>
# include <cstdlib>
# include <cctype>
# include <map>
# include <cmath>
# include "term.hpp"

class Computor
{
	private:

		// Variables

		std::vector<Term>		_data;
		std::vector<Term>		_leftTerm;
		std::vector<Term>		_rightTerm;
		std::string				leftPoly;
		std::string				RightPoly;
		int						_deg;

	public:
		
		// Constructors

		Computor(void);
		Computor(const std::string &input);
		Computor(const Computor &other);
		Computor &operator=(const Computor &other);
		~Computor();

		// Getters

		const std::vector<Term>	&getLeftTerm(void) const;
		const std::vector<Term>	&getRightTerm(void) const;
		const std::vector<Term>	&getData(void) const;
		Term					getTerm(const std::vector<Term> &, int);
		const int				&getDegree(void) const;

		// Methods for Parsing

		std::vector<Term>		parsePolynomial(const std::string &);
		std::vector<Term>		simplifyEq(const std::vector<Term> &, const std::vector<Term> &);
		Term					parseTerm(const std::string &);
		double					getGCD(double, double);
		int						reduce(void);
		double					findDisc(double, double, double);
		void					solveEq(void);
		void					printSimplify(const std::vector<Term> &, const std::vector<Term> &);
		void					printGCD(double);
		void					displayPolynomial(const std::vector<Term> &);
		void					solve(void);
		void					solveConstants();
		void					solveLinearEqs();
		void					solveQuadraticEqs();
		std::string				getFractionalPart(double a, double b);
		std::string				getFractionSqRoot(double a, double b, double sq);
		std::string				doubleToStr(double);
		std::string				format_clean_double(double value);
		void					printComplexFraction(double, double, double);
		void					printComplexDecimal(double, double, double);
		void					printRealFraction(double, double, double);
		void					printRealDecimal(double, double, double);
		std::string				setColor(int);
		int						getMaxDeg();
};


#endif