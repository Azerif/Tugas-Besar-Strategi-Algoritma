async function addFood() {
  const name = document.getElementById('namaMakanan').value;
  const price = parseInt(document.getElementById('harga').value.replace(/[^0-9]/g, ''));
  const calories = parseInt(document.getElementById('kalori').value);
  const protein = parseInt(document.getElementById('protein').value);
  const fat = parseInt(document.getElementById('lemak').value);
  const cholesterol = document.getElementById('kolesterol').value;

  const response = await fetch('/add_food', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify({ name, price, calories, protein, fat, cholesterol })
  });

  const result = await response.json();
  if (result.success) {
      alert('Makanan berhasil ditambahkan');
      location.reload(); // Reload the page to update the food list
  }
}

async function addActivity() {
  const name = document.getElementById('namaAktivitas').value;
  const calories = parseInt(document.getElementById('kaloriAktivitas').value);

  const response = await fetch('/add_activity', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify({ name, calories })
  });

  const result = await response.json();
  if (result.success) {
      alert('Aktivitas berhasil ditambahkan');
      location.reload(); // Reload the page to update the activity list
  }
}

async function addTotalHidangan() {
  const total = parseInt(document.getElementById('totalHidangan').value);

  const response = await fetch('/set_total_hidangan', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify({ total })
  });

  const result = await response.json();
  if (result.success) {
      alert('Total hidangan berhasil disimpan');
  }
}

function formatRupiah(input) {
  let value = input.value.replace(/[^,\d]/g, '').toString();
  let split = value.split(',');
  let sisa = split[0].length % 3;
  let rupiah = split[0].substr(0, sisa);
  let ribuan = split[0].substr(sisa).match(/\d{3}/g);

  if (ribuan) {
      let separator = sisa ? '.' : '';
      rupiah += separator + ribuan.join('.');
  }

  rupiah = split[1] !== undefined ? rupiah + ',' + split[1] : rupiah;
  input.value = 'Rp ' + rupiah;
}
// Menampilkan riwayat makanan
function displayFoodHistory(history) {
    const historyContainer = document.getElementById('historyContainer');
    historyContainer.innerHTML = ''; // Bersihkan kontainer sebelum menambahkan data baru

    history.forEach(food => {
        const div = document.createElement('div');
        div.className = 'history-item';
        div.innerHTML = `
            <span>${food.name} - </span>
            <span>Rp ${food.price} -</span>
            <span>${food.calories} kalori</span>
            <span>- Kolesterol ${food.cholesterol}</span>
        `;
        historyContainer.appendChild(div);
    });
}

// Menampilkan riwayat aktivitas
function displayActivityHistory(history) {
    const activityContainer = document.getElementById('activityContainer');
    activityContainer.innerHTML = ''; // Bersihkan kontainer sebelum menambahkan data baru

    history.forEach(activity => {
        const div = document.createElement('div');
        div.className = 'history-item';
        div.innerHTML = `
            <span>${activity.name} - </span>
            <span>${activity.calories} kalori</span>
        `;
        activityContainer.appendChild(div);
    });
}

// Fungsi untuk memperbarui riwayat makanan dan aktivitas setelah menambahkan data baru
async function updateHistory() {
    const foodResponse = await fetch('/get_food_history'); // Ganti dengan rute yang sesuai di server Flask
    const foodHistory = await foodResponse.json();
    displayFoodHistory(foodHistory);

    const activityResponse = await fetch('/get_activity_history'); // Ganti dengan rute yang sesuai di server Flask
    const activityHistory = await activityResponse.json();
    displayActivityHistory(activityHistory);
}

async function getRecommendations() {
    const response = await fetch('/get_recommendations', {
        method: 'GET'
    });

    const result = await response.json();

    // Update greedy results
    const greedyResults = document.getElementById('greedyResults');
    greedyResults.innerHTML = '';
    result.greedy.forEach(food => {
        const div = document.createElement('div');
        div.innerText = `${food[0]} - Skor ${food[1]} - Kalori ${food[2]} - Kolesterol ${food[3]}`;
        greedyResults.appendChild(div);
    });

    // Update greedy steps
    const greedySteps = document.getElementById('greedySteps');
    greedySteps.innerHTML = `Jumlah langkah: ${result.greedy_steps}`;

    // Update greedy execution time
    const greedyTime = document.createElement('p');
    greedyTime.innerHTML = `Waktu eksekusi: ${result.greedy_execution_time.toFixed(12)} detik`;
    greedySteps.appendChild(greedyTime);

    // Update backtracking results
    const backtrackingResults = document.getElementById('backtrackingResults');
    backtrackingResults.innerHTML = '';
    result.backtracking.forEach(food => {
        const div = document.createElement('div');
        div.innerText = `${food[0]} - Skor ${food[1]} - Kalori ${food[2]} - Kolesterol ${food[3]}`;
        backtrackingResults.appendChild(div);
    });

    // Update backtracking steps
    const backtrackingSteps = document.getElementById('backtrackingSteps');
    backtrackingSteps.innerHTML = `Jumlah langkah: ${result.backtracking_steps}`;

    // Update backtracking execution time
    const backtrackingTime = document.createElement('p');
    backtrackingTime.innerHTML = `Waktu eksekusi: ${result.backtracking_execution_time.toFixed(12)} detik`;  
    backtrackingSteps.appendChild(backtrackingTime);

    document.getElementById('totalMakananTersedia').innerText = result.total_makanan;
    document.getElementById('totalKaloriTerbakar').innerText = result.total_kalori;
}

document.addEventListener('DOMContentLoaded', async function() {
    await getRecommendations();
    await updateHistory();
});