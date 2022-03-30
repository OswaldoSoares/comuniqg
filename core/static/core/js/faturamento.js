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
                $('.card-selecionadas').fadeOut(500)
            },
            success:function(data) {
                $('.card-selecionadas').html(data['html_cliente_faturada'])
                $('.card-selecionadas').fadeIn(500)
            },
        });
    });

    $(document).on('click', '.js-print-fatura', function() {
        var v_idobj = $(this).data('idobj')
        $.ajax({
            type: 'GET',
            url: 'print_fatura',
            data: {
                idobj: v_idobj,
            },
            beforeSend: function() {
                $('.card-selecionadas').fadeOut(500)
            },
            success:function(data) {
                $('.card-selecionadas').html(data['html_cliente_faturada'])
                $('.card-selecionadas').fadeIn(500)
            },
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
            },
            success:function(data) {
                $('.card-servico').html(data['html_servico_faturada'])
                $('.card-servico').fadeIn(500)
            },
        });
    });

    $('.box-loader').hide()
})