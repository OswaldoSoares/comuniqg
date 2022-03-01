function openMyModal(event) {
    var modal = initModalDialog(event, '#MyModal');
    var url = $(event.target).data('action');
    var idobj = $(event.target).data('idobj');
    /**
     * tipotb usado no app tabelas
     */
    var tipotb = $(event.target).data('tipo-tb');
    $.ajax({
        type: "GET",
        url: url,
        data : {
            idobj: idobj,
            tipotb: tipotb,
        }
    }).done(function(data, textStatus, jqXHR) {
        modal.find('.modal-body').html(data.html_form);
        $('.box-loader').hide()
        modal.modal('show');
        formAjaxSubmit(modal, url, null, null);
    }).fail(function(jqXHR, textStatus, errorThrown) {

    });
}

function initModalDialog(event, modal_element) {
    var modal = $(modal_element);
    var target = $(event.target);
    var title = target.data('title') || '';
    var subtitle = target.data('subtitle') || '';
    var dialog_class = (target.data('dialog-class') || '') + ' modal-dialog';
    var icon_class = (target.data('icon') || 'fa-laptop') + ' fa modal-icon';
    var button_save_label = target.data('button-save-label') || 'Save changes';
    modal.find('.modal-dialog').attr('class', dialog_class);
    modal.find('.modal-title').text(title);
    modal.find('.modal-subtitle').text(subtitle);
    modal.find('.modal-header .title-wrapper i').attr('class', icon_class);
    modal.find('.modal-footer .btn-save').text(button_save_label);
    modal.find('.modal-body').html('');
    modal.data('target', target);
    return modal;
}

function formAjaxSubmit(modal, action, cbAfterLoad, cbAfterSuccess) {
    var form = modal.find('.modal-body form');
    var header = $(modal).find('.modal-header');
    var btn_save = modal.find('.modal-footer .btn-save');
    if (btn_save) {
        modal.find('.modal-body form .form-submit-row').hide();
        btn_save.off().on('click', function(event) {
            modal.find('.modal-body form').submit();
        });
    }
    if (cbAfterLoad) { cbAfterLoad(modal); }
    modal.find('form input:visible').first().focus();
    $(form).on('submit', function(event) {
        $('.row').hide()
        $('.box-loader').show()
        event.preventDefault();
        header.addClass('loading');
        var url = $(this).attr('action') || action;
        $.ajax({
            type: $(this).attr('method'),
            url: url,
            data: $(this).serialize(),
            success: function(xhr, ajaxOptions, thrownError) {
                $(modal).find('.modal-body').html(xhr['html_form']);
                if ($(xhr['html_form']).find('.errorlist').length > 0) {
                    formAjaxSubmit(modal, url, cbAfterLoad, cbAfterSuccess);
                } else {
                    $(modal).modal('hide');
                    $('.menu-extra').fadeOut(500)
                    if (xhr['nova_tabela']) {
                        $('.item-tabela').data('idobj', xhr['idobj'])
                        $('.item-zerado').data('idobj', xhr['idobj'])
                        $('.item-tabela').show()
                        $('.item-zerado').show()
                    }
                    if (xhr['tabela_padrao']) {
                        $('.item-tabela').data('idobj', '')
                        $('.item-zerado').data('idobj', '')
                        $('.item-tabela').hide()
                        $('.item-zerado').hide()
                    }
                    $('.menu-extra').fadeIn(500)
                    $('.tabela-selecionada').fadeOut(500)
                    $('.tabela-selecionada').html()
                    $('.tabela-selecionada').html(xhr['html_tabela_selecionada'])
                    $('.tabela-selecionada').fadeIn(500)
                    $('.tabela-propria').fadeOut(500)
                    $('.tabela-propria').html()
                    $('.tabela-propria').html(xhr['html_tabela_propria'])
                    $('.tabela-propria').fadeIn(500)
                    if (cbAfterSuccess) { 
                        cbAfterSuccess(modal);
                    }
                }
            },
            error: function(xhr, ajaxOptions, thrownError) {s
                // $(".mensagem-erro").text(thrownError);
                // mostraMensagemErro()
            },
            complete: function() {
                header.removeClass('loading');
            }
        });
    });
}