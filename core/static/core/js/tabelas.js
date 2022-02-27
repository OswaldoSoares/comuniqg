$(document).ready(function(){
    $(document).on('click', '.tp-delete', function() {
        var idcadastro = $(this).attr('data-idcadastro')
        $.ajax({
            type: 'GET',
            url: 'delete_tabela',
            data: {
                idcadastro: idcadastro,
            },
            beforeSend: function() {
                $('.tabela-selecionada').fadeOut(500)
                $('.tabela-propria').fadeOut(500)
            },
            success:function(data) {
                $('.tabela-propria').html(data['html_tabela_propria'])
                $('.tabela-selecionada').html(data['html_tabela_selecionada'])
                $('.tabela-selecionada').fadeIn(500)
                $('.tabela-propria').fadeIn(500)
            },
        });
    });

    $(document).on('click', '.tp-select', function() {
        var idcadastro = $(this).attr('data-idcadastro')
        $.ajax({
            type: 'GET',
            url: 'carrega_tabela',
            data: {
                idcadastro: idcadastro,
            },
            beforeSend: function() {
                $('.tabela-selecionada').fadeOut(500)
                $('.tabela-propria').fadeOut(500)
            },
            success:function(data) {
                $('.tabela-selecionada').html(data['html_tabela_selecionada'])
                $('.tabela-selecionada').fadeIn(500)
                $('.tabela-propria').fadeIn(500)
            },
        });
    });
    
    $('.box-loader').hide()

})