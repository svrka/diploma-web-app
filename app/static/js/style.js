$(function () {
    $('#navbar a').each(function () {
        if ($(this).prop('pathname') == $(location).attr('pathname')) {
            $(this).children('li').addClass('active-page');
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
        $('#flash-msg-count').text(n);
        flashMsg.css('display', 'block');
        setTimeout(showFlashMsg, 500);
        setTimeout(hideFlashMsg, 4500);
    } else {
        console.log('hey');
    };

    flashMsg.hover(showFlashMsg, hideFlashMsg);
});