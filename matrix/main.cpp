#include "matrix.hpp"

typedef std::complex<double>    cd;

/* ------------------------------------------------------------------ */
/*  Printing helpers                                                   */
/* ------------------------------------------------------------------ */

static void section(const std::string &title)
{
    std::cout << "\n==================================================\n"
              << "  " << title << "\n"
              << "==================================================\n";
}

// Runs one test; a thrown exception is reported instead of aborting the run.
static void test(const std::string &name, const std::function<void()> &fn)
{
    std::cout << "\n--- " << name << " ---\n";
    try
    {
        fn();
    }
    catch (const std::exception &e)
    {
        std::cout << "[exception] " << e.what() << "\n";
    }
    catch (...)
    {
        std::cout << "[exception] unknown error\n";
    }
}

// Prints "label:" then the value on the following line(s), so matrices align.
template <typename T>
static void show(const std::string &label, const T &value)
{
    std::cout << label << ":\n" << value << "\n";
}

// Prints "label: value" on a single line (scalars).
template <typename T>
static void line(const std::string &label, const T &value)
{
    std::cout << label << ": " << value << "\n";
}

/* ------------------------------------------------------------------ */
/*  Real (float) tests                                                 */
/* ------------------------------------------------------------------ */

static void float_vector_basics()
{
    section("FLOAT | Vector: add / sub / scl");

    test("add", []() {
        Vector<float> u = {2.0f, 4.0f};
        Vector<float> v = {13.0f, 24.0f};
        show("u", u);
        show("v", v);
        u.add(v);
        show("u + v", u);
    });
    test("sub", []() {
        Vector<float> u = {2.0f, 4.0f};
        Vector<float> v = {13.0f, 24.0f};
        show("u", u);
        show("v", v);
        u.sub(v);
        show("u - v", u);
    });
    test("scl", []() {
        Vector<float> u = {2.0f, 4.0f};
        show("u", u);
        u.scl(2.5f);
        show("u * 2.5", u);
    });
}

static void float_linear_combination()
{
    section("FLOAT | Linear combination");

    test("3 vectors, 3 coefficients", []() {
        std::vector<Vector<float> > u;
        u.push_back({1.f, 2.5f, 0.f});
        u.push_back({0.f, 1.f, 0.f});
        u.push_back({0.f, 0.f, 1.f});

        std::vector<float> coefs;
        coefs.push_back(10.f);
        coefs.push_back(-2.f);
        coefs.push_back(0.5f);

        for (size_t i = 0; i < u.size(); ++i)
            std::cout << "u[" << i << "] * " << coefs[i] << " : " << u[i] << "\n";
        show("result", linear_combination(u, coefs));
    });
}

static void float_lerp()
{
    section("FLOAT | Linear interpolation (lerp)");

    test("scalar lerp(0, 100, 0.75)", []() {
        line("lerp", lerp(0, 100, 0.75));
    });
    test("vector lerp(u, v, 0.5)", []() {
        Vector<float> u = {2.0f, 4.0f};
        Vector<float> v = {13.0f, 24.0f};
        show("u", u);
        show("v", v);
        show("lerp(u, v, 0.5)", lerp(u, v, 0.5));
    });
    test("matrix lerp(n, m, 0.5)", []() {
        Matrix<float> m = {
            {10.0, 21.0, 40.0},
            {5.0, 14.0, 20.0},
            {3.0, 18.0, 25.0}
        };
        Matrix<float> n = {
            {9.0, 20.0, 39.0},
            {4.0, 13.0, 19.0},
            {2.0, 17.0, 24.0}
        };
        show("n", n);
        show("m", m);
        show("lerp(n, m, 0.5)", lerp(n, m, 0.5));
    });
}

static void float_dot()
{
    section("FLOAT | Dot product");

    test("dot", []() {
        Vector<float> u = {2.0f, 4.0f};
        Vector<float> v = {13.0f, 24.0f};
        show("u", u);
        show("v", v);
        line("u . v", u.dot(v));
    });
}

