#!/usr/bin/env python3
"""
A simple BMI (Body‑Mass Index) calculator.

This script prompts the user to enter their weight (in kilograms) and height
either in metres or centimetres. It calculates the BMI using the formula

    BMI = weight / (height ** 2)

and classifies the result into categories such as underweight, normal,
overweight or obese. The program loops until the user chooses to exit.

Usage:
    Run the script directly. It will prompt for input. To exit, type
    ``q`` when asked for a new calculation.
"""

import sys


def calculate_bmi(weight: float, height: float) -> float:
    """Calculate the Body Mass Index (BMI).

    Args:
        weight: Weight in kilograms.
        height: Height in metres.

    Returns:
        The BMI as a floating point number.
    """
    if height <= 0:
        raise ValueError("Height must be greater than zero.")
    return weight / (height ** 2)


def classify_bmi(bmi: float) -> str:
    """Return a human readable classification for a BMI value.

    Args:
        bmi: The computed BMI.

    Returns:
        A string describing the weight category.
    """
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 24.9:
        return "Normal weight"
    elif 25 <= bmi < 29.9:
        return "Overweight"
    else:
        return "Obese"


def prompt_float(prompt: str) -> float:
    """Prompt the user for a floating point number.

    Re-prompts until a valid number is entered.

    Args:
        prompt: The prompt string to display.

    Returns:
        The numeric value entered by the user.
    """
    while True:
        user_input = input(prompt).strip()
        try:
            value = float(user_input)
            return value
        except ValueError:
            print("Invalid input. Please enter a numeric value.")


def get_height() -> float:
    """Ask the user for their height and normalize to metres.

    The user can enter height in metres (e.g. 1.75) or centimetres (e.g. 175).

    Returns:
        Height in metres.
    """
    while True:
        height_input = input(
            "Enter your height (in metres or centimetres, e.g. 1.75 or 175): "
        ).strip()
        try:
            height_value = float(height_input)
            # If the user entered a value greater than 3, assume centimetres
            if height_value > 3:
                height_value /= 100
            return height_value
        except ValueError:
            print("Invalid input. Please enter a numeric value.")


def main() -> None:
    """Entry point of the BMI calculator."""
    print("BMI Calculator\n==================")
    while True:
        response = input(
            "\nPress Enter to calculate a new BMI or type 'q' to quit: "
        ).strip().lower()
        if response == 'q':
            print("Goodbye!")
            break

        # Collect input values
        weight = prompt_float("Enter your weight in kilograms: ")
        height = get_height()
        try:
            bmi = calculate_bmi(weight, height)
        except ValueError as exc:
            print(f"Error: {exc}")
            continue

        category = classify_bmi(bmi)
        print(f"\nYour BMI is: {bmi:.2f}")
        print(f"Weight category: {category}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # Gracefully handle Ctrl+C
        print("\nInterrupted. Exiting...")
        sys.exit(0)
