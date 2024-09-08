from flask import Flask, render_template, request, jsonify
import time
app = Flask(__name__)

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
    # Inisialisasi variabel dan penghitungan kalori maksimum berdasarkan total kalori aktivitas
    max_calories = 1200 + total_activity_calories
    total_calories = 0
    high_cholesterol_count = 0
    medium_cholesterol_count = 0
    selected_foods = []  # List untuk menyimpan makanan yang dipilih secara rakus
    total_steps = 0  # Total langkah atau iterasi yang diambil dalam algoritma

    # Urutkan makanan berdasarkan skor kalori tertinggi hingga terendah
    foods.sort(key=lambda x: x[1], reverse=True)

    # Loop melalui setiap makanan dan pilih makanan sesuai dengan kriteria
    for food in foods:
        total_steps += 1
        # Cek apakah total kalori termasuk makanan saat ini tidak melebihi batas maksimum
        if total_calories + food[2] <= max_calories:
            # Jika makanan memiliki kolesterol tinggi dan batas kolesterol tinggi belum tercapai
            if food[3] == 'tinggi' and high_cholesterol_count < 1:
                # Kurangi kalori aktivitas jika tersedia
                if total_activity_calories > 0:
                    total_activity_calories -= 100
                    # Jika total kalori aktivitas kurang dari atau sama dengan nol, berhenti
                    if total_activity_calories <= 0:
                        break
                else:
                    break  # Jika tidak ada kalori aktivitas, berhenti
                # Tambahkan makanan ke dalam daftar yang dipilih
                selected_foods.append(food)
                total_calories += food[2]  # Tambahkan kalori makanan ke total kalori
                high_cholesterol_count += 1  # Tandai bahwa satu makanan dengan kolesterol tinggi telah dipilih
            # Jika makanan memiliki kolesterol sedang dan batas kolesterol sedang belum tercapai
            elif food[3] == 'sedang' and medium_cholesterol_count < 2:
                selected_foods.append(food)  # Tambahkan makanan ke dalam daftar yang dipilih
                total_calories += food[2]  # Tambahkan kalori makanan ke total kalori
                medium_cholesterol_count += 1  # Tandai bahwa satu makanan dengan kolesterol sedang telah dipilih
            # Jika makanan memiliki kolesterol rendah
            elif food[3] == 'rendah':
                selected_foods.append(food)  # Tambahkan makanan ke dalam daftar yang dipilih
                total_calories += food[2]  # Tambahkan kalori makanan ke total kalori

    return selected_foods, total_steps  # Kembalikan daftar makanan yang dipilih beserta total langkah yang diambil



# Algoritma Backtracking
def backtrack_algorithm(foods, max_calories, total_activity_calories, index=0, current_calories=0, high_chol=0, med_chol=0, current_solution=None, best_solution=None, total_steps=0):
    total_steps += 1

    # Base case: Jika solusi saat ini atau solusi terbaik belum ditentukan
    if current_solution is None:
        current_solution = []
    if best_solution is None:
        best_solution = []

    if index == len(foods):  # Base case: Jika sudah mencapai akhir daftar makanan
        # Bandingkan solusi saat ini dengan solusi terbaik
        if sum(food[1] for food in current_solution) > sum(food[1] for food in best_solution):
            return current_solution.copy(), total_steps  # Return current solution if it's better
        return best_solution, total_steps  # Return best solution

    # Recursive case: Explore options for including or excluding the current food item
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
            # Explore including the current food item
            solution_with, steps = backtrack_algorithm(
                foods, max_calories, total_activity_calories, index + 1,
                current_calories + food_calories, new_high_chol, new_med_chol,
                current_solution, best_solution, total_steps
            )
            total_steps = steps
            if sum(food[1] for food in solution_with) > sum(food[1] for food in best_solution):
                best_solution = solution_with
            current_solution.pop()

    # Explore excluding the current food item
    solution_without, steps = backtrack_algorithm(
        foods, max_calories, total_activity_calories, index + 1,
        current_calories, high_chol, med_chol,
        current_solution, best_solution, total_steps
    )
    total_steps = steps

    # Update best solution if the solution without the current food item is better
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
activities = [
    {'name': 'Jogging', 'calories': 150},
    {'name': 'Skipping', 'calories': 150},
]
total_hidangan = 0

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_food', methods=['POST'])
def add_food():
    food_data = request.get_json()
    name = food_data['name']
    price = food_data['price']
    calories = food_data['calories']
    protein = food_data['protein']
    fat = food_data['fat']
    cholesterol = food_data['cholesterol']

    food = Food(name, price, calories, protein, fat, cholesterol)
    foods.append(food)

    return jsonify({'success': True})


@app.route('/add_activity', methods=['POST'])
def add_activity():
    activity_data = request.get_json()
    name = activity_data['name']
    calories = activity_data['calories']

    activities.append({'name': name, 'calories': calories})

    return jsonify({'success': True})

@app.route('/set_total_hidangan', methods=['POST'])
def set_total_hidangan():
    total = request.get_json()['total']
    global total_hidangan
    total_hidangan = total

    return jsonify({'success': True})
@app.route('/get_food_history', methods=['GET'])
def get_food_history():
    # Logika untuk mengambil riwayat makanan dari database atau sumber data lainnya
    # Misalnya, foods adalah list makanan yang telah dimasukkan sebelumnya
    food_history = [{'name': food.name, 'price': food.price, 'calories': food.calories, 'cholesterol': food.cholesterol} for food in foods]
    return jsonify(food_history)

@app.route('/get_activity_history', methods=['GET'])
def get_activity_history():
    # Logika untuk mengambil riwayat aktivitas dari database atau sumber data lainnya
    # Misalnya, activities adalah list aktivitas yang telah dimasukkan sebelumnya
    activity_history = [{'name': activity['name'], 'calories': activity['calories']} for activity in activities]
    return jsonify(activity_history)

@app.route('/get_recommendations', methods=['GET'])
def get_recommendations():
    total_activity_calories = sum(activity['calories'] for activity in activities)
    filtered_foods = filter_food_by_rules(foods)
    sorted_foods = sorted(filtered_foods, key=lambda x: x[1], reverse=True)

    # Greedy Algorithm Execution Time
    start_time_greedy = time.perf_counter()
    greedy_result, greedy_steps = greedy_algorithm(sorted_foods, total_activity_calories)
    end_time_greedy = time.perf_counter()
    greedy_execution_time = end_time_greedy - start_time_greedy

    greedy_result = [(food[0], food[1], food[2], food[3]) for food in greedy_result]

    # Backtracking Algorithm Execution Time
    max_calories_bt = 1200 + total_activity_calories
    start_time_backtracking = time.perf_counter()
    backtracking_result, backtracking_steps = backtrack_algorithm(sorted_foods, max_calories_bt, total_activity_calories)
    end_time_backtracking = time.perf_counter()
    backtracking_execution_time = end_time_backtracking - start_time_backtracking

    backtracking_result = [(food[0], food[1], food[2], food[3]) for food in backtracking_result]

    return jsonify({
        'greedy': greedy_result,
        'greedy_steps': greedy_steps,
        'greedy_execution_time': greedy_execution_time,
        'backtracking': backtracking_result,
        'backtracking_steps': backtracking_steps,
        'backtracking_execution_time': backtracking_execution_time,
        'total_makanan': len(foods),
        'total_kalori': total_activity_calories
    })
    
if __name__ == '__main__':
    app.run(debug=True)