static void float_norms()
{
    section("FLOAT | Norms");

    test("norm_1 / norm / norm_inf", []() {
        Vector<float> u = {-2.0f, 4.0f};
        Vector<float> v = {13.0f, -24.0f};
        show("u", u);
        show("v", v);
        std::cout << "          u        v\n";
        std::cout << "norm_1:   " << u.norm_1()   << "   " << v.norm_1()   << "\n";
        std::cout << "norm:     " << u.norm()     << "   " << v.norm()     << "\n";
        std::cout << "norm_inf: " << u.norm_inf() << "   " << v.norm_inf() << "\n";
    });
}

static void float_angle()
{
    section("FLOAT | Cosine of angle");

    test("angle_cos", []() {
        Vector<float> u = {-2.0f, 4.0f};
        Vector<float> v = {13.0f, -24.0f};
        show("u", u);
        show("v", v);
        line("cos(u, v)", angle_cos(u, v));
    });
}

static void float_cross()
{
    section("FLOAT | Cross product");

    test("cross_product", []() {
        Vector<float> u = {-2.0f, 4.0f, 6.0f};
        Vector<float> v = {13.0f, -24.0f, 5.0f};
        show("u", u);
        show("v", v);
        show("u x v", cross_product(u, v));
    });
}

static void float_matrix_mul()
{
    section("FLOAT | Matrix multiplication");

    Matrix<float> m = {
        {10.0, 21.0, 40.0},
        {5.0, 14.0, 20.0},
        {3.0, 18.0, 25.0}
    };
    Matrix<float> n = {
        {20.0, 22.0, 39.0},
        {6.0, 15.0, 21.0},
        {4.0, 17.0, 24.0}
    };
    Vector<float> u = {-2.0, 4.0, 6.0};

    test("matrix x vector", [&]() {
        show("m", m);
        show("u", u);
        show("m * u", m.mul_vec(u));
    });
    test("matrix x matrix", [&]() {
        show("m", m);
        show("n", n);
        show("m * n", m.mul_mat(n));
    });
}

static void float_trace_transpose()
{
    section("FLOAT | Trace & Transpose");

    Matrix<float> m = {
        {10.0, 21.0, 40.0},
        {5.0, 14.0, 20.0},
        {3.0, 18.0, 25.0}
    };

    test("trace", [&]() {
        show("m", m);
        line("trace(m)", m.trace());
    });
    test("transpose", [&]() {
        show("m", m);
        show("m^T", m.transpose());
    });
}

static void float_row_echelon()
{
    section("FLOAT | Row echelon form");

    test("3x3", []() {
        Matrix<float> m = {
            {10.0, 21.0, 40.0},
            {5.0, 14.0, 20.0},
            {3.0, 18.0, 25.0}
        };
        show("m", m);
        show("row_echelon(m)", m.row_echelon());
    });
    test("2x3 (non-square)", []() {
        Matrix<float> m = {
            {8, 1, 7},
            {6, 3, 6}
        };
        show("m", m);
        show("row_echelon(m)", m.row_echelon());
    });
    test("2x2", []() {
        Matrix<float> m = {
            {8, 1},
            {6, 3}
        };
        show("m", m);
        show("row_echelon(m)", m.row_echelon());
    });
}

static void float_determinant()
{
    section("FLOAT | Determinant");

    test("4x4", []() {
        Matrix<float> m = {
            {7, 6, 2, 3},
            {6, 8, 8, 9},
            {9, 2, 7, 0},
            {4, 0, 1, 3}
        };
        show("m", m);
        line("det(m)", m.determinant());
    });
}

static void float_inverse()
{
    section("FLOAT | Inverse");

    test("3x3", []() {
        Matrix<float> m = {
            {7, 6, 2},
            {6, 8, 8},
            {9, 2, 7}
        };
        show("m", m);
        show("inverse(m)", m.inverse());
    });
}

