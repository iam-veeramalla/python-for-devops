"""A slightly larger Day-01 Python example script."""


def greet(name: str) -> str:
    """Return a friendly greeting for a given name."""
    return f"Hello, {name}!"


def show_day_plan() -> None:
    """Print a simple plan for Day-01 learning."""
    topics = [
        "Print statements",
        "Variables",
        "Functions",
        "Lists",
        "Loops",
    ]

    print("Day-01 Learning Plan")
    print("-" * 22)
    for index, topic in enumerate(topics, start=1):
        print(f"{index}. {topic}")


if __name__ == "__main__":
    print(greet("Python Learner"))
    show_day_plan()
