$(function () {
    $('.navbar-a').each(function () {
        if ($(this).prop('pathname') == $(location).attr('pathname')) {
            $(this).addClass('active-page');
        }
    });
});

$(function () {
    var flashMsg = $('#flash-messages');
    var flashMsgUl = $('#flash-msg-ul');
    var flashMsgLi = $('.flash-msg-li');

    var n = flashMsgLi.length;

    var showFlashMsg = function () {
        flashMsg.addClass('view-flash-msg');
        flashMsgUl.addClass('view-flash-msg-ul');
        flashMsgLi.addClass('view-flash-msg-li');
    };

    var hideFlashMsg = function () {
        flashMsg.removeClass('view-flash-msg');
        flashMsgUl.removeClass('view-flash-msg-ul');
        flashMsgLi.removeClass('view-flash-msg-li');
    };

    if (n) {
        flashMsg.fadeIn('slow');
        setTimeout(showFlashMsg, 500);
        setTimeout(hideFlashMsg, 4500);
        setTimeout(function () { flashMsg.fadeOut('slow') }, 5000);
    };

    flashMsg.hover(showFlashMsg, hideFlashMsg);
});

$(function () {
    $('input:text, input:password').blur(function () {
        if (!$(this).val()) {
            $(this).removeClass('not-empty-field');
        } else {
            $(this).addClass('not-empty-field');
        }
    });

    $('.error-msg').prev().addClass('error-input');
});