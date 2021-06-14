$(function () {
    $('#navbar a').each(function () {
        if ($(this).prop('pathname') == $(location).attr('pathname')) {
            $(this).children('li').addClass('active-page');
        }
    });
});