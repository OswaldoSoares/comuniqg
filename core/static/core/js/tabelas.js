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
                $('.tabela-propria').fadeOut(500)
            },
            success:function(data) {
                $('.tabela-propria').html(data['html_tabela_propria'])
                $('.tabela-propria').fadeIn(500)
            },
        });
    });

    /*$(document).on('click', '.tc-lista-produtos', function() {
        var idproduto = $(this).attr('data-idproduto')
        $.ajax({
            type: 'GET',
            url: 'altera_valor_produto',
            data: {
                idproduto: idproduto,
            },
            beforeSend: function() {

            },
            success: function(data) {

            },
        });
    });*/
})