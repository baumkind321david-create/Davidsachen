function werteBis100(){
    i=1;
    let zahlen="";
    while(i<101){
        if(i%3===0 && i%5===0){
          zahlen+="TicTac ";
        }else if(i%3===0){
           zahlen+="Tic ";
        }else if(i%5===0){
            zahlen+="Tac ";
        }else{zahlen+=i+" ";}
       
        i++;
    }
    console.log(zahlen)
    
}
werteBis100();
