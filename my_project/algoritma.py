import time
# Kelas dan Fungsi Utilitas
class Food:
    def __init__(self, name, price, calories, protein, fat, cholesterol):
        self.name = name
        self.price = price
        self.calories = calories
        self.protein = protein
        self.fat = fat
        self.cholesterol = cholesterol
        self.score = self.calculate_score()

    def calculate_score(self):
        return (self.calories / 100) + (self.protein * 2) - self.fat - (self.price / 10000)

def filter_food_by_rules(foods):
    filtered_foods = []
    for food in foods:
        filtered_foods.append((food.name, food.score, food.calories, food.cholesterol))
    return filtered_foods

# Algoritma Greedy
def greedy_algorithm(foods, total_activity_calories):
    max_calories = 1200 + total_activity_calories
    total_calories = 0
    high_cholesterol_count = 0
    medium_cholesterol_count = 0
    selected_foods = []
    total_steps = 0

    foods.sort(key=lambda x: x[1], reverse=True)

    for food in foods:
        total_steps += 1
        if total_calories + food[2] <= max_calories:
            if food[3] == 'tinggi' and high_cholesterol_count < 1:
                if total_activity_calories > 0:
                    total_activity_calories -= 100
                    if total_activity_calories <= 0:
                        break
                else:
                    break
                selected_foods.append(food)
                total_calories += food[2]
                high_cholesterol_count += 1
            elif food[3] == 'sedang' and medium_cholesterol_count < 2:
                selected_foods.append(food)
                total_calories += food[2]
                medium_cholesterol_count += 1
            elif food[3] == 'rendah':
                selected_foods.append(food)
                total_calories += food[2]

    return selected_foods, total_steps

# Algoritma Backtracking
def backtrack_algorithm(foods, max_calories, total_activity_calories, index=0, current_calories=0, high_chol=0, med_chol=0, current_solution=None, best_solution=None, total_steps=0):
    total_steps += 1

    if current_solution is None:
        current_solution = []
    if best_solution is None:
        best_solution = []

    if index == len(foods):
        if sum(food[1] for food in current_solution) > sum(food[1] for food in best_solution):
            return current_solution.copy(), total_steps
        return best_solution, total_steps

    food = foods[index]
    food_name, food_score, food_calories, food_cholesterol = food

    if current_calories + food_calories <= max_calories:
        add_food = False
        if food_cholesterol == 'tinggi' and high_chol < 1:
            if total_activity_calories > 0:
                total_activity_calories -= 100
                if total_activity_calories > 0:
                    add_food = True
        elif food_cholesterol == 'sedang' and med_chol < 2:
            add_food = True
        elif food_cholesterol == 'rendah':
            add_food = True

        if add_food:
            current_solution.append(food)
            new_high_chol = high_chol + 1 if food_cholesterol == 'tinggi' else high_chol
            new_med_chol = med_chol + 1 if food_cholesterol == 'sedang' else med_chol
            solution_with, steps = backtrack_algorithm(
                foods, max_calories, total_activity_calories, index + 1,
                current_calories + food_calories, new_high_chol, new_med_chol,
                current_solution, best_solution, total_steps
            )
            total_steps = steps
            if sum(food[1] for food in solution_with) > sum(food[1] for food in best_solution):
                best_solution = solution_with
            current_solution.pop()

    solution_without, steps = backtrack_algorithm(
        foods, max_calories, total_activity_calories, index + 1,
        current_calories, high_chol, med_chol,
        current_solution, best_solution, total_steps
    )
    total_steps = steps

    if sum(food[1] for food in solution_without) > sum(food[1] for food in best_solution):
        best_solution = solution_without

    return best_solution, total_steps

# Data dan Inisialisasi
foods = [
    # Food("Nasi Goreng", 25000, 300, 10, 15, "rendah"),
    # Food("Ayam Bakar", 40000, 450, 20, 8, "sedang"),
    # Food("Sate Kambing", 50000, 500, 25, 20, "tinggi"),
    # Food("Salad Buah", 30000, 150, 5, 2, "rendah"),
    # Food("Steak", 35000, 600, 30, 12, "sedang"),
    # Food("Bakso", 20000, 400, 15, 10, "Tinggi"),
    # Food("Sop Iga", 45000, 550, 20, 18, "Tinggi"),
    # Food("Gado-Gado", 35000, 200, 8, 5, "rendah"),
    # Food("Nasi Kuning", 30000, 350, 12, 6, "rendah"),
    # Food("Mie Goreng", 28000, 400, 14, 9, "sedang"),
    Food("Ayam bakar", 30000, 250, 20, 10, "sedang"),
    Food("Ikan salmon", 50000, 350, 25, 15, "sedang"),
    Food("Tahu goreng", 10000, 150, 12, 8, "rendah"),
    Food("Sayur asem", 20000, 100, 5, 2, "rendah"),
    Food("Tempe bacem", 15000, 200, 15, 10, "rendah"),
    Food("Sate ayam", 40000, 300, 22, 12, "sedang"),
    Food("Nasi goreng", 25000, 400, 10, 20, "rendah"),
    Food("Udang goreng", 60000, 200, 20, 15, "tinggi"),
    Food("Telur dadar", 5000, 150, 13, 10, "tinggi"),
    Food("Ayam geprek", 20000, 246, 18, 10, "sedang"),
    
]

filtered_foods = filter_food_by_rules(foods)
sorted_foods = sorted(filtered_foods, key=lambda x: x[1], reverse=True)

print("Data Makanan Setelah Filtrasi dan Diurutkan:")
for food in sorted_foods:
    print(food)
print("\n")

# Eksekusi dan Pengukuran Waktu - Greedy
total_activity_calories = 500

start_time = time.perf_counter()
selected_foods, total_steps = greedy_algorithm(sorted_foods, total_activity_calories)
end_time = time.perf_counter()
execution_time = end_time - start_time

print("Hasil Greedy:")
print("Hidangan terpilih:")
for food in selected_foods:
    print(food)
print(f"Total Langkah: {total_steps}")
print("Waktu Eksekusi: {:.12f} detik\n".format(execution_time))

# Eksekusi dan Pengukuran Waktu - Backtracking
total_activity_calories_bt = 500
max_calories_bt = 1200 + total_activity_calories_bt

start_time_bt = time.perf_counter()
selected_foods_bt, total_steps_bt = backtrack_algorithm(sorted_foods, max_calories_bt, total_activity_calories_bt)
end_time_bt = time.perf_counter()
execution_time_bt = end_time_bt - start_time_bt

print("Hasil Backtracking:")
print("Hidangan terpilih:")
for food in selected_foods_bt:
    print(food)
print("Total Langkah: {}".format(total_steps_bt))
print("Waktu Eksekusi: {:.12f} detik\n".format(execution_time_bt))
