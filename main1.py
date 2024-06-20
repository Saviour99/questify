from generator import Objective

def main():
    content = """
    Entrepreneurship is the process of creating, developing, and managing a new business venture to generate profit, often by addressing a market need or problem.
    Entrepreneurs are innovative individuals who harness their skills to establish startups that cater to unmet needs in the market.
    Businessmen and investors play crucial roles in funding and scaling these ventures, ensuring their sustainability and growth.
    """

    objective = Objective(content, noOfQues=10)
    mcq_data = objective.generate_test()

    print(mcq_data)
    for mcq in mcq_data:
        print(f"Question: {mcq['Question']}")
        print(f"Answer: {mcq['Answer']}")
        print(f"Options: {mcq['Options']}")
        print()

if __name__ == "__main__":
    main()
