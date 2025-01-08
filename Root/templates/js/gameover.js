async function getdata() {
    const response = await fetch('/final-score');
    const data = await response.json();
    return data;
}

function show_score(score){
    const final_score = score;
    document.getElementById('final_score').textContent = final_score;
}

window.onload = async function setup(){
    const data = await getdata();
    show_score(data.final_score);
}