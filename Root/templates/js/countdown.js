function countdown(initialValue) {
    //変数
    var count = initialValue;

    //要素
    var box = document.getElementById('box');
    var msg = document.getElementById('msg');
    
    var timerID = setInterval( 
        function(){
            if(count == 0){
                clearInterval(timerID);
                box.classList.remove("css1");
                msg.classList.add("title");
                msg.textContent = "Start";
               
                setTimeout(function() {
                    window.location.href = "score.html";
                }, 1000); 

            }else{
                msg.textContent = count;
                count--;
            }      
        }, 1000
    );

    
}

window.onload = function setup(){
    const initialValue = 5;
    countdown(initialValue);
}