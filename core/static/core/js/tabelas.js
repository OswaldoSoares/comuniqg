$(document).ready(function(){
    $(document).on('click', '.tp-delete', function() {
        alert($(this).attr('data-idcadastro'))
    });
})