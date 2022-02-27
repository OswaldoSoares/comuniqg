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
                $('.menu-extra').fadeOut(500)
            },
            success:function(data) {
                $('.item-tabela').hide()
                $('.item-zerado').hide()
                $('.menu-extra').fadeIn(500)
                $('.tabela-selecionada').html(data['html_tabela_selecionada'])
                $('.tabela-selecionada').fadeIn(500)
                $('.tabela-propria').html(data['html_tabela_propria'])
                $('.tabela-propria').fadeIn(500)
            },
        });
    });

    $(document).on('click', '.tp-select', function() {
        var idcadastro = $(this).attr('data-idcadastro')
        $('.item-tabela').attr('data-idcadastro', idcadastro)
        $('.item-zerado').attr('data-idcadastro', idcadastro)
        $.ajax({
            type: 'GET',
            url: 'carrega_tabela',
            data: {
                idcadastro: idcadastro,
            },
            beforeSend: function() {
                $('.tabela-selecionada').fadeOut(500)
                $('.tabela-propria').fadeOut(500)
                $('.menu-extra').fadeOut(500)
            },
            success:function(data) {
                $('.item-tabela').show()
                $('.item-zerado').show()
                $('.menu-extra').fadeIn(500)
                $('.tabela-selecionada').html(data['html_tabela_selecionada'])
                $('.tabela-selecionada').fadeIn(500)
                $('.tabela-propria').fadeIn(500)
            },
        });
    });

    $(document).on('click', '.item-zerado', function() {
        var idcadastro = $(this).attr('data-idcadastro')
        $.ajax({
            type: 'GET',
            url: 'delete_zerado',
            data: {
                idcadastro: idcadastro,
            },
            beforeSend: function() {
                $('.tabela-selecionada').fadeOut(500)
                $('.tabela-propria').fadeOut(500)
                $('.menu-extra').fadeOut(500)
            },
            success:function(data) {
                if (data['tabela_padrao']) {
                    $('.item-tabela').attr('data-idcadastro', '')
                    $('.item-zerado').attr('data-idcadastro', '')
                    $('.item-tabela').hide()
                    $('.item-zerado').hide()
                }
                $('.menu-extra').fadeIn(500)
                $('.tabela-selecionada').html(data['html_tabela_selecionada'])
                $('.tabela-selecionada').fadeIn(500)
                $('.tabela-propria').html(data['html_tabela_propria'])
                $('.tabela-propria').fadeIn(500)
            },
        });
    });
    
    $('.box-loader').hide()
    $('.item-tabela').hide()
    $('.item-zerado').hide()

})