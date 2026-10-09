#include <vector>
#include <iostream>
#include <stdexcept>
#include <iomanip>
#include <complex>
#include <cstdlib>
#include <ctime>
#include <functional>

/*
 *   Structure of Vector
*/

template<typename K>
K   _abs(const K &k) { return (k < K(0) ? -k : k); }

template<typename K>
K   _sqrt(const K &k)
{
    if (k < K(0))
        throw std::runtime_error("Math error: sqrt of a negative number");
    if (k == K(0))
        return K(0);
    return static_cast<K>(std::pow(static_cast<double>(k), 0.5));
}

template<typename K>
K   _abs(const std::complex<K> &z)
{
    return _sqrt(z.real() * z.real() + z.imag() * z.imag());
}

template <typename K>
K conjugate(const K &x) { return x; }

template <typename K>
std::complex<K> conjugate(const std::complex<K> &z) { return std::conj(z); }

template<typename K>
struct Vector {
    std::vector<K>  data;

    Vector() {}
    Vector(std::initializer_list<K> vals) : data(vals) {}

    void    add(const Vector<K> &v)
    {
        for (size_t i = 0; i < data.size(); i++)
            data[i] += v.data[i];
    }

    void    sub(const Vector<K> &v)
    {
        for (size_t i = 0; i < data.size(); i++)
            data[i] -= v.data[i];
    }

    void    scl(const K & a)
    {
        for (size_t i = 0; i < data.size(); i++)
            data[i] *= a;
    }

    K dot(const Vector<K> &v) const
    {
        K result = K();
        for (size_t i = 0; i < data.size(); i++)
            result += conjugate(data[i]) * v.data[i];
        return result;
    }

    float   norm_1() const
    {
        float   result = 0.0f;
        for (size_t i = 0; i < data.size(); i++)
            result += static_cast<float>(_abs(data[i]));
        return result;
    }

    float   norm() const { return static_cast<float>(_sqrt(std::real(dot(*this)))); }

    float   norm_inf() const
    {
        float   result = 0.0f;
        for (size_t i = 0; i < data.size(); i++)
        {
            float   a = static_cast<float>(_abs(data[i]));
            if (result < a)
                result = a;
        }
        return result;
    }
};

/*
 *   Structure of Matrix
*/

template<typename K>
struct Matrix {
    std::vector<std::vector<K>> data;

    Matrix() {}
    Matrix(std::initializer_list<std::vector<K>> rows) : data(rows) {}

    void    add(const Matrix<K> &m)
    {
        for (size_t i = 0; i < data.size(); i++)
            for (size_t j = 0; j < data.size(); j++)
                data[i][j] += m.data[i][j];
    }

    void    sub(const Matrix<K> &m)
    {
        for (size_t i = 0; i < data.size(); i++)
            for (size_t j = 0; j < data.size(); j++)
                data[i][j] -= m.data[i][j];
    }

    void    scl(const K &a)
    {
        for (size_t i = 0; i < data.size(); i++)
            for (size_t j = 0; j < data.size(); j++)
                data[i][j] *= a;
    }

    Vector<K>   mul_vec(Vector<K> &vec)
    {
        Vector<K>   results;
        results.data.resize(data.size(), K());
        for (size_t i = 0; i < data.size(); i++)
            for (size_t j = 0; j < data.size(); j++)
                results.data[i] += data[i][j] * vec.data[j];
        return results;
    }

    Matrix<K>   mul_mat(const Matrix<K> &m) const
    {
        size_t m_rows = data.size();
        size_t m_cols = data[0].size();
        size_t p_cols = m.data[0].size();

        Matrix<K> result;
        result.data.resize(m_rows);
        for (size_t i = 0; i < m_rows; i++)
            result.data[i].resize(p_cols, K());

        for (size_t i = 0; i < m_rows; i++)
            for (size_t j = 0; j < p_cols; j++)
                for (size_t k = 0; k < m_cols; k++)
                    result.data[i][j] += data[i][k] * m.data[k][j];

        return result;
    }

    K   trace() const
    {
        K   results = 0.0;
        for (size_t i = 0; i < data.size(); i++)
            results += data[i][i];
        return results;
    }

