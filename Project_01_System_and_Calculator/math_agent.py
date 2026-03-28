import math

class MathAgent:
    def __init__(self):
        self.operations = {
            "add": lambda a, b: a + b,
            "sub": lambda a, b: a - b,
            "mul": lambda a, b: a * b,
            "div": lambda a, b: a / b if b != 0 else "Cannot divide by zero",
            "pow": lambda a, b: math.pow(a, b),

            "sqrt": lambda a: math.sqrt(a),
            "log": lambda a: math.log(a),
            "log10": lambda a: math.log10(a),

            "sin": lambda a: math.sin(math.radians(a)),
            "cos": lambda a: math.cos(math.radians(a)),
            "tan": lambda a: math.tan(math.radians(a)),

            "fact": lambda a: math.factorial(int(a))
        }

    def handle(self, query: str):
        try:
            parts = query.lower().split()

            if len(parts) == 3:  # binary operations
                op, a, b = parts
                a, b = float(a), float(b)

                if op in self.operations:
                    return self.operations[op](a, b)

            elif len(parts) == 2:  # unary operations
                op, a = parts
                a = float(a)

                if op in self.operations:
                    return self.operations[op](a)

            return "Invalid query format"

        except Exception as e:
            return f"Error: {str(e)}"


# -------- Run Agent --------
# if __name__ == "__main__":
#     agent = MathAgent()

#     print("🤖 Math Agent Ready (type 'exit' to quit)")
#     print("Examples: add 5 3 | sqrt 25 | sin 30")

#     while True:
#         user_input = input(">> ")

#         if user_input.lower() == "exit":
#             break

#         result = agent.handle(user_input)
#         print("Result:", result)