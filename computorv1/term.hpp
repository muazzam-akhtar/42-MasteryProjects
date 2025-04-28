#ifndef TERM_HPP
# define TERM_HPP

class Term
{
	public:

		double	coefficient;
		int		exponent;

		const double &getCoefficient() const;
		const int &getExponent() const;
};

#endif