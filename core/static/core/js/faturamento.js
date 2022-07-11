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
                $('.card-selecionadas').hide()
                $('.card-servico').hide()
                $('.card-pagamento-fatura').hide()
                $('.card-faturar').hide()
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

    $(document).on('change', '.js-dinheiro', function() {
        // saldo_fatura = $('.js-saldo').val() - $(this).val()
        soma_entrada()
    })

    $(document).on('click', '.js-bt-dinheiro', function() {
        var saldo = $('.js-saldo').val()
        $('.js-dinheiro').val(saldo)
        $('.js-debito').val('0.00')
        $('.js-credito').val('0.00')
        $('.js-pix').val('0.00')
        $('.js-deposito').val('0.00')
        $('.js-desconto').val('0.00')
        $('.js-receber').val('0.00')
    })

    $(document).on('change', '.js-debito', function() {
        // saldo_fatura = $('.js-debito').val() - $(this).val()
        soma_entrada()
    })

    $(document).on('click', '.js-bt-debito', function() {
        var saldo = $('.js-saldo').val()
        $('.js-dinheiro').val('0.00')
        $('.js-debito').val(saldo)
        $('.js-credito').val('0.00')
        $('.js-pix').val('0.00')
        $('.js-deposito').val('0.00')
        $('.js-desconto').val('0.00')
        $('.js-receber').val('0.00')
    })

    $(document).on('change', '.js-credito', function() {
        // saldo_fatura = $('.js-credito').val() - $(this).val()
        soma_entrada()
    })

    $(document).on('click', '.js-bt-credito', function() {
        var saldo = $('.js-saldo').val()
        $('.js-dinheiro').val('0.00')
        $('.js-debito').val('0.00')
        $('.js-credito').val(saldo)
        $('.js-pix').val('0.00')
        $('.js-deposito').val('0.00')
        $('.js-desconto').val('0.00')
        $('.js-receber').val('0.00')
    })

    $(document).on('change', '.js-pix', function() {
        // saldo_fatura = $('.js-pix').val() - $(this).val()
        // soma_entrada()
    })

    $(document).on('click', '.js-bt-pix', function() {
        // var saldo = $('.js-saldo').val()
        // $('.js-dinheiro').val('0.00')
        // $('.js-debito').val('0.00')
        // $('.js-credito').val('0.00')
        // $('.js-pix').val(saldo)
        // $('.js-deposito').val('0.00')
        // $('.js-desconto').val('0.00')
        // $('.js-receber').val('0.00')
    })

    $(document).on('change', '.js-deposito', function() {
        // saldo_fatura = $('.js-deposito').val() - $(this).val()
        soma_entrada()
    })

    $(document).on('click', '.js-bt-deposito', function() {
        var saldo = $('.js-saldo').val()
        $('.js-dinheiro').val('0.00')
        $('.js-debito').val('0.00')
        $('.js-credito').val('0.00')
        $('.js-pix').val('0.00')
        $('.js-deposito').val(saldo)
        $('.js-desconto').val('0.00')
        $('.js-receber').val('0.00')
    })

    $(document).on('click', '.js-bt-desconto', function() {
        var saldo = $('.js-receber').val()
        $('.js-desconto').val(saldo)
        soma_entrada()
    })

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

    $(document).on('submit', '.js-paga-fatura', function(event) {
        event.preventDefault();
        $.ajax({
            type: $(this).attr('method'),
            url: '/faturamento/paga_fatura',
            data: $(this).serialize(),
            beforeSend: function() {
                $('.card-faturadas').hide()
                $('.card-servico').hide()
                $('.card-selecionadas').hide()
                $('.card-faturar').hide()
                $('.card-pagamento-fatura').hide()
                $('.text-loader').text('AGUARDE CARREGANDO FATURAS...')
                $(".box-loader").show();
            },
            success: function(data) {
                $('.card-faturadas').html(data['html_fatura_agrupada'])
                $('.card-faturadas').show()
                if (data['html_cliente_faturada'] != '') {
                    $('.card-selecionadas').html(data['html_cliente_faturada'])
                    $('.card-selecionadas').show()
                } else {
                    $('.card-faturar').show()
                };
                bodyHeight()
                $(".box-loader").hide();
                $('.text-loader').text('AGUARDE...')
            },
        });
    });

    $('.box-loader').hide()
    $('.card-selecionadas').hide()
    $('.card-servico').hide()
    $('.card-pagamento-fatura').hide()
    bodyHeight()
})

var soma_entrada = function() {
    saldo_fatura = $('.js-saldo').val()
    dinheiro = parseFloat($('.js-dinheiro').val())
    debito = parseFloat($('.js-debito').val())
    credito = parseFloat($('.js-credito').val())
    pix = parseFloat($('.js-pix').val())
    deposito = parseFloat($('.js-deposito').val())
    desconto = parseFloat($('.js-desconto').val())
    total = dinheiro + debito + credito + pix + deposito + desconto
    saldo = (saldo_fatura - total).toFixed(2)
    $(".js-dinheiro").val(dinheiro.toFixed(2));
    $(".js-debito").val(debito.toFixed(2));
    $(".js-credito").val(credito.toFixed(2));
    $(".js-pix").val(pix.toFixed(2));
    $(".js-deposito").val(deposito.toFixed(2));
    $('.js-receber').val(saldo)
}

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