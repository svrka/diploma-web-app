$(function () {
    $('#navbar a').each(function () {
        if ($(this).prop('pathname') == $(location).attr('pathname')) {
            $(this).children('li').addClass('active-page');
        }
    });
});

$(function () {
    if ($('#flash-messages').children().length > 0) {
        $('#flash-messages').addClass('new-messages');
    };

    n = $('.flash-msg-li').length;
    $('#flash-msg-count').text(n);
});