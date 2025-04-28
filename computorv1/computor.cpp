#include "computor.hpp"

Computor::Computor() {};

Computor::~Computor() {};

Computor::Computor(const Computor &other) { *this = other; }

Computor	&Computor::operator=(const Computor &other)
{
	if (this != &other)
	{
		this->_data = other._data;
		this->_leftTerm = other._leftTerm;
		this->_rightTerm = other._rightTerm;
	}
	return (*this);
}

Computor::Computor(const std::string &input)
{
	size_t eqPos = input.find("=");
	if (eqPos == std::string::npos)
	{
		this->leftPoly = input;
		this->_leftTerm = parsePolynomial(leftPoly);
	}
	else
	{
		this->leftPoly = input.substr(0, eqPos);
		this->RightPoly = input.substr(eqPos + 1);
		this->_leftTerm = parsePolynomial(leftPoly);
		this->_rightTerm = parsePolynomial(RightPoly);
	}
	this->_data = simplifyEq(this->_leftTerm, this->_rightTerm);
	if (reduce())
		return ;
	solve();
}

int	Computor::getMaxDeg()
{
	int	pow = 0;
	for (size_t	i = 0; i < this->_leftTerm.size(); i++)
	{
		if (this->_leftTerm[i].exponent > pow)
			pow = this->_leftTerm[i].exponent;
	}
	return pow;
}

const std::vector<Term>	&Computor::getData() const { return (this->_data); }

const std::vector<Term>	&Computor::getLeftTerm() const { return (this->_leftTerm); }

const std::vector<Term>	&Computor::getRightTerm() const { return (this->_rightTerm); }