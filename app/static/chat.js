var exam_id = '';
var chat = false;

function set_message_count(n) {
    if (n && !$('#exams-count').length) {
        console.log('hey');
        var badge = $('<span id="exams-count"></span>');
        $('#link-exams').append(badge);
    };
    console.log('there');
    $('#exams-count').text(n);
    $('#exams-count').css('visibility', n ? 'visible' : 'hidden');
};

function add_new_message(msg, clss) {
    var message = $("<p></p>").text(msg);
    $('#messages').prepend(message);
    $('#messages p:first').addClass(clss);
};

$(function () {

    if ($('#messages').length) {
        chat = true;
        exam_id = $(location).attr('pathname').split('/')[2];
    };
    // TODO: Decrease interval
    setInterval(function () {
        $.ajax('/messages?c=' + chat + '&e=' + exam_id).done(
            function (messages) {
                for (var i = 0; i < messages.length; i++) {
                    if (messages[i].status) {
                        if (($('#messages').length) && (messages[i].exam_id == parseInt(exam_id))) {
                            var message = messages[i].author + ': ' + messages[i].payload_json;
                            add_new_message(message, 'message-new');
                        } else set_message_count(messages[i].unread_exams);
                    };
                };
            }
        );
    }, 10000);

});

$(function () {

    $('#message').on('input focus', function () {
        $('.message-new').removeClass('message-new');
    });

    $('#message-form').on('submit', function (e) {

        $.ajax({

            data: {
                message: $('#message').val(),
                exam_id: exam_id
            },
            type: 'POST',
            url: '/send_message'

        }).done(function (data) {

            $('#message').val('');
            var msg = data.author + ': ' + data.message;
            add_new_message(msg);

        });

        e.preventDefault();

    });

    $('#message-form').keypress((e) => {
        if (e.which === 13) {
            $('#message-form').submit();
        }
    });

});


