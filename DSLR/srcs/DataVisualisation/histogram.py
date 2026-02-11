import sys
import csv
import matplotlib.pyplot as plt


def load_data(filename):
    """Load the dataset from CSV file"""
    data = []
    headers = []

    try:
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            headers = next(reader)
            for row in reader:
                data.append(row)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

    return data, headers


def get_numerical_features(headers):
    """Get indices of numerical features (subjects)"""
    # Skip Index, Hogwarts House, First Name, Last Name, Birthday, Best Hand
    numerical_start_idx = 6  # Starting from Arithmancy
    numerical_features = []

    for i in range(numerical_start_idx, len(headers)):
        numerical_features.append((i, headers[i]))

    return numerical_features


def parse_numerical_data(data, feature_idx):
    """Parse numerical data for a specific feature, handling missing values"""
    values_by_house = {
        'Gryffindor': [],
        'Slytherin': [],
        'Ravenclaw': [],
        'Hufflepuff': []
    }
    for row in data:
        house = row[1]
        if house in values_by_house:
            try:
                value = row[feature_idx]
                if value and value.strip():
                    values_by_house[house].append(float(value))
            except (ValueError, IndexError):
                continue

    return values_by_house


def calculate_homogeneity_score(values_by_house):
    """Calculate a homogeneity score based on coefficient of variation"""
    house_stats = {}

    for house, values in values_by_house.items():
        if len(values) > 0:
            mean_val = sum(values) / len(values)
            variance = sum((x - mean_val) ** 2 for x in values) / len(values)
            std_val = variance ** 0.5
            cv = std_val / mean_val if mean_val != 0 else float('inf')
            house_stats[house] = {'mean': mean_val, 'std': std_val,
                                  'cv': cv, 'count': len(values)}

    if len(house_stats) >= 4:
        cvs = [stats['cv'] for stats in house_stats.values()
               if stats['cv'] != float('inf')]
        if len(cvs) >= 4:
            mean_cv = sum(cvs) / len(cvs)
            cv_variance = sum((cv - mean_cv) ** 2 for cv in cvs) / len(cvs)
            return cv_variance, house_stats

    return float('inf'), house_stats


def create_histogram(data, headers):
    """Create histogram for all numerical features"""
    numerical_features = get_numerical_features(headers)

    if not numerical_features:
        print("No numerical features found.")
        return

    homogeneity_scores = []

    for feature_idx, feature_name in numerical_features:
        values_by_house = parse_numerical_data(data, feature_idx)
        score, stats = calculate_homogeneity_score(values_by_house)
        homogeneity_scores.append((score, feature_name,
                                  values_by_house, stats))

    homogeneity_scores.sort(key=lambda x: x[0])

    if homogeneity_scores:
        most_homogeneous = homogeneity_scores[0]
        print(f"\nMost homogeneous course: {most_homogeneous[1]}")
        print(f"Homogeneity score: {most_homogeneous[0]:.6f}")
        print("\nStatistics by house:")
        for house, stats in most_homogeneous[3].items():
            printMean = f'Mean={stats["mean"]:.2f}'
            printStd = f'Std={stats["std"]:.2f}'
            printCV = f'CV={stats["cv"]:.4f}'
            printCount = f'Count={stats["count"]}'
            print(f"{house}: {printMean}, {printStd}, {printCV}, {printCount}")

    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('Histograms of Most Homogeneous Courses by House',
                 fontsize=16)

    house_colors = {
        'Gryffindor': 'red', 'Slytherin': 'green', 'Ravenclaw': 'blue',
        'Hufflepuff': 'yellow'}

    for i, (score, feature_name, values_by_house,
            stats) in enumerate(homogeneity_scores[:4]):
        row = i // 2
        col = i % 2
        ax = axes[row, col]

        for house, values in values_by_house.items():
            if values:
                ax.hist(values, bins=20, alpha=0.6, label=house,
                        color=house_colors[house])

        ax.set_title(f'{feature_name}\n(Homogeneity Score: {score:.6f})')
        ax.set_xlabel('Score')
        ax.set_ylabel('Frequency')
        ax.legend()
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()
    print("\nTop 5 most homogeneous courses:")
    for i, (score, feature_name, _, _) in enumerate(homogeneity_scores[:5]):
        print(f"{i+1}. {feature_name} (score: {score:.6f})")


def main():
    if len(sys.argv) != 2:
        print("Usage: python histogram.py <dataset.csv>")
        sys.exit(1)
    filename = sys.argv[1]
    data, headers = load_data(filename)
    if not data or headers[1] != 'Hogwarts House':
        print("No data found in the file.")
        sys.exit(1)

    print(f"Loaded {len(data)} records with {len(headers)} features.")
    create_histogram(data, headers)


if __name__ == "__main__":
    main()
