async function updateDate() {
    const response = await fetch('/state-data');
    const data = await response.json();

    const score = data.score;
    const level = data.level;
    const bonus = data.bonus;
    const next_point = data.next_point;
    const ranking = data.ranking;

    // const score = 1;
    // const level = 2;
    // const bonus = 3;
    // const next_point = 4;
    // const ranking = [5,3,2];

    document.getElementById('score').textContent = score;
    document.getElementById('level').textContent = level;
    document.getElementById('bonus').textContent = bonus;
    document.getElementById('next_point').textContent = next_point
    document.getElementById('ranking_one').textContent = ranking[0];
    document.getElementById('ranking_two').textContent = ranking[1];
    document.getElementById('ranking_three').textContent = ranking[2];

}

window.onload = function setup(){
    setInterval(updateDate, 1000);
}