static void float_rank()
{
    section("FLOAT | Rank");

    test("3x3 (rank-deficient)", []() {
        Matrix<float> m = {
            {1, 0, 0},
            {6, 0, 0},
            {9, 0, 1}
        };
        show("m", m);
        line("rank(m)", m.rank());
    });
}

static void float_projection()
{
    section("FLOAT | Projection matrix");

    test("fov 60, ratio 1, near 0.1, far 100", []() {
        const float fov = 60.0f, ratio = 1080.0f / 1080.0f;
        const float near = 0.1f, far = 100.0f;

        line("fov", fov);
        line("ratio", ratio);
        line("near", near);
        line("far", far);
        show("projection", projection(fov, ratio, near, far));
    });
}

/* ------------------------------------------------------------------ */
/*  Complex tests                                                      */
/* ------------------------------------------------------------------ */

static void complex_vector_basics()
{
    section("COMPLEX | Vector: add / sub / scl");

    Vector<cd> base = {cd(3.0, 4.0), cd(5.0, 3.0)};
    Vector<cd> other = {cd(5.0, 3.0), cd(3.0, 4.0)};
    cd scalar(5.0, 7.0);

    test("add", [&]() {
        Vector<cd> v = base;
        show("v", v);
        show("w", other);
        v.add(other);
        show("v + w", v);
    });
    test("sub", [&]() {
        Vector<cd> v = base;
        show("v", v);
        show("w", other);
        v.sub(other);
        show("v - w", v);
    });
    test("scl", [&]() {
        Vector<cd> v = base;
        show("v", v);
        line("scalar", scalar);
        v.scl(scalar);
        show("v * scalar", v);
    });
}

static void complex_linear_combination()
{
    section("COMPLEX | Linear combination");

    test("2 vectors, 2 coefficients", []() {
        Vector<cd> v1 = {cd(3.0, 4.0), cd(5.0, 3.0), cd(7.0, 6.0)};
        Vector<cd> v2 = {cd(2.0, 3.0), cd(4.0, 5.0), cd(6.0, 7.0)};

        std::vector<Vector<cd> > u;
        u.push_back(v1);
        u.push_back(v2);

        std::vector<cd> coefs;
        coefs.push_back(cd(5.0, 3.0));
        coefs.push_back(cd(3.0, 4.0));

        for (size_t i = 0; i < u.size(); ++i)
            std::cout << "u[" << i << "] * " << coefs[i] << " : " << u[i] << "\n";
        show("result", linear_combination(u, coefs));
    });
}

static void complex_lerp()
{
    section("COMPLEX | Linear interpolation (lerp)");

    test("vector lerp(v, w, 0.5)", []() {
        Vector<cd> v = {cd(3.0, 4.0), cd(5.0, 3.0), cd(7.0, 6.0)};
        Vector<cd> w = {cd(5.0, 3.0), cd(3.0, 4.0), cd(5.0, 7.0)};
        show("v", v);
        show("w", w);
        show("lerp(v, w, 0.5)", lerp(v, w, 0.5));
    });
}

static void complex_dot()
{
    section("COMPLEX | Dot product");

    test("dot", []() {
        Vector<cd> v = {cd(3.0, 4.0), cd(5.0, 3.0)};
        Vector<cd> w = {cd(5.0, 3.0), cd(3.0, 4.0)};
        show("v", v);
        show("w", w);
        line("v . w", v.dot(w));
    });
}

static void complex_norms()
{
    section("COMPLEX | Norms");

    test("norm_1 / norm / norm_inf", []() {
        Vector<cd> v = {cd(3.0, 4.0), cd(5.0, 3.0)};
        show("v", v);
        line("norm_1", v.norm_1());
        line("norm", v.norm());
        line("norm_inf", v.norm_inf());
    });
}

