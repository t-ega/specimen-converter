def convert_size(measured_size, magnification, target_unit):
    # Convert measured size to actual size
    actual_size_mm = measured_size / magnification

    # Conversion factors from mm to other units
    conversion_factors = {
        "mm": 1,
        "µm": 1000,       # micrometers
        "um": 1000,       # micrometers (alternative spelling)
        "nm": 1_000_000,  # nanometers
        "cm": 0.1,
        "m": 0.001
    }

    if target_unit not in conversion_factors:
        print(f"Unsupported unit: {target_unit}")
        return None

    converted_size = actual_size_mm * conversion_factors[target_unit]
    return converted_size


def main():
    print("=== Specimen Size Converter ===")

    try:
        measured_size = float(input("Enter the measured size (in mm): "))
        magnification = float(input("Enter the magnification used: "))
        target_unit = input("Enter the unit to convert to (mm, µm, nm, cm, m): ").strip()

        result = convert_size(measured_size, magnification, target_unit)
        if result is not None:
            print(f"\nActual size of specimen: {result:.4f} {target_unit}")
    except ValueError:
        print("Invalid input. Please enter numeric values for size and magnification.")

if __name__ == "__main__":
    main()
