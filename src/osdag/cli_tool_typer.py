import typer

def greet(name: str = "World"):
    print(f"Hello, {name}!")

if __name__ == "__main__":
    typer.run(greet)