static void complex_angle()
{
    section("COMPLEX | Cosine of angle");

    test("angle_cos", []() {
        Vector<cd> v = {cd(3.0, 4.0), cd(5.0, 3.0), cd(8.0, 6.0)};
        Vector<cd> u = {cd(1.0, 0.0), cd(9.0, 10.0), cd(3.0, 7.0)};
        show("v", v);
        show("u", u);
        line("cos(v, u)", angle_cos(v, u));
    });
}

static void complex_cross()
{
    section("COMPLEX | Cross product");

    test("cross_product", []() {
        Vector<cd> v = {cd(3.0, 4.0), cd(5.0, 3.0), cd(8.0, 6.0)};
        Vector<cd> u = {cd(1.0, 0.0), cd(9.0, 10.0), cd(3.0, 7.0)};
        show("v", v);
        show("u", u);
        show("v x u", cross_product(v, u));
    });
}

static void complex_matrix_mul()
{
    section("COMPLEX | Matrix multiplication (random matrices)");

    test("matrix x vector, matrix x matrix", []() {
        Vector<cd> v = {cd(3.0, 4.0), cd(5.0, 3.0), cd(8.0, 6.0)};
        Matrix<cd> m = random_matrix<cd>(3, 3, random_complex);
        Matrix<cd> n = random_matrix<cd>(3, 3, random_complex);

        show("m", m);
        show("n", n);
        show("v", v);
        show("m * v", m.mul_vec(v));
        show("m * n", m.mul_mat(n));
    });
}

static void complex_trace_transpose()
{
    section("COMPLEX | Trace & Transpose (random matrices)");

    test("trace", []() {
        Matrix<cd> m = random_matrix<cd>(3, 3, random_complex);
        show("m", m);
        line("trace(m)", m.trace());
    });
    test("transpose", []() {
        Matrix<cd> m = random_matrix<cd>(3, 3, random_complex);
        show("m", m);
        show("m^T", m.transpose());
    });
}

static void complex_row_echelon()
{
    section("COMPLEX | Row echelon form (random matrix)");

    test("3x3", []() {
        Matrix<cd> m = random_matrix<cd>(3, 3, random_complex);
        show("m", m);
        show("row_echelon(m)", m.row_echelon());
    });
}

static void complex_determinant()
{
    section("COMPLEX | Determinant (random matrix)");

    test("3x3", []() {
        Matrix<cd> m = random_matrix<cd>(3, 3, random_complex);
        show("m", m);
        line("det(m)", m.determinant());
    });
}

static void complex_inverse()
{
    section("COMPLEX | Inverse (random matrix)");

    test("3x3", []() {
        Matrix<cd> m = random_matrix<cd>(3, 3, random_complex);
        show("m", m);
        show("inverse(m)", m.inverse());
    });
}

static void complex_rank()
{
    section("COMPLEX | Rank (random matrix)");

    test("3x3", []() {
        Matrix<cd> m = random_matrix<cd>(3, 3, random_complex);
        show("m", m);
        line("rank(m)", m.rank());
    });
}

/* ------------------------------------------------------------------ */

int main()
{
    // ---- Real numbers (float) ----
    float_vector_basics();
    float_linear_combination();
    float_lerp();
    float_dot();
    float_norms();
    float_angle();
    float_cross();
    float_matrix_mul();
    float_trace_transpose();
    float_row_echelon();
    float_determinant();
    float_inverse();
    float_rank();
    float_projection();

    // ---- Complex numbers (std::complex<double>) ----
    complex_vector_basics();
    complex_linear_combination();
    complex_lerp();
    complex_dot();
    complex_norms();
    complex_angle();
    complex_cross();
    complex_matrix_mul();
    complex_trace_transpose();
    complex_row_echelon();
    complex_determinant();
    complex_inverse();
    complex_rank();

    std::cout << std::endl;
    return 0;
}