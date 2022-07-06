$(document).ready(function() {
    $(document).on('click', '.js-cliente-faturada', function() {
        var v_idobj = $(this).data('idobj')
        $.ajax({
            type: 'GET',
            url: 'cliente_faturada',
            data: {
                idobj: v_idobj,
            },
            beforeSend: function() {
                $('.card-servico').hide()
                $('.card-selecionadas').hide()
                $('.card-faturar').hide()
                $('.card-pagamento-fatura').hide()
                $('.text-loader').text('AGUARDE CARREGANDO FATURAS...')
                $('.box-loader').show()
                $('.js-card-body').css('height', '');
            },
            success: function(data) {
                $('.card-selecionadas').html(data['html_cliente_faturada'])
                $('.card-selecionadas').show()
                bodyHeight()
                $('.box-loader').hide()
                $('.text-loader').text('AGUARDE...')
            },
            error: function(errors) {
                console.log(errors)
            }
        });
    });

    $(document).on('click', '.js-servico-fatura', function() {
        var v_idobj = $(this).data('idobj')
        $.ajax({
            type: 'GET',
            url: 'servico_fatura',
            data: {
                idobj: v_idobj,
            },
            beforeSend: function() {
                $('.card-servico').hide()
                $('.text-loader').text('AGUARDE CARREGANDO SERVIÇOS...')
                $('.box-loader').show()
            },
            success: function(data) {
                $('.card-servico').html(data['html_servico_faturada'])
                $('.card-servico').show()
                $('.card-pagamento-fatura').html(data['html_pagamento_fatura'])
                $('.card-pagamento-fatura').show()
                bodyHeight()
                $('.box-loader').hide()
                $('.text-loader').text('AGUARDE...')
            },
            error: function(errors) {
                console.log(errors)
            }
        });
    });

    $('.box-loader').hide()
    $('.card-selecionadas').hide()
    $('.card-servico').hide()
    bodyHeight()
})


var bodyHeight = function() {
    var maxHeight = 0;
    var topPosition = 0;
    $('.js-card-body').each(function(index) {
        if (index === 0) {
            topPosition = $(this).position().top
        }
        var thisH = $(this).height();
        if (thisH > maxHeight) {
            maxHeight = thisH
        }
    });
    $('.js-card-body').each(function() {
        if ($(this).position().top == topPosition) {
            $(this).height(maxHeight)
        }
    });
}