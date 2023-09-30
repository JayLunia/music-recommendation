$(document).ready(function(){

  
    $('#recommend').on('click', function(){
        let movie=$('#search').val();
        if(movie=='-1')
            alert('Please select a movie');
        else
            location.href = `music/${encodeURIComponent(movie)}`;
    })
    $('#recommend-music').on('click', function(){
        let movie=$('#search').val();
        if(movie=='-1')
            alert('Please select a movie');
        else
            location.href = `${encodeURIComponent(movie)}`;
    })
});