    Matrix<K>   transpose() const
    {
        size_t  m_rows = data.size();
        size_t  m_cols = data[0].size();
        Matrix<K>   results;

        results.data.resize(m_cols);
        for (size_t i = 0; i < m_cols; i++)
            results.data[i].resize(m_rows, K());

        for (size_t i = 0; i < m_rows; i++)
            for (size_t j = 0; j < m_cols; j++)
                results.data[j][i] = data[i][j];
        return results;
    }

    Matrix<K>   row_echelon() const
    {
        Matrix<K> results;
        size_t m_rows = data.size();
        size_t m_cols = data[0].size();
        size_t pivot_row = 0;

        results.data.resize(m_rows);
        for (size_t i = 0; i < m_rows; i++)
            results.data[i].resize(m_cols, K());

        for (size_t i = 0; i < m_rows; i++)
            for (size_t j = 0; j < m_cols; j++)
                results.data[i][j] = data[i][j];

        for (size_t j = 0; j < m_cols && pivot_row < m_rows; j++)
        {
            size_t pivot = pivot_row;
            while (pivot < m_rows && results.data[pivot][j] == K())
                pivot++;

            if (pivot < m_rows)
            {
                if (pivot != pivot_row)
                    std::swap(results.data[pivot], results.data[pivot_row]);

                K div = results.data[pivot_row][j];
                for (size_t c = 0; c < m_cols; c++)
                    results.data[pivot_row][c] /= div;

                for (size_t i = 0; i < m_rows; i++)
                {
                    if (i != pivot_row)
                    {
                        K factor = results.data[i][j];
                        if (factor != K())
                        {
                            for (size_t c = 0; c < m_cols; c++)
                                results.data[i][c] -= factor * results.data[pivot_row][c];
                        }
                    }
                }
                pivot_row++;
            }
        }
        return results;
    }

    K   det_3(const Matrix<K> &m) const
    {
        K   c11 = m.data[0][0];
        K   c12 = m.data[0][1];
        K   c13 = m.data[0][2];
        K   c21 = m.data[1][0];
        K   c22 = m.data[1][1];
        K   c23 = m.data[1][2];
        K   c31 = m.data[2][0];
        K   c32 = m.data[2][1];
        K   c33 = m.data[2][2];

        K   m1 = (c11 * ((c22 * c33) - (c23 * c32)));
        K   m2 = (c12 * ((c21 * c33) - (c31 * c23)));
        K   m3 = (c13 * ((c21 * c32) - (c31 * c22)));
        return (m1 - m2 + m3);
    }

    K   det_4(const Matrix<K> &m) const
    {
        K   c11 = m.data[0][0];
        K   c12 = m.data[0][1];
        K   c13 = m.data[0][2];
        K   c14 = m.data[0][3];
        K   c21 = m.data[1][0];
        K   c22 = m.data[1][1];
        K   c23 = m.data[1][2];
        K   c24 = m.data[1][3];
        K   c31 = m.data[2][0];
        K   c32 = m.data[2][1];
        K   c33 = m.data[2][2];
        K   c34 = m.data[2][3];
        K   c41 = m.data[3][0];
        K   c42 = m.data[3][1];
        K   c43 = m.data[3][2];
        K   c44 = m.data[3][3];
        Matrix<K>   results = {
            {c22, c23, c24},
            {c32, c33, c34},
            {c42, c43, c44},
        };

        K   m1 = c11 * det_3(results);
        results = {
            {c21, c23, c24},
            {c31, c33, c34},
            {c41, c43, c44},
        };
        K   m2 = c12 * det_3(results);
        results = {
            {c21, c22, c24},
            {c31, c32, c34},
            {c41, c42, c44},
        };
        K   m3 = c13 * det_3(results);
        results = {
            {c21, c22, c23},
            {c31, c32, c33},
            {c41, c42, c43},
        };
        K   m4 = c14 * det_3(results);
        return (m1 - m2 + m3 - m4);
    }

    K   determinant() const
    {
        if (data.size() == 1)
            return data[0][0];
        else if (data.size() == 2)
            return ((data[0][0] * data[1][1]) - (data[1][0] * data[0][1]));
        else if (data.size() == 3)
            return det_3(*this);
        else if (data.size() == 4)
            return det_4(*this);
        return 0;
    }

