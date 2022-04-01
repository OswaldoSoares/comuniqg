$(document).ready(function(){
    $(document).on('click', '.js-cliente-faturada', function() {
        var v_idobj = $(this).data('idobj')
        $.ajax({
            type: 'GET',
            url: 'cliente_faturada',
            data: {
                idobj: v_idobj,
            },
            beforeSend: function() {
                $('.card-servico').fadeOut(500)
                $('.card-selecionadas').fadeOut(500)
                $('.text-loader').text('AGUARDE CARREGANDO FATURAS...')
                $('.box-loader').fadeIn(50)
                $('.js-card-body').css('height', '');
            },
            success:function(data) {
                $('.card-selecionadas').html(data['html_cliente_faturada'])
                $('.card-selecionadas').fadeIn(500)
                bodyHeight()
                $('.box-loader').fadeOut(50)
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
                $('.card-servico').fadeOut(500)
                $('.text-loader').text('AGUARDE CARREGANDO SERVIÇOS...')
                $('.box-loader').fadeIn(50)
            },
            success:function(data) {
                $('.card-servico').html(data['html_servico_faturada'])
                $('.card-servico').fadeIn(500)
                bodyHeight()
                $('.box-loader').fadeOut(50)
                $('.text-loader').text('AGUARDE...')
            },
        });
    });

    $('.box-loader').hide()
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