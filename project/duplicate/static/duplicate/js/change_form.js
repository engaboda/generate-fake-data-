window.onload = function(){
    console.log("dd")
    url = window.location.href;

    if ( url.search("add") == -1){
        document.getElementById("duplicate").style="display:inlline";
    }
    else{
        document.getElementById("duplicate").style="display:none";
    }


    href = window.location.href // get current path (url)
    id = href.split('/')[6] //split url to  get id of current item
    model = href.split('/')[5]//model name as string
    app = href.split('/')[4]


    try {
        btn = document.getElementById("duplicate")
        btn.addEventListener("click" , function(){
            str = '';
            $.ajax({
                url:"/duplicate/duplicate_row/",
                method:'post',
                data:{"item":id , 'url':window.location.href , 'app':app , 'model':model},
                success:function(data){
                    window.location.href = data;
                },
                error:function(error){console.log("error")}
            })
        } )
        
        // fakebtn = document.getElementById("fakebtn")
        // fakebtn.addEventListener('click' , function(){
        //     $.ajax({
        //         url:"/duplicate/fake_data/",
        //         method:'post',
        //         data:{'app':app , 'model':model},
        //         success:function(data){
        //             window.location.href = data;
        //         },
        //         error:function(error){console.log("error")}             
        //     })
        // } )


    } catch (error) {
        console.log(error)
    }




}