    Matrix<K>   cofactors_2(const Matrix<K> &m) const
    {
        K   c11 = m.data[1][1];
        K   c12 = -m.data[1][0];
        K   c21 = -m.data[0][1];
        K   c22 = m.data[0][0];
        Matrix<K> res = {
            {c11, c12},
            {c21, c22}
        };
        return (res); 
    }

    Matrix<K>   cofactors_3(const Matrix<K> &m) const
    {
        K   c11 = m.data[0][0];
        K   c12 = m.data[0][1];
        K   c13 = m.data[0][2];
        K   c21 = m.data[1][0];
        K   c22 = m.data[1][1];
        K   c23 = m.data[1][2];
        K   c31 = m.data[2][0];
        K   c32 = m.data[2][1];
        K   c33 = m.data[2][2];

        K   m11 = (c22 * c33) - (c32 * c23);
        K   m12 = -((c21 * c33) - (c31 * c23));
        K   m13 = (c21 * c32) - (c31 * c22);
        K   m21 = -((c12 * c33) - (c32 * c13));
        K   m22 = (c11 * c33) - (c31 * c13);
        K   m23 = -((c11 * c32) - (c31 * c12));
        K   m31 = (c12 * c23) - (c22 * c13);
        K   m32 = -((c11 * c23) - (c21 * c13));
        K   m33 = (c11 * c22) - (c21 * c12);
        Matrix<K> res = {
            {m11, m12, m13},
            {m21, m22, m23},
            {m31, m32, m33}
        };
        return (res); 
    }

    Matrix<K>   cofactors_fun(const Matrix<K> &m) const
    {
        Matrix<K> results;
        size_t m_rows = m.data.size();
        size_t m_cols = m.data[0].size();

        results.data.resize(m_rows);
        for (size_t i = 0; i < m_rows; i++)
            results.data[i].resize(m_cols, K());
        for (size_t i = 0; i < m_rows; i++)
            for (size_t j = 0; j < m_cols; j++)
                results.data[i][j] = 1;
        if (m_rows == 2 && m_cols == 2)
            results = cofactors_2(*this);
        else if (m_rows == 3 && m_cols == 3)
            results = cofactors_3(*this);
        results = results.transpose();
        return results;
    }

    Matrix<K>   inverse() const
    {
        K   det = determinant();
        if (det == K(0))
            throw std::runtime_error("Math error: Division by 0");
        Matrix<K>   inv = cofactors_fun(*this);
        inv.scl(K(1) / det);
        return (inv);
    }

    int rank() const
    {
        Matrix<K>   form = this->row_echelon();
        int rank = 0;

        for (size_t i = 0; i < form.data.size(); i++)
        {
            for (size_t j = 0; j < form.data[i].size(); j++)
                if (form.data[i][j] != K(0))
                {
                    rank++;
                    break;
                }
        }
        return rank;
    }
};

/*
 *   Printing
*/

template<typename K>
std::ostream    &operator<<(std::ostream &os, const std::complex<K> &v)
{
    os << v.real() << (v.imag() < 0 ? " - " : " + ") << _abs(v.imag()) << "i";
    return os;
}

template<typename K>
std::ostream    &operator<<(std::ostream &os, const Vector<K> &v)
{
    os << "[";
    for (size_t i = 0; i < v.data.size(); i++)
    {
        if (i > 0)
            os << ", ";
        os << v.data[i];
    }
    os << "]";
    return os;
}

template<typename K>
std::ostream    &operator<<(std::ostream &os, const Vector<std::complex<K>> &v)
{
    os << "[";
    for (size_t i = 0; i < v.data.size(); i++)
    {
        if (i > 0)
            os << ", ";
        os << "(" << v.data[i].real() << (v.data[i].imag() < 0 ? " - " : " + ") << _abs(v.data[i].imag()) << "i)";
    }
    os << "]";
    return os;
}

/*
 *   Printing a Matrix
*/

template<typename K>
std::ostream    &operator<<(std::ostream &os, const Matrix<K> &m) {
    for (size_t i = 0; i < m.data.size(); i++)
    {
        const std::vector<K>    &row = m.data[i];
        for (size_t j = 0; j < row.size(); j++)
        {
            if (j > 0)
                os << ", ";
            os << row[j];
        }
        os << "\n";
    }
    return os;
}

