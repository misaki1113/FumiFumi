onload = function(){
    //変数
    var count = 5;
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
                    window.location.href = "/score";
                }, 1000); 

            }else{
                msg.textContent = count;
                count--;
            }      
        }, 1000
    );

    
}