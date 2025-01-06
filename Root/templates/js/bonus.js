async function getdata() {
    const response = await fetch('/bonus');
    const data = await response.json();
    return data;
}

function show_bonus(red, blue, white){
    const result_bonus = [red, blue, white];
    document.getElementById('red').textContent = result_bonus[0];
    document.getElementById('blue').textContent = result_bonus[1];
    document.getElementById('white').textContent = result_bonus[2];
}

window.onload = async function setup(){
    const data = await getdata();
    show_bonus(data.result_bonus[0], data.result_bonus[1], data.result_bonus[2]);
}