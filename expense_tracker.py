from expense import Expense

import calendar
import datetime

def main():
    expense_file_path = "expenses.csv"
    budget = 1000

    # Get user input for expense
    expense = get_user_expense()

    # Write to a file
    save_expense_to_file(expense, expense_file_path)
    
    # Read from a file + summarize
    summarize_expenses(expense_file_path, budget)

    pass


def get_user_expense():
    expense_name = input("Enter the expense name: ")
    expense_amount = float(input("Enter the expense amount: $"))
    expense_categories = [
        "🥖 Food",
        "🏠 Home",
        "💼 Work",
        "🎮 Fun",
        "💰 Other",
    ]

    while True:
        print("Select the expense category: ")
        for i, category_name in enumerate(expense_categories):
            print(f"{i + 1}. {category_name}")
        
        value_range = f"[1 - {len(expense_categories)}]"
        
        selected_index = int(input(f"Enter the number of the category {value_range}: ")) - 1

        if selected_index in range(len(expense_categories)):
            selected_category = expense_categories[selected_index]
            new_expense = Expense(
                name=expense_name, amount=expense_amount,category=selected_category
            )
            return new_expense
        else:
            print("Invalid category, please try again")


def save_expense_to_file(expense: Expense, expense_file_path):
    with open(expense_file_path, "a") as f:
        f.write(f"{expense.name},{expense.amount},{expense.category}\n")


def summarize_expenses(expense_file_path, budget):
    print("🟢 Summarizing expenses")
    expenses: list[Expense] = []
    with open(expense_file_path, "r") as f:
        lines = f.readlines()
        for line in lines:
            expense_name, expense_amount, expense_category = line.strip().split(",")
            line_expense = Expense(
                name=expense_name,
                amount=float(expense_amount),
                category=expense_category
            )
            expenses.append(line_expense)

    amount_by_category = {}
    for expense in expenses:
        key = expense.category
        if key in amount_by_category:
            amount_by_category[key] += expense.amount
        else:
            amount_by_category[key] = expense.amount
    
    print("🟢 Expenses by category:")
    for key, amount in amount_by_category.items():
        print(f"  {key}: ${amount:.2f}")
    
    total_spent = sum([x.amount for x in expenses])
    print(f"💸 You've spent ${total_spent:.2f} this month")

    remaining_budget = budget - total_spent
    print(f"💰 Budget remaining: ${remaining_budget:.2f}")

    # Calculate remaining days in month
    now = datetime.datetime.now()

    # Get the number of days in the current month
    days_in_month = calendar.monthrange(now.year, now.month)[1]

    # Calculate remaining days in month
    remaining_days = days_in_month - now.day
    print(f"🔮 Days remaining in month: {remaining_days}")

    daily_budget = remaining_budget / remaining_days
    print(green(f"💰 Daily budget: ${daily_budget:.2f}"))
    
def green(text):
    return f"\033[92m{text}\033[0m"

if __name__ == "__main__":
    main()