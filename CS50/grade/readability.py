
def main():
    text = input("Text: ")

    letters = sum(1 for c in text if c.isalpha())
    words = text.count(" ") + 1
    sentences = sum(1 for c in text if c in ".!?")

    L = (letters / words) * 100
    S = (sentences / words) * 100

    index = round(0.0588 * L - 0.296 * S - 15.8)

    if index < 1:
        print("Before Grade 1")
    elif index >= 16:
        print("Grade 16+")
    else:
        print(f"Grade {index}")


if __name__ == "__main__":
    main()