template<typename K>
std::ostream    &operator<<(std::ostream &os, const Matrix<std::complex<K>> &m) {
    for (size_t i = 0; i < m.data.size(); i++)
    {
        const std::vector<std::complex<K>>    &row = m.data[i];
        for (size_t j = 0; j < row.size(); j++)
        {
            if (j > 0)
                os << ", ";
            os << "(" << row[j].real() << (row[j].imag() < 0 ? " - " : " + ") << _abs(row[j].imag()) << "i)";
        }
        os << "\n";
    }
    return os;
}

/*
 *   Linear Combination function
 *   V = ∑(λk * Xk)
*/

template<typename K>
Vector<K>   linear_combination(const std::vector<Vector<K>> &u, const std::vector<K> &coeffs)
{
    Vector<K>   results;

    results.data.resize(u[0].data.size(), K());
    for (size_t i = 0; i < u.size(); i++)
        for (size_t j = 0; j < u[i].data.size(); j++)
            results.data[j] += coeffs[i] * u[i].data[j];
    return (results);
}

/*
 *   Linear Interpolation
 *   V = (u, v, t)
 *   r = ((v - u) * t) + u
*/

template<typename K, typename T>
K   lerp(const K &u, const K &v, const T &t)
{
    return ((v - u) * t) + u;
}

template<typename K, typename T>
Vector<K>  lerp(const Vector<K> &u, const Vector<K> &v, const T &t)
{
    Vector<K>   result = u;
    Vector<K>   diff = v;

    diff.sub(u);
    diff.scl(t);
    result.add(diff);
    return result;
}

template<typename K, typename T>
Matrix<K>  lerp(const Matrix<K> &u, const Matrix<K> &v, const T &t)
{
    Matrix<K>   result = u;
    Matrix<K>   diff = v;

    diff.sub(u);
    diff.scl(t);
    result.add(diff);
    return result;
}

template <typename K>
float cos_from_dot(const K &z) { return static_cast<float>(z); }

template <typename K>
float cos_from_dot(const std::complex<K> &z) {
    return static_cast<float>(_abs(z));
}

template <typename K>
float angle_cos(const Vector<K> &u, const Vector<K> &v) {
    return cos_from_dot(u.dot(v)) / (u.norm() * v.norm());
}

template<typename K>
Vector<K>   cross_product(const Vector<K> &u, const Vector<K> &v)
{
    K   first_row = ((u.data[1] * v.data[2]) - (u.data[2] * v.data[1]));
    K   second_row = ((u.data[0] * v.data[2]) - (u.data[2] * v.data[0]));
    K   third_row = ((u.data[0] * v.data[1]) - (u.data[1] * v.data[0]));
    Vector<K>   results = {first_row, -second_row, third_row};
    
    return results;
}

Matrix<float>   projection(float fov, float ratio, float near, float far)
{
    float radians = fov * M_PI / 180.0f;
    float tanHalfFov = std::tan(radians / 2.0f);
    float xScale = 1.0f / (ratio * tanHalfFov);
    float yScale = 1.0f / tanHalfFov;

    Matrix<float> p = {
        {xScale, 0, 0, 0},
        {0, yScale, 0, 0},
        {0, 0, -(far + near) / (far - near), -2 * (near * far) / (far - near)},
        {0, 0, -1, 0}
    };
    return p;
}

double random_real(double lo = -10.0, double hi = 10.0) {
    double t = static_cast<double>(std::rand()) / static_cast<double>(RAND_MAX);
    return lo + t * (hi - lo);
}

std::complex<double> random_complex() {
    double  lo = -10.0;
    double  hi = 10.0;
    return std::complex<double>(random_real(lo, hi), random_real(lo, hi));
}

template <typename K, typename Gen>
Matrix<K> random_matrix(size_t rows, size_t cols, Gen gen) {
    Matrix<K> m;
    for (size_t i = 0; i < rows; ++i)
    {
        std::vector<K> row;
        for (size_t j = 0; j < cols; ++j)
            row.push_back(gen());
        m.data.push_back(row);
    }
    return m;
}
