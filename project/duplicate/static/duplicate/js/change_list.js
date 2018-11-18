window.onload = function(){

    href = window.location.href // get current path (url)
    model = href.split('/')[5]//model name as string
    app = href.split('/')[4]

    try {
        fakebtn = document.getElementById("fakebtn")
        fakebtn.addEventListener('click' , function(){
            $.ajax({
                url:"/duplicate/fake_data/",
                method:'post',
                data:{'app':app , 'model':model},
                success:function(data){
                    console.log(data);
                },
                error:function(error){console.log("error")}             
            })
        } )
    } catch (error) {
        console.log(error)
    }


}