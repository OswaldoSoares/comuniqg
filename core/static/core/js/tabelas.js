$(document).ready(function(){
    $(document).on('click', '.item-zerado', function() {
        var v_idobj = $(this).data('idobj')
        $.ajax({
            type: 'GET',
            url: 'delete_zerado',
            data: {
                idobj: v_idobj,
            },
            beforeSend: function() {
                $('.tabela-selecionada').fadeOut(500)
                $('.tabela-propria').fadeOut(500)
                $('.menu-extra').fadeOut(500)
                $('.text-loader').text('AGUARDE APAGANDO PRODUTOS ZERADOS...')
                $('.box-loader').fadeIn(50)
            },
            success:function(data) {
                if (data['tabela_padrao']) {
                    $('.item-tabela').data('idobj', '')
                    $('.item-zerado').data('idobj', '')
                    $('.item-tabela').hide()
                    $('.item-zerado').hide()
                }
                $('.menu-extra').fadeIn(500)
                $('.tabela-selecionada').html(data['html_tabela_selecionada'])
                $('.tabela-selecionada').fadeIn(500)
                $('.tabela-propria').html(data['html_tabela_propria'])
                $('.tabela-propria').fadeIn(500)
                $('.box-loader').fadeOut(50)
                $('.text-loader').text('AGUARDE...')
            },
        });
    });

    $(document).on('click', '.tp-delete', function() {
        var v_idobj = $(this).data('idobj')
        $.ajax({
            type: 'GET',
            url: 'delete_tabela',
            data: {
                idobj: v_idobj,
            },
            beforeSend: function() {
                $('.tabela-selecionada').fadeOut(500)
                $('.tabela-propria').fadeOut(500)
                $('.menu-extra').fadeOut(500)
                $('.text-loader').text('AGUARDE APAGANDO TABELA...')
                $('.box-loader').fadeIn(50)
            },
            success:function(data) {
                $('.item-tabela').hide()
                $('.item-zerado').hide()
                $('.menu-extra').fadeIn(500)
                $('.tabela-selecionada').html(data['html_tabela_selecionada'])
                $('.tabela-selecionada').fadeIn(500)
                $('.tabela-propria').html(data['html_tabela_propria'])
                $('.tabela-propria').fadeIn(500)
                $('.box-loader').fadeOut(50)
                $('.text-loader').text('AGUARDE...')
            },
        });
    });

    $(document).on('click', '.tp-select', function() {
        var v_idobj = $(this).data('idobj')
        $('.item-tabela').data('idobj', v_idobj)
        $('.item-zerado').data('idobj', v_idobj)
        $.ajax({
            type: 'GET',
            url: 'carrega_tabela',
            data: {
                idobj: v_idobj,
            },
            beforeSend: function() {
                $('.tabela-selecionada').fadeOut(500)
                $('.tabela-propria').fadeOut(500)
                $('.menu-extra').fadeOut(500)
                $('.text-loader').text('AGUARDE CARREGANDO TABELA...')
                $('.box-loader').fadeIn(50)
            },
            success:function(data) {
                $('.item-tabela').show()
                $('.item-zerado').show()
                $('.menu-extra').fadeIn(500)
                $('.tabela-selecionada').html(data['html_tabela_selecionada'])
                $('.tabela-selecionada').fadeIn(500)
                $('.tabela-propria').fadeIn(500)
                $('.box-loader').fadeOut(50)
                $('.text-loader').text('AGUARDE...')
            },
        });
    });

    $('.box-loader').hide()
    $('.item-tabela').hide()
    $('.item-zerado').hide()
})