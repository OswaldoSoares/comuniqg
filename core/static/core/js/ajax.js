function executarAjax(url, type, data, sucessoCallback) {
    $.ajax({
        type: type,
        url: url,
        data: data,
        beforeSend: function() {
            $(".box-loader").show();
        },
        success: function(response) {
            sucessoCallback(response);
            $("html, body").scrollTop(0);
            $(".box-loader").hide();
        },
        error: function(error) {
            console.log("ERROR: ", error);
            $(".box-loader").hide();
        }
